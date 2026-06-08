from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List
import pandas as pd
import joblib

app = FastAPI()

# Static files mount MUST come before routes
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Load model
model = joblib.load("app/model/placement_model.pkl")


# Recommendation Engine
def generate_recommendations(
    cgpa: float,
    backlogs: int,
    coding_skills: int,
    aptitude_score: int,
    communication_skills: int,
    internships: int,
    projects_count: int,
    certifications: int,
    hackathons: int,
) -> List[str]:
    recs = []

    if cgpa < 7.0:
        recs.append("Improve your CGPA - aim for 7.5+ to stay competitive")
    elif cgpa < 8.0:
        recs.append("Good CGPA! Push above 8.0 for premium company shortlists")

    if backlogs > 0:
        recs.append(f"Clear your {backlogs} active backlog(s) - most companies filter on this")

    if coding_skills < 50:
        recs.append("Practice DSA daily on LeetCode / HackerRank to boost coding skills")
    elif coding_skills < 70:
        recs.append("Level up coding skills - solve medium/hard DSA problems consistently")

    if aptitude_score < 50:
        recs.append("Work on aptitude - practice quant, logical reasoning, and verbal ability")
    elif aptitude_score < 70:
        recs.append("Improve aptitude score - target 70+ for written test shortlists")

    if communication_skills < 50:
        recs.append("Build communication skills - join a debate club or practice mock GDs/PIs")
    elif communication_skills < 70:
        recs.append("Sharpen communication - work on structured answers using STAR method")

    if internships == 0:
        recs.append("Gain at least one internship - it significantly boosts placement chances")
    elif internships == 1:
        recs.append("One more internship or a strong project can differentiate your profile")

    if projects_count < 2:
        recs.append("Build 2-3 strong end-to-end projects and host them on GitHub")
    elif projects_count < 4:
        recs.append("Add one more impactful project - preferably with a live demo or deployment")

    if certifications == 0:
        recs.append("Earn certifications in your domain (AWS, Google, Coursera, etc.)")
    elif certifications < 3:
        recs.append("Add 1-2 more relevant certifications to strengthen your resume")

    if hackathons == 0:
        recs.append("Participate in hackathons - they build problem-solving skills and visibility")
    elif hackathons < 2:
        recs.append("Try one more hackathon - winning or completing strengthens your profile")

    if not recs:
        recs.append("Excellent profile! Keep it updated and apply to your dream companies")
        recs.append("Prepare for system design interviews for senior roles")
        recs.append("Consider open-source contributions to stand out further")

    return recs


# GET /
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request":         request,
            "result":          None,
            "probability":     0,
            "summary":         {},
            "recommendations": [],
        },
    )


# POST /predict
@app.post("/predict")
def predict(
    request: Request,
    cgpa: float = Form(...),
    backlogs: int = Form(...),
    coding_skills: int = Form(...),       # UI sends 0-100
    aptitude_score: int = Form(...),      # UI sends 0-100
    communication_skills: int = Form(...), # UI sends 0-100
    internships: int = Form(...),
    projects_count: int = Form(...),
    certifications: int = Form(...),
    hackathons: int = Form(...),
):
    # Convert slider values from UI scale (0-100) to model scale (1-10)
    # Model was trained on 1-10 scale — sending 0-100 gives garbage predictions
    coding_skills_scaled        = round(coding_skills        / 10, 1)
    aptitude_score_scaled       = round(aptitude_score       / 10, 1)
    communication_skills_scaled = round(communication_skills / 10, 1)

    # Build DataFrame with model-expected column names and scale
    data = pd.DataFrame(
        [[
            cgpa,
            backlogs,
            coding_skills_scaled,
            aptitude_score_scaled,
            communication_skills_scaled,
            internships,
            projects_count,
            certifications,
            hackathons,
        ]],
        columns=[
            "cgpa",
            "backlogs",
            "coding_skills",
            "aptitude_score",
            "communication_skills",
            "internships",
            "projects",
            "certifications",
            "hackathons",
        ],
    )

    # Predict
    prediction  = model.predict(data)[0]
    probability = model.predict_proba(data)[0][1]

    result = "Placed" if prediction == 1 else "Not Placed"

    # Summary for profile card — show original 0-100 values to user
    summary = {
        "cgpa":                 cgpa,
        "backlogs":             backlogs,
        "coding_skills":        coding_skills,
        "aptitude_score":       aptitude_score,
        "communication_skills": communication_skills,
        "internships":          internships,
        "projects":             projects_count,
        "certifications":       certifications,
        "hackathons":           hackathons,
    }

    recommendations = generate_recommendations(
        cgpa=cgpa,
        backlogs=backlogs,
        coding_skills=coding_skills,
        aptitude_score=aptitude_score,
        communication_skills=communication_skills,
        internships=internships,
        projects_count=projects_count,
        certifications=certifications,
        hackathons=hackathons,
    )

    return templates.TemplateResponse(
        "index.html",
        {
            "request":         request,
            "result":          result,
            "probability":     round(probability * 100),
            "summary":         summary,
            "recommendations": recommendations,
        },
    )