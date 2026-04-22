import pandas as pd
import numpy as np
import joblib
import os
import sys

# Physically define the tokenizer here to avoid dependency on train_model.py
def comma_tokenizer(text):
    if not isinstance(text, str):
        return []
    return text.split(',')

# Inject into __main__ so joblib finds it when loading models that used it
if not hasattr(sys.modules['__main__'], 'comma_tokenizer'):
    setattr(sys.modules['__main__'], 'comma_tokenizer', comma_tokenizer)

class CareerPredictor:
    def __init__(self):
        self.base_dir = os.path.join(os.path.dirname(__file__), "weights")
        self.load_assets()

    def load_assets(self):
        print("Loading ML assets from weights directory...")
        # Check for assets directly in base_dir or a nested weights folder
        assets_dir = self.base_dir
        if not os.path.exists(os.path.join(assets_dir, "career_model.pkl")):
            # Try subfolder if main doesn't have it
            assets_dir = os.path.join(self.base_dir, "weights")
            
        if not os.path.exists(os.path.join(assets_dir, "career_model.pkl")):
            raise FileNotFoundError(f"Model assets not found in {self.base_dir}")
            
        self.model = joblib.load(os.path.join(assets_dir, "career_model.pkl"))
        self.tech_vectorizer = joblib.load(os.path.join(assets_dir, "tech_vectorizer.pkl"))
        self.soft_vectorizer = joblib.load(os.path.join(assets_dir, "soft_vectorizer.pkl"))
        self.le_interest = joblib.load(os.path.join(assets_dir, "le_interest.pkl"))
        self.le_extra = joblib.load(os.path.join(assets_dir, "le_extra.pkl"))
        self.le_salary = joblib.load(os.path.join(assets_dir, "le_salary.pkl"))
        self.le_career = joblib.load(os.path.join(assets_dir, "le_career.pkl"))
        self.feature_names = joblib.load(os.path.join(assets_dir, "feature_names.pkl"))
        print("ML assets loaded successfully.")

    def _safe_label_encode(self, encoder, value):
        if value is None: return 0
        value_str = str(value)
        try:
            return encoder.transform([value_str])[0]
        except ValueError:
            known_classes = list(encoder.classes_)
            value_lower = value_str.lower()
            for cls in known_classes:
                if value_lower in str(cls).lower() or str(cls).lower() in value_lower:
                    return encoder.transform([cls])[0]
            return 0

    def _is_meaningful_text(self, text):
        clean_text = str(text).strip()
        if not clean_text:
            return False
            
        # Allow short terms like 'AI', 'ML', 'C', 'Go' if they are purely alphanumeric
        if len(clean_text) < 3:
            return clean_text.isalnum()
            
        # 1. Reject purely numeric strings (e.g., "123123")
        if clean_text.isdigit():
            return False

        # 2. Check for minimum alphabet content (actual words/skills)
        # Professional skills should contain at least 50% letters
        letters = sum(1 for char in clean_text if char.isalpha())
        alphabet_ratio = letters / len(clean_text)
        
        if alphabet_ratio < 0.5:
            return False

        # 3. Numeric density: If it contains more than 3 numbers and is a single "word", it's likely junk
        digits = sum(1 for char in clean_text if char.isdigit())
        if digits > 3 and " " not in clean_text:
            # Special case for potentially valid terms like "React18" or "Python3"
            if len(clean_text) > 10: # Long mixed strings like 'die2u498492u4' are definitely junk
                return False

        # 4. Reject repetitive junk (e.g., "aaaaa")
        from collections import Counter
        counts = Counter(clean_text.lower())
        if counts and max(counts.values()) / len(clean_text) > 0.8 and len(clean_text) > 4:
            return False
            
        # 5. Check for special character density
        special_chars = sum(1 for char in clean_text if not char.isalnum() and not char.isspace())
        if special_chars / len(clean_text) > 0.5:
            return False
            
        return True

    def check_input_validity(self, interests, tech_skills, soft_skills):
        tech_str = ",".join(tech_skills) if isinstance(tech_skills, list) else str(tech_skills)
        soft_str = ",".join(soft_skills) if isinstance(soft_skills, list) else str(soft_skills)
        
        is_tech = self._is_meaningful_text(tech_str)
        is_soft = self._is_meaningful_text(soft_str)
        is_interest = self._is_meaningful_text(interests)
        
        # STRICT BLOCKING: If ANY field that was filled is nonsense, block it entirely.
        if not is_tech:
            return False, "Your 'Technical Skills' contain non-standard characters. Please use real words."
        if not is_soft:
            return False, "Your 'Soft Skills' contain non-standard characters. Please use real words."
        if not is_interest:
            return False, "Your 'Primary Interests' contain non-standard characters. Please use real words."
            
        return True, ""

    def predict(self, academic_percentage, interests, extracurriculars, tech_skills, soft_skills, salary_expectation, leadership_preference):
        # 0. Basic Validation
        tech_str = ",".join(tech_skills) if isinstance(tech_skills, list) else str(tech_skills)
        soft_str = ",".join(soft_skills) if isinstance(soft_skills, list) else str(soft_skills)
        
        is_tech_meaningful = self._is_meaningful_text(tech_str)
        is_soft_meaningful = self._is_meaningful_text(soft_str)
        is_interest_meaningful = self._is_meaningful_text(interests)

        # 1. Transform categorical inputs
        interest_encoded = self._safe_label_encode(self.le_interest, interests)
        extra_encoded = self._safe_label_encode(self.le_extra, extracurriculars)
        salary_encoded = self._safe_label_encode(self.le_salary, salary_expectation)
        lead_val = 1 if leadership_preference else 0

        # 2. Vectorize collections
        X_tech = self.tech_vectorizer.transform([tech_str])
        tech_columns = [f"tech_{name}" for name in self.tech_vectorizer.get_feature_names_out()]
        df_tech = pd.DataFrame(X_tech.toarray(), columns=tech_columns)

        X_soft = self.soft_vectorizer.transform([soft_str])
        soft_columns = [f"soft_{name}" for name in self.soft_vectorizer.get_feature_names_out()]
        df_soft = pd.DataFrame(X_soft.toarray(), columns=soft_columns)

        # Signal Strength Check: How many actual tokens were recognized?
        tech_signal = X_tech.nnz # Number of non-zero elements
        soft_signal = X_soft.nnz
        total_signal = tech_signal + soft_signal

        # 3. Combine features
        base_features = pd.DataFrame({
            'Academic_Percentage': [academic_percentage],
            'interest_encoded': [interest_encoded],
            'extra_encoded': [extra_encoded],
            'salary_encoded': [salary_encoded],
            'Leadership_Preference': [lead_val]
        })

        X_input = pd.concat([base_features, df_tech, df_soft], axis=1)

        # Align columns with training
        for col in self.feature_names:
            if col not in X_input.columns:
                X_input[col] = 0
        X_input = X_input[self.feature_names]

        # 4. Predict probabilities
        probas = self.model.predict_proba(X_input)[0]
        top_indices = np.argsort(probas)[-5:][::-1]

        recommendations = []
        for idx in top_indices:
            career_name = self.le_career.inverse_transform([idx])[0]
            confidence = probas[idx]
            
            # --- INTELLIGENT PENALIZATION ---
            # If input was junk or had zero recognized tokens, drastically reduce confidence
            if not is_tech_meaningful and not is_soft_meaningful:
                confidence *= 0.1 # Severe penalty for gibberish
            elif total_signal == 0:
                confidence *= 0.3 # Moderate penalty if skills don't match anything in our database
            
            if confidence < 0.05: continue # Skip very low confidence
            
            recommendations.append({
                "career_title": career_name,
                "match_score": float(confidence)
            })

        # If everything is low confidence, return an empty list to signal "Inconclusive"
        return recommendations

# Singleton instance
predictor = None

def validate_assessment_data(assessment_data):
    global predictor
    if predictor is None:
        predictor = CareerPredictor()
    
    tech = getattr(assessment_data, 'tech_skills', '')
    soft = getattr(assessment_data, 'soft_skills', '')
    interest = getattr(assessment_data, 'interests', '')
    
    return predictor.check_input_validity(interest, tech, soft)

def get_ml_recommendations(assessment_data):
    global predictor
    try:
        if predictor is None:
            predictor = CareerPredictor()

        # Handle simplified assessment data (mapping removed fields to defaults)
        percentage = getattr(assessment_data, 'academic_percentage', 85)
        interest = getattr(assessment_data, 'interests', '')
        extra = getattr(assessment_data, 'extracurriculars', '')
        tech = getattr(assessment_data, 'tech_skills', '')
        soft = getattr(assessment_data, 'soft_skills', '')
        
        # Legacy fields for model compatibility
        salary = "Any"
        leadership = False

        return predictor.predict(
            percentage, 
            interest, 
            extra, 
            tech if isinstance(tech, list) else tech.split(',') if tech else [], 
            soft if isinstance(soft, list) else soft.split(',') if soft else [], 
            salary, 
            leadership
        )
    except Exception as e:
        print(f"ML Predictor Error: {str(e)}")
        return []
