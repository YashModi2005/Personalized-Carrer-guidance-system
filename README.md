# 🚀 AI CareerPilot: Neural Career Guidance System

[![React](https://img.shields.io/badge/Frontend-React.js-blue?style=for-the-badge&logo=react)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-orange?style=for-the-badge&logo=scikitlearn)](https://scikit-learn.org/)
[![MySQL](https://img.shields.io/badge/Database-MySQL-blue?style=for-the-badge&logo=mysql)](https://www.mysql.com/)

An advanced, end-to-end career guidance platform powered by **Explainable AI (XAI)**. This system predicts career trajectories by analyzing technical competencies, soft skills, and academic metrics, providing users with a "Neural Reasoning" thought stream and interactive coaching.

---

## 📸 Preview
> *Tip: Upload your project screenshots to the `assets/` folder and link them here!*
![Dashboard Preview](https://via.placeholder.com/800x450?text=AI+CareerPilot+Premium+Dashboard)

---

## ✨ Key Modules

### 1. 🧠 Neural Prediction Engine
Utilizes a **Naive Bayes & Random Forest Ensemble** to predict the top 3 career matches with probability scores.
- **Explainable AI**: Visualizes SHAP values to show *why* a specific career was recommended.
- **Skill Gap Analysis**: Compares user skills against industry standards.

### 2. 🤖 Neural Reasoning Agent
A proactive AI coach that simulates human reasoning to guide users through their career path.
- **Interactive Chat**: Natural language processing for career-related queries.
- **Step-by-Step Roadmaps**: Dynamically generated learning paths.

### 3. 💎 Premium UI/UX
- **Glassmorphism Design**: High-end visual aesthetic with blurred backgrounds and neon accents.
- **Real-time Data Visualization**: Interactive charts for salary growth and market trends.
- **Responsive Layout**: Seamless experience across Desktop and Mobile.

---

## 📂 Repository Hygiene: Excluded Files
To maintain a clean and secure repository, the following are **not** committed. Follow these steps to regenerate them:

| Excluded Item | Description | Restoration Command / Action |
| :--- | :--- | :--- |
| `node_modules/` | Frontend dependencies | `cd frontend && npm install` |
| `.env` | Secret API/DB keys | Create `backend/.env` (see template below) |
| `__pycache__/` | Python byte code | Automatically created on run |
| `*.log` | Server error logs | Automatically created on run |

---

## 🛠️ Detailed Setup Guide

### 1. Database Initialization
1. Open your MySQL client (Workbench or CMD).
2. Create a database: `CREATE DATABASE career_guidance;`
3. Import the schema from `backend/view_data.sql`.

### 2. Environment Variables
Create a file named `.env` in the `backend/` folder:
```env
# Database Config
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=career_guidance

# AI Config (Optional)
AI_MODEL_PATH=weights/career_model_nb.pkl
```

### 3. Backend Installation
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Frontend Installation
```bash
cd frontend
npm install
```

---

## 🔌 API Documentation (Endpoints)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/login` | User/Admin Authentication |
| `POST` | `/api/predict` | ML Career Prediction Engine |
| `GET` | `/api/dashboard/{user_id}` | Fetch personalized career data |
| `POST` | `/api/chat` | Interact with the Neural Reasoning Agent |

---

## 📉 Machine Learning Architecture
The system processes **25+ input features** including:
- **Technical**: Programming, Database, Cloud, UI/UX skills.
- **Soft Skills**: Communication, Leadership, Problem Solving.
- **Academic**: CGPA, Internships, Projects.

**Model Pipeline:**
1. **Preprocessing**: Label Encoding + Scaling.
2. **Feature Extraction**: TF-IDF for text-based interests.
3. **Classification**: Naive Bayes (Fast) + Random Forest (High Accuracy).

---

## 🔑 Access Credentials

*   **Admin Dashboard**: `Admin` / `123456`
*   **Student Dashboard**: `Yash` / `123456`

---

## 🚀 Future Roadmap
- [ ] Integration with LinkedIn API for real-time job listings.
- [ ] PDF Certificate generation for assessment completion.
- [ ] Dark/Light mode toggle for the UI.
- [ ] Mobile App version using React Native.

---

## 🛡️ License & Copyright
Developed by **Yash Modi** for the Final Year Capstone Project. All rights reserved. 
