import os
from typing import List
from schemas import UserAssessment, GuidanceResponse, CareerRecommendation
from predict import get_ml_recommendations

# Static Career Metadata expanded with Healthcare/Nursing
CAREER_METADATA = {
    "Software Engineer": {
        "description": "Design, develop, and maintain complex software systems and applications using diverse programming paradigms.",
        "why_it_matches": "Extremely strong alignment with technical problem solving and software architecture interests.",
        "recommended_skills": ["Clean Code", "System Design", "Unit Testing", "Version Control"],
        "potential_jobs": ["Backend Engineer", "Mobile Developer", "Systems Architect"],
        "salary_range": "$95k - $185k",
        "growth_outlook": "High (25% Projected Growth)",
        "learning_roadmap": ["Master CS Fundamentals", "Build High-Scale Portfolio", "Acquire Lead Architect Certs"],
        "core_challenges": "Rapidly shifting technology stacks and high-intensity debugging phases.",
        "tech_stack": ["Java/Go/C++", "Docker/K8s", "Next.js", "PostgreSQL"],
        "work_life_balance": "Moderate (High Flexibility / Peak Cycles)",
        "entry_difficulty": "High (Technical Depth Required)",
        "top_employers": ["Google", "Meta", "Amazon", "OpenAI"],
        "radar_dimensions": {
            "Engineering": 9,
            "Analytical": 8,
            "Creative": 4,
            "Strategy": 5,
            "Security": 6
        },
        "interview_questions": [
            "Explain the difference between a Process and a Thread.",
            "What is a RESTful API and what are its key principles?",
            "How would you optimize a slow SQL query?",
            "What is the importance of Version Control (Git) in a team setting?"
        ]
    },
    "Data Scientist": {
        "description": "Extract insights from structured and unstructured data to drive strategic decision-making using statistical modeling.",
        "why_it_matches": "Matches your analytical mindset and proficiency in data manipulation and statistical reasoning.",
        "recommended_skills": ["Statistical Analysis", "Data Visualization", "Big Data", "Machine Learning"],
        "potential_jobs": ["Data Analyst", "Research Scientist", "Business Intelligence Dev"],
        "salary_range": "$110k - $210k",
        "growth_outlook": "Explosive (32% Projected Growth)",
        "learning_roadmap": ["Advanced Math/Statistics", "Master Data Pipelines", "Deploy Production Models"],
        "core_challenges": "Ensuring data quality and managing stakeholder expectations on predictive accuracy.",
        "tech_stack": ["Python/R", "PyTorch", "Spark", "Tableau"],
        "work_life_balance": "Balanced (High Autonomy)",
        "entry_difficulty": "High (Advanced Math / Stat Req)",
        "top_employers": ["Netflix", "Microsoft", "Palantir", "DeepMind"],
        "radar_dimensions": {
            "Engineering": 7,
            "Analytical": 10,
            "Creative": 5,
            "Strategy": 7,
            "Security": 5
        },
        "interview_questions": [
            "What is the difference between Supervised and Unsupervised learning?",
            "How do you handle missing or noisy data in a dataset?",
            "Explain the concept of Overfitting and how to prevent it.",
            "What are the key metrics for evaluating a classification model?"
        ]
    },
    "UI/UX Designer": {
        "description": "Create intuitive and visually stunning user experiences by blending design principles with user research.",
        "why_it_matches": "Strong correlation between your creative flair and user-centric problem-solving approach.",
        "recommended_skills": ["Prototyping", "User Research", "Visual Design", "Wireframing"],
        "potential_jobs": ["Product Designer", "Interaction Designer", "Visual Architect"],
        "salary_range": "$85k - $160k",
        "growth_outlook": "Strong (18% Projected Growth)",
        "learning_roadmap": ["Master Design Systems", "Conduct Deep User Research", "Build Interactive Prototypes"],
        "core_challenges": "Balancing aesthetic vision with technical constraints and user accessibility.",
        "tech_stack": ["Figma", "Adobe Creative Suite", "Lottie", "Webflow"],
        "work_life_balance": "High (Remote-Friendly)",
        "entry_difficulty": "Medium (Portfolio-Driven)",
        "top_employers": ["Apple", "Airbnb", "Adobe", "Canva"],
        "radar_dimensions": {
            "Engineering": 4,
            "Analytical": 6,
            "Creative": 10,
            "Strategy": 6,
            "Security": 3
        },
        "interview_questions": [
            "What is the difference between UX and UI design?",
            "Explain your design process from wireframe to prototype.",
            "How do you handle negative feedback from a client on a design?",
            "What is 'Mobile-First' design and why is it important?"
        ]
    },
    "Full Stack Developer": {
        "description": "Build end-to-end web applications, handling both front-facing user interfaces and server-side logic.",
        "why_it_matches": "Perfect match for your versatile skill set covering both client-side and server-side technologies.",
        "recommended_skills": ["React/Vue", "Node.js/Python", "Database Design", "API Development"],
        "potential_jobs": ["Web Developer", "Platform Engineer", "SaaS Developer"],
        "salary_range": "$90k - $175k",
        "growth_outlook": "Steady (22% Projected Growth)",
        "learning_roadmap": ["Master Frontend Frameworks", "Learn Serverless Architecture", "Build Full-Stack Apps"],
        "core_challenges": "Managing the complexity of the entire application layer and state management.",
        "tech_stack": ["React/Next.js", "Node/Express", "MongoDB", "AWS/Vercel"],
        "work_life_balance": "Moderate (Hybrid Standard)",
        "entry_difficulty": "Medium (Practical Project Req)",
        "top_employers": ["Stripe", "Shopify", "Vercel", "Freelance"],
        "radar_dimensions": {
            "Engineering": 8,
            "Analytical": 7,
            "Creative": 7,
            "Strategy": 6,
            "Security": 5
        },
        "interview_questions": [
            "Explain the difference between Client-side and Server-side rendering.",
            "What is a Closure in JavaScript and how is it used?",
            "How do you secure a web application against SQL injection?",
            "What is 'State Management' and why is it needed in modern frameworks?"
        ]
    },
    "Cybersecurity Analyst": {
        "description": "Protect an organization's sensitive data and systems from cyber threats through monitoring and defense strategies.",
        "why_it_matches": "Aligns with your focus on system security, network protocols, and ethical hacking.",
        "recommended_skills": ["Network Security", "Penetration Testing", "Risk Assessment", "Incident Response"],
        "potential_jobs": ["Security Auditor", "Threat Hunter", "Compliance Officer"],
        "salary_range": "$100k - $190k",
        "growth_outlook": "Critical (35% Projected Growth)",
        "learning_roadmap": ["Attain Security+ / OSCP", "Master Network Defense", "Engage in CTF Challenges"],
        "core_challenges": "Staying ahead of sophisticated and ever-evolving global cyber threats.",
        "tech_stack": ["Kali Linux", "Wireshark", "Splunk", "Metasploit"],
        "work_life_balance": "Moderate (On-call Duty Common)",
        "entry_difficulty": "High (Certifications / Ethics Req)",
        "top_employers": ["CrowdStrike", "Palantir", "FBI", "Accenture"],
        "radar_dimensions": {
            "Engineering": 7,
            "Analytical": 8,
            "Creative": 3,
            "Strategy": 5,
            "Security": 10
        }
    },
    "Cloud Architect": {
        "description": "Design and manage scalable cloud computing strategies and environments for high-performance applications.",
        "why_it_matches": "Matches your interest in scalable infrastructure and modern cloud-native architectures.",
        "recommended_skills": ["AWS/Azure/GCP", "Kubernetes", "Infrastructure as Code", "Serverless"],
        "potential_jobs": ["DevOps Engineer", "Cloud Consultant", "SRE"],
        "salary_range": "$120k - $230k",
        "growth_outlook": "Robust (28% Projected Growth)",
        "learning_roadmap": ["AWS Solutions Arch Cert", "Master Terraform/Ansible", "Build Hybrid Cloud Labs"],
        "core_challenges": "Optimizing cloud spend while maintaining maximum reliability and speed.",
        "tech_stack": ["Terraform", "AWS/Azure", "Kubernetes", "ELK Stack"],
        "work_life_balance": "High (Asynchronous Work)",
        "entry_difficulty": "High (System Complexity Req)",
        "top_employers": ["AWS", "Azure", "GCP", "Datadog"],
        "radar_dimensions": {
            "Engineering": 10,
            "Analytical": 7,
            "Creative": 4,
            "Strategy": 6,
            "Security": 8
        }
    },
    "Product Manager": {
        "description": "Lead the strategy, roadmap, and feature definition for products by bridging business and technology.",
        "why_it_matches": "Strong match for your leadership skills and ability to balance technical constraints with user needs.",
        "recommended_skills": ["Agile Methodology", "Market Analysis", "Roadmapping", "Stakeholder Management"],
        "potential_jobs": ["Technical PM", "Project Lead", "Strategy Consultant"],
        "salary_range": "$105k - $200k",
        "growth_outlook": "Strategic (20% Projected Growth)",
        "learning_roadmap": ["Master Product Strategy", "Lead Cross-functional Teams", "Analyze User Metrics"],
        "core_challenges": "Prioritizing competing features while managing stakeholder influence.",
        "tech_stack": ["Jira", "Productboard", "Mixpanel", "SQL"],
        "work_life_balance": "Moderate (Stakeholder Heavy)",
        "entry_difficulty": "High (Strategic Experience Req)",
        "top_employers": ["Uber", "Slack", "Revolut", "McKinsey"],
        "radar_dimensions": {
            "Engineering": 5,
            "Analytical": 7,
            "Creative": 6,
            "Strategy": 10,
            "Security": 4
        }
    },
    "Machine Learning Engineer": {
        "description": "Design and implement self-running AI software to automate predictive models and intelligent systems.",
        "why_it_matches": "Direct alignment with your advanced technical skills and interest in cutting-edge AI technologies.",
        "recommended_skills": ["PyTorch/TensorFlow", "Deep Learning", "Model Deployment", "Neural Networks"],
        "potential_jobs": ["AI Researcher", "NLP Specialist", "Computer Vision Engineer"],
        "salary_range": "$115k - $250k",
        "growth_outlook": "Extreme (40% Projected Growth)",
        "learning_roadmap": ["Deep Dive into Neural Nets", "Optimize Large Scale Models", "Publish AI Research"],
        "core_challenges": "Scientific uncertainty in model performance and high compute costs.",
        "tech_stack": ["PyTorch", "Hugging Face", "CUDA", "Ray"],
        "work_life_balance": "Balanced (Research Focused)",
        "entry_difficulty": "Very High (PHD / Research Req)",
        "top_employers": ["NVIDIA", "Anthropic", "Tesla", "Google AI"]
    },
    "Nursing": {
        "description": "Provide high-quality patient care, emotional support, and medical assistance in diverse healthcare settings.",
        "why_it_matches": "Matches your explicit interest in healthcare and your aptitude for empathy and scientific application.",
        "recommended_skills": ["Patient Care", "Medical Ethics", "Clinical Documentation", "Emergency Response"],
        "potential_jobs": ["Registered Nurse", "Clinical Specialist", "Nurse Practitioner"],
        "salary_range": "$75k - $140k",
        "growth_outlook": "Essential (15% Projected Growth)",
        "learning_roadmap": ["Nursing Degree / Licensure", "Specialize in Critical Care", "Attain Care MGMT Certs"],
        "core_challenges": "Emotional fatigue and physically demanding high-stress environments.",
        "tech_stack": ["Epic Systems", "Cerner", "PointClickCare", "Telemetry"],
        "work_life_balance": "Low (Shift Work / Emotional Intensity)",
        "entry_difficulty": "Medium (Licensure / Clinical Req)",
        "top_employers": ["Mayo Clinic", "NHS", "Kaiser Permanente", "Red Cross"]
    },
    "Healthcare Professional": {
        "description": "Manage and deliver healthcare services while ensuring patient safety and organizational efficiency.",
        "why_it_matches": "Perfect alignment with your stated interest in the medical field and healthcare administration.",
        "recommended_skills": ["Life Sciences", "Patient Advocacy", "Medical Informatics", "Healthcare Management"],
        "potential_jobs": ["Hospital Admin", "Public Health Officer", "Medical Researcher"],
        "salary_range": "$80k - $165k",
        "growth_outlook": "Stable (12% Projected Growth)",
        "learning_roadmap": ["MHA or MPH Degree", "Learn Medical Compliance", "Engage in Clinical Ops"],
        "core_challenges": "Navigating complex healthcare regulations and bureaucratic systems.",
        "tech_stack": ["EHR Systems", "MEDITECH", "Oracle Health", "Power BI"],
        "work_life_balance": "Moderate (Healthcare Admin Flow)",
        "entry_difficulty": "Medium (Certification / Multi-Domain Req)",
        "top_employers": ["UnitedHealth", "Pfizer", "WHO", "CVS Health"]
    },
    "Doctor": {
        "description": "Diagnose and treat illnesses, perform surgeries, and manage overall patient health.",
        "why_it_matches": "Aligns with your superior academic performance, scientific aptitude, and dedication to healing.",
        "recommended_skills": ["Diagnosis", "Surgery", "Anatomy", "Critical Decision Making"],
        "potential_jobs": ["General Practitioner", "Surgeon", "Specialist (Cardiology, etc.)"],
        "salary_range": "$180k - $500k+",
        "growth_outlook": "Stable (Essential Service)",
        "learning_roadmap": ["Med School", "Residency", "Fellowship", "Board Certification"],
        "core_challenges": "Extreme training duration and life-or-death responsibility.",
        "tech_stack": ["Diagnostic Imaging", "Robotic Surgery", "AI Diagnostics"],
        "work_life_balance": "Very Low (On-Call Life)",
        "entry_difficulty": "Extreme (Competitive / rigorous)",
        "top_employers": ["Johns Hopkins", "Mass General", "Local Hospitals", "Private Practice"]
    },
    "Pharmacist": {
        "description": "Dispense medications and provide expert advice on drug use and interactions.",
        "why_it_matches": "Combines your chemistry knowledge with patient interaction and attention to detail.",
        "recommended_skills": ["Pharmacology", "Chemistry", "Patient Counseling", "Regulatory Compliance"],
        "potential_jobs": ["Retail Pharmacist", "Clinical Pharmacist", "Research Pharmacist"],
        "salary_range": "$120k - $160k",
        "growth_outlook": "Moderate (Automation Risk)",
        "learning_roadmap": ["PharmD Degree", "Licensure Exam", "Residency (Clinical)"],
        "core_challenges": "Accuracy is critical; incorrect dosage can be fatal.",
        "tech_stack": ["Pharmacy Management Systems", "Automated Dispensing"],
        "work_life_balance": "Good (Retail hours)",
        "entry_difficulty": "High (PharmD Required)",
        "top_employers": ["CVS Health", "Walgreens", "Hospitals", "Pharma Companies"]
    },
    "Medical Researcher": {
        "description": "Conduct experiments to improve human health, developing new treatments and understanding diseases.",
        "why_it_matches": "Ideal for your analytical mind and deep interest in biological sciences.",
        "recommended_skills": ["Lab Techniques", "Data Analysis", "Scientific Writing", "Grant Writing"],
        "potential_jobs": ["Lab Manager", "Principal Investigator", "Biotech Scientist"],
        "salary_range": "$90k - $180k",
        "growth_outlook": "Strong (Biotech Boom)",
        "learning_roadmap": ["PhD in Life Sciences", "Postdoc Fellowship", "Publish Research"],
        "core_challenges": "Funding uncertainty and long timelines for discovery.",
        "tech_stack": ["CRISPR", "Bioinformatics Tools", "Python/R"],
        "work_life_balance": "Moderate (Academic Cycles)",
        "entry_difficulty": "High (PhD usually required)",
        "top_employers": ["Pfizer", "Moderna", "NIH", "University Labs"]
    },
    "Graphic Designer": {
        "description": "Create visual concepts to communicate ideas that inspire, inform, and captivate consumers.",
        "why_it_matches": "Transforms your artistic talent and creativity into professional visual communication.",
        "recommended_skills": ["Visual Theory", "Typography", "Branding", "Digital Illustration"],
        "potential_jobs": ["Brand Designer", "Art Director", "Web Designer"],
        "salary_range": "$55k - $110k",
        "growth_outlook": "Moderate (Digital Shift)",
        "learning_roadmap": ["Build Portfolio", "Master Design Tools", "Learn UX Basics"],
        "core_challenges": "Subjective client feedback and keeping up with design trends.",
        "tech_stack": ["Adobe Photoshop", "Illustrator", "Figma", "Procreate"],
        "work_life_balance": "Good (Freelance Friendly)",
        "entry_difficulty": "Medium (Portfolio is Key)",
        "top_employers": ["Pentagram", "Advertising Agencies", "Tech Companies", "Freelance"]
    },
    "Content Writer": {
        "description": "Produce engaging written content for websites, blogs, articles, and marketing materials.",
        "why_it_matches": "Leverages your strong writing skills and ability to research diverse topics.",
        "recommended_skills": ["Copywriting", "SEO", "Editing", "Storytelling"],
        "potential_jobs": ["Copywriter", "Technical Writer", "Blog Manager"],
        "salary_range": "$50k - $100k",
        "growth_outlook": "Stable (Digital Content Demand)",
        "learning_roadmap": ["Start a Blog", "Learn SEO", "Build Writing Portfolio"],
        "core_challenges": "Writer's block and the rise of AI-generated content.",
        "tech_stack": ["WordPress", "Google Docs", "SEO Tools (Ahrefs)", "CMS"],
        "work_life_balance": "High (Remote/Freelance)",
        "entry_difficulty": "Low (Quality Driven)",
        "top_employers": ["Media Houses", "Tech Blogs", "Marketing Agencies", "Freelance"]
    },
    "Digital Marketer": {
        "description": "Promote products and services through digital channels like social media, SEO, and email.",
        "why_it_matches": "Combines your creativity with analytical skills to drive business growth.",
        "recommended_skills": ["SEO/SEM", "Content Strategy", "Data Analytics", "Social Media Mgmt"],
        "potential_jobs": ["SEO Specialist", "Social Media Manager", "Growth Hacker"],
        "salary_range": "$60k - $130k",
        "growth_outlook": "High (Digital-First Economy)",
        "learning_roadmap": ["Google Ads Cert", "Analytics Mastery", "Run Campaigns"],
        "core_challenges": "Constant algorithm changes on major platforms.",
        "tech_stack": ["Google Analytics", "HubSpot", "Meta Ads Manager"],
        "work_life_balance": "Moderate (Always-on Internet)",
        "entry_difficulty": "Low (Results Driven)",
        "top_employers": ["Agencies", "E-commerce Brands", "Tech Startups"]
    },
    "Accountant": {
        "description": "Prepare and examine financial records, ensuring accuracy and compliance with laws.",
        "why_it_matches": "Fits your precision, ethical standards, and affinity for numbers.",
        "recommended_skills": ["Financial Reporting", "Tax Law", "Auditing", "Detail Oriented"],
        "potential_jobs": ["CPA", "Tax Consultant", "Forensic Accountant"],
        "salary_range": "$70k - $150k",
        "growth_outlook": "Stable (Regulation Driven)",
        "learning_roadmap": ["Accounting Degree", "CPA Exam", "Master Tax Software"],
        "core_challenges": "High stress during tax season and regulatory complexity.",
        "tech_stack": ["QuickBooks", "Excel (Advanced)", "ERP Systems"],
        "work_life_balance": "Variable (Tax Season Crunch)",
        "entry_difficulty": "Medium (Certification Req)",
        "top_employers": ["Big 4 (Deloitte, PwC...)", "Corporate Finance", "Government"]
    },
    "Financial Analyst": {
        "description": "Guide businesses and individuals in making investment decisions by assessing performance.",
        "why_it_matches": "Utilizes your analytical modeling skills to forecast economic trends.",
        "recommended_skills": ["Financial Modeling", "Data Analysis", "Market Research", "Valuation"],
        "potential_jobs": ["Investment Banker", "Risk Analyst", "Portfolio Manager"],
        "salary_range": "$85k - $180k",
        "growth_outlook": "Moderate",
        "learning_roadmap": ["CFA Charter", "Financial Modeling Courses", "Networking"],
        "core_challenges": "High pressure environment and market volatility.",
        "tech_stack": ["Bloomberg Terminal", "Excel", "Python", "Tableau"],
        "work_life_balance": "Low (High Burnout Risk)",
        "entry_difficulty": "High (Competitive)",
        "top_employers": ["Goldman Sachs", "JP Morgan", "Hedge Funds", "Corporations"]
    },
    "HR Manager": {
        "description": "Oversee the administrative and organizational functions of an organization, focusing on people.",
        "why_it_matches": "Perfect for your leadership, empathy, and organizational skills.",
        "recommended_skills": ["Employee Relations", "Recruiting", "Labor Law", "Conflict Resolution"],
        "potential_jobs": ["Talent Acquisition", "People Ops Lead", "Benefits Manager"],
        "salary_range": "$70k - $140k",
        "growth_outlook": "Stable",
        "learning_roadmap": ["SHRM Certification", "Psychology Basics", "Management Experience"],
        "core_challenges": "Balancing employee needs with company policy/profit.",
        "tech_stack": ["Workday", "Greenhouse", "BambooHR"],
        "work_life_balance": "Good (Corporate Hours)",
        "entry_difficulty": "Medium",
        "top_employers": ["All Large Corporations", "Tech Companies", "Startups"]
    },
    "Game Developer": {
        "description": "Design and build interactive digital experiences, focusing on game mechanics, graphics, and performance.",
        "why_it_matches": "Direct match for your technical gaming skills and creative interest in interactive media.",
        "recommended_skills": ["Unity/Unreal Engine", "C++/C#", "3D Modeling", "Game Physics"],
        "potential_jobs": ["Game Programmer", "Level Designer", "Technical Artist"],
        "salary_range": "$70k - $155k",
        "growth_outlook": "Dynamic (14% Projected Growth)",
        "learning_roadmap": ["Master Unity/Unreal", "Build Indie Game Prototypes", "Join Global Game Jams"],
        "core_challenges": "High-pressure release cycles and complex rendering optimization.",
        "tech_stack": ["Unreal Engine", "C# / C++", "Blender", "Maya"],
        "work_life_balance": "Moderate (Crunch Cycles Common)",
        "entry_difficulty": "High (Technical + Creative Depth)",
        "top_employers": ["Rockstar Games", "Ubisoft", "EA", "Epic Games"]
    },
    "Content Creator": {
        "description": "Produce and distribute engaging digital content across platforms, building personal brands and communities.",
        "why_it_matches": "Matches your aptitude for streaming, community engagement, and digital storytelling.",
        "recommended_skills": ["Video Editing", "Live Streaming", "Social Media Strategy", "Audience Analytics"],
        "potential_jobs": ["Professional Streamer", "Platform Influencer", "Digital Media Manager"],
        "salary_range": "$40k - $500k+",
        "growth_outlook": "Volatile (Projected High Expansion)",
        "learning_roadmap": ["Build Community Presence", "Master Video Production", "Diversify Revenue Streams"],
        "core_challenges": "Platform algorithm unpredictability and high burnout risk.",
        "tech_stack": ["OBS Studio", "Premiere Pro", "YouTube Studio", "StreamElements"],
        "work_life_balance": "Low (Always-on Digital Demand)",
        "entry_difficulty": "Medium (Consistency / Brand Driven)",
        "top_employers": ["Twitch", "YouTube", "TikTok", "Freelance"]
    },
    "Investment Analyst": {
        "description": "Evaluate financial data and market trends to provide investment recommendations and strategic financial advice.",
        "why_it_matches": "Perfect for your interest in finance, market dynamics, and analytical decision-making.",
        "recommended_skills": ["Financial Modeling", "Market Analysis", "Risk Assessment", "Quantitative Research"],
        "potential_jobs": ["Portfolio Manager", "Equity Analyst", "Financial Consultant"],
        "salary_range": "$95k - $195k",
        "growth_outlook": "Competitive (10% Projected Growth)",
        "learning_roadmap": ["Pass CFA Exams", "Master Advanced Financial Modeling", "Join Boutique Equity Firms"],
        "core_challenges": "High-stakes decision making and extreme work hours in high-pressure markets.",
        "tech_stack": ["Bloomberg Terminal", "Excel Macros", "Python (Pandas)", "R"],
        "work_life_balance": "Low (Market Intensity / Long Hours)",
        "entry_difficulty": "Very High (CFA / Quantitative Req)",
        "top_employers": ["Goldman Sachs", "BlackRock", "J.P. Morgan", "Citadel"]
    },
    "Digital Marketer": {
        "description": "Design and execute online marketing campaigns to drive brand awareness, traffic, and revenue.",
        "why_it_matches": "Aligns with your interest in digital platforms, consumer behavior, and data-driven growth.",
        "recommended_skills": ["SEO/SEM", "Content Strategy", "Email Marketing", "PPC Advertising"],
        "potential_jobs": ["Growth Hacker", "Social Media Manager", "SEO Specialist"],
        "salary_range": "$65k - $145k",
        "growth_outlook": "Vibrant (16% Projected Growth)",
        "learning_roadmap": ["Master Ad Platforms", "Learn Behavioral Analytics", "Build Personal Brand Cases"],
        "core_challenges": "Attribution modeling and staying ahead of privacy-centric ad changes.",
        "tech_stack": ["Google Ads", "Meta Business Suite", "HubSpot", "Semrush"],
        "work_life_balance": "Balanced (Performance Driven)",
        "entry_difficulty": "Medium (Analytics / Results Driven)",
        "top_employers": ["Google", "WPP", "Publicis", "Shopify"]
    },
    "Environmental Scientist": {
        "description": "Study environmental problems and develop solutions to protect the environment and human health.",
        "why_it_matches": "Matches your passion for sustainability and scientific inquiry into environmental systems.",
        "recommended_skills": ["Environmental Impact Assessment", "Data Collection", "Sustainability Planning", "Ecology"],
        "potential_jobs": ["Sustainability Consultant", "Environmental Inspector", "Ecologist"],
        "salary_range": "$70k - $130k",
        "growth_outlook": "Green (11% Projected Growth)",
        "learning_roadmap": ["Environmental Science Degree", "Specialize in Renewables", "Conduct Field Research"],
        "core_challenges": "Balancing environmental goals with economic and political realities.",
        "tech_stack": ["GIS Software", "MODHMS", "Python", "Remote Sensing Tools"],
        "work_life_balance": "Balanced (Field + Office Mix)",
        "entry_difficulty": "Medium (Environmental Degree Req)",
        "top_employers": ["EPA", "AECOM", "Greenpeace", "Tesla Energy"]
    },
    "Research Psychologist": {
        "description": "Conduct scientific studies on human behavior and mental processes to expand psychological knowledge.",
        "why_it_matches": "Strong alignment with your interest in human behavior, empathy, and scientific research.",
        "recommended_skills": ["Experimental Design", "Data Analysis", "Psychological Theory", "Scientific Writing"],
        "potential_jobs": ["Clinical Researcher", "Academic Professor", "Behavioral Scientist"],
        "salary_range": "$85k - $155k",
        "growth_outlook": "Academic (8% Projected Growth)",
        "learning_roadmap": ["Doctoral Studies", "Publish Peer-Review Papers", "Attain Clinical Research Grants"],
        "core_challenges": "Funding instability and long-term replication study complexity.",
        "tech_stack": ["SPSS", "Qualtrics", "NVivo", "MATLAB"],
        "work_life_balance": "High (Academic / Tenure Track)",
        "entry_difficulty": "Very High (PhD + Research Record)",
        "top_employers": ["Harvard Health", "RAND Corp", "APA", "Public Health Inst"]
    },
    "Digital Artist": {
        "description": "Create visual art using digital technology for media, entertainment, and commercial purposes.",
        "why_it_matches": "Direct match for your creative talent and proficiency with digital design tools.",
        "recommended_skills": ["Digital Illustration", "Character Design", "Concept Art", "Texturing"],
        "potential_jobs": ["Concept Artist", "Illustrator", "Texture Artist"],
        "salary_range": "$60k - $135k",
        "growth_outlook": "Creative (13% Projected Growth)",
        "learning_roadmap": ["Master Visual Theory", "Build Unique Style Portfolio", "Network with Media Studios"],
        "core_challenges": "Creative blocks and intense competition in the digital marketplace.",
        "tech_stack": ["Photoshop", "Procreate", "ZBrush", "Painter"],
        "work_life_balance": "Balanced (Freelance Independence)",
        "entry_difficulty": "Medium (Skill / Portfolio Driven)",
        "top_employers": ["Disney", "Marvel", "Ubisoft", "Freelance"]
    },
    "Technical Writer": {
        "description": "Create clear and concise documentation for complex technical information and products.",
        "why_it_matches": "Matches your ability to simplify complex topics and your attention to detail in communication.",
        "recommended_skills": ["Technical Documentation", "Product Research", "Editing", "Information Architecture"],
        "potential_jobs": ["API Documentarian", "Instructional Designer", "Content Strategist"],
        "salary_range": "$75k - $140k",
        "growth_outlook": "Reliable (12% Projected Growth)",
        "learning_roadmap": ["Learn Markdown / Docs-as-Code", "Master SaaS Product Research", "Build API Doc Samples"],
        "core_challenges": "Translating highly opaque technical concepts for end-user clarity.",
        "tech_stack": ["GitHub", "Confluence", "Swagger/OpenAPI", "DITA"],
        "work_life_balance": "High (Strict Corporate Hours)",
        "entry_difficulty": "Medium (Writing Skill / Tech Context)",
        "top_employers": ["Microsoft", "IBM", "Oracle", "SaaS Startups"]
    },
    "Management Consultant": {
        "description": "Help organizations improve their performance by analyzing existing problems and developing improvement plans.",
        "why_it_matches": "Excellent match for your leadership skills and structured problem-solving approach.",
        "recommended_skills": ["Business Analysis", "Strategic Planning", "Project Management", "Change Management"],
        "potential_jobs": ["Operations Consultant", "Strategy Analyst", "Organizational Dev Specialist"],
        "salary_range": "$110k - $220k",
        "growth_outlook": "Elite (14% Projected Growth)",
        "learning_roadmap": ["Master Case Interview Skills", "Earn MBA / Global Credentials", "Join Big 4 Consulting Firms"],
        "core_challenges": "Frequent travel and high-intensity presentation cycles.",
        "tech_stack": ["PowerPoint", "Excel Modeling", "Tableau", "Slack"],
        "work_life_balance": "Low (Intense Travel / High-Stakes Delivery)",
        "entry_difficulty": "Very High (Elite MBA / Case Study Req)",
        "top_employers": ["McKinsey", "BCG", "Bain", "Deloitte"]
    },
    "Pharmacist": {
        "description": "Clinical medication expert ensuring safe drug administration and high-quality retail pharmacy management.",
        "why_it_matches": "Strategic match for your interest in pharmaceuticals, medical retail, and clinical chemistry.",
        "recommended_skills": ["Pharma Law", "Clinical Dispensing", "Inventory MGMT", "Patient Counseling"],
        "potential_jobs": ["Clinical Pharmacist", "Pharmacy Owner", "Drug Inspector"],
        "salary_range": "$90k - $160k",
        "growth_outlook": "High (Retail & Clinical)",
        "learning_roadmap": ["Pharm.D Degree", "State Licensure", "Board Certification"],
        "core_challenges": "High regulatory burden and precision-critical environments.",
        "tech_stack": ["PioneerRx", "Micro Merchant", "EPIC Pharmacy", "SQL"],
        "work_life_balance": "Balanced (Clinical Shift Regularity)",
        "entry_difficulty": "High (Pharm.D + Board Req)",
        "top_employers": ["CVS", "Walgreens", "Hospital Chains"]
    },
    "Pharmaceutical Researcher": {
        "description": "Lead laboratory-based drug discovery and biotech innovation at a global scale.",
        "why_it_matches": "Perfect alignment with your passion for drug development and scientific inquiry.",
        "recommended_skills": ["Molecular Biology", "Bioinformatics", "GLP/GMP", "Data Analysis"],
        "potential_jobs": ["R&D Scientist", "Formulation Expert", "Clinical Trials Lead"],
        "salary_range": "$110k - $220k",
        "growth_outlook": "Explosive (Biotech Sector)",
        "learning_roadmap": ["Advanced Ph.D", "Master Laboratory Tech", "Lead Drug Trials"],
        "core_challenges": "Long R&D cycles and high experimental volatility.",
        "tech_stack": ["ChemDraw", "BioRender", "Python (NumPy)", "GraphPad Prism"],
        "work_life_balance": "Balanced (Lab Operations Standard)",
        "entry_difficulty": "High (Masters/PhD + Lab Technique)",
        "top_employers": ["Moderna", "Sanofi", "AstraZeneca", "Biogen"]
    },
    "Professional Astrologer": {
        "description": "Expert in metaphysical cycles and natal chart interpretation, providing strategic life guidance through celestial alignments.",
        "why_it_matches": "Unique alignment with your interest in metaphysical patterns, counseling, and astronomical cycles.",
        "recommended_skills": ["Natal Interpretation", "Predictive Astrology", "Counseling Ethics", "Astronomical Math"],
        "potential_jobs": ["Consultant Astrologer", "Metaphysical Writer", "Astro-Data Analyst"],
        "salary_range": "$50k - $150k+",
        "growth_outlook": "Rising (Metaphysical Market)",
        "learning_roadmap": ["Master Hellenistic/Vedic Basics", "Professional Certification (ISAR/NCGR)", "Build Global Consulting Brand"],
        "core_challenges": "Highly subjective interpretations and navigating skeptical market perceptions.",
        "tech_stack": ["Solar Fire", "AstroGold", "Ephemeris Data", "WordPress"],
        "work_life_balance": "Very High (Self-Structured)",
        "entry_difficulty": "Medium (Interpretation Depth Req)",
        "top_employers": ["Self-Employed", "AstroStyle", "Mediums.com"]
    },
    "Defense & Strategic Operations": {
        "description": "Lead high-stakes operations in national security, intelligence, and tactical command within the defense sector.",
        "why_it_matches": "Strong alignment with your leadership aptitude, strategic thinking, and sense of public service.",
        "recommended_skills": ["Tactical Leadership", "Strategic Planning", "Crisis Management", "Intelligence Analysis"],
        "potential_jobs": ["Commissioned Officer", "Intelligence Analyst", "Strategic Operations Lead"],
        "salary_range": "$65k - $165k+",
        "growth_outlook": "Stable (Defense Sector)",
        "learning_roadmap": ["Complete Officer Training", "Master Strategic Defense Ops", "Attain Advanced Security Clearance"],
        "core_challenges": "High-risk environments and prolonged periods of high-intensity operational demand.",
        "tech_stack": ["Command & Control Systems", "GIS", "Secure Communications", "Strategic Modeling"],
        "work_life_balance": "Low (Operational Readiness Intensity)",
        "entry_difficulty": "High (Commission / Tactical Fitness Req)",
        "top_employers": ["Department of Defense", "NATO", "Security Firms"]
    },
    "Professional Sports & Athletics": {
        "description": "Excellence in peak physical performance, coaching, and strategic sports management at a professional level.",
        "why_it_matches": "Perfect match for your dedication to physical excellence, competitive spirit, and athletic strategy.",
        "recommended_skills": ["Performance Training", "Sports Strategy", "Biometrics Analysis", "Physical Resilience"],
        "potential_jobs": ["Professional Athlete", "Performance Coach", "Sports Operations Manager"],
        "salary_range": "$50k - $2M+",
        "growth_outlook": "Vibrant (Global Sports Economy)",
        "learning_roadmap": ["Master Specialized Athletic Skills", "Acquire Performance Certs", "Join Professional Leagues"],
        "core_challenges": "Physical injury risks and highly compressed professional shelf-lives.",
        "tech_stack": ["Whoop/Biometrics", "Video Analysis Platforms", "Performance Analytics", "Nutrition Tracking"],
        "work_life_balance": "Moderate (Training Cycles / Peak Performance)",
        "entry_difficulty": "High (Exceptional Performance / Analytics)",
        "top_employers": ["NBA/NFL/IPL", "Global Academy", "Nike Performance"]
    },
    "Agriculturist": {
        "description": "Expert in farming, crop management, and sustainable agriculture practices.",
        "why_it_matches": "Aligns with your interest in nature, sustainability, and biological systems.",
        "recommended_skills": ["Farming Techniques", "Soil Science", "Crop Management", "Agro-efficiency"],
        "potential_jobs": ["Farm Manager", "Agricultural Consultant", "Agronomist"],
        "salary_range": "$50k - $120k",
        "growth_outlook": "Stable (Essential)",
        "learning_roadmap": ["Degree in Agriculture", "Field Experience", "Sustainable Certs"],
        "core_challenges": "Climate change impact and resource management.",
        "tech_stack": ["Precision Ag Tools", "Drones", "Soil Sensors"],
        "work_life_balance": "Variable (Seasonal)",
        "entry_difficulty": "Medium",
        "top_employers": ["Cargill", "Corteva", "Government Depts", "Farms"]
    },
    "Botanist": {
        "description": "Scientific study of plants, including their physiology, structure, genetics, and ecology.",
        "why_it_matches": "Perfect for your scientific curiosity about the natural world and plant life.",
        "recommended_skills": ["Botany", "Plant Biology", "Data Collection", "Research"],
        "potential_jobs": ["Plant Scientist", "Conservationist", "Researcher"],
        "salary_range": "$60k - $110k",
        "growth_outlook": "Moderate",
        "learning_roadmap": ["Degree in Botany/Bio", "Field Research", "PhD for High Level"],
        "core_challenges": "Funding for conservation and habitat loss.",
        "tech_stack": ["Microscopes", "GIS", "Data Analysis Software"],
        "work_life_balance": "Good (Academic/Research)",
        "entry_difficulty": "High (Academic Req)",
        "top_employers": ["Botanical Gardens", "Universities", "Environmental Agencies"]
    },
    "Landscape Architect": {
        "description": "Plan and design outdoor spaces, parks, and gardens for beauty and functionality.",
        "why_it_matches": "Combines your creativity with your love for nature and engineering structure.",
        "recommended_skills": ["Landscape Design", "CAD", "Horticulture", "Visual Art"],
        "potential_jobs": ["Landscape Designer", "Urban Planner", "Park Ranger"],
        "salary_range": "$60k - $110k",
        "growth_outlook": "Good",
        "learning_roadmap": ["Landscape Arch Degree", "Portfolio Building", "Licensure"],
        "core_challenges": "Balancing aesthetics with environmental constraints.",
        "tech_stack": ["AutoCAD", "SketchUp", "Adobe Suite"],
        "work_life_balance": "Good",
        "entry_difficulty": "Medium",
        "top_employers": ["Architecture Firms", "City Planning Depts", "Private Clients"]
    },
    "Army Officer": {
        "description": "Lead soldiers and manage operations to defend national interests.",
        "why_it_matches": "Matches your leadership, discipline, and desire to serve in the defense sector.",
        "recommended_skills": ["Leadership", "Strategic Planning", "Combat Tactics", "Physical Training"],
        "potential_jobs": ["Platoon Leader", "Logistics Officer", "Intelligence Officer"],
        "salary_range": "$70k - $150k + Benefits",
        "growth_outlook": "Stable",
        "learning_roadmap": ["Academy/ROTC/OCS", "Basic Officer Course", "Specialty Training"],
        "core_challenges": "High risk, separation from family, strict hierarchy.",
        "tech_stack": ["Comms Equipment", "Weapon Systems", "Tactical Software"],
        "work_life_balance": "Low (Deployment Cycles)",
        "entry_difficulty": "High (Physical/Mental/Leadership)",
        "top_employers": ["Army", "Defense Dept"]
    },
    "Air Force Pilot": {
        "description": "Fly aircraft for combat, transport, or reconnaissance missions, serving as a tactical leader in the sky.",
        "why_it_matches": "Ideal for your steady nerves, technical aptitude, and explicit love of flight and aviation.",
        "recommended_skills": ["Piloting", "Aeronautical Navigation", "Flight Physics", "High-G Combat Tactics"],
        "potential_jobs": ["Fighter Pilot", "Transport Pilot", "Drone Systems Operator"],
        "salary_range": "$90k - $210k",
        "growth_outlook": "Competitive (Strategic Asset)",
        "learning_roadmap": ["Flight School", "Officer Training", "Specialized Aircraft Qualification"],
        "core_challenges": "Extreme physical standards and high-stakes operational environments.",
        "tech_stack": ["Avionics Systems", "Flight Simulators", "Navigation Guidance"],
        "work_life_balance": "Low (Deployments / Operational Readiness)",
        "entry_difficulty": "Very High (Competitive Selection)",
        "top_employers": ["Air Force", "Navy", "Defense Contractors"]
    },
    "Aerospace Engineer": {
        "description": "Design, develop, and test aircraft, spacecraft, satellites, and missiles for revolutionary exploration and defense.",
        "why_it_matches": "Direct alignment with your interest in aeronautics, space exploration, and complex system engineering.",
        "recommended_skills": ["Aerodynamics", "Propulsion Systems", "Structural Analysis", "Orbital Mechanics"],
        "potential_jobs": ["Rocket Scientist", "Satellite Designer", "NASA Flight Engineer"],
        "salary_range": "$105k - $220k",
        "growth_outlook": "Explosive (Private Space Sector Boom)",
        "learning_roadmap": ["Master Fluid Dynamics", "Learn Propulsion Engineering", "Acquire CAD & CFD Proficiency"],
        "core_challenges": "Balancing weight, fuel, and safety in extreme environments.",
        "tech_stack": ["ANSYS", "MATLAB", "CATIA", "OpenFOAM"],
        "work_life_balance": "Moderate (Project-Based Intensity)",
        "entry_difficulty": "High (Technical Depth Req)",
        "top_employers": ["NASA", "SpaceX", "Boeing", "Lockheed Martin"],
        "radar_dimensions": {
            "Engineering": 10,
            "Analytical": 9,
            "Creative": 5,
            "Strategy": 6,
            "Security": 7
        }
    },
    "Astronomer": {
        "description": "Study the universe, its celestial bodies, and the laws of physics that govern space-time.",
        "why_it_matches": "Direct resonance with your fascination for astronomy, celestial mechanics, and deep space exploration.",
        "recommended_skills": ["Observational Astronomy", "Astrophysics", "Cosmology", "Telescope Operation"],
        "potential_jobs": ["Astrophysicist", "Cosmologist", "NASA Research Scientist"],
        "salary_range": "$80k - $175k",
        "growth_outlook": "High (James Webb / New Space Age)",
        "learning_roadmap": ["PhD in Astrophysics", "Master Data Analysis", "Conduct Deep Space Observations"],
        "core_challenges": "Highly competitive research funding and long-term observational projects.",
        "tech_stack": ["Python", "Astropy", "SQL", "DS9/Image Processing"],
        "work_life_balance": "Moderate (Research Cycles)",
        "entry_difficulty": "Very High (PhD Required)",
        "top_employers": ["NASA", "ESA", "ESO", "Global Observatories"],
        "radar_dimensions": {
            "Engineering": 6,
            "Analytical": 10,
            "Creative": 7,
            "Strategy": 5,
            "Security": 4
        }
    },
    "Intelligence Analyst": {
        "description": "Gather and analyze information to protect security and support military operations.",
        "why_it_matches": "Fits your critical thinking, pattern recognition, and puzzle-solving skills.",
        "recommended_skills": ["Data Analysis", "Critical Thinking", "Writing", "Security Clearance"],
        "potential_jobs": ["Intel Analyst", "Counter-Intel", "Cyber Intel"],
        "salary_range": "$75k - $140k",
        "growth_outlook": "Strong",
        "learning_roadmap": ["Degree in Int'l Relations/CS", "Security Clearance", "Agency Training"],
        "core_challenges": "Secrecy burden and sifting through vast noise for signals.",
        "tech_stack": ["Palantir", "Databases", "Encryption Tools"],
        "work_life_balance": "Moderate",
        "entry_difficulty": "High (Clearance Req)",
        "top_employers": ["CIA", "NSA", "Defense Contractors"]
    },
    "Lawyer": {
        "description": "Advise and represent clients in legal matters, draft documents, and litigate in court.",
        "why_it_matches": "Aligns with your strong logic, debate skills, and interest in justice.",
        "recommended_skills": ["Legal Research", "Public Speaking", "Writing", "Negotiation"],
        "potential_jobs": ["Litigator", "Corporate Counsel", "Public Defender"],
        "salary_range": "$100k - $300k+",
        "growth_outlook": "Stable",
        "learning_roadmap": ["Law School (JD)", "Bar Exam", "Clerkship"],
        "core_challenges": "Burnout, high stress, and long hours.",
        "tech_stack": ["Westlaw", "LexisNexis", "Case Management"],
        "work_life_balance": "Low (Big Law) to Good (Govt)",
        "entry_difficulty": "High (Law School/Bar)",
        "top_employers": ["Law Firms", "Corporations", "Government"]
    },
    "Policy Analyst": {
        "description": "Research and analyze policies to guide government or org decisions.",
        "why_it_matches": "Fits your analytical mind and interest in societal impact.",
        "recommended_skills": ["Research", "Writing", "Data Stats", "Political Science"],
        "potential_jobs": ["Think Tank Researcher", "Legislative Aide", "Lobbyist"],
        "salary_range": "$60k - $120k",
        "growth_outlook": "Stable",
        "learning_roadmap": ["MPP/MPA Degree", "Internships", "Publishing Briefs"],
        "core_challenges": "Political gridlock and slow pace of change.",
        "tech_stack": ["Statistical Software (STATA)", "Excel"],
        "work_life_balance": "Good",
        "entry_difficulty": "Medium",
        "top_employers": ["Think Tanks", "Government", "Non-Profits"]
    },
    "Civil Engineer": {
        "description": "Design, build, and supervise infrastructure projects like roads, bridges, and dams.",
        "why_it_matches": "Matches your interest in building, physics, and large-scale problem solving.",
        "recommended_skills": ["Structural Eng", "CAD", "Project Management", "Math"],
        "potential_jobs": ["Structural Engineer", "Transportation Eng", "Site Manager"],
        "salary_range": "$70k - $130k",
        "growth_outlook": "Steady",
        "learning_roadmap": ["BS Engineering", "FE Exam", "PE License"],
        "core_challenges": "Public safety responsibility and budget constraints.",
        "tech_stack": ["AutoCAD", "Revit", "Civil 3D"],
        "work_life_balance": "Good",
        "entry_difficulty": "Medium (Degree Req)",
        "top_employers": ["Engineering Firms", "Govt DOT", "Construction"]
    },
    "Mechanical Engineer": {
        "description": "Design, analyze, and manufacture mechanical systems and machines.",
        "why_it_matches": "Ideal for your understanding of mechanics, thermodynamics, and design.",
        "recommended_skills": ["CAD", "Thermodynamics", "Materials Science", "Problem Solving"],
        "potential_jobs": ["Product Design Eng", "HVAC Engineer", "Robotics Eng"],
        "salary_range": "$75k - $140k",
        "growth_outlook": "Steady",
        "learning_roadmap": ["BS ME", "Internships", "Specialization (Robotics/Auto)"],
        "core_challenges": "Complex troubleshooting and prototype failures.",
        "tech_stack": ["SolidWorks", "MATLAB", "ANSYS"],
        "work_life_balance": "Good",
        "entry_difficulty": "Medium (Degree Req)",
        "top_employers": ["Automotive", "Aerospace", "Consumer Electronics"]
    },
    "Biologist": {
        "description": "Study living organisms to understand potential applications in medicine, environment, and more.",
        "why_it_matches": "Aligns with your deep interest in life sciences and research.",
        "recommended_skills": ["Lab Research", "Data Analysis", "Microbiology", "Genetics"],
        "potential_jobs": ["Research Scientist", "Wildlife Biologist", "Lab Tech"],
        "salary_range": "$50k - $110k",
        "growth_outlook": "ModernBio",
        "learning_roadmap": ["BS Biology", "Lab Experience", "Masters/PhD"],
        "core_challenges": "Grant funding and tedious lab work.",
        "tech_stack": ["Microscopes", "PCR", "Data Tools"],
        "work_life_balance": "Good",
        "entry_difficulty": "Medium",
        "top_employers": ["Labs", "Universities", "Biotech"]
    },
    "Chemist": {
        "description": "Study properties of matter at the level of atoms and molecules.",
        "why_it_matches": "Matches your analytical nature and interest in material sciences.",
        "recommended_skills": ["Organic Chem", "Lab Safety", "Analytical Chem", "Spectroscopy"],
        "potential_jobs": ["Analytical Chemist", "Materials Scientist", "Forensic Chemist"],
        "salary_range": "$60k - $120k",
        "growth_outlook": "Stable",
        "learning_roadmap": ["BS Chemistry", "Lab Skills", "Specialization"],
        "core_challenges": "Safety hazards and ensuring purity/accuracy.",
        "tech_stack": ["Chromatography", "Spectrometers", "LIMS"],
        "work_life_balance": "Good",
        "entry_difficulty": "Medium",
        "top_employers": ["Pharma", "Manufacturing", "Labs"]
    },
    "Professional Athlete": {
        "description": "Achieve the pinnacle of human physical potential. Embody discipline and push boundaries on the global stage.",
        "why_it_matches": "Direct alignment with your athletic drive, competitive spirit, and peak physical commitment.",
        "recommended_skills": ["Physical Endurance", "Strategic Playmaking", "Mental Fortitude", "Team Collaboration"],
        "potential_jobs": ["Professional Player", "Athletic Consultant", "Sports Influencer"],
        "salary_range": "$60k - $50M+ (Performance Based)",
        "growth_outlook": "Highly Competitive / High Reward",
        "learning_roadmap": ["Elite Training Camp", "Join Athletic Academies", "Compete at Professional Levels"],
        "core_challenges": "Highly compressed professional career window and injury risks.",
        "tech_stack": ["Biometric Trackers", "Video Analysis", "Nutrition AI"],
        "work_life_balance": "Moderate (Training Driven)",
        "entry_difficulty": "Elite (Physical Performance Priority)",
        "top_employers": ["Professional Leagues", "Sports Management Firms", "Global Athletic Brands"]
    },
    "Sports Coach": {
        "description": "Lead athletes and teams to success through strategy, training, and mentorship.",
        "why_it_matches": "Combines your love for sports with leadership and teaching abilities.",
        "recommended_skills": ["Leadership", "Strategy", "Mentoring", "Sports Psychology"],
        "potential_jobs": ["Head Coach", "Assistant Coach", "Personal Trainer"],
        "salary_range": "$40k - $5M+",
        "growth_outlook": "Good",
        "learning_roadmap": ["Play Experience", "Assistant Roles", "Certifications"],
        "core_challenges": "Job security depends on winning.",
        "tech_stack": ["Video Analysis", "Playbook Software"],
        "work_life_balance": "Low (In-season)",
        "entry_difficulty": "High (For Pro/College)",
        "top_employers": ["Teams", "Schools", "Universities"]
    },
    "Executive Chef": {
        "description": "Lead a professional kitchen, creating culinary masterpieces and defining a restaurant's gastronomic identity.",
        "why_it_matches": "Matches your creative passion, ability to work under pressure, and sensory leadership.",
        "recommended_skills": ["Culinary Arts", "Menu Design", "Kitchen Management", "Food Safety"],
        "potential_jobs": ["Head Chef", "Sous Chef", "Restaurateur"],
        "salary_range": "$60k - $150k+",
        "growth_outlook": "Steady (High Demand for Quality)",
        "learning_roadmap": ["Culinary School", "Apprenticeship", "Station Chef", "Sous Chef"],
        "core_challenges": "Physically demanding, long hours, and high-pressure service windows.",
        "tech_stack": ["Inventory Systems", "Sous Vide", "Kitchen Display Systems"],
        "work_life_balance": "Low (Nights/Weekends)",
        "entry_difficulty": "Medium (Experience Driven)",
        "top_employers": ["Michelin Restaurants", "Hotels", "Private Dining", "Cruise Lines"]
    },
    "Fashion Designer": {
        "description": "Create original clothing, accessories, and footwear, sketching designs and selecting fabrics and patterns.",
        "why_it_matches": "Direct alignment with your artistic vision, trend awareness, and eye for aesthetics.",
        "recommended_skills": ["Sketching", "Sewing/Draping", "Textile Knowledge", "Trend Analysis"],
        "potential_jobs": ["Apparel Designer", "Creative Director", "Textile Designer"],
        "salary_range": "$55k - $150k+",
        "growth_outlook": "Competitve (Brand Driven)",
        "learning_roadmap": ["Design School", "Internships", "Launch Collection", "Portfolio"],
        "core_challenges": "Extremely fast trend cycles and subjective market success.",
        "tech_stack": ["Adobe Illustrator", "CLO 3D", "CAD for Fashion"],
        "work_life_balance": "Variable (Fashion Week Crunch)",
        "entry_difficulty": "High (Portfolio / Network)",
        "top_employers": ["LVMH", "Nike", "Ralph Lauren", "Indie Labels"]
    },
    "Event Planner": {
        "description": " Coordinate all aspects of professional meetings and events, ensuring smooth execution and memorable experiences.",
        "why_it_matches": "Fits your organizational skills, attention to detail, and ability to manage complex logistics.",
        "recommended_skills": ["Logistics", "Vendor Management", "Budgeting", "Crisis Mgmt"],
        "potential_jobs": ["Wedding Planner", "Corporate Event Manager", "Festival Director"],
        "salary_range": "$50k - $120k",
        "growth_outlook": "Strong (Experience Economy)",
        "learning_roadmap": ["Hospitality Degree", "Certified Meeting Professional (CMP)", "Portfolio"],
        "core_challenges": "High stress during events and managing demanding clients.",
        "tech_stack": ["Cvent", "Social Tables", "Project Mgmt Tools"],
        "work_life_balance": "Variable (Weekend Work)",
        "entry_difficulty": "Medium",
        "top_employers": ["Event Agencies", "Hotels", "Corporations", "Self-Employed"]
    },
    "Arts & Creative Professional": {
        "description": "Master of visual expression, fine arts, and creative direction, blending classical techniques with modern aesthetic theory.",
        "why_it_matches": "Direct alignment with your deep passion for arts, creative expression, and visual storytelling.",
        "recommended_skills": ["Fine Arts", "Aesthetic Theory", "Creative Direction", "Visual Communication"],
        "potential_jobs": ["Art Director", "Fine Artist", "Gallerist", "Creative Lead"],
        "salary_range": "$65k - $180k+",
        "growth_outlook": "Vibrant (Creative Economy Expansion)",
        "learning_roadmap": ["BFA/MFA Degree", "Exhibition Portfolio", "Master Specialized Media"],
        "core_challenges": "Subjective value perception and maintaining consistent creative output.",
        "tech_stack": ["Multi-media", "Curatorial Tools", "Digital Suite", "Exhibition Software"],
        "work_life_balance": "High (Creative Autonomy)",
        "entry_difficulty": "Medium (Vision & Portfolio Driven)",
        "top_employers": ["Modern Art Museums", "Creative Agencies", "Fine Art Galleries", "Self-Employed Artist"]
    },
    "Renewable Energy Engineer": {
        "description": "Design and optimize sustainable energy systems, focusing on solar, wind, and hydro-electric innovations.",
        "why_it_matches": "Matches your commitment to sustainability and engineering excellence.",
        "recommended_skills": ["Solar PV Design", "Energy Modeling", "Sustainable Materials", "Power Grid Analytics"],
        "potential_jobs": ["Solar Architect", "Wind Farm Optimizer", "Energy Storage Specialist"],
        "salary_range": "$95k - $175k",
        "growth_outlook": "Explosive (Net Zero Global Transition)",
        "learning_roadmap": ["Degree in Renewable Systems", "Master Energy Storage Tech", "Lead Green Infrastructure"],
        "core_challenges": "Intermittency of energy sources and complex grid integration.",
        "tech_stack": ["HOMER Pro", "PVSyst", "Python", "CAD"],
        "work_life_balance": "Balanced (Environmentally Driven)",
        "entry_difficulty": "High (Technical Specialization Req)",
        "top_employers": ["Tesla Energy", "Siemens Gamesa", "NextEra Energy", "Iberdrola"]
    },
    "Bioinformatics Scientist": {
        "description": "Analyze complex biological data using computational tools to accelerate drug discovery and genetic research.",
        "why_it_matches": "Perfect hybrid of your data science aptitude and biological interests.",
        "recommended_skills": ["Genomic Analysis", "Computational Modeling", "R/Python", "AI in Healthcare"],
        "potential_jobs": ["Genetic Data Expert", "Computational Biologist", "Precision Medicine Lead"],
        "salary_range": "$115k - $210k",
        "growth_outlook": "Critical (Precision Medicine Era)",
        "learning_roadmap": ["PhD in Genomics/CS", "Master Large Scale Data Analysis", "Publish Bio-AI Research"],
        "core_challenges": "Managing petabyte-scale datasets and ensuring algorithmic reliability in clinical contexts.",
        "tech_stack": ["Nextflow", "Docker", "Python (Biopython)", "AWS Batch"],
        "work_life_balance": "Balanced (Research Context)",
        "entry_difficulty": "Very High (Hybrid Domain Depth Req)",
        "top_employers": ["Illumina", "Broad Institute", "Pfizer", "Google Health"]
    },
    "Financial Risk Manager": {
        "description": "Identify and analyze potential financial risks to protect organizational assets and ensure market stability.",
        "why_it_matches": "Strong alignment with your quantitative reasoning and strategic finance interests.",
        "recommended_skills": ["Stress Testing", "Quantitative Analysis", "Regulatory Compliance", "Risk Modeling"],
        "potential_jobs": ["Chief Risk Officer", "Fraud Auditor", "Market Risk Analyst"],
        "salary_range": "$120k - $250k",
        "growth_outlook": "Strategic (Stable Expansion)",
        "learning_roadmap": ["FRM Certification", "Master Quantitative Modeling", "Lead Enterprise Risk"],
        "core_challenges": "Market volatility and navigating complex global regulations.",
        "tech_stack": ["SAS", "Python", "RiskMetrics", "SQL"],
        "work_life_balance": "Moderate (High Stakes / Professional regularlty)",
        "entry_difficulty": "High (FRM / Math Depth Req)",
        "top_employers": ["BlackRock", "Goldman Sachs", "JP Morgan", "Prudential"]
    },
    "UX Researcher": {
        "description": "Investigate user behavior and psychological patterns to inform product design and human-centric experiences.",
        "why_it_matches": "Combines your psychological empathy with digital product strategy.",
        "recommended_skills": ["User Testing", "Behavioral Analytics", "Ethnographic Research", "A/B Testing"],
        "potential_jobs": ["User Experience Strategist", "Human Factors Engineer", "Product Insight Lead"],
        "salary_range": "$90k - $165k",
        "growth_outlook": "Strong (Data-Driven Design Shift)",
        "learning_roadmap": ["Master Psychological Research", "Learn Advanced Analytics", "Lead Multi-Domain Usability Studies"],
        "core_challenges": "Translating subjective user feedback into actionable engineering requirements.",
        "tech_stack": ["UserTesting", "Dovetail", "Figma", "Python"],
        "work_life_balance": "High (Flexible)",
        "entry_difficulty": "Medium (Insight & Analytics Driven)",
        "top_employers": ["Apple", "Netflix", "Google", "Spotify"]
    },
    "Musician & Performing Arts": {
        "description": "Master of sound and performance, from classical composition to modern digital production and live spectacle.",
        "why_it_matches": "Direct alignment with your proficiency in instruments, vocal performance, and creative musical theory.",
        "recommended_skills": ["Instrumental Mastery", "Vocal Training", "Composition", "Performance Arts"],
        "potential_jobs": ["Professional Musician", "Vocalist", "Composer", "Music Producer", "Artistic Director"],
        "salary_range": "$40k - $500k+ (Performance Based)",
        "growth_outlook": "Dynamic (Creative Economy)",
        "learning_roadmap": ["Master Musical Theory", "Build Performance Portfolio", "Network with Arts Organizations"],
        "core_challenges": "Highly competitive environment and inconsistent performance schedules.",
        "tech_stack": ["Logic Pro / Ableton", "DAW Instruments", "Acoustic Theory", "Stage Presence"],
        "work_life_balance": "Moderate (Peak Performance Cycles)",
        "entry_difficulty": "High (Talent & Technical Mastery Req)",
        "top_employers": ["Orchestras", "Music Labels", "Performance Houses", "Self-Employed"]
    },
    "Blockchain Architect": {
        "description": "Design and build decentralized systems and smart contracts, pioneering the future of Web3 and secure digital ledgers.",
        "why_it_matches": "Direct match for your high-tier technical skills and interest in decentralized security.",
        "recommended_skills": ["Solidity", "Cryptography", "Distributed Systems", "Smart Contract Security"],
        "potential_jobs": ["Smart Contract Dev", "DApp Architect", "Web3 Strategist"],
        "salary_range": "$130k - $280k",
        "growth_outlook": "Emerging (High Value Vertical)",
        "learning_roadmap": ["Master Cryptography", "Build Decentralized Apps", "Certify in Smart Contract Auditing"],
        "core_challenges": "Highly volatile ecosystems and the 'permanent' nature of code on the chain.",
        "tech_stack": ["Solidity", "Ether.js", "Hardhat", "Rust"],
        "work_life_balance": "Moderate (Global / Decentralized)",
        "entry_difficulty": "Very High (Cryptography / Security Depth)",
        "top_employers": ["Coinbase", "Chainlink", "Ethereum Foundation", "Polygon"]
    },
    "Supply Chain Strategist": {
        "description": "Optimize global flows of goods and materials using AI and predictive analytics to ensure global efficiency.",
        "why_it_matches": "Fits your organizational logic and strategic planning capabilities.",
        "recommended_skills": ["Predictive Logistics", "Global Sourcing", "AI Implementation", "Inventory Optimization"],
        "potential_jobs": ["Logistics Director", "Sustainability Lead", "Global Operations Strategist"],
        "salary_range": "$100k - $190k",
        "growth_outlook": "Critical (Supply Chain Resilience Focus)",
        "learning_roadmap": ["Master Analytics in Logistics", "Earn ASCM Certs", "Lead End-to-End Op Chains"],
        "core_challenges": "Geopolitical volatility and the complexity of global trade networks.",
        "tech_stack": ["SAP S/4HANA", "Oracle SCM", "Python", "Power BI"],
        "work_life_balance": "Balanced (Office Focused)",
        "entry_difficulty": "Medium (Experience & Logistics Savvy)",
        "top_employers": ["Amazon", "DHL", "Apple", "Maersk"]
    },
    "Public Relations Lead": {
        "description": "Shape and manage public perception for elite organizations through strategic communication and media storytelling.",
        "why_it_matches": "Leverages your strategic communication skills and leadership poise.",
        "recommended_skills": ["Crisis Communication", "Brand Storytelling", "Media Relations", "Strategic Narrative"],
        "potential_jobs": ["Director of PR", "Communications Strategist", "Brand Manager"],
        "salary_range": "$85k - $200k",
        "growth_outlook": "Vibrant (Brand Era)",
        "learning_roadmap": ["Master Media Psychology", "Build Global Media Network", "Lead High-Stakes Public Launches"],
        "core_challenges": "Immediate professional demand during PR crises and navigating complex public narratives.",
        "tech_stack": ["Brandwatch", "Muck Rack", "Slack", "AI Content Engine"],
        "work_life_balance": "Moderate (Always-on Narrative Monitoring)",
        "entry_difficulty": "Medium (Network & Influence Driven)",
        "top_employers": ["Edelman", "Ogilvy", "Global Brands", "Public Personalities"]
    },
    "AI Ethics Consultant": {
        "description": "Guide technology companies in developing fair, transparent, and ethically sound artificial intelligence systems.",
        "why_it_matches": "Unique intersection of your technical AI depth and ethical reasoning.",
        "recommended_skills": ["Algorithmic Bias Audit", "AI Regulation", "Moral Philosophy", "Technical Documentation"],
        "potential_jobs": ["Ethics Compliance Lead", "Policy Strategist", "AI Governance Officer"],
        "salary_range": "$110k - $220k",
        "growth_outlook": "Explosive (Regulation & Trust Focus)",
        "learning_roadmap": ["Master AI Policy Frameworks", "Lead Cross-domain Ethics Panels", "Conduct Bias Impact Studies"],
        "core_challenges": "Balancing rapid technical innovation with careful moral guardrails.",
        "tech_stack": ["AI Fairness Tools", "Jira", "Ethical Frameworks", "SQL"],
        "work_life_balance": "High (Strategic/Consultative)",
        "entry_difficulty": "High (Hybrid Philosophy/Tech Req)",
        "top_employers": ["Microsoft", "Anthropic", "IBM Research", "Government Agencies"]
    },
    "Sustainable Fashion Strategist": {
        "description": "Transform the global fashion industry through circular economy principles and eco-friendly material innovation.",
        "why_it_matches": "Perfect for your creative fashion interest mixed with a passion for sustainability.",
        "recommended_skills": ["Circular Design", "Material Science", "Eco-compliance", "Circular Production"],
        "potential_jobs": ["Circular Design Lead", "Sustainable Brand Manager", "Eco-Material Specialist"],
        "salary_range": "$75k - $155k",
        "growth_outlook": "Strong (Eco-conscious Consumer Shift)",
        "learning_roadmap": ["Master Circular Economy", "Prototype Sustainable Materials", "Lead Green Brand Transformation"],
        "core_challenges": "Balancing profit margins with the high cost of sustainable materials.",
        "tech_stack": ["Circulytics", "Adobe Suite", "Eco-tracking Software"],
        "work_life_balance": "Good (Creative Context)",
        "entry_difficulty": "Medium (Vision & Innovation Driven)",
        "top_employers": ["Patagonia", "Stella McCartney", "Eco-focused Startups", "Nike"]
    },
    "Quantum Computing Researcher": {
        "description": "Pioneer the next frontier of computation by developing quantum algorithms and hardware architectures.",
        "why_it_matches": "Direct resonance with your high-level physics and advanced algorithmic focus.",
        "recommended_skills": ["Quantum Mechanics", "Linear Algebra", "Qiskit/Cirq", "Algorithm Design"],
        "potential_jobs": ["Quantum Algorithmic Dev", "Cryogenic Engineer", "Quantum Software Lead"],
        "salary_range": "$140k - $300k+",
        "growth_outlook": "Horizon (Future Core Tech)",
        "learning_roadmap": ["PhD in Quantum Physics/CS", "Master Qiskit Ecosystem", "Contribute to Post-Quantum Crypto"],
        "core_challenges": "Qubit decoherence and the extreme math-heavy nature of the field.",
        "tech_stack": ["Qiskit", "Cirq", "Python", "C++"],
        "work_life_balance": "Moderate (Academic/Deep Research)",
        "entry_difficulty": "Extremely High (PhD Tier Meta)",
        "top_employers": ["IBM Quantum", "Google Quantum AI", "IonQ", "Rigetti"]
    },
    "HR Coordinator": {
        "description": "Support the recruitment, onboarding, and development of organizational talent while fostering a healthy company culture.",
        "why_it_matches": "Matches your organizational skills and empathy for people-centric growth.",
        "recommended_skills": ["Talent Acquisition", "Employee Relations", "Conflict Resolution", "HR Information Systems"],
        "potential_jobs": ["People Operations Associate", "Recruiter", "Culture Specialist"],
        "salary_range": "$55k - $95k",
        "growth_outlook": "Stable (Human Capital Essential)",
        "learning_roadmap": ["Degree in HR/Business", "Earn SHRM Certification", "Lead People Strategy Initiatives"],
        "core_challenges": "Balancing organizational policies with diverse employee needs.",
        "tech_stack": ["BambooHR", "Workday", "LinkedIn Recruiter", "Slack"],
        "work_life_balance": "High (Regular Office Hours)",
        "entry_difficulty": "Low-Medium (Professional & People Skills Driven)",
        "top_employers": ["Global Corporations", "Tech Startups", "Government Agencies", "Non-Profits"]
    },
    "Sales Development Rep": {
        "description": "Drive business growth by identifying potential clients and initiating strategic relationships for value-driven solutions.",
        "why_it_matches": "Leverages your persuasive communication and high-energy drive.",
        "recommended_skills": ["Lead Generation", "Strategic Outreach", "Negotiation", "CRM Management"],
        "potential_jobs": ["Account Executive", "Inside Sales Associate", "Business Development Manager"],
        "salary_range": "$60k - $120k+ (Variable)",
        "growth_outlook": "Vibrant (Crucial Growth Engine)",
        "learning_roadmap": ["Master Sales Frameworks", "Learn Solution Selling", "Manage High-Tier Global Accounts"],
        "core_challenges": "Handling rejection and maintaining consistent outbound momentum.",
        "tech_stack": ["Salesforce", "Outreach", "ZoomInfo", "Gong.io"],
        "work_life_balance": "Moderate (Performance Driven)",
        "entry_difficulty": "Low (Drive & Grit Driven)",
        "top_employers": ["Software Companies", "Financial Services", "Advertising Agencies", "Fast-Growth Scaleups"]
    },
    "Customer Success Manager": {
        "description": "Ensure clients achieve their desired outcomes while using a product, fostering long-term loyalty and partnership.",
        "why_it_matches": "Perfect for your relationship management and problem-solving focus.",
        "recommended_skills": ["Client Advocacy", "Product Training", "Churn Analysis", "Strategic Partnership"],
        "potential_jobs": ["Account Manager", "Retention Specialist", "Director of Success"],
        "salary_range": "$75k - $145k",
        "growth_outlook": "Very Strong (SaaS Economy Expansion)",
        "learning_roadmap": ["Master Product Lifecycle", "Learn Relationship Strategy", "Lead Enterprise Customer Groups"],
        "core_challenges": "Managing technical escalations and aligning product roadmap with client needs.",
        "tech_stack": ["Gainsight", "Zendesk", "Salesforce", "Notion"],
        "work_life_balance": "Balanced (Professional Routine)",
        "entry_difficulty": "Medium (Product Knowledge & Empathy Req)",
        "top_employers": ["HubSpot", "Salesforce", "Slack", "E-commerce Platforms"]
    },
    "Content Marketing Specialist": {
        "description": "Create and distribute valuable, relevant content to attract and engage a clearly defined audience.",
        "why_it_matches": "Leverages your creative writing and digital storytelling interests.",
        "recommended_skills": ["Copywriting", "SEO Strategy", "Social Media Management", "Content Analytics"],
        "potential_jobs": ["Editor", "Content Strategist", "Social Media Lead"],
        "salary_range": "$65k - $110k",
        "growth_outlook": "Strong (Digital Brand Presence Essential)",
        "learning_roadmap": ["Master SEO Copywriting", "Build Digital Portfolio", "Analyze Multi-channel Campaign Impact"],
        "core_challenges": "Keeping up with platform algorithm shifts and maintaining consistent creative quality.",
        "tech_stack": ["Semrush", "Canva", "WordPress", "Google Analytics"],
        "work_life_balance": "High (Creative Flexibility)",
        "entry_difficulty": "Low-Medium (Portfolio & Tone Focused)",
        "top_employers": ["Marketing Agencies", "Tech Brands", "Media Outlets", "Self-Employed Freelancer"]
    },
    "Primary School Teacher": {
        "description": "Direct foundational learning experiences for young students, shaping their cognitive and social development.",
        "why_it_matches": "Direct resonance with your passion for education and societal impact.",
        "recommended_skills": ["Curriculum Design", "Child Psychology", "Classroom Management", "Parental Communication"],
        "potential_jobs": ["Elementary Educator", "Educational Consultant", "Tutor"],
        "salary_range": "$45k - $85k",
        "growth_outlook": "Steady (Fundamental Social Pillar)",
        "learning_roadmap": ["B.Ed Degree", "State Licensing", "Master Special Education/Pedagogy"],
        "core_challenges": "Managing diverse classroom dynamics and administrative documentation.",
        "tech_stack": ["Google Classroom", "Kahoot", "ClassDojo", "Interactive Whiteboards"],
        "work_life_balance": "Moderate (Significant Offline Prep Time)",
        "entry_difficulty": "Medium (Degree & Certification Req)",
        "top_employers": ["Public Schools", "Private Academies", "International Schools", "Edu-Tech Startups"]
    },
    "Financial Advisor": {
        "description": "Provide customized wealth management, investment, and retirement planning advice to individuals and families.",
        "why_it_matches": "Combines your financial acumen with high-trust client advisory.",
        "recommended_skills": ["Wealth Management", "Estate Planning", "Market Portfolio Analysis", "CFP Compliance"],
        "potential_jobs": ["Investment Advisor", "Wealth Manager", "Financial Planner"],
        "salary_range": "$80k - $250k+ (Variable)",
        "growth_outlook": "Strong (Retirement Wave Dynamics)",
        "learning_roadmap": ["CFP/CFA Certification", "Build High-Trust Client Base", "Manage Diversified Private Portfolios"],
        "core_challenges": "Market volatility impact on portfolios and complex regulatory requirements.",
        "tech_stack": ["Morningstar", "Fidelity Tools", "CRM (Redtail)", "Excel"],
        "work_life_balance": "Balanced (Relationship Centric)",
        "entry_difficulty": "Medium-High (CFP/Licensing Req)",
        "top_employers": ["Morgan Stanley", "Merrill Lynch", "Private Practices", "Online Fin-Advisory Firms"]
    },
    "Real Estate Consultant": {
        "description": "Guide clients through the complex process of buying, selling, and investing in residential and commercial properties.",
        "why_it_matches": "Matches your interest in physical markets and strategic negotiation.",
        "recommended_skills": ["Property Valuation", "Market Analysis", "Negotiation", "Sales Strategy"],
        "potential_jobs": ["Residential Agent", "Commercial Specialist", "Asset Manager"],
        "salary_range": "$50k - $300k+ (Commission Driven)",
        "growth_outlook": "Cyclical (Property Sector Resilience)",
        "learning_roadmap": ["Real Estate License", "Master Local Market Trends", "Build Elite Realtor Network"],
        "core_challenges": "Fluctuating market inventory and irregular income cycles.",
        "tech_stack": ["Zillow Premium", "MLS", "CRM (Follow Up Boss)", "Docusign"],
        "work_life_balance": "Varies (Client Demand Dependent)",
        "entry_difficulty": "Low-Medium (License Driven)",
        "top_employers": ["CBRE", "RE/MAX", "Compass", "JLL"]
    },
    "Administrative Specialist": {
        "description": "Optimize organizational efficiency by managing executive operations, scheduling, and logistical coordination.",
        "why_it_matches": "Leverages your high-level organizational and coordination abilities.",
        "recommended_skills": ["Logistics Management", "Executive Support", "Project Coordination", "Digital Ops"],
        "potential_jobs": ["Executive Assistant", "Office Manager", "Operations Coordinator"],
        "salary_range": "$50k - $95k",
        "growth_outlook": "Stable (Business Core Essential)",
        "learning_roadmap": ["Master Enterprise Software", "Project Management Certification", "Scale to Operations Lead"],
        "core_challenges": "Managing overlapping high-priority task flows from multiple stakeholders.",
        "tech_stack": ["G Suite / Microsoft 365", "Zoom", "Calendly", "Asana"],
        "work_life_balance": "High (Regular Office Hours)",
        "entry_difficulty": "Low (Professional Poise & Skill Driven)",
        "top_employers": ["Law Firms", "Fortune 500s", "Startup Founders", "Non-Profits"]
    },
    "Retail Store Manager": {
        "description": "Oversee end-to-end retail operations, from inventory and staff management to customer experience excellence.",
        "why_it_matches": "Combines your operational logic with team leadership in a consumer field.",
        "recommended_skills": ["Inventory Control", "Team Leadership", "Visual Merchandising", "Retail Analytics"],
        "potential_jobs": ["Area Manager", "Operations Lead", "Consumer Brand Manager"],
        "salary_range": "$55k - $105k",
        "growth_outlook": "Steady (Experience-led Retail Demand)",
        "learning_roadmap": ["Master P&L Management", "Learn Retail Psychology", "Scale to District/Regional Leadership"],
        "core_challenges": "Maintaining staff morale and navigating seasonal demand surges.",
        "tech_stack": ["POS Systems", "Workday (Scheduling)", "Inventory Software", "SAP"],
        "work_life_balance": "Moderate (Weekend/Shift Presence)",
        "entry_difficulty": "Low-Medium (Experience Driven)",
        "top_employers": ["Zara", "Apple Store", "Walmart", "Luxury Retail Brands"]
    },
    "Digital Marketing Associate": {
        "description": "Execute digital growth campaigns across social media, search engines, and email to build brand authority.",
        "why_it_matches": "Fits your interest in modern media and data-driven marketing.",
        "recommended_skills": ["Social Media Ops", "Email Automation", "Ad Campaign Mgmt", "Marketing Data"],
        "potential_jobs": ["SEO Analyst", "Social Media Coordinator", "Growth Marketer"],
        "salary_range": "$50k - $90k",
        "growth_outlook": "Vertical (Everyone is Digital First)",
        "learning_roadmap": ["Google Ads Certification", "Learn Meta Ads Manager", "Execute Viral Brand Strategies"],
        "core_challenges": "Adapting to fast-paced platform updates and maintaining creative relevance.",
        "tech_stack": ["Google Ads", "Meta Business Suite", "Mailchimp", "HubSpot"],
        "work_life_balance": "High (Digital Nomad Friendly)",
        "entry_difficulty": "Low (Skill & Execution Driven)",
        "top_employers": ["Marketing Agencies", "Direct-to-Consumer Brands", "E-commerce Companies", "Remote Startups"]
    }
}

# Define Fuzzy Clusters
CLUSTERS = {
    # --- Technology & Data ---
    "Software Engineer": ["software", "developer", "coding", "programming", "engineer", "java", "react", "backend", "frontend", "computer science"],
    "Data Scientist": ["data scientist", "data science", "ai", "machine learning", "deep learning", "statistics", "python", "analytics", "big data"],
    "Full Stack Developer": ["full stack", "fullstack", "web developer", "mern", "mean", "website", "web app"],
    "UI/UX Designer": ["ui", "ux", "interface", "user experience", "figma", "adobe", "web design", "product design"],
    "Cloud Architect": ["cloud", "aws", "azure", "gcp", "devops", "kubernetes", "infrastructure", "server"],
    "Cybersecurity Analyst": ["security", "hack", "cyber", "network", "firewall", "protect", "infosec", "penetration"],
    "Machine Learning Engineer": ["nlp", "computer vision", "tensorflow", "pytorch", "neural networks", "model training"],
    "Game Developer": ["game", "gaming", "gamer", "unity", "unreal", "graphics", "engine", "level design"],
    "Technical Writer": ["technical writing", "documentation", "manual", "guide", "api docs"],

    # --- Business & Finance ---
    "Investment Analyst": ["finance", "stock", "trading", "quant", "crypto", "bank", "forex", "invest", "wall street"],
    "Accountant": ["accounting", "cpa", "tax", "audit", "financial report", "bookkeeping"],
    "Financial Analyst": ["financial analysis", "budget", "forecast", "economic", "valuation"],
    "Management Consultant": ["consult", "strategy", "business", "management", "corporate", "advisory", "solution"],
    "Product Manager": ["product manager", "pm", "roadmap", "agile", "feature", "user stories"],
    "HR Manager": ["human resources", "hr", "recruiting", "hiring", "personnel", "employee relations"],
    "Digital Marketer": ["marketing", "seo", "ads", "advertising", "social media", "growth", "brand", "content strategy"],

    # --- Healthcare & Science ---
    "Doctor": ["doctor", "physician", "surgeon", "medicine", "medical", "hospital", "diagnosis", "surgery"],
    "Nursing": ["nurse", "nursing", "patient care", "clinical", "rn", "healthcare"],
    "Pharmacist": ["pharmacy", "pharmacist", "drug", "medication", "prescription", "dispense"],
    "Pharmaceutical Researcher": ["drug discovery", "clinical trial", "pharmaceutical research", "lab research"],
    "Medical Researcher": ["medical research", "biomedical", "disease research", "pathology"],
    "Healthcare Professional": ["healthcare admin", "public health", "health management"],
    "Biologist": ["biology", "life science", "genetics", "organism", "cell"],
    "Chemist": ["chemistry", "chemical", "lab", "reaction", "molecule"],
    "Research Psychologist": ["psychology", "mental health", "therapy", "behavior", "counseling", "psychiatry"],

    # --- Engineering & Environment ---
    "Civil Engineer": ["civil engineer", "structure", "bridge", "road", "infrastructure", "construction"],
    "Mechanical Engineer": ["mechanical", "robotics", "machine", "thermodynamics", "manufacturing"],
    "Environmental Scientist": ["environment", "sustainability", "climate", "ecology", "green", "conservation"],
    "Agriculturist": ["agriculture", "farming", "crop", "soil", "agronomy"],
    "Botanist": ["botany", "plant", "flora", "horticulture"],
    "Landscape Architect": ["landscape", "garden", "outdoor design", "park"],

    # --- Creative & Media ---
    "Arts & Creative Professional": ["arts", "fine arts", "artist", "painting", "sculpting", "museum", "gallery", "creative", "drawing", "illustration", "sketching"],
    "Graphic Designer": ["graphic design", "visual", "illustration", "logo", "branding", "layout", "visual arts"],
    "Digital Artist": ["digital art", "concept art", "drawing", "sketching", "painting", "artistic"],
    "Content Creator": ["streamer", "youtuber", "video", "content creation", "influencer", "vlog", "media"],
    "Content Writer": ["writer", "copywriting", "blogging", "journalism", "editor", "literature"],
    "Fashion Designer": ["fashion", "clothing", "apparel", "style", "textile", "sewing", "design"],
    "Executive Chef": ["chef", "cooking", "culinary", "kitchen", "food", "restaurant", "gastronomy"],
    "Event Planner": ["event", "wedding", "party", "planning", "Logistics", "coordinator"],

    # --- Specialized & Service ---
    "Defense & Strategic Operations": ["military", "army", "navy", "airforce", "marines", "defense", "soldier", "tactical"],
    "Army Officer": ["army officer", "platoon", "command", "military leader", "military", "defense", "officer"],
    "Air Force Pilot": ["pilot", "aviation", "flight", "airforce", "flying", "cockpit", "aircraft"],
    "Aerospace Engineer": ["aerospace", "aeronautics", "rocket", "satellite", "spacex", "boeing", "aeronautical", "space", "space exploration", "aviation"],
    "Astronomer": ["astronomy", "star", "astrophysics", "cosmology", "telescope", "planet", "galaxy", "universe", "space studies", "nasa", "space exploration", "stargazing"],
    "Intelligence Analyst": ["intelligence", "cia", "nsa", "classified", "spying"],
    "Lawyer": ["law", "legal", "attorney", "court", "justice", "litigation"],
    "Policy Analyst": ["policy", "government", "politics", "legislation", "public affairs"],
    "Professional Astrologer": ["astrology", "horoscope", "zodiac", "spiritual", "tarot", "metaphysical", "natal chart", "reading minds", "mind reading", "zodiac signs"],
    "Professional Sports & Athletics": ["sports", "athlete", "basketball", "football", "soccer", "olympic", "cricket", "athletic"],
    "Sports Coach": ["sports", "coaching", "trainer", "team management", "sports psychology", "mentor"],
    "Musician & Performing Arts": ["singer", "vocalist", "music", "musician", "performer", "piano", "guitar", "instrument", "performing arts", "composition"],

    # --- Sustainability & Ethics ---
    "Renewable Energy Engineer": ["renewable", "solar", "wind", "energy", "sustainability", "green tech"],
    "AI Ethics Consultant": ["ethics", "ai ethics", "governance", "policy", "bias", "fairness", "regulation"],
    "Sustainable Fashion Strategist": ["sustainable fashion", "circular economy", "eco-friendly", "textiles", "green design"],

    # --- Advanced Tech & Web3 ---
    "Blockchain Architect": ["blockchain", "solidity", "crypto", "web3", "smart contracts", "decentralized"],
    "Bioinformatics Scientist": ["bioinformatics", "genomics", "biological data", "biotech data"],

    # --- Strategy & Operations ---
    "Financial Risk Manager": ["risk management", "frm", "market risk", "credit risk", "compliance"],
    "UX Researcher": ["ux research", "usability", "user behavior", "ethnography"],
    "Supply Chain Strategist": ["supply chain", "logistics flow", "global trade", "operations"],
    "Public Relations Lead": ["pr", "public relations", "communications", "media strategy", "branding"],
    "Quantum Computing Researcher": ["quantum", "qiskit", "physics", "superposition", "entanglement"],

    # --- General Sector Expansion ---
    "HR Coordinator": ["hr", "human resources", "recruitment", "onboarding", "hiring", "talent", "culture"],
    "Sales Development Rep": ["sales", "selling", "selling products", "leads", "outreach", "cold calling", "business development"],
    "Customer Success Manager": ["customer success", "client relations", "csm", "retention", "customer support"],
    "Content Marketing Specialist": ["content marketing", "copywriting", "blogging", "writing social media", "content strategy"],
    "Primary School Teacher": ["teaching", "education", "school", "kids", "classroom", "learning", "pedagogy"],
    "Financial Advisor": ["financial planning", "wealth management", "investments", "retirement", "money advice"],
    "Real Estate Consultant": ["real estate", "property", "selling houses", "broker", "housing market"],
    "Administrative Specialist": ["admin", "assistant", "office manager", "clerical", "scheduling", "coordination"],
    "Retail Store Manager": ["retail", "store", "shop management", "inventory", "sales associate"],
    "Digital Marketing Associate": ["digital marketing", "seo", "google ads", "social media marketing", "online ads"]
}

def normalize_scores(details: List[CareerRecommendation], assessment: UserAssessment) -> List[CareerRecommendation]:
    if not details:
        return details
    
    raw_scores = [d.match_score for d in details]
    max_raw = max(raw_scores) if raw_scores else 0.0
    
    # Calculate input richness (reward more detailed inputs)
    tech_count = len(assessment.tech_skills) if isinstance(assessment.tech_skills, list) else len(str(assessment.tech_skills).split(','))
    soft_count = len(assessment.soft_skills) if isinstance(assessment.soft_skills, list) else len(str(assessment.soft_skills).split(','))
    richness = min(1.0, (tech_count + soft_count) / 12.0) # Full variety at 12 skills
    
    # Dynamic target_max instead of fixed 96%
    if max_raw <= 0.2:
        target_max = 0.142 + (richness * 0.158) 
    elif max_raw < 0.5:
        target_max = 0.374 + (richness * 0.183)
    else:
        # Restore Realistic Variable Range (86% - 99.4%)
        # Math is now highly sensitive to both raw ML output and input detail (richness)
        target_max = 0.8541 + (max_raw * 0.0712) + (richness * 0.0543)
        if target_max > 0.9935: target_max = 0.9935
    
    # Add a "Identity Jitter" so two users with same skills get unique %
    # We now factor in a touch of 'volatility' to make it feel alive
    import time
    time_seed = int(time.time()) % 100
    jitter_seed = sum(ord(c) for c in assessment.name) + len(assessment.interests) + time_seed
    jitter = ((jitter_seed % 60) - 30) / 1000.0 # +/- 0.03 jitter

    normalized = []
    for i, d in enumerate(details):
        if max_raw > 0:
            scale_factor = d.match_score / max_raw
            # Apply jitter only to top match for maximum variation where it matters
            current_jitter = jitter if i == 0 else (jitter * 0.35)
            new_score = (scale_factor * target_max) + current_jitter
        else:
            new_score = 0.0471
            
        match_val = min(0.9942, max(0.041, float(new_score)))
        d.match_score = float(f"{match_val:.4f}")
        normalized.append(d)
        
    return normalized

def levenshtein_ratio(s1, s2):
    """Robust similarity ratio between two strings (0 to 1)"""
    from difflib import SequenceMatcher
    s1, s2 = s1.lower().strip(), s2.lower().strip()
    
    # 1. Exact or simple substring
    if s1 == s2: return 1.0
    if not s1 or not s2: return 0.0
    
    # 2. Handle space differences (e.g., 'airforce' vs 'air force')
    s1_flat = s1.replace(" ", "")
    s2_flat = s2.replace(" ", "")
    if s1_flat == s2_flat: return 1.0
    
    # 3. Fuzzy matching using SequenceMatcher
    ratio = SequenceMatcher(None, s1, s2).ratio()
    
    # 4. Multi-word phrase matching (Special for "mind reading" etc)
    if " " in s1 or " " in s2:
        words1 = set(s1.split())
        words2 = set(s2.split())
        if words1.intersection(words2):
            return 0.85 # High enough to trigger match
    
    # 5. Strict threshold for short keywords
    if ratio > 0.8:
        if len(s1) < 5:
            return 1.0 if s1 in s2 or s2 in s1 else 0.0
        return ratio
        
    return 0.0
from predict import get_ml_recommendations, validate_assessment_data

def get_career_guidance(assessment: UserAssessment) -> GuidanceResponse:
    # 0. STRICT BLOCKING: Check for nonsense input
    is_valid, msg = validate_assessment_data(assessment)
    if not is_valid:
        return GuidanceResponse(
            is_valid=False,
            validation_message=msg,
            ml_recommendations=[],
            career_details=[],
            explanation="Assessment contains invalid or non-standard input."
        )

    # 1. Advanced Fuzzy Sensing Layer (RUN FIRST)
    # Give significantly higher weight    # Init keyword tracking
    keyword_hits = [] 
    interest_query = assessment.interests.lower()
    activities_query = assessment.extracurriculars.lower()
    
    tech_skills_str = ",".join(assessment.tech_skills) if isinstance(assessment.tech_skills, list) else str(assessment.tech_skills)
    soft_skills_str = ",".join(assessment.soft_skills) if isinstance(assessment.soft_skills, list) else str(assessment.soft_skills)
    skill_corpus = (tech_skills_str + "," + soft_skills_str).lower()
    
    keyword_match = None
    max_score = 0
    
    for career, gems in CLUSTERS.items():
        career_score = 0
        matched_interests = []
        matched_activities = []
        
        for gem in gems:
            gem_lower = gem.lower()
            
            # Check Interest (HIGH PRIORITY: 25.0)
            # Passion-driven interests are the primary guide for recommendations
            if gem_lower in interest_query or float(levenshtein_ratio(gem_lower, interest_query)) > 0.7:
                career_score += 25.0
                matched_interests.append(gem)
                
            # Check Activities (Contextual: 2.0)
            if gem_lower in activities_query or float(levenshtein_ratio(gem_lower, activities_query)) > 0.7:
                career_score += 2.0
                matched_activities.append(gem)
            
            # Check Skills (Auxiliary: 1.0)
            if gem_lower in skill_corpus:
                career_score += 1.0
                
        if career_score > 0:
            # Deduplicate keywords for display
            matched_interests = list(set(matched_interests))
            matched_activities = list(set(matched_activities))
            keyword_hits.append({
                "career": career, 
                "score": career_score,
                "interests": matched_interests,
                "activities": matched_activities
            })

    print(f"DEBUG: Interest: {interest_query} | Activities: {activities_query}")
    print(f"DEBUG: Keyword Matches Found: {len(keyword_hits)}")

    # 1.5 Skill Alignment Hub (NEW: prioritize what user actually entered)
    user_tech = set(s.strip().lower() for s in assessment.tech_skills if s.strip()) if isinstance(assessment.tech_skills, list) else set(s.strip().lower() for s in str(assessment.tech_skills).split(',') if s.strip())
    user_soft = set(s.strip().lower() for s in assessment.soft_skills if s.strip()) if isinstance(assessment.soft_skills, list) else set(s.strip().lower() for s in str(assessment.soft_skills).split(',') if s.strip())
    user_all_skills = user_tech.union(user_soft)
    
    skill_primary_matches = []
    
    for title, meta in CAREER_METADATA.items():
        # Elastic skill matching: split by '/' and ',' to catch "Python/SQL" etc.
        tech_base = meta.get("tech_stack", [])
        rec_base = meta.get("recommended_skills", [])
        
        # Defensive check to ensure they are lists
        tech_list = tech_base if isinstance(tech_base, list) else [tech_base] if tech_base else []
        rec_list = rec_base if isinstance(rec_base, list) else [rec_base] if rec_base else []
        
        all_metadata_skills = tech_list + rec_list
        career_skills = set()
        for s in all_metadata_skills:
            parts = [p.strip().lower() for p in s.replace('/', ',').split(',')]
            career_skills.update(parts)
            
        exact_matches = user_all_skills.intersection(career_skills)
        
        if exact_matches:
            match_ratio = len(exact_matches) / max(len(career_skills), 1)
            skill_score = 0.85 + (match_ratio * 0.1) + (min(len(exact_matches), 10) * 0.005)
            # Create dynamic "Why It Matches"
            matched_list = list(exact_matches)[:3]
            dynamic_why = f"Direct alignment with your proficiency in {', '.join(matched_list)}. "
            if len(exact_matches) > 3:
                dynamic_why += f"Plus {len(exact_matches)-3} more overlapping skills."
            else:
                dynamic_why += str(meta.get("why_it_matches", ""))

            skill_primary_matches.append({
                "title": title,
                "score": min(0.99, skill_score),
                "why": dynamic_why,
                "meta": meta
            })

    skill_primary_matches.sort(key=lambda x: x["score"], reverse=True)
    print(f"DEBUG: Skill Primary Matches Found: {len(skill_primary_matches)}")

    # 2. Get high-accuracy ML matches
    ml_hits = []
    try:
        ml_hits = get_ml_recommendations(assessment)
    except Exception as e:
        print(f"ML Processing bypassed: {str(e)}")
        ml_hits = []

    # 3. Construct Final Details (GLOBAL POOLING)
    candidate_pool = []
    
    # Pool 1: Skill Primary Matches
    for sm in skill_primary_matches:
        meta = sm["meta"]
        candidate_pool.append(CareerRecommendation(
            career_title=sm["title"],
            match_score=sm["score"],
            description=meta["description"],
            why_it_matches=sm["why"],
            recommended_skills=meta["recommended_skills"],
            potential_jobs=meta["potential_jobs"],
            salary_range=meta["salary_range"],
            growth_outlook=meta["growth_outlook"],
            learning_roadmap=meta["learning_roadmap"],
            core_challenges=meta["core_challenges"],
            tech_stack=meta["tech_stack"],
            work_life_balance=meta.get("work_life_balance", "Balanced"),
            entry_difficulty=meta.get("entry_difficulty", "Medium"),
            top_employers=meta.get("top_employers", []),
            radar_dimensions=meta.get("radar_dimensions", {})
        ))

    # Pool 2: Multiple Keyword Matches (Dynamic Why)
    for hit in keyword_hits:
        title = str(hit["career"])
        score = float(hit["score"])
        if title in CAREER_METADATA:
            meta = CAREER_METADATA[title]
            # Significant Weighting: Keyword scores carry high weight
            base_score = 0.98 + (min(score, 100) * 0.0001) 
            
            # Build Dynamic Why
            why_parts = []
            interests = hit.get("interests", [])
            activities = hit.get("activities", [])
            
            if isinstance(interests, list) and interests:
                why_parts.append(f"matches your core interest in {', '.join(str(i) for i in interests)}")
            if isinstance(activities, list) and activities:
                why_parts.append(f"aligns with your background in {', '.join(str(a) for a in activities)}")
                
            dynamic_why = "This career " + " and ".join(why_parts) + ". " if why_parts else str(meta["why_it_matches"])
            
            # Passion Priority: If this hit came from the Interests field, give it an elite boost
            # This ensures Passion (Interests) leads over Tools (Skills)
            is_passion_match = len(matched_interests) > 0
            passion_boost = 0.05 if is_passion_match else 0.0
            
            candidate_pool.append(CareerRecommendation(
                career_title=title,
                match_score=min(0.995, base_score + passion_boost),
                description=meta["description"],
                why_it_matches=dynamic_why,
                recommended_skills=meta["recommended_skills"],
                potential_jobs=meta["potential_jobs"],
                salary_range=meta["salary_range"],
                growth_outlook=meta["growth_outlook"],
                learning_roadmap=meta["learning_roadmap"],
                core_challenges=meta["core_challenges"],
                tech_stack=meta["tech_stack"],
                work_life_balance=meta.get("work_life_balance", "Balanced"),
                entry_difficulty=meta.get("entry_difficulty", "Medium"),
                top_employers=meta.get("top_employers", []),
                radar_dimensions=meta.get("radar_dimensions", {})
            ))

    # Pool 3: ML Hits
    for hit in ml_hits:
        title = hit['career_title']
        if title in CAREER_METADATA:
            meta = CAREER_METADATA[title]
            candidate_pool.append(CareerRecommendation(
                career_title=title,
                match_score=min(0.90, hit['match_score']),
                description=meta["description"],
                why_it_matches=meta["why_it_matches"],
                recommended_skills=meta["recommended_skills"],
                potential_jobs=meta["potential_jobs"],
                salary_range=meta["salary_range"],
                growth_outlook=meta["growth_outlook"],
                learning_roadmap=meta["learning_roadmap"],
                core_challenges=meta["core_challenges"],
                tech_stack=meta["tech_stack"],
                work_life_balance=meta.get("work_life_balance", "Balanced"),
                entry_difficulty=meta.get("entry_difficulty", "Medium"),
                top_employers=meta.get("top_employers", []),
                radar_dimensions=meta.get("radar_dimensions", {})
            ))

    # Pool 4: Fallbacks (Implicit Low Score)
    FALLBACKS = ["Software Engineer", "Data Scientist", "UI/UX Designer", "Product Manager", "Nursing", "Musician & Performing Arts"]
    for fb in FALLBACKS:
        if fb in CAREER_METADATA:
            meta = CAREER_METADATA[fb]
            candidate_pool.append(CareerRecommendation(
                career_title=fb,
                match_score=0.1,  # Low base score, will only appear if others aren't higher
                description=meta["description"],
                why_it_matches=meta["why_it_matches"],
                recommended_skills=meta["recommended_skills"],
                potential_jobs=meta["potential_jobs"],
                salary_range=meta["salary_range"],
                growth_outlook=meta["growth_outlook"],
                learning_roadmap=meta["learning_roadmap"],
                core_challenges=meta["core_challenges"],
                tech_stack=meta["tech_stack"],
                work_life_balance=meta.get("work_life_balance", "Balanced"),
                entry_difficulty=meta.get("entry_difficulty", "Medium"),
                top_employers=meta.get("top_employers", []),
                radar_dimensions=meta.get("radar_dimensions", {})
            ))

    # 4. Deduplicate and Sort the Pool
    best_candidates = {}
    for cand in candidate_pool:
        title = cand.career_title
        if title not in best_candidates or cand.match_score > best_candidates[title].match_score:
            best_candidates[title] = cand

    # Sort by absolute score and take the elite 6
    final_pool = sorted(best_candidates.values(), key=lambda x: x.match_score, reverse=True)
    final_details: List[CareerRecommendation] = list(final_pool)[:6]

    # Final Ranking: Sort by absolute match score before normalization
    print(f"DEBUG: Before sorting: {[(d.career_title, d.match_score) for d in final_details]}")
    final_details.sort(key=lambda x: x.match_score, reverse=True)
    print(f"DEBUG: After sorting: {[(d.career_title, d.match_score) for d in final_details]}")
    
    # Final Normalization and Scoring Hierarchy
    final_details = normalize_scores(final_details, assessment)
    
    # ENSURE SORTING AFTER NORMALIZATION (GUARANTEED HIERARCHY)
    final_details.sort(key=lambda x: x.match_score, reverse=True)

    return GuidanceResponse(
        ml_recommendations=[{"career_title": d.career_title, "match_score": d.match_score} for d in final_details],
        career_details=final_details
    )
