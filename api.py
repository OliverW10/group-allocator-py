import datetime
from fastapi import APIRouter, Depends, FastAPI, Request
from sqlalchemy.orm import Session
from db import Assignment, Client, Preference, SolveRun, Student, User, get_db
import csv
from io import StringIO
from fastapi import UploadFile, File
from db import Project
from solver import assign_students_to_projects

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
    # Get preferences and will_sign_contract from request body
    preferences_data = preferences.get("preferences", [])
    will_sign_contract = preferences.get("will_sign_contract", False)

    # Validate preference strengths
    for pref in preferences_data:
        if pref["strength"] > 1:
            return {"error": "Preference strength cannot be greater than 1"}

    # Create user record if it doesn't exist
    user_id = user.get("sub")
    user_record = db.query(User).filter(User.id == user_id).first()
    if not user_record:
        user_record = User(id=user_id, admin=False, name=user.get("name"))
        db.add(user_record)
        db.commit()

    # Get or create student record
    student = db.query(Student).filter(Student.id == user_id).first()
    if not student:
        student = Student(id=user_id, will_sign_contract=will_sign_contract)
        db.add(student)
        db.commit()
        db.refresh(student)
    else:
        student.will_sign_contract = will_sign_contract
        db.commit()

    # Delete existing preferences for this student
    db.query(Preference).filter(Preference.student_id == user_id).delete()
    # Check if student has existing preferences and delete them
    existing_preferences = db.query(Preference).filter(Preference.student_id == user_id).all()
    if existing_preferences:
        db.query(Preference).filter(Preference.student_id == user_id).delete()
        db.commit()

    # Add new preferences
    for pref in preferences_data:
        preference = Preference(
            student_id=user_id,
            project_id=pref["project_id"],
            strength=pref["strength"]
        )
        db.add(preference)
    
    db.commit()
    return {"message": "Preferences saved successfully"}

@router.get("/preferences")
async def get_preferences(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user:
        return {"error": "Not authenticated"}

    user_id = user.get("sub")
    
    # Get preferences for current user joined with projects and clients
    preferences = db.query(
        Preference,
        Project,
        Client.name.label('client_name')
    ).join(Student)\
     .join(Project)\
     .join(Client)\
     .filter(Student.id == user_id)\
     .all()

    # Format response 
    preference_list = []
    for pref, project, client_name in preferences:
        preference_list.append({
            "id": pref.id,
            "project_id": project.id,
            "project_name": project.name,
            "client_name": client_name,
            "strength": pref.strength
        })

    return preference_list

@router.get("/all-preferences")
async def get_all_preferences(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user:
        return {"error": "Not authenticated"}

    user_id = user.get("sub")
    user_record = db.query(User).filter(User.id == user_id).first()
    if not user_record or not user_record.admin:
        return {"error": "Not authorized"}

    # Get all preferences joined with students, projects and clients
    preferences = db.query(
        Preference,
        Student,
        Project,
        Client.name.label('client_name')
    ).join(Student)\
     .join(Project)\
     .join(Client)\
     .all()
    # Group preferences by student
    students_dict = {}
    for pref, student, project, client_name in preferences:
        if student.id not in students_dict:
            students_dict[student.id] = {
                "id": student.id,
                "will_sign_contract": student.will_sign_contract,
                "preferences": []
            }
        
        # Add this preference to the student's preferences list
        students_dict[student.id]["preferences"].append({
            "id": pref.id,
            "project_id": project.id,
            "strength": pref.strength,
            "project": {
                "id": project.id,
                "name": project.name,
                "client_name": client_name,
                "requires_contract": project.requires_contract
            }
        })
    
    # Convert dictionary to list for the response
    students_list = list(students_dict.values())

    return students_list


@router.post("/solve")
async def solve(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user:
        return {"error": "Not authenticated"}
    
    user_id = user.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.admin:
        return {"error": "Not authorized"}

    # Get all required data from database
    students = [s.id for s in db.query(Student).all()]
    projects = [p.id for p in db.query(Project).all()]
    
    # Get student preferences
    preferences = db.query(Student, Preference, Project)\
        .join(Preference)\
        .join(Project)\
        .order_by(Student.id, Preference.strength.desc())\
        .all()
    
    # Build preferences dictionary
    student_preferences = {}
    for student, pref, project in preferences:
        if student.id not in student_preferences:
            student_preferences[student.id] = []
        student_preferences[student.id].append(str(project.id))
    
    # Get contract information
    contract_willing_students = [
        s.id for s in db.query(Student).filter(Student.will_sign_contract == True).all()
    ]
    contract_required_projects = [
        str(p.id) for p in db.query(Project).filter(Project.requires_contract == True).all()
    ]
    
    # Get client projects
    clients = db.query(Client).all()
    client_projects = {
        str(client.id): [str(p.id) for p in client.projects]
        for client in clients
    }
    
    # Convert project IDs to strings for solver
    projects = [str(p) for p in projects]
    
    # Call solver
    assignments, score = assign_students_to_projects(
        students=students,
        projects=projects,
        student_preferences=student_preferences,
        contract_willing_students=contract_willing_students,
        contract_required_projects=contract_required_projects,
        client_projects=client_projects,
        pre_allocations={},  # Empty for now, could be added later
        min_group_size=3,
        max_group_size=4
    )
    
    if not assignments:
        return {"error": "No valid solution found"}
    
    try:
        # Create a solve run record
        solve_run = SolveRun(timestamp=datetime.datetime.now(tz=datetime.UTC))
        db.add(solve_run)
        
        # Create new assignments
        for project_id, student_list in assignments.items():
            for student_id in student_list:
                assignment = Assignment(
                    student_id=student_id,
                    project_id=int(project_id),  # Convert back to integer
                    solve_run_id=solve_run.id
                )
                db.add(assignment)
        
        
        db.commit()
        
        return {
            "message": "Successfully created new assignments",
            "score": score,
            "assignments": assignments
        }
        
    except Exception as e:
        db.rollback()
        return {"error": f"Failed to save assignments: {str(e)}"}

