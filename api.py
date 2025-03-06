
from fastapi import Depends, FastAPI, Request
from sqlalchemy.orm import Session
from db import Preference, User, get_db


def add_crud_api(app: FastAPI):
    @app.get("/health")
    async def health(request: Request):
        return {"status": "yeah yeah"}

    @app.post("/api/submit-preferences")
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
    
    @app.post("/api/solve")
    async def solve(request: Request, db: Session = Depends(get_db)):
        user = request.session.get("user")
        if not user:
            return {"error": "Not authenticated"}
        
        user_id = user.get("sub")
        student = db.query(User).filter(User.user_id == user_id).first()

        
        db.commit()
        return {"message": "Preferences saved successfully"}

