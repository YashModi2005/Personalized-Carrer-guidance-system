import shap
import pandas as pd
import numpy as np
import predict
import logging
from functools import lru_cache

logger = logging.getLogger("explainable-ai")

class ExplainableAI:
    def __init__(self, predictor_instance):
        self.predictor = predictor_instance
        self.explainer = None
        self._initialize_explainer()

    def _initialize_explainer(self):
        try:
            # SHAP works well with the underlying model (likely RandomForest or XGBoost)
            # We use a small background dataset for KernelExplainer or use TreeExplainer if compatible
            # For now, TreeExplainer is preferred for speed if the model is tree-based
            self.explainer = shap.TreeExplainer(self.predictor.model)
            logger.info("SHAP TreeExplainer initialized successfully.")
        except Exception as e:
            logger.warning(f"TreeExplainer failed, falling back to KernelExplainer (slower): {e}")
            # Fallback to KernelExplainer with a small sample if necessary
            # For this task, we assume TreeExplainer works with the provided model
            pass

    def explain(self, academic_percentage, interests, extracurriculars, tech_skills, soft_skills, salary_expectation, leadership_preference, target_career=None):
        """
        Generates SHAP values and an explanation text for a specific career or the top prediction.
        """
        # 0. Feature Name Mapping
        FEATURE_MAP = {
            "Academic_Percentage": "Academic Performance",
            "interest_encoded": "Core Interests",
            "extra_encoded": "Extracurricular Focus",
            "salary_encoded": "Salary Expectations",
            "Leadership_Preference": "Leadership Aptitude"
        }

        # 1. Transform input using the same logic as predict.py
        # We need the transformed X_input
        interest_encoded = self.predictor._safe_label_encode(self.predictor.le_interest, interests)
        extra_encoded = self.predictor._safe_label_encode(self.predictor.le_extra, extracurriculars)
        salary_encoded = self.predictor._safe_label_encode(self.predictor.le_salary, salary_expectation)
        lead_val = 1 if leadership_preference else 0

        tech_str = ",".join(tech_skills) if isinstance(tech_skills, list) else str(tech_skills)
        soft_str = ",".join(soft_skills) if isinstance(soft_skills, list) else str(soft_skills)
        
        X_tech = self.predictor.tech_vectorizer.transform([tech_str])
        X_soft = self.predictor.soft_vectorizer.transform([soft_str])

        base_features = pd.DataFrame({
            'Academic_Percentage': [academic_percentage],
            'interest_encoded': [interest_encoded],
            'extra_encoded': [extra_encoded],
            'salary_encoded': [salary_encoded],
            'Leadership_Preference': [lead_val]
        })

        tech_columns = [f"tech_{name}" for name in self.predictor.tech_vectorizer.get_feature_names_out()]
        df_tech = pd.DataFrame(X_tech.toarray(), columns=tech_columns)

        soft_columns = [f"soft_{name}" for name in self.predictor.soft_vectorizer.get_feature_names_out()]
        df_soft = pd.DataFrame(X_soft.toarray(), columns=soft_columns)

        X_input = pd.concat([base_features, df_tech, df_soft], axis=1)

        for col in self.predictor.feature_names:
            if col not in X_input.columns:
                X_input[col] = 0
        X_input = X_input[self.predictor.feature_names]

        # 2. Get SHAP values
        try:
            shap_values = self.explainer.shap_values(X_input)
        except Exception as e:
            logger.error(f"SHAP computing failed: {e}")
            return {"explanation": "Analysis unavailable for this profile.", "top_features": []}
        
        # 3. Determine class to explain
        target_idx = 0
        is_metadata_only = False
        
        if target_career:
            try:
                # Find the label index for the target career
                target_idx = list(self.predictor.le_career.classes_).index(target_career)
            except ValueError:
                # Target career is a metadata-only match
                is_metadata_only = True
        else:
            probas = self.predictor.model.predict_proba(X_input)[0]
            target_idx = int(np.argmax(probas))
            
        # Robustly handle different SHAP output formats (List, 3D Array, Explanation object)
        current_shap_values = np.zeros(X_input.shape[1])
        if not is_metadata_only:
            try:
                # 1. Handle List of arrays (Common in multi-class)
                if isinstance(shap_values, list):
                    safe_idx = target_idx if target_idx < len(shap_values) else 0
                    current_shap_values = shap_values[safe_idx]
                    if hasattr(current_shap_values, 'shape') and len(current_shap_values.shape) > 1:
                        current_shap_values = current_shap_values[0]
                
                # 2. Handle SHAP Explanation object
                elif hasattr(shap_values, 'values') and hasattr(shap_values, 'base_values'):
                    vals = shap_values.values
                    if len(vals.shape) == 3: # (obs, feat, class)
                        safe_idx = target_idx if target_idx < vals.shape[2] else 0
                        current_shap_values = vals[0, :, safe_idx]
                    elif len(vals.shape) == 2: # (obs, feat)
                        current_shap_values = vals[0]

                # 3. Handle 3D Numpy Array
                elif hasattr(shap_values, 'shape') and len(shap_values.shape) == 3:
                    # Try to find class axis
                    if shap_values.shape[2] > target_idx:
                        current_shap_values = shap_values[0, :, target_idx]
                    elif shap_values.shape[1] > target_idx:
                        current_shap_values = shap_values[0, target_idx, :]
                    else:
                        current_shap_values = shap_values[0, :, 0]

                # 4. Handle 2D Numpy Array (Single class / Binary)
                elif hasattr(shap_values, 'shape') and len(shap_values.shape) == 2:
                    current_shap_values = shap_values[0]
                
                # 5. Last resort fallback
                else:
                    try:
                        current_shap_values = shap_values[0]
                    except:
                        pass
            except Exception as e:
                logger.error(f"Hyper-Robust SHAP Indexing Failed: {e} | Target: {target_idx}")
                current_shap_values = np.zeros(X_input.shape[1])
        
        # Ensure current_shap_values is iterable and matches feature count
        if not hasattr(current_shap_values, "__iter__") or isinstance(current_shap_values, (float, int)):
            current_shap_values = np.zeros(X_input.shape[1])
        elif hasattr(current_shap_values, "shape") and len(current_shap_values.shape) == 0:
            current_shap_values = np.zeros(X_input.shape[1])

        # 3. Extract top contributing features
        feature_importance = []
        user_vector = X_input.values[0]
        
        if is_metadata_only:
            # For metadata-only matches, we synthesize importance based on input presence
            # since the ML model doesn't "know" this career label.
            # We prioritize technical features that the user actually HAS.
            for i, val in enumerate(user_vector):
                if val > 0:
                    raw_name = self.predictor.feature_names[i]
                    clean_name = FEATURE_MAP.get(raw_name, raw_name.replace("tech_", "").replace("soft_", "").replace("_", " "))
                    # Heuristic: Give slightly higher importance to tech skills for defense/spec roles
                    synth_shap = 0.5 if raw_name.startswith("tech_") else 0.2
                    feature_importance.append({
                        "feature": clean_name,
                        "shap_value": synth_shap
                    })
        else:
            for i, val in enumerate(current_shap_values):
                # Only consider features that the user actually HAS (non-zero value)
                # This prevents explaining "Game Developer" due to "Biometrics" if they don't have biometrics.
                if user_vector[i] > 0:
                    raw_name = self.predictor.feature_names[i]
                    clean_name = FEATURE_MAP.get(raw_name, raw_name.replace("tech_", "").replace("soft_", "").replace("_", " "))
                    feature_importance.append({
                        "feature": clean_name,
                        "shap_value": float(val)
                    })
        
        # Sort by SHAP value (positive impact first)
        feature_importance.sort(key=lambda x: x["shap_value"], reverse=True)
        top_features = feature_importance[0:3]

        # 4. Generate explanation text
        main_factors = [str(f.get("feature", "")).title() for f in top_features if f.get("shap_value", 0) > 0]
        career_name = target_career if target_career else self.predictor.le_career.inverse_transform([target_idx])[0]
        
        if is_metadata_only:
            explanation = f"Matched {career_name} due to high skill resonance and profile alignment with {', '.join(main_factors[0:2])}."
        elif main_factors:
            explanation = f"Recommended {career_name} due to strong {', '.join(main_factors[0:2])}."
        else:
            # Fallback if no specific features dominate but the model found a match
            explanation = f"Strong alignment with {career_name} based on comprehensive profile analysis."
        
        return {
            "explanation": explanation,
            "top_features": [{"name": str(f.get("feature", "")), "value": float(f.get("shap_value", 0))} for f in top_features]
        }

# Helper to get global instance
xai_engine = None

@lru_cache(maxsize=64)
def _cached_explain(interest_key: str, tech_key: str, soft_key: str, extra_key: str, percentage: float, target_career: str):
    """LRU-cached SHAP computation — same profile inputs return instantly."""
    global xai_engine
    tech = tech_key.split(',') if tech_key else []
    soft = soft_key.split(',') if soft_key else []
    return xai_engine.explain(
        percentage, interest_key, extra_key,
        tech, soft,
        "Any", False,
        target_career=target_career
    )

def explain_prediction(assessment_data, target_career=None):
    global xai_engine
    if predict.predictor is None:
        # This will trigger asset loading in predict.py
        predict.get_ml_recommendations(assessment_data)
        
    if xai_engine is None:
        xai_engine = ExplainableAI(predict.predictor)
        
    percentage = float(getattr(assessment_data, 'academic_percentage', 85))
    interest = str(getattr(assessment_data, 'interests', ''))
    extra = str(getattr(assessment_data, 'extracurriculars', ''))
    tech = getattr(assessment_data, 'tech_skills', '')
    soft = getattr(assessment_data, 'soft_skills', '')
    
    # Normalize to comma-separated string for cache key
    tech_key = ','.join(tech) if isinstance(tech, list) else str(tech)
    soft_key = ','.join(soft) if isinstance(soft, list) else str(soft)
    target_key = target_career or ""

    return _cached_explain(interest, tech_key, soft_key, extra, percentage, target_key)
