import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, classification_report

def comma_tokenizer(text):
    return text.split(',')

def train_career_model(data_path: str):
    print(f"--- Loading Cleaned Dataset: {data_path} ---")
    if not os.path.exists(data_path):
        print("Error: Cleaned dataset not found. Please run preprocess.py first.")
        return

    df = pd.read_csv(data_path)
    print(f"Dataset Size: {len(df)} rows")

    # 1. Feature Engineering
    print("Engineering features...")
    
    # Vectorizing Technical Skills
    # We replace commas with spaces so CountVectorizer can tokenize them
    technical_vectorizer = CountVectorizer(tokenizer=comma_tokenizer, token_pattern=None)
    X_tech = technical_vectorizer.fit_transform(df['Technical_Skills'])
    tech_columns = [f"tech_{name}" for name in technical_vectorizer.get_feature_names_out()]
    df_tech = pd.DataFrame(X_tech.toarray(), columns=tech_columns)

    # Vectorizing Soft Skills
    soft_vectorizer = CountVectorizer(tokenizer=comma_tokenizer, token_pattern=None)
    X_soft = soft_vectorizer.fit_transform(df['Soft_Skills'])
    soft_columns = [f"soft_{name}" for name in soft_vectorizer.get_feature_names_out()]
    df_soft = pd.DataFrame(X_soft.toarray(), columns=soft_columns)

    # Encoding Interest_Areas & Extracurriculars
    le_interest = LabelEncoder()
    df['interest_encoded'] = le_interest.fit_transform(df['Interest_Areas'])

    le_extra = LabelEncoder()
    df['extra_encoded'] = le_extra.fit_transform(df['Extracurriculars'])
    
    # Encoding Salary Expectation
    le_salary = LabelEncoder()
    df['salary_encoded'] = le_salary.fit_transform(df['Salary_Expectation'])

    import scipy.sparse as sp

    # Convert non-text features to sparse matrix
    # Added salary_encoded and Leadership_Preference
    print("Converting numeric features to sparse matrix...")
    numeric_features = df[['Academic_Percentage', 'interest_encoded', 'extra_encoded', 'salary_encoded', 'Leadership_Preference']]
    X_numeric = sp.csr_matrix(numeric_features.values)

    # Combine all features using sparse hstack
    print("Combining features directly into sparse matrix...")
    X = sp.hstack([X_numeric, X_tech, X_soft], format='csr')

    # Encoding Target (Career_Path)
    le_career = LabelEncoder()
    y = le_career.fit_transform(df['Career_Path'])

    print("--- Training Multiple Models for Comparison ---")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    models = {
        "Random Forest": RandomForestClassifier(n_estimators=50, max_depth=20, random_state=42, n_jobs=-1),
        "Gradient Boosting": HistGradientBoostingClassifier(max_iter=100, random_state=42),
        "SGD Classifier (SVM-like)": SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, random_state=42, max_iter=5, tol=None)
    }

    best_name = ""
    best_acc = 0.0
    best_model = None

    for name, model in models.items():
        print(f"\nTraining {name}...")
        try:
            # Note: SGD requires scaling usually, but for this massive dataset text features are sparse.
            # We run it as a quick linear baseline.
            if name == "Gradient Boosting":
                # Histogram Boosting handles dense/sparse mixed but prefers dense. 
                # Converting 500k rows to dense might be memory intensive.
                # We will try; if it fails, we skip.
                try:
                    model.fit(X_train.toarray(), y_train)
                except Exception as e:
                    print(f"⚠️ Gradient Boosting skipped (Memory/Format issue): {e}")
                    continue
            else:
                model.fit(X_train, y_train)
            
            if name == "Gradient Boosting":
                 preds = model.predict(X_test.toarray())
            else:
                 preds = model.predict(X_test)

            acc = accuracy_score(y_test, preds)
            print(f"✅ {name} Accuracy: {acc:.4f}")

            if acc > best_acc:
                best_acc = acc
                best_model = model
                best_name = name
        except Exception as e:
            print(f"❌ {name} Failed: {e}")

    print(f"\n🏆 BEST MODEL: {best_name} with Accuracy {best_acc:.4f}")
    
    # Use the best model for saving
    clf = best_model

    # 4. Evaluation (of best model)
    # y_pred = clf.predict(X_test) # Already computed
    print(f"Final Selected Model: {best_name}")
    
    # 5. Saving Assets
    print("Saving model assets...")
    save_dir = os.path.join(os.path.dirname(__file__), "weights")
    os.makedirs(save_dir, exist_ok=True)

    # Reconstruct feature names
    feature_names = (
        ['Academic_Percentage', 'interest_encoded', 'extra_encoded', 'salary_encoded', 'Leadership_Preference'] +
        [f"tech_{name}" for name in technical_vectorizer.get_feature_names_out()] +
        [f"soft_{name}" for name in soft_vectorizer.get_feature_names_out()]
    )

    joblib.dump(clf, os.path.join(save_dir, "career_model.pkl"))
    joblib.dump(technical_vectorizer, os.path.join(save_dir, "tech_vectorizer.pkl"))
    joblib.dump(soft_vectorizer, os.path.join(save_dir, "soft_vectorizer.pkl"))
    joblib.dump(le_interest, os.path.join(save_dir, "le_interest.pkl"))
    joblib.dump(le_extra, os.path.join(save_dir, "le_extra.pkl"))
    joblib.dump(le_salary, os.path.join(save_dir, "le_salary.pkl"))
    joblib.dump(le_career, os.path.join(save_dir, "le_career.pkl"))
    joblib.dump(feature_names, os.path.join(save_dir, "feature_names.pkl"))
    
    print(f"✨ All assets saved successfully in {save_dir}/")

if __name__ == "__main__":
    cleaned_path = os.path.join(os.path.dirname(__file__), "career_data_large_cleaned.csv")
    train_career_model(cleaned_path)
