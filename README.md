# 🚀 AI CareerPilot: Personalized Career Guidance System

A premium, full-stack career trajectory prediction and guidance system. This platform uses machine learning to analyze technical skills, soft skills, and academic performance to recommend optimal career paths with high-accuracy roadmaps and AI coaching.

---

## ✨ Key Features
- **AI-Driven Recommendations**: Predicts top career matches using Scikit-Learn models.
- **Dynamic Roadmaps**: Generates step-by-step career progression plans.
- **Neural Reasoning Agent**: Real-time AI coach that "thinks" through your career options.
- **Premium UI**: Modern glassmorphism interface with fluid animations.
- **Growth Analysis**: Visualization of salary expectations and market demand.

---

## 🛠️ Tech Stack
- **Frontend**: React.js, Lucide Icons, Vanilla CSS (Custom Design System).
- **Backend**: FastAPI (Python), MySQL.
- **Machine Learning**: Scikit-Learn, Pandas, SHAP (Explainable AI).
- **Large File Support**: Git LFS for ML Model weights.

---

## 📂 Repository Note: Excluded Files
For security and efficiency, some files are **not** included in this repository. Here is how to restore them:

1.  **`node_modules/`**:
    *   **Why excluded**: Thousands of library files that are bulky.
    *   **How to restore**: Run `npm install` inside the `frontend` folder.
2.  **`.env` File**:
    *   **Why excluded**: Contains sensitive database passwords.
    *   **How to restore**: Create a `.env` file in the `backend/` folder (see [Environment Variables](#-environment-variables) below).
3.  **Local Database (`.db`)**:
    *   **Why excluded**: Local test data is specific to the development machine.
    *   **How to restore**: Run the SQL scripts in `backend/view_data.sql` to initialize your MySQL database.

---

## 🚀 Installation & Setup

### 1. Prerequisites
- **Node.js**: (LTS version)
- **Python**: 3.8+
- **MySQL**: Installed and running.

### 2. Backend Configuration
Create a `.env` file in the `backend/` directory:
```env
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=career_guidance
```

Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

### 3. Frontend Configuration
```bash
cd frontend
npm install
```

---

## 🚦 How to Run

### Option A: Quick Start (Windows)
We provide two batch files for easy startup:
1.  **Run Backend**: Double-click `start_backend.bat`
2.  **Run Frontend**: Double-click `start_frontend.bat`

### Option B: Manual Start
**Backend:**
```bash
cd backend
python main.py
```

**Frontend:**
```bash
cd frontend
npm run dev
```

---

## 🔑 Access Credentials

| User Type | Username | Password |
| :--- | :--- | :--- |
| **Admin** | `Admin` | `123456` |
| **Student** | `Yash` | `123456` |

---

## 📊 Project Structure
- `backend/`: FastAPI server, ML prediction logic, and database handlers.
- `frontend/`: React components and premium CSS styles.
- `backend/weights/`: Pre-trained ML model files (handled via Git LFS).
- `generate_report.py`: Utility for generating career PDF reports.

---

## 🛡️ License
This project is for academic/viva purposes. All rights reserved.
