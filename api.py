from fastapi import APIRouter, Depends, FastAPI, Request
from sqlalchemy.orm import Session
from db import Preference, User, get_db

router = APIRouter()

@router.get("/status")
async def status(request: Request):
    return {"status": "yeah yeah"}

@router.post("/submit-preferences")
async def save_preferences(request: Request, preferences: dict, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user:
        return {"error": "Not authenticated"}
    
    user_id = user.get("sub")
    student = db.query(User).filter(User.user_id == user_id).first()
    if not student:
        student = User(user_id=user_id)
        db.add(student)
        db.commit()
        db.refresh(student)
    
    for project_id in preferences.get("project_ids", []):
        preference = Preference(student_id=student.id, project_id=project_id)
        db.add(preference)
    
    db.commit()
    return {"message": "Preferences saved successfully"}

@router.post("/submit-preferences")
async def save_preferences(request: Request, preferences: dict, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user:
        return {"error": "Not authenticated"}
    
    user_id = user.get("sub")
    student = db.query(User).filter(User.user_id == user_id).first()
    if not student:
        student = User(user_id=user_id)
        db.add(student)
        db.commit()
        db.refresh(student)
    
    for project_id in preferences.get("project_ids", []):
        preference = Preference(student_id=student.id, project_id=project_id)
        db.add(preference)
    
    db.commit()
    return {"message": "Preferences saved successfully"}

@router.post("/solve")
async def solve(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user:
        return {"error": "Not authenticated"}
    
    user_id = user.get("sub")
    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None or not user.is_admin:
        return {"error": "Not authorized"}

    db.query(User)



@router.post("/solve")
async def solve(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user:
        return {"error": "Not authenticated"}
    
    user_id = user.get("sub")
    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None or not user.is_admin:
        return {"error": "Not authorized"}

    # TODO: run the solver
    return {"message": "running"}    

