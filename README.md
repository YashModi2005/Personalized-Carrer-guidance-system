# 🚀 AI CareerPilot: Your Intelligent Career Counselor

Welcome to **AI CareerPilot**! This is a smart web application designed to help students find their perfect career path. Instead of guessing what you should do next, our AI analyzes your skills and tells you exactly which job fits you best.

---

## 🌟 What does this project do? (In Simple Terms)

Imagine you have a personal mentor who knows every job in the IT industry. You tell this mentor your grades, what programming languages you know, and what you are interested in. The mentor then says: *"Based on your skills, you would be an amazing Data Scientist! Here is your roadmap to get there."*

**That is exactly what this app does!**

### Main Features:
1.  **Smart Career Prediction**: Take a simple test, and our AI (trained on thousands of records) predicts your top 3 career matches.
2.  **AI Coach (The "Brain")**: A chat system that doesn't just give answers, but "thinks" out loud to help you understand your options.
3.  **Beautiful Dashboard**: A clean, modern place to see your results, salary trends, and roadmaps.
4.  **Step-by-Step Roadmaps**: Not just a job title, but a full plan on what to learn next.

---

## 🛠️ The "Engine" (How it's built)

We used the best modern tools to build this:
*   **The Face (Frontend)**: **React.js** – This makes the website fast, smooth, and beautiful.
*   **The Brain (Backend)**: **FastAPI (Python)** – This is the high-speed engine that handles all the logic.
*   **The Memory (Database)**: **MySQL** – This is where we safely store your profile and scores.
*   **The Intelligence (AI)**: **Scikit-Learn** – This is the math part that "learns" from data to make predictions.

---

## 📂 Missing Something? (The "Invisible" Files)

When you download this from GitHub, some files might be "missing." Don't worry! We do this to keep the project light and secure.

1.  **The "Libraries" (`node_modules`)**: These are like the tools in a toolbox. We don't carry the toolbox, we just give you the list. You get them back by running one simple command: `npm install`.
2.  **The "Secrets" (`.env`)**: This is where you put your database password. We don't share ours for security, so you just create your own!
3.  **The "Heavy Models" (`.pkl`)**: These are the actual AI brains. They are very large, so we use a special system called **Git LFS** to store them.

---

## 🚀 How to Set It Up on Your Computer

Think of this as a two-step process: setting up the **Backend (Brain)** and the **Frontend (Face)**.

### Step 1: The Backend (The Brain)
1.  Go into the `backend` folder.
2.  Create a file named `.env` and put your database details inside (Host, User, Password).
3.  Install the Python tools:
    ```bash
    pip install -r requirements.txt
    ```
4.  Start the server:
    ```bash
    python main.py
    ```

### Step 2: The Frontend (The Face)
1.  Go into the `frontend` folder.
2.  Install the tools:
    ```bash
    npm install
    ```
3.  Start the website:
    ```bash
    npm run dev
    ```

---

## 🕹️ How to Use the App

1.  **Login**: Use `Yash` (Password: `123456`) or create a new account.
2.  **Take the Assessment**: Answer questions about your skills (Python, SQL, Communication, etc.).
3.  **Get Results**: See your top career matches immediately.
4.  **Chat with AI**: Ask the AI coach, *"How can I improve my SQL skills?"* or *"What is the salary of a Web Developer?"*

---

## 📊 How the AI "Thinks"

Our AI looks at over 25 different things about you, including:
*   How good you are at coding.
*   If you like talking to people or working alone.
*   Your college grades.
*   Your interests (like Web Design or Hacking).

It then compares you to thousands of other successful professionals to find your best match.

---

## 🔑 Login Details (For Testing)

| Role | Username | Password |
| :--- | :--- | :--- |
| **Admin** | `Admin` | `123456` |
| **Student** | `Yash` | `123456` |

---

## 👨‍💻 Author
**Yash Modi**
*Final Year Project - Dedicated to helping students navigate their future.*

---
*If you like this project, feel free to ⭐ it on GitHub!*
