import pandas as pd
import numpy as np
import os
from sklearn.metrics.pairwise import cosine_similarity
import predict
import logging

logger = logging.getLogger("personalization-service")

class PersonalizationEngine:
    def __init__(self, predictor_instance):
        self.predictor = predictor_instance
        self.dataset_path = os.path.join(os.path.dirname(__file__), "career_data_large_cleaned.csv")
        self.df = None
        self.feature_matrix = None
        self._load_dataset()

    def _load_dataset(self):
        try:
            if os.path.exists(self.dataset_path):
                self.df = pd.read_csv(self.dataset_path)
                # Sample for performance if dataset is massive
                if len(self.df) > 10000:
                    self.df = self.df.sample(10000, random_state=42).reset_index(drop=True)
                logger.info(f"Dataset loaded and sampled for personalization: {len(self.df)} rows.")
                self._precompute_features()
            else:
                logger.error(f"Dataset not found at {self.dataset_path}")
        except Exception as e:
            logger.error(f"Error loading personalization dataset: {e}")

    def _precompute_features(self):
        """
        Precompute the feature matrix for the entire dataset to speed up similarity searches.
        """
        try:
            # We need to transform the entire dataset using the same vectorizers
            # This is memory intensive but faster for queries
            # For a large dataset, we might want to sample or use a more efficient approach
            # but here we follow the "large" cleaned data constraint.
            
            # 1. Prepare categorical features
            logger.info("Precomputing feature matrix for personalization...")
            int_encoded = self.df['Interest_Areas'].apply(lambda x: self.predictor._safe_label_encode(self.predictor.le_interest, x))
            ext_encoded = self.df['Extracurriculars'].apply(lambda x: self.predictor._safe_label_encode(self.predictor.le_extra, x))
            sal_encoded = self.df['Salary_Expectation'].apply(lambda x: self.predictor._safe_label_encode(self.predictor.le_salary, x))
            
            # 2. Vectorize collections
            X_tech = self.predictor.tech_vectorizer.transform(self.df['Technical_Skills'].fillna(""))
            X_soft = self.predictor.soft_vectorizer.transform(self.df['Soft_Skills'].fillna(""))
            
            # 3. Combine
            base = pd.DataFrame({
                'Academic_Percentage': self.df['Academic_Percentage'],
                'interest_encoded': int_encoded,
                'extra_encoded': ext_encoded,
                'salary_encoded': sal_encoded,
                'Leadership_Preference': self.df['Leadership_Preference']
            })
            
            # Construct names for alignment
            tech_columns = [f"tech_{name}" for name in self.predictor.tech_vectorizer.get_feature_names_out()]
            soft_columns = [f"soft_{name}" for name in self.predictor.soft_vectorizer.get_feature_names_out()]
            
            df_full = pd.concat([
                base.reset_index(drop=True), 
                pd.DataFrame(X_tech.toarray(), columns=tech_columns),
                pd.DataFrame(X_soft.toarray(), columns=soft_columns)
            ], axis=1)
            
            # Align with model features
            for col in self.predictor.feature_names:
                if col not in df_full.columns:
                    df_full[col] = 0
            
            self.feature_matrix = df_full[self.predictor.feature_names].values
            logger.info("Feature matrix precomputed.")
        except Exception as e:
            logger.error(f"Error precomputing feature matrix: {e}")

    def find_twins(self, user_vector, top_n=5):
        if self.feature_matrix is None:
            return []
            
        # Calculate cosine similarity
        similarities = cosine_similarity(user_vector.reshape(1, -1), self.feature_matrix)[0]
        
        # Get top indices
        top_indices = np.argsort(similarities)[-top_n:][::-1]
        
        twins = []
        # Check if user has technical or soft skills (index 5 starts tech features)
        user_has_skills = np.count_nonzero(user_vector[5:]) > 0
        
        for idx in top_indices:
            row = self.df.iloc[idx]
            sim = float(similarities[idx])
            
            # Dampen similarity for sparse profiles to avoid widespread 100% scores
            # This ensures that even if categorical features match, the absence of skills
            # doesn't falsely imply perfect resonance.
            if not user_has_skills and sim > 0.9:
                sim = 0.85 + (sim * 0.1) 

            twins.append({
                "similarity_score": round(sim, 3),
                "common_skills": self._get_common_skills(user_vector, self.feature_matrix[idx]),
                "predicted_career_path": row['Career_Path']
            })
        return twins

    def _get_common_skills(self, user_vec, twin_vec):
        # Identify non-zero technical/soft skills that match
        common = []
        for i, val in enumerate(user_vec):
            if val > 0 and twin_vec[i] > 0:
                feat_name = self.predictor.feature_names[i]
                if feat_name.startswith("tech_") or feat_name.startswith("soft_"):
                    common.append(feat_name.replace("tech_", "").replace("soft_", ""))
        return common[:5] # Return top 5 common skills

# Helper
personalization_engine = None

def find_career_twins(assessment_data):
    global personalization_engine
    if predict.predictor is None:
        predict.get_ml_recommendations(assessment_data)
        
    if personalization_engine is None:
        personalization_engine = PersonalizationEngine(predict.predictor)
        
    # Transform user input to vector
    percentage = getattr(assessment_data, 'academic_percentage', 85)
    interest = getattr(assessment_data, 'interests', '')
    extra = getattr(assessment_data, 'extracurriculars', '')
    tech = getattr(assessment_data, 'tech_skills', '')
    soft = getattr(assessment_data, 'soft_skills', '')
    
    # 1. Transform categorical
    int_enc = predict.predictor._safe_label_encode(predict.predictor.le_interest, interest)
    ext_enc = predict.predictor._safe_label_encode(predict.predictor.le_extra, extra)
    sal_enc = predict.predictor._safe_label_encode(predict.predictor.le_salary, "Any")
    lead_val = 0
    
    # 2. Vectorize
    tech_str = tech if isinstance(tech, str) else ",".join(tech)
    soft_str = soft if isinstance(soft, str) else ",".join(soft)
    
    X_tech = predict.predictor.tech_vectorizer.transform([tech_str])
    X_soft = predict.predictor.soft_vectorizer.transform([soft_str])
    
    # 3. Combine
    user_df = pd.DataFrame({
        'Academic_Percentage': [percentage],
        'interest_encoded': [int_enc],
        'extra_encoded': [ext_enc],
        'salary_encoded': [sal_enc],
        'Leadership_Preference': [lead_val]
    })
    
    tech_cols = [f"tech_{name}" for name in predict.predictor.tech_vectorizer.get_feature_names_out()]
    soft_cols = [f"soft_{name}" for name in predict.predictor.soft_vectorizer.get_feature_names_out()]
    
    user_full = pd.concat([
        user_df,
        pd.DataFrame(X_tech.toarray(), columns=tech_cols),
        pd.DataFrame(X_soft.toarray(), columns=soft_cols)
    ], axis=1)
    
    for col in predict.predictor.feature_names:
        if col not in user_full.columns:
            user_full[col] = 0
    
    user_vec = user_full[predict.predictor.feature_names].values[0]
    
    return personalization_engine.find_twins(user_vec)
