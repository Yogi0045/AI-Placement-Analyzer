# 🚀 AI Placement Analyzer

An AI-powered Placement Prediction System that predicts a student's placement probability using Machine Learning and provides personalized recommendations for improvement.

---

## 📌 Project Overview

AI Placement Analyzer helps students evaluate their placement readiness based on academic performance, technical skills, communication ability, internships, projects, certifications, and hackathon participation.

The application uses a trained XGBoost Machine Learning model deployed through FastAPI and integrated with a modern responsive web interface.

---

## ✨ Features

- Placement Probability Prediction
- Real-time Student Profile Analysis
- Personalized Recommendations
- Modern Responsive UI
- FastAPI Backend
- Machine Learning Powered Insights
- Interactive Placement Readiness Assessment

---

## 🧠 Machine Learning Features

The model evaluates students using:

- CGPA
- Backlogs
- Coding Skills
- Aptitude Score
- Communication Skills
- Internships
- Projects
- Certifications
- Hackathons

---

## 🛠️ Technologies Used

### Machine Learning

- Python
- Pandas
- NumPy
- Scikit-Learn
- XGBoost
- Joblib

### Backend

- FastAPI
- Uvicorn
- Jinja2 Templates

### Frontend

- HTML5
- CSS3

### Development Tools

- Git
- GitHub
- VS Code

---

## 🏗️ Project Architecture

Student Input
↓
HTML Form
↓
FastAPI Backend
↓
XGBoost Model
↓
Prediction & Probability
↓
Recommendations
↓
Result Dashboard

---

## 📊 Model Output

The system predicts:

- Placement Status
  - Likely to be Placed
  - Placement Risk Detected

- Placement Probability (%)

- Improvement Recommendations

---

## 📁 Project Structure

```text
AI-Placement-Analyzer/

├── app/
│   ├── main.py
│   ├── model/
│   │   └── placement_model.pkl
│   ├── templates/
│   │   └── index.html
│   └── static/
│       └── style.css
│
├── requirements.txt
├── README.md
└── .gitignore
