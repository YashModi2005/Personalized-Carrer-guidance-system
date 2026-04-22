import pandas as pd
import numpy as np
import random
import os

def generate_kaggle_like_dataset(file_path: str, num_rows: int = 500000):
    print(f"--- Generating {num_rows} Kaggle-style records in {file_path} ---")
    
    technical_skills_pool = [
        "Python", "Java", "C++", "React", "SQL", "Cloud Computing", "Data Analysis", "Cybersecurity", "Blockchain",
        "Biology", "Chemistry", "Anatomy", "Patient Care", "Medical Ethics", "Pharmacology",
        "Graphic Design", "Sketching", "Video Editing", "Content Writing", "SEO",
        "Accounting", "Financial Modeling", "Taxation", "Project Management",
        "Botany", "Soil Science", "Farming Techniques", "Sustainability", "Landscape Design",
        "Military Strategy", "Weaponry Systems", "Navigation", "Combat Training", "Intelligence Analysis",
        "Legal Research", "Constitutional Law", "Debate", "Policy Analysis", "Contracts",
        "Thermodynamics", "CAD (AutoCAD)", "Structural Analysis", "Circuit Design", "Mechanics",
        "Sports Science", "Kinesiology", "Coaching", "Athletic Training"
    ]
    soft_skills_pool = ["Communication", "Leadership", "Teamwork", "Problem Solving", "Creativity", "Critical Thinking", "Empathy", "Time Management", "Adaptability", "Discipline", "Resilience", "Ethics", "Public Speaking"]
    interests_pool = [
        "Artificial Intelligence", "Sustainability", "Finance", "Healthcare", "E-commerce", "Education", "Gaming",
        "Medicine", "Mental Health", "Art", "Writing", "Business", "Environment",
        "Nature/Plants", "Military/Defense", "Law/Politics", "Engineering/Building", "Sports/Fitness", "Science/Research"
    ]
    extracurriculars_pool = ["Sports", "Art", "Volunteering", "Photography", "Debate", "Music", "Red Cross", "Science Club", "Coding Club", "ROTC/Cadets", "Gardening Club", "Student Government", "Robotics Club", "Legal Aid"]
    
    career_paths = [
        "Software Engineer", "Data Scientist", "UI/UX Designer", "Full Stack Developer", "Cybersecurity Analyst", "Cloud Architect", "Product Manager", "Machine Learning Engineer",
        "Nurse", "Doctor", "Pharmacist", "Medical Researcher",
        "Graphic Designer", "Content Writer", "Digital Marketer",
        "Accountant", "Financial Analyst", "HR Manager",
        "Agriculturist", "Botanist", "Landscape Architect",
        "Army Officer", "Air Force Pilot", "Intelligence Analyst",
        "Lawyer", "Policy Analyst",
        "Civil Engineer", "Mechanical Engineer",
        "Biologist", "Chemist", "Environmental Scientist",
        "Professional Athlete", "Sports Coach"
    ]

    # 1. Generate base features first
    data = {
        "User_ID": range(1, num_rows + 1),
        "Age": np.random.randint(18, 25, num_rows),
        "Academic_Percentage": np.random.uniform(60, 100, num_rows),
        "Technical_Skills": [",".join(random.sample(technical_skills_pool, random.randint(2, 5))) for _ in range(num_rows)],
        "Soft_Skills": [",".join(random.sample(soft_skills_pool, random.randint(2, 4))) for _ in range(num_rows)],
        "Interest_Areas": [random.choice(interests_pool) for _ in range(num_rows)],
        "Extracurriculars": [random.choice(extracurriculars_pool) for _ in range(num_rows)],
    }

    # 2. Logic-based Career Path Assignment
    career_weights = {
        "Software Engineer": {"Python": 2, "Java": 2, "C++": 2, "Problem Solving": 1},
        "Data Scientist": {"Data Analysis": 3, "Python": 2, "Artificial Intelligence": 3, "Critical Thinking": 1},
        "UI/UX Designer": {"Creativity": 3, "Art": 3, "Gaming": 1, "Graphic Design": 2},
        "Full Stack Developer": {"React": 3, "SQL": 2, "Java": 1, "Communication": 1},
        "Cybersecurity Analyst": {"Cybersecurity": 5, "Critical Thinking": 2, "Problem Solving": 1},
        "Cloud Architect": {"Cloud Computing": 5, "Blockchain": 1, "Sustainability": 1},
        "Product Manager": {"Leadership": 4, "Communication": 3, "Finance": 2, "Debate": 1},
        "Machine Learning Engineer": {"Artificial Intelligence": 5, "Python": 2, "Blockchain": 1},
        
        "Nurse": {"Patient Care": 5, "Biology": 3, "Empathy": 4, "Healthcare": 3, "Volunteering": 1},
        "Doctor": {"Medicine": 5, "Anatomy": 4, "Biology": 3, "Critical Thinking": 3, "Science Club": 1},
        "Pharmacist": {"Pharmacology": 5, "Chemistry": 4, "Medicine": 2, "Patient Care": 1},
        "Medical Researcher": {"Biology": 4, "Chemistry": 4, "Data Analysis": 2, "Critical Thinking": 3},
        
        "Graphic Designer": {"Graphic Design": 5, "Sketching": 4, "Creativity": 3, "Art": 3},
        "Content Writer": {"Content Writing": 5, "SEO": 2, "Creativity": 3, "Writing": 4},
        "Digital Marketer": {"SEO": 4, "Data Analysis": 2, "Communication": 3, "Writing": 2},
        
        "Accountant": {"Accounting": 5, "Taxation": 4, "Finance": 3, "Critical Thinking": 2},
        "Financial Analyst": {"Financial Modeling": 5, "Data Analysis": 3, "Finance": 4, "Problem Solving": 2},
        "HR Manager": {"Communication": 4, "Empathy": 3, "Leadership": 3, "Business": 2},

        # --- NEW DOMAINS ---
        "Agriculturist": {"Farming Techniques": 5, "Soil Science": 4, "Sustainability": 3, "Nature/Plants": 3, "Gardening Club": 2},
        "Botanist": {"Botany": 5, "Biology": 4, "Nature/Plants": 4, "Science/Research": 3, "Gardening Club": 2},
        "Landscape Architect": {"Landscape Design": 5, "Botany": 3, "CAD (AutoCAD)": 3, "Creativity": 3},
        
        "Army Officer": {"Military Strategy": 5, "Leadership": 4, "Discipline": 4, "Combat Training": 3, "Military/Defense": 3, "ROTC/Cadets": 2},
        "Air Force Pilot": {"Navigation": 5, "Physics": 3, "Discipline": 4, "Military/Defense": 3, "Video Editing": 1}, # Video games -> reflexes?
        "Intelligence Analyst": {"Intelligence Analysis": 5, "Critical Thinking": 4, "Cybersecurity": 2, "Military Strategy": 2},
        
        "Lawyer": {"Legal Research": 5, "Constitutional Law": 4, "Debate": 4, "Public Speaking": 3, "Law/Politics": 3, "Legal Aid": 2},
        "Policy Analyst": {"Policy Analysis": 5, "Legal Research": 3, "Writing": 3, "Law/Politics": 3},
        
        "Civil Engineer": {"Structural Analysis": 5, "CAD (AutoCAD)": 4, "Physics": 3, "Engineering/Building": 3},
        "Mechanical Engineer": {"Mechanics": 5, "Thermodynamics": 4, "CAD (AutoCAD)": 4, "Robotics Club": 2},
        
        "Biologist": {"Biology": 5, "Science/Research": 4, "Data Analysis": 2, "Science Club": 2},
        "Chemist": {"Chemistry": 5, "Science/Research": 4, "Data Analysis": 2, "Science Club": 2},
        "Environmental Scientist": {"Sustainability": 5, "Biology": 3, "Ecology": 3, "Environment": 4},
        
        "Professional Athlete": {"Sports Science": 2, "Discipline": 5, "Resilience": 4, "Sports/Fitness": 5, "Sports": 5},
        "Sports Coach": {"Coaching": 5, "Leadership": 4, "Communication": 3, "Sports/Fitness": 4, "Sports": 3}
    }

    careers = []
    for i in range(num_rows):
        tech_s = data["Technical_Skills"][i]
        soft_s = data["Soft_Skills"][i]
        interest = data["Interest_Areas"][i]
        extra = data["Extracurriculars"][i]
        
        scores = {c: 1.0 for c in career_paths} # Default base score
        for career, weights in career_weights.items():
            for feature_val, weight in weights.items():
                if feature_val in tech_s or feature_val in soft_s or feature_val == interest or feature_val == extra:
                    scores[career] += weight
        
        # Pick best career with slight noise
        if random.random() < 0.05: # 5% noise
            careers.append(random.choice(career_paths))
        else:
            careers.append(max(scores, key=scores.get))
    
    data["Career_Path"] = careers
    df = pd.DataFrame(data)
    
    # 3. Add Kaggle-specific noise (duplicates, nulls, outliers)
    dup_indices = random.sample(range(num_rows), int(num_rows * 0.03))
    df = pd.concat([df, df.iloc[dup_indices]], ignore_index=True)
    
    null_indices = random.sample(range(len(df)), int(len(df) * 0.01))
    df.loc[null_indices, 'Academic_Percentage'] = np.nan
    
    outlier_indices = random.sample(range(len(df)), int(len(df) * 0.005))
    df.loc[outlier_indices, 'Academic_Percentage'] = np.random.uniform(200, 500, len(outlier_indices))
    
    df.to_csv(file_path, index=False)
    print(f"✅ Success: Dataset saved with {len(df)} rows.")

if __name__ == "__main__":
    csv_path = os.path.join(os.path.dirname(__file__), "kaggle_career_dataset.csv")
    generate_kaggle_like_dataset(csv_path)
