from fastapi import APIRouter, Depends, FastAPI, Request
from sqlalchemy.orm import Session
from db import Client, Preference, User, get_db
import csv
from io import StringIO
from fastapi import UploadFile, File
from db import Project

router = APIRouter()

@router.get("/status")
async def status(request: Request):
    return {"status": "yeah yeah"}

@router.post("/upload-projects")
async def upload_projects(request: Request, file: UploadFile = File(...), db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user:
        return {"error": "Not authenticated"}
    
    # Read and decode the CSV file
    content = await file.read()
    csv_text = content.decode()
    csv_file = StringIO(csv_text)
    csv_reader = csv.reader(csv_file)
    
    # Skip header row
    next(csv_reader)
    
    projects_added = 0
    for row in csv_reader:
        if len(row) != 4:
            continue

        project_id, name, requires_contract, client_name = row

        client = db.query(Client).filter(Client.name == client_name).first()
        if client is None:
            client = Client(name=client_name, min_projects=0, max_projects=2)
            db.add(client)
            db.commit()
            db.refresh(client)
        client_id = client.id
        print("client_id", client_id)
        # Check if project already exists
        existing = db.query(Project).filter(Project.id == client_id).first()
        if existing:
            continue
            
        project = Project(
            id=int(project_id),
            name=name,
            requires_contract=bool(int(requires_contract)),
            client_id=client_id
        )
        print("project", project)
        db.add(project)
        projects_added += 1
    
    db.commit()
    return {"message": f"Successfully added {projects_added} projects"}

@router.get("/projects")
async def get_projects(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user:
        return {"error": "Not authenticated"}
    
    # Query projects joined with clients
    projects = db.query(Project, Client.name.label('client_name'))\
        .join(Client)\
        .all()
    
    # Format response
    project_list = []
    for project, client_name in projects:
        project_list.append({
            "id": project.id,
            "name": project.name,
            "requires_contract": project.requires_contract,
            "client_name": client_name
        })
    
    return project_list


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

