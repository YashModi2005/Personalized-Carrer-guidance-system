import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI, HTTPException, UploadFile, File, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
import uvicorn
import shutil
import os
from pydantic import BaseModel
from typing import Optional

from schemas import UserAssessment, GuidanceResponse, ChatMessage, ChatResponse
from model import get_career_guidance
from explainable_ai import explain_prediction
from personalization_service import find_career_twins
from skill_analyzer import analyze_skill_gap
from agent import coach_agent
import database
import auth

# Thread pool for running sync-heavy ML tasks concurrently
_executor = ThreadPoolExecutor(max_workers=4)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("career-pilot-api")

# Tokenizer for joblib
def comma_tokenizer(text):
    return text.split(',')

app = FastAPI(title="Personalized Career Guidance System")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
database.init_db()

class UserCreate(BaseModel):
    username: str
    password: str
    role: str
    secret_key: Optional[str] = None

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "AI Career Pilot Engine is operational",
        "version": "1.1.0"
    }

@app.post("/auth/signup")
async def signup(user_data: UserCreate):
    # Admin Security Check
    if user_data.role == 'counselor':
        admin_key = os.getenv('ADMIN_SECRET_KEY', 'admin')
        if user_data.secret_key != admin_key:
            raise HTTPException(status_code=403, detail="Invalid admin secret key")

    hashed_pwd = auth.get_password_hash(user_data.password)
    success = database.create_user(user_data.username, hashed_pwd, user_data.role)
    if not success:
        raise HTTPException(status_code=400, detail="Username already registered")
    return {"message": "User created successfully"}

@app.post("/auth/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    secret_key: Optional[str] = Form(None)
):
    user = database.get_user_by_username(form_data.username)
    if not user or not auth.verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    # Admin Security Check for existing accounts
    if user["role"] == 'counselor':
        admin_key = os.getenv('ADMIN_SECRET_KEY', 'admin')
        if secret_key != admin_key:
            raise HTTPException(status_code=403, detail="Admin secret key required for Counselor access")

    access_token = auth.create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer", "role": user["role"]}

@app.get("/admin/recommendations")
async def get_recommendations(current_user: dict = Depends(auth.role_required(["counselor"]))):
    try:
        data = database.get_all_recommendations()
        return {"recommendations": data}
    except Exception as e:
        logger.error(f"Admin Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch recommendations")

@app.get("/admin/stats")
async def get_admin_stats(current_user: dict = Depends(auth.role_required(["counselor"]))):
    try:
        return database.get_stats()
    except Exception as e:
        logger.error(f"Stats Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch stats")

@app.post("/admin/upload-dataset")
async def upload_dataset(file: UploadFile = File(...), current_user: dict = Depends(auth.role_required(["counselor"]))):
    try:
        data_dir = os.path.join(os.path.dirname(__file__), "data")
        os.makedirs(data_dir, exist_ok=True)
        file_path = os.path.join(data_dir, f"new_dataset_{file.filename}")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"status": "success", "message": f"Dataset {file.filename} uploaded."}
    except Exception as e:
        logger.error(f"Upload Error: {e}")
        raise HTTPException(status_code=500, detail="File upload failed")

@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage, current_user: dict = Depends(auth.get_current_user)):
    try:
        response = await coach_agent.process_message(message, user_id=current_user["id"])
        database.save_chat(current_user["id"], message.message, response.response, session_id=message.session_id)
        return response
    except Exception as e:
        logger.error(f"Chat Error: {e}")
        raise HTTPException(status_code=500, detail="The AI Coach is currently unavailable.")

@app.get("/student/history")
async def get_student_history(current_user: dict = Depends(auth.get_current_user)):
    try:
        data = database.get_user_recommendations(current_user["id"])
        return {"recommendations": data}
    except Exception as e:
        logger.error(f"History Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch history")

@app.get("/student/chats")
async def get_student_chats(current_user: dict = Depends(auth.get_current_user)):
    try:
        data = database.get_user_chats(current_user["id"], limit=100)
        return {"chats": data}
    except Exception as e:
        logger.error(f"Chat History Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch chat logs")

@app.post("/recommend", response_model=GuidanceResponse)
async def recommend(assessment: UserAssessment, current_user: dict = Depends(auth.get_current_user)):
    try:
        loop = asyncio.get_event_loop()
        
        # Step 1: Core career guidance (blocking, must run first)
        guidance = await loop.run_in_executor(_executor, get_career_guidance, assessment)
        
        # If invalid, stop here and return the validation error
        if not guidance.is_valid:
            return guidance
            
        top_prediction_obj = guidance.career_details[0]
        top_prediction = top_prediction_obj.career_title
        
        # Step 2: Run SHAP, twins, and skill-gap CONCURRENTLY for a big speed boost
        def _xai():
            return explain_prediction(assessment, target_career=top_prediction)
        def _twins():
            return find_career_twins(assessment)
        def _gap():
            return analyze_skill_gap(top_prediction, assessment.tech_skills, assessment.soft_skills)
        
        xai_future = loop.run_in_executor(_executor, _xai)
        twins_future = loop.run_in_executor(_executor, _twins)
        gap_future = loop.run_in_executor(_executor, _gap)
        
        xai_data, twins, gap = await asyncio.gather(xai_future, twins_future, gap_future)
        
        # Step 3: Map skill gaps to resources
        from skill_analyzer import SKILL_RESOURCES
        resources = {}
        for skill in gap:
            if skill in SKILL_RESOURCES:
                resources[skill] = SKILL_RESOURCES[skill]
        
        guidance.explanation = xai_data["explanation"]
        guidance.top_features = xai_data["top_features"]
        guidance.career_twin = twins
        guidance.skill_gap = gap
        guidance.skill_resources = resources
        
        # Step 4: Persist to DB asynchronously
        import json
        full_json = json.dumps(guidance.dict(), default=str)
        loop.run_in_executor(
            _executor, 
            database.save_recommendation, 
            assessment, 
            top_prediction,
            top_prediction_obj.match_score, 
            current_user.get("id"), 
            full_json
        )
        
        return guidance
    except Exception as e:
        logger.error(f"Recommendation Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
