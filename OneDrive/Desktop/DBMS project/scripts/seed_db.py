import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal, engine, Base
from backend.models import User, Venue, Event
from backend.utils.auth import get_password_hash

def seed_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Create Admin
    admin_email = "admin@example.com"
    if not db.query(User).filter(User.email == admin_email).first():
        admin = User(
            username="Admin User",
            email=admin_email,
            password_hash=get_password_hash("password"),
            role="Admin"
        )
        db.add(admin)

    # Create Student
    student_email = "student@example.com"
    if not db.query(User).filter(User.email == student_email).first():
        student = User(
            username="Student User",
            email=student_email,
            password_hash=get_password_hash("password"),
            role="Attendee"
        )
        db.add(student)
        
    db.commit()
    print("Database seeded with Admin and Student.")
    db.close()

if __name__ == "__main__":
    seed_data()
