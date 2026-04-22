import pandas as pd
import numpy as np
import os
from scipy import stats

def preprocess_data(file_path: str):
    print(f"\n🚀 Starting Massive Data Preprocessing for: {file_path}")
    
    # 1. Load Data
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found.")
        return None
    
    df = pd.read_csv(file_path)
    initial_count = len(df)
    print(f"📊 Initial row count: {initial_count:,}")

    # 2. Handle Duplicates
    print("🔍 Searching for duplicates...")
    df.drop_duplicates(inplace=True)
    duplicates_removed = initial_count - len(df)
    print(f"✅ Removed {duplicates_removed:,} duplicate rows.")

    # 3. Handle Null Values
    print("🔍 Checking for null values...")
    null_count = df.isnull().sum().sum()
    df.dropna(inplace=True)
    print(f"✅ Dropped {null_count:,} rows with missing values.")

    # 4. Handle Outliers (using Z-Score)
    # Focus on 'Academic_Percentage' as requested for dataset integrity
    if 'Academic_Percentage' in df.columns:
        print("🔍 Detecting outliers using Z-Score method for Academic_Percentage...")
        # Fill NA for z-score calculation if any slipped through
        df['Academic_Percentage'] = df['Academic_Percentage'].fillna(df['Academic_Percentage'].mean())
        z_scores = np.abs(stats.zscore(df['Academic_Percentage']))
        outlier_mask = z_scores > 3
        outliers_count = np.sum(outlier_mask)
        
        if outliers_count > 0:
            print(f"🚨 Found {outliers_count:,} outliers in 'Academic_Percentage'.")
            df = df[~outlier_mask]
        print(f"✅ Cleaned row count: {len(df):,}")

    # 5. Save Cleaned Data
    output_path = file_path.replace(".csv", "_cleaned.csv")
    print(f"💾 Saving cleaned dataset to: {output_path}...")
    df.to_csv(output_path, index=False)
    print("✨ Preprocessing Complete!")
    
    return df

if __name__ == "__main__":
    csv_path = os.path.join(os.path.dirname(__file__), "career_data_large.csv")
    preprocess_data(csv_path)
