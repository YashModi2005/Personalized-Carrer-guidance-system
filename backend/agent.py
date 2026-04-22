import logging
import asyncio
import re
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor

import database
from schemas import ChatMessage, ChatResponse, UserAssessment, GuidanceResponse
from model import get_career_guidance
from explainable_ai import explain_prediction
from personalization_service import find_career_twins
from skill_analyzer import analyze_skill_gap

logger = logging.getLogger("career-coach-agent")

# Shared executor for heavy ML tasks
_agent_executor = ThreadPoolExecutor(max_workers=3)

class CareerCoachAgent:
    def __init__(self):
        # Base Personalities
        self.personalities = {
            "professional": (
                "You are a Senior Strategic AI Career Coach. "
                "Personality: Executive, precise, and data-obsessed. "
                "Goal: Provide high-fidelity career guidance mapping the user's current 'Input Signals' to 'Market Trajectories'. "
                "Rule: Always reference at least one specific skill from the user's profile."
            ),
            "friendly": (
                "You are a Friendly Career Mentor (Bhai/Friend). "
                "Personality: Warm, encouraging, and uses Hinglish (mix of Hindi and English) occasionally. "
                "Goal: Make career planning feel easy and stress-free. Use terms like 'Bhai', 'Don't worry', 'Sahi hai'. "
                "Rule: Keep responses conversational but still data-driven."
            )
        }
        
        # Regex Intents (Expanded for robustness)
        self.intents = {
            "prediction": re.compile(r"\b(predict|recommend|career|suggest|match|path|jobs|future)\b", re.I),
            "skill_guidance": re.compile(r"\b(skill|learn|study|roadmap|gap|improve|course|resources|mastery)\b", re.I),
            "explanation": re.compile(r"\b(why|reason|explain|how match|logic|evidence)\b", re.I),
            "personalization": re.compile(r"\b(similar|twin|people like me|benchmark|comparison|peers)\b", re.I),
            "greeting": re.compile(r"\b(hello|hi|hey|greetings|start|startup|coach|help)\b", re.I),
            "roadmap_query": re.compile(r"\b(roadmap|path|steps|journey|process|milestones|plan)\b", re.I),
            "skills_query": re.compile(r"\b(what skills|tools|tech stack|knowledge|stack|requirements)\b", re.I),
            "roles_query": re.compile(r"\b(jobs|roles|titles|positions|careers|market)\b", re.I),
            "salary_faq": re.compile(r"\b(salary|negotiate|pay|money|package|compensation|earnings)\b", re.I),
            "interview_faq": re.compile(r"\b(interview|questions|prep|prepare|tips|assessment)\b", re.I),
            "portfolio_faq": re.compile(r"\b(portfolio|projects|showcase|github|resume|cv)\b", re.I),
            "cert_faq": re.compile(r"\b(cert|certificate|credentials|badges|learning|study|courses)\b", re.I),
            "interview_mode": re.compile(r"\b(mock interview|start interview|practice questions|test me|ask me|interview practice)\b", re.I)
        }

    def _get_mastery_time(self, difficulty: str) -> str:
        """Calculate estimated learning curve based on trajectory difficulty."""
        mapping = {
            "High": "Accelerated Mastery (6-9 Months)",
            "Medium": "Strategic Focus (3-5 Months)",
            "Low": "Rapid Deployment (1-2 Months)"
        }
        return mapping.get(difficulty, "Standard Development (4 Months)")

    async def _get_context(self, user_id: int, session_id: Optional[str] = None) -> str:
        """Build a context string from DB history and latest recommendations."""
        if not user_id:
            return ""
            
        # 1. Fetch Chat History (Last 5 in current session or global fallback)
        history = database.get_user_chats(user_id, limit=5, session_id=session_id)
        history_str = "\n".join([f"User: {c['message']}\nAI: {c['response']}" for c in history])
        
        # 2. Fetch Latest Recommendation
        rec = database.get_latest_recommendation(user_id)
        rec_str = ""
        if rec:
            rec_str = (
                f"\n[Context: User is interested in {rec['interests']}. "
                f"Top Career Match: {rec['predicted_career']} ({int(rec['match_score']*100)}% match).]"
            )
            
        return f"{history_str}\n{rec_str}\n"

    def _detect_intent(self, message: str) -> str:
        msg = message.lower()
        
        # Priority: Check all registered intents in self.intents
        for name, pattern in self.intents.items():
            if pattern.search(msg):
                return name
                
        return "general"

    async def process_message(self, chat_msg: ChatMessage, user_id: Optional[int] = None) -> ChatResponse:
        message = chat_msg.message
        context_data = chat_msg.context # Frontend state fallback
        session_id = chat_msg.session_id
        personality_key = chat_msg.personality or "professional"
        system_prompt = self.personalities.get(personality_key, self.personalities["professional"])
        
        intent = self._detect_intent(message)
        logger.info(f"User {user_id} | Session: {session_id} | Personality: {personality_key} | Intent: {intent}")
        
        # Build context/history string (logged for terminal debug)
        history_context = await self._get_context(user_id, session_id=session_id)
        
        loop = asyncio.get_event_loop()

        # Handle Intent: Greeting
        if intent == "greeting":
            return ChatResponse(
                response=(
                    "Hello! I am your Professional AI Career Coach. I've analyzed your profile and I am ready to guide you. "
                    "**I can help you with these questions:**"
                ),
                intent="greeting",
                suggestions=[
                    "What's my top match?", 
                    "Show my roadmap", 
                    "What skills do I need?", 
                    "Start Mock Interview", 
                    "Interview tips", 
                    "Salary advice"
                ]
            )

        # Profile Resolution
        profile_data = context_data
        rec = database.get_latest_recommendation(user_id) if user_id else None
        
        if not profile_data and not rec:
            return ChatResponse(
                response="I'd love to help, but I don't have your career profile yet. Please complete the assessment first!",
                intent="general"
            )

        # Construct assessment object
        if profile_data:
            assessment = UserAssessment(**profile_data)
        else:
            assessment = UserAssessment(
                name=rec["name"],
                academic_percentage=rec["academic_percentage"],
                interests=rec["interests"],
                tech_skills=rec["tech_skills"].split(',') if isinstance(rec["tech_skills"], str) else rec["tech_skills"],
                soft_skills=rec["soft_skills"].split(',') if isinstance(rec["soft_skills"], str) else rec["soft_skills"],
                extracurriculars=rec["extracurriculars"]
            )

        # Handle Intent: Prediction
        if intent == "prediction":
            try:
                guidance = await loop.run_in_executor(_agent_executor, get_career_guidance, assessment)
                top = guidance.career_details[0]
                mastery = self._get_mastery_time(top.entry_difficulty)
                response = (
                    f"Based on your profile synchronization, **{top.career_title}** remains your strongest trajectory "
                    f"with a {int(top.match_score * 100)}% accuracy rating. {top.why_it_matches}\n\n"
                    f"**Learning Curve:** {mastery}"
                )
                return ChatResponse(response=response, intent="prediction", data=guidance, suggestions=["Why this career?", "What are the skill gaps?"])
            except Exception as e:
                logger.error(f"Agent Prediction Error: {e}")
                return ChatResponse(response="I'm having trouble analyzing your profile. Could you try refreshing your assessment?", intent="general")

        # Handle Intent: Skill Guidance
        if intent == "skill_guidance":
            try:
                career_title = rec["predicted_career"] if rec else (await loop.run_in_executor(_agent_executor, get_career_guidance, assessment)).career_details[0].career_title
                gap = await loop.run_in_executor(_agent_executor, analyze_skill_gap, career_title, assessment.tech_skills, assessment.soft_skills)
                
                # Fetch mastery time if we have metadata
                import model
                meta = model.CAREER_METADATA.get(career_title, {})
                mastery = self._get_mastery_time(meta.get("entry_difficulty", "Medium"))
                
                response = (
                    f"For the **{career_title}** path, your primary growth areas are: {', '.join(gap[:3])}. "
                    f"Mastering these will hyper-accelerate your growth! estimated **Learning Curve:** {mastery}."
                )
                return ChatResponse(response=response, intent="skill_guidance", suggestions=["Show resources", "How does this match?"])
            except Exception as e:
                return ChatResponse(response="Your current skills provide a solid foundation. Focus on technical depth and project work.", intent="general")

        # Handle Intent: Explanation
        if intent == "explanation":
            try:
                career_title = rec["predicted_career"] if rec else (await loop.run_in_executor(_agent_executor, get_career_guidance, assessment)).career_details[0].career_title
                xai_data = await loop.run_in_executor(_agent_executor, explain_prediction, assessment, career_title)
                return ChatResponse(response=xai_data["explanation"], intent="explanation", suggestions=["What skills do I need?", "Show similar profiles"])
            except Exception as e:
                return ChatResponse(response="This career matches your combined academic performance and technical interests.", intent="general")

        # Handle Intent: Personalization
        if intent == "personalization":
            try:
                twins = await loop.run_in_executor(_agent_executor, find_career_twins, assessment)
                paths = ", ".join([t['predicted_career_path'] for t in twins[:2]])
                response = f"People with profiles similar to yours often pursue paths like: {paths}. It's a proven roadmap for success!"
                return ChatResponse(response=response, intent="personalization", suggestions=["Bridge my skill gap", "Salary details"])
            except Exception as e:
                return ChatResponse(response="Many successful professionals with your skill set have found great careers in various technical domains.", intent="general")

        # Handle Intent: Roadmap
        if intent == "roadmap_query":
            import model
            career_title = rec["predicted_career"] if rec else (await loop.run_in_executor(_agent_executor, get_career_guidance, assessment)).career_details[0].career_title
            meta = model.CAREER_METADATA.get(career_title, {})
            steps = meta.get("learning_roadmap", ["Master core fundamentals", "Build projects", "Apply for internships"])
            response = f"Your personalized journey to becoming a **{career_title}** involves these key milestones:\n\n" + "\n".join([f"{i+1}. {step}" for i, step in enumerate(steps)])
            return ChatResponse(response=response, intent="roadmap_query", suggestions=["What skills are needed?", "Show similar profiles"])

        # Handle Intent: Recommended Skills
        if intent == "skills_query":
            import model
            career_title = rec["predicted_career"] if rec else (await loop.run_in_executor(_agent_executor, get_career_guidance, assessment)).career_details[0].career_title
            meta = model.CAREER_METADATA.get(career_title, {})
            skills = meta.get("recommended_skills", [])
            tech = meta.get("tech_stack", [])
            response = f"To excel in the **{career_title}** domain, you should prioritize these skills:\n\n* **Core**: {', '.join(skills)}\n* **Tech Stack**: {', '.join(tech)}"
            return ChatResponse(response=response, intent="skills_query", suggestions=["How long to master these?", "Show roadmap"])

        # Handle Intent: Potential Roles
        if intent == "roles_query":
            import model
            career_title = rec["predicted_career"] if rec else (await loop.run_in_executor(_agent_executor, get_career_guidance, assessment)).career_details[0].career_title
            meta = model.CAREER_METADATA.get(career_title, {})
            roles = meta.get("potential_jobs", ["Specialist", "Consultant", "Lead"])
            response = f"The **{career_title}** path opens doors to several exciting roles, such as: **{', '.join(roles)}**. Which of these interests you most?"
            return ChatResponse(response=response, intent="roles_query", suggestions=["What's the salary?", "Describe the roadmap"])

        # Handle Intent: Salary FAQ
        if intent == "salary_faq":
            return ChatResponse(
                response=(
                    "When negotiating salary, research market rates for your role (e.g., Glassdoor). "
                    "Focus on the value you bring and your technical specialized skills. Always ask for a "
                    "range and be prepared to discuss total compensation, including benefits."
                ),
                intent="salary_faq",
                suggestions=["Average salary for my role", "How to negotiate?"]
            )

        # Handle Intent: Interview FAQ
        if intent == "interview_faq":
            return ChatResponse(
                response=(
                    "To ace your interview: 1. Research the company thoroughly. 2. Practice STAR method for "
                    "behavioral questions. 3. Be ready for a live technical assessment or portfolio review. "
                    "Always have 3 questions ready to ask the interviewer!"
                ),
                intent="interview_faq",
                suggestions=["Common coding questions", "Mock interview tips"]
            )

        # Handle Intent: Portfolio FAQ
        if intent == "portfolio_faq":
            return ChatResponse(
                response=(
                    "A great portfolio should showcase 3-5 high-quality projects. Focus on 'Process over Result'—"
                    "explain the problem you solved, the tools used, and the impact. Use platforms like GitHub "
                    "for code or Behance for design."
                ),
                intent="portfolio_faq",
                suggestions=["Show project ideas", "How to host my portfolio?"]
            )

        # Handle Intent: Certification FAQ
        if intent == "cert_faq":
            return ChatResponse(
                response=(
                    "Certifications validate your skills but don't replace projects. For technical roles, "
                    "look into platform-specific certs (AWS, Google Cloud, Cisco) or specialized ones (OSCP for security). "
                    "Continuous learning is key in this rapidly evolving market."
                ),
                intent="cert_faq",
                suggestions=["Top certs for my role", "Learning roadmap"]
            )

        # Handle Intent: Interview Mode (Dynamic Q&A)
        if intent == "interview_mode":
            import model
            career_title = rec["predicted_career"] if rec else (await loop.run_in_executor(_agent_executor, get_career_guidance, assessment)).career_details[0].career_title
            meta = model.CAREER_METADATA.get(career_title, {})
            questions = meta.get("interview_questions", ["What are your long-term career goals?", "Tell me about a challenging project you've worked on.", "How do you stay updated with industry trends?"])
            
            # Check history to see how many questions were asked
            asked_count = 0
            for c in (database.get_user_chats(user_id, limit=10, session_id=session_id) if user_id else []):
                if any(q in c['response'] for q in questions):
                    asked_count += 1
            
            if asked_count < len(questions):
                next_q = questions[asked_count]
                response = (
                    f"### 🎙️ Neural Interview Mode: **{career_title}**\n"
                    f"Let's test your readiness! Question {asked_count + 1} of {len(questions)}:\n\n"
                    f"**{next_q}**"
                )
                return ChatResponse(response=response, intent="interview_mode", suggestions=["Skip to next", "I'm not sure", "End interview"])
            else:
                return ChatResponse(
                    response="You've completed all the practice questions for this role! Great job. Would you like to review your roadmap or explore other careers?",
                    intent="interview_mode",
                    suggestions=["Show roadmap", "Check skill gaps"]
                )

        # Default Response
        return ChatResponse(
            response="That's a great point. As your career coach, I'm here to navigate your potential. Would you like to discuss your latest matches or explore missing skills?",
            intent="general",
            suggestions=["Top career match", "Skill roadmap", "Similar profiles"]
        )

# Singleton Instance
coach_agent = CareerCoachAgent()
