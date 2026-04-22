import pandas as pd
import numpy as np
import random
import os
import sys

# Ensure we can import from model.py
sys.path.append(os.path.dirname(__file__))
from model import CAREER_METADATA, CLUSTERS

def generate_enterprise_dataset(file_path: str, samples_per_career: int = 11000):
    print(f"--- Starting Enterprise Data Generation ---")
    print(f"Target: {samples_per_career} samples per career x {len(CAREER_METADATA)} careers")
    
    all_data = []
    
    # Salary Brackets
    SALARY_OPTIONS = ["Any", "$50k+", "$100k+", "$200k+"]
    
    # Common soft skills to mix in
    COMMON_SOFT_SKILLS = ["Communication", "Teamwork", "Problem Solving", "Adaptability", "Time Management"]

    for career, meta in CAREER_METADATA.items():
        # Get keywords for this career from CLUSTERS
        # Find the cluster that matches this career key
        keywords = CLUSTERS.get(career, [])
        tech_stack = meta.get("tech_stack", [])
        recommended_skills = meta.get("recommended_skills", [])
        
        salary_text = meta.get("salary_range", "$0")
        is_high_salary = "$100k" in salary_text or "$200k" in salary_text or "$150k" in salary_text
        is_elite_salary = "$200k" in salary_text or "$300k" in salary_text or "Million" in salary_text
        
        is_leadership = any(role in career for role in ["Manager", "Chief", "Head", "Director", "Officer", "Coach", "Planner"])
        
        print(f"Generating data for: {career}...")
        
        for _ in range(samples_per_career):
            # 1. Academic Score (Normal Dist based on difficulty)
            difficulty = meta.get("entry_difficulty", "Medium")
            if "High" in difficulty or "Extreme" in difficulty:
                score = min(100, max(60, np.random.normal(90, 5)))
            else:
                score = min(100, max(50, np.random.normal(75, 10)))
                
            # 2. Interests (Pick 1-2 keywords from cluster)
            # Sometimes pick a random one to add noise/robustness
            if random.random() < 0.8 and keywords:
                interest = random.choice(keywords)
            else:
                interest = "General"
                
            # 3. Technical Skills (Mix of recommended + tech stack)
            # Pick 2-4 appropriate skills
            pool = recommended_skills + tech_stack
            if pool:
                k = random.randint(2, min(4, len(pool)))
                selected_tech = random.sample(pool, k)
            else:
                selected_tech = ["General Skills"]
                
            # 4. Soft Skills
            selected_soft = random.sample(COMMON_SOFT_SKILLS, 2)
            
            # 5. Salary Expectation
            # If career matches high salary, user likely picked High or Any
            if is_elite_salary:
                salary_pref = random.choice(["$200k+", "$100k+", "Any"])
            elif is_high_salary:
                salary_pref = random.choice(["$100k+", "$50k+", "Any"])
            else:
                salary_pref = random.choice(["$50k+", "Any"])
                
            # 6. Leadership Preference
            # If it's a leadership role, high chance they wanted leadership
            if is_leadership:
                lead_pref = random.choice([True, True, True, False]) # 75% chance
            else:
                lead_pref = random.choice([False, False, True]) # 33% chance
            
            # 7. Extracurriculars
            # Simple random selection for now, could be smarter but this is fine
            extras = random.choice(["Sports", "Volunteering", "Debate Club", "Coding Club", "None", "Arts"])

            row = {
                "Academic_Percentage": round(score, 1),
                "Interest_Areas": interest,
                "Extracurriculars": extras,
                "Technical_Skills": ",".join(selected_tech),
                "Soft_Skills": ",".join(selected_soft),
                "Salary_Expectation": salary_pref,
                "Leadership_Preference": 1 if lead_pref else 0,
                "Career_Path": career
            }
            all_data.append(row)
            
    df = pd.DataFrame(all_data)
    
    # Shuffle
    df = df.sample(frac=1).reset_index(drop=True)
    
    # Save
    df.to_csv(file_path, index=False)
    print(f"SUCCESS: Generated {len(df)} rows for {len(CAREER_METADATA)} careers.")

if __name__ == "__main__":
    csv_path = os.path.join(os.path.dirname(__file__), "career_data_large.csv")
    generate_enterprise_dataset(csv_path)
