# How to Run the AI Career Pilot

Follow these steps to get your high-accuracy career guidance system up and running.

## 1. Prerequisites
Ensure you have the following installed:
- **Node.js**: For the React frontend.
- **Python 3.8+**: For the FastAPI backend.
- **No API key needed** — the system runs fully locally using scikit-learn ML.

## 2. Start the Backend (FastAPI)
Open a terminal and run:
```powershell
cd "backend"
# Optional: Create and activate a virtual environment
# python -m venv venv
# .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```
The backend will be running at `http://localhost:8000`.

## 3. Start the Frontend (React)
Open a **new** terminal and run:
```powershell
cd "frontend"
npm install
npm run dev
```
The frontend will be available at `http://localhost:5173`.

## 4. Usage
1. Open the frontend URL in your browser.
2. Click **"Begin Career Assessment"**.
3. Fill in your details (Technical skills like `Python, SQL`, Soft skills like `Leadership`).
4. Click **"Generate Career Roadmap"** and wait for the AI to analyze your profile.
