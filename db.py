from sqlalchemy import Boolean, DateTime, Float, create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Database setup
DATABASE_URL = "postgresql://user:password@localhost/dbname"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# might want a seperate table for student and for admin
class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    admin = Column(Boolean)
    name = Column(String)

class Student(Base):
    __tablename__ = "students"
    will_sign_contract = Column(Boolean)
    id = Column(String, ForeignKey("users.id"), primary_key=True, index=True)
    preferences = relationship("Preference", back_populates="student")
    assignments = relationship("Assignment", back_populates="student")

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    requires_contract = Column(Boolean)
    client_id = Column(Integer, ForeignKey("clients.id"))
    preferences = relationship("Preference", back_populates="project")

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    min_projects = Column(Integer)
    max_projects = Column(Integer)
    projects = relationship("Project"

class Preference(Base):
    __tablename__ = "preferences"
    id = Column(Integer, primary_key=True, index=True)
    strength = Column(Float)
    student_id = Column(String, ForeignKey("students.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    student = relationship("Student", back_populates="preferences")
    project = relationship("Project", back_populates="preferences")

class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, ForeignKey("students.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    solve_run_id = Column(Integer, ForeignKey("solveruns.id"), nullable=True)
    solve_run = relationship("SolveRun", back_populates="assignments")
    student = relationship("Student", back_populates="assignments")
    project = relationship("Project")
)

class SolveRun(Base):
    __tablename__ = "solveruns"
    id = Column(Integer, primary_key=True, index=True)
    assignments = relationship("Assignment", backref="solve_run")
    timestamp = Column(DateTime)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    