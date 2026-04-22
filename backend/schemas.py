from pydantic import BaseModel, field_validator
from typing import List, Optional, Union

class UserAssessment(BaseModel):
    name: str
    academic_percentage: float
    interests: str
    tech_skills: List[str]
    soft_skills: Union[List[str], str]
    extracurriculars: str

    @field_validator('tech_skills', 'soft_skills', mode='before')
    @classmethod
    def parse_skills(cls, v):
        if isinstance(v, str):
            return [s.strip() for s in v.split(',') if s.strip()]
        return v

class CareerRecommendation(BaseModel):
    career_title: str
    match_score: float
    description: str
    why_it_matches: str
    recommended_skills: List[str]
    potential_jobs: List[str]
    salary_range: str
    growth_outlook: str
    learning_roadmap: List[str]
    core_challenges: str
    tech_stack: List[str]
    work_life_balance: str
    entry_difficulty: str
    top_employers: List[str]
    radar_dimensions: Optional[dict] = {}

class FeatureImportance(BaseModel):
    name: str
    value: float

class GuidanceResponse(BaseModel):
    is_valid: bool = True
    validation_message: Optional[str] = ""
    ml_recommendations: List[dict]
    career_details: List[CareerRecommendation]
    explanation: Optional[str] = ""
    top_features: Optional[List[FeatureImportance]] = []
    career_twin: Optional[List[dict]] = []
    skill_gap: Optional[List[str]] = []
    skill_resources: Optional[dict] = {}

class ChatMessage(BaseModel):
    message: str
    session_id: str
    personality: Optional[str] = "professional" # "professional" or "friendly"
    context: Optional[dict] = {}

class ChatResponse(BaseModel):
    response: str
    intent: str
    data: Optional[GuidanceResponse] = None
    suggestions: Optional[List[str]] = []
