from fastapi import FastAPI, Depends, Request
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session

from db import Preference, Student, get_db


app = FastAPI()

# Load environment variables
config = Config()
SECRET_KEY = "your-secret-key"  # Change this to a secure random key
CLIENT_ID = "your-microsoft-client-id"
CLIENT_SECRET = "your-microsoft-client-secret"
REDIRECT_URI = "http://localhost:8000/auth/callback"

oauth = OAuth(config)
oauth.register(
    name="microsoft",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    authorize_url="https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
    authorize_params={"scope": "openid profile email"},
    access_token_url="https://login.microsoftonline.com/common/oauth2/v2.0/token",
    access_token_params=None,
    client_kwargs={"scope": "openid profile email"},
)

# Middleware for session management
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

@app.get("/auth/login")
async def login(request: Request):
    redirect_uri = REDIRECT_URI
    return await oauth.microsoft.authorize_redirect(request, redirect_uri)

@app.get("/auth/callback")
async def auth_callback(request: Request):
    token = await oauth.microsoft.authorize_access_token(request)
    user = await oauth.microsoft.parse_id_token(request, token)
    request.session["user"] = user
    return {"message": "Authentication successful", "user": user}

@app.get("/auth/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(url="/")

@app.get("/auth/user")
async def get_user(request: Request):
    user = request.session.get("user")
    if not user:
        return {"error": "Not authenticated"}
    return user

@app.post("/student/preferences")
async def save_preferences(request: Request, preferences: dict, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user:
        return {"error": "Not authenticated"}
    
    user_id = user.get("sub")
    student = db.query(Student).filter(Student.user_id == user_id).first()
    if not student:
        student = Student(user_id=user_id)
        db.add(student)
        db.commit()
        db.refresh(student)
    
    for project_id in preferences.get("project_ids", []):
        preference = Preference(student_id=student.id, project_id=project_id)
        db.add(preference)
    
    db.commit()
    return {"message": "Preferences saved successfully"}
