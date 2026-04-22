from model import CAREER_METADATA
import logging

logger = logging.getLogger("skill-analyzer")

# Course mappings for the Smart Resource Hub
SKILL_RESOURCES = {
    "Clean Code": [
        {"platform": "Udemy", "title": "Clean Code: Writing Code for Humans", "url": "https://www.udemy.com/course/clean-code/"},
        {"platform": "YouTube", "title": "Principles of Clean Code", "url": "https://www.youtube.com/watch?v=UjhX2anvkM8"}
    ],
    "System Design": [
        {"platform": "Coursera", "title": "Software Design and Architecture", "url": "https://www.coursera.org/specializations/software-design-architecture"},
        {"platform": "YouTube", "title": "System Design Interview Prep", "url": "https://www.youtube.com/watch?v=m8Icp_CidEc"}
    ],
    "Machine Learning": [
        {"platform": "Coursera", "title": "Machine Learning Specialization", "url": "https://www.coursera.org/specializations/machine-learning-introduction"},
        {"platform": "Udemy", "title": "Machine Learning A-Z", "url": "https://www.udemy.com/course/machinelearning/"}
    ],
    "Data Visualization": [
        {"platform": "Udemy", "title": "Tableau 2024 A-Z", "url": "https://www.udemy.com/course/tableau10/"},
        {"platform": "YouTube", "title": "Data Visualization Principles", "url": "https://www.youtube.com/watch?v=9S_O5O8Z0-4"}
    ],
    "Prototyping": [
        {"platform": "Udemy", "title": "Figma UI/UX Design Essentials", "url": "https://www.udemy.com/course/figma-ux-ui-design-user-experience-tutorial-course/"},
        {"platform": "YouTube", "title": "High-Fidelity Prototyping in Figma", "url": "https://www.youtube.com/watch?v=0LshjKgej9U"}
    ],
    "Network Security": [
        {"platform": "Coursera", "title": "Google Cybersecurity Certificate", "url": "https://www.coursera.org/professional-certificates/google-cybersecurity"},
        {"platform": "YouTube", "title": "Network Security Fundamentals", "url": "https://www.youtube.com/watch?v=U_PzSInq3To"}
    ],
    "Agile Methodology": [
        {"platform": "Coursera", "title": "Agile with Atlassian Jira", "url": "https://www.coursera.org/learn/agile-atlassian-jira"},
        {"platform": "YouTube", "title": "Agile Scrum Tutorial", "url": "https://www.youtube.com/watch?v=9TycLR0TqFA"}
    ],
    "Statistical Analysis": [
        {"platform": "Coursera", "title": "Statistics with Python Specialization", "url": "https://www.coursera.org/specializations/statistics-with-python"},
        {"platform": "YouTube", "title": "Statistics for Data Science", "url": "https://www.youtube.com/watch?v=Vfo5le26IhY"}
    ],
    "Big Data": [
        {"platform": "Udemy", "title": "The Ultimate Hands-On Hadoop", "url": "https://www.udemy.com/course/the-ultimate-hands-on-hadoop-tame-your-big-data/"},
        {"platform": "YouTube", "title": "Big Data Fundamentals", "url": "https://www.youtube.com/watch?v=bAyrObl7TYE"}
    ],
    "Observational Astronomy": [
        {"platform": "Coursera", "title": "Astronomy: Exploring Time and Space", "url": "https://www.coursera.org/learn/astronomy"},
        {"platform": "YouTube", "title": "Introduction to Observational Astronomy", "url": "https://www.youtube.com/watch?v=0_u6Wz_tV_U"}
    ],
    "Astrophysics": [
        {"platform": "edX", "title": "Astrophysics Series", "url": "https://www.edx.org/course/astrophysics-exploring-exoplanets"},
        {"platform": "YouTube", "title": "Astrophysics for Beginners", "url": "https://www.youtube.com/watch?v=hBToM-f8n6o"}
    ],
    "Psychological Astrology": [
        {"platform": "Udemy", "title": "Psychological Astrology & Self-Discovery", "url": "https://www.udemy.com/course/psychological-astrology/"},
        {"platform": "YouTube", "title": "Astrology and Psychology Dynamics", "url": "https://www.youtube.com/watch?v=XhF6p_S3Z28"}
    ],
    "Experimental Design": [
        {"platform": "Coursera", "title": "Research Methods and Statistics", "url": "https://www.coursera.org/specializations/research-methods"},
        {"platform": "YouTube", "title": "Principles of Experimental Design", "url": "https://www.youtube.com/watch?v=1Gf-t8_Lsh4"}
    ]
}

def analyze_skill_gap(predicted_career: str, user_tech_skills: str, user_soft_skills: str):
    """
    Compares user's current skills with the recommended skills for the predicted career.
    """
    try:
        if predicted_career not in CAREER_METADATA:
            logger.warning(f"Career '{predicted_career}' not found in metadata.")
            return []
            
        required_skills = CAREER_METADATA[predicted_career].get("recommended_skills", [])
        
        # Parse user skills
        user_skills_list = []
        if isinstance(user_tech_skills, str):
            user_skills_list.extend([s.strip().lower() for s in user_tech_skills.split(',') if s.strip()])
        if isinstance(user_soft_skills, str):
            user_skills_list.extend([s.strip().lower() for s in user_soft_skills.split(',') if s.strip()])
            
        gap = []
        for skill in required_skills:
            if skill.lower() not in user_skills_list:
                gap.append(skill)
                
        return gap
    except Exception as e:
        logger.error(f"Error in skill gap analysis: {e}")
        return []
