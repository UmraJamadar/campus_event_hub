from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import bcrypt
import jwt
from datetime import datetime, timedelta
from typing import Optional
from database import Database

load_dotenv()

app = FastAPI(
    title="Campus Event Hub API",
    description="Backend API for Campus Event Hub",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24
ADMIN_EMAIL = "umra@jain.com"

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    college: str
    year: int
    branch: str
    role: str = "student"

class AdminRegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    admin_code: str

class LoginRequest(BaseModel):
    email: str
    password: str

class CreateEventRequest(BaseModel):
    name: str
    description: str
    category: str
    college: str
    date: str
    time: str
    location: str
    venue:Optional[str] = None
    seats: int
    organizer_email: str

class OrganizerApplicationRequest(BaseModel):
    institute_name: str
    city: str
    type_: str
    contact_email: str
    reason: str

class ApproveEventRequest(BaseModel):
    event_id: str
    action: str

class ApproveOrganizerRequest(BaseModel):
    college_id: str
    action: str

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def create_jwt_token(email: str, role: str) -> str:
    payload = {
        "email": email,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/")
def read_root():
    return {"message": "Welcome to Campus Event Hub API!", "status": "Server is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Campus Event Hub API"}

@app.get("/api/test")
def test_endpoint():
    return {
        "message": "Frontend and Backend are connected!",
        "api_version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/demo/load-data")
def load_demo_data():
    try:
        admin = Database.get_user_by_email(ADMIN_EMAIL)
        if not admin:
            hashed_password = hash_password("admin@123")
            admin = Database.create_user(
                name="Admin User",
                email=ADMIN_EMAIL,
                password_hash=hashed_password,
                college="Admin",
                year=0,
                branch="Admin",
                role="admin"
            )
        
        demo_student = Database.get_user_by_email("demo@student.com")
        if not demo_student:
            hashed_password = hash_password("demo@123")
            demo_student = Database.create_user(
                name="Demo Student",
                email="demo@student.com",
                password_hash=hashed_password,
                college="MIT",
                year=2,
                branch="CSE",
                role="student"
            )
        
        demo_events = [
            {"title": "AI Workshop", "description": "Learn AI basics and machine learning fundamentals", "category": "Tech", "date": "2025-02-15", "time": "10:00", "venue": "Auditorium A", "max_participants": 100},
            {"title": "Web Dev Bootcamp", "description": "Full stack development with React and Node.js", "category": "Tech", "date": "2025-02-20", "time": "14:00", "venue": "Lab 1", "max_participants": 50},
            {"title": "Sports Day", "description": "Annual sports event with cricket, badminton, and athletics", "category": "Sports", "date": "2025-02-25", "time": "09:00", "venue": "Ground", "max_participants": 200},
            {"title": "Hackathon 2025", "description": "24-hour coding challenge with prizes worth 50k", "category": "Hackathon", "date": "2025-03-01", "time": "08:00", "venue": "Tech Hub", "max_participants": 150},
            {"title": "Cultural Fest", "description": "Music and dance performances by student groups", "category": "Cultural", "date": "2025-03-05", "time": "18:00", "venue": "Main Hall", "max_participants": 300},
            {"title": "Python Workshop", "description": "Advanced Python programming techniques and best practices", "category": "Workshop", "date": "2025-02-18", "time": "15:00", "venue": "Lab 2", "max_participants": 60},
            {"title": "Data Science Seminar", "description": "Industry experts discuss data science trends and applications", "category": "Seminar", "date": "2025-02-22", "time": "11:00", "venue": "Conference Room", "max_participants": 80},
            {"title": "Cloud Computing Workshop", "description": "AWS and Azure cloud services training and deployment", "category": "Workshop", "date": "2025-03-03", "time": "13:00", "venue": "Lab 3", "max_participants": 70},
        ]
        
        event_ids = []
        for event_data in demo_events:
            existing = Database.get_event_by_title(event_data["title"])
            if not existing:
                event = Database.create_event(
                    title=event_data["title"],
                    description=event_data["description"],
                    college_id=admin["id"],
                    category=event_data["category"],
                    date=event_data["date"],
                    time=event_data["time"],
                    venue=event_data["venue"],
                    max_participants=event_data["max_participants"],
                    status="approved"
                )
                if event:
                    event_ids.append(event["id"])
            else:
                event_ids.append(existing["id"])
        
        if demo_student and event_ids:
            for event_id in event_ids[:4]:
                if not Database.check_registration_exists(demo_student["id"], event_id):
                    Database.register_student_for_event(demo_student["id"], event_id)
        
        return {"status": "Demo data loaded successfully", "events_created": len(event_ids), "demo_student_email": "demo@student.com", "demo_password": "demo@123"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/api/auth/register")
def register_student(request: RegisterRequest):
    try:
        print(f"[REGISTER] Attempting to register: {request.email}")
        
        existing_user = Database.get_user_by_email(request.email)
        if existing_user:
            print(f"[REGISTER] Email already exists: {request.email}")
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_password = hash_password(request.password)
        
        user = Database.create_user(
            name=request.name,
            email=request.email,
            password_hash=hashed_password,
            college=request.college,
            year=request.year,
            branch=request.branch,
            role="student"
        )
        
        if not user:
            print(f"[REGISTER] Failed to create user in database")
            raise HTTPException(status_code=500, detail="Failed to create user in database")
        
        print(f"[REGISTER] User created successfully: {request.email}")
        
        token = create_jwt_token(request.email, "student")
        
        return {
            "status": "Registration successful",
            "message": f"Welcome {request.name}!",
            "token": token,
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "college": user["college"],
                "role": "student"
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"[REGISTER] Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Registration error: {str(e)}")

@app.post("/api/auth/admin-register")
def register_admin(request: AdminRegisterRequest):
    try:
        print(f"[ADMIN-REGISTER] Attempting admin registration: {request.email}")
        
        if request.email != ADMIN_EMAIL:
            print(f"[ADMIN-REGISTER] Invalid email: {request.email}")
            raise HTTPException(status_code=403, detail="Only authorized email can register as admin")
        
        ADMIN_CODE = os.getenv("ADMIN_CODE", "admin123")
        if request.admin_code != ADMIN_CODE:
            print(f"[ADMIN-REGISTER] Invalid admin code")
            raise HTTPException(status_code=403, detail="Invalid admin code")
        
        existing_user = Database.get_user_by_email(request.email)
        if existing_user:
            print(f"[ADMIN-REGISTER] Admin already exists")
            raise HTTPException(status_code=400, detail="Admin already registered")
        
        hashed_password = hash_password(request.password)
        
        user = Database.create_user(
            name=request.name,
            email=request.email,
            password_hash=hashed_password,
            college="Admin",
            year=0,
            branch="Admin",
            role="admin"
        )
        
        if not user:
            print(f"[ADMIN-REGISTER] Failed to create admin in database")
            raise HTTPException(status_code=500, detail="Failed to create admin")
        
        print(f"[ADMIN-REGISTER] Admin created successfully: {request.email}")
        
        token = create_jwt_token(request.email, "admin")
        
        return {
            "status": "Admin registration successful",
            "message": f"Welcome Admin {request.name}!",
            "token": token,
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "role": "admin"
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ADMIN-REGISTER] Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Admin registration error: {str(e)}")

@app.post("/api/auth/login")
def login_user(request: LoginRequest):
    try:
        print(f"[LOGIN] Attempting login: {request.email}")
        
        user = Database.get_user_by_email(request.email)
        if not user:
            print(f"[LOGIN] User not found: {request.email}")
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        if not verify_password(request.password, user["password_hash"]):
            print(f"[LOGIN] Invalid password for: {request.email}")
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        print(f"[LOGIN] Login successful: {request.email}")
        
        token = create_jwt_token(request.email, user["role"])
        
        return {
            "status": "Login successful",
            "message": f"Welcome back {user['name']}!",
            "token": token,
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "college": user["college"],
                "role": user["role"]
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"[LOGIN] Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Login error: {str(e)}")

@app.get("/api/auth/profile/{email}")
def get_user_profile(email: str):
    user = Database.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "status": "Profile found",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "college": user["college"],
            "year": user["year"],
            "branch": user["branch"],
            "role": user["role"],
            "coins": user["coins"],
            "badge": user["badge"],
            "created_at": user["created_at"]
        }
    }

@app.post("/api/organizer/apply")
def apply_as_organizer(request: OrganizerApplicationRequest):
    try:
        college = Database.create_college(
            name=request.institute_name,
            city=request.city,
            type_=request.type_,
            contact_email=request.contact_email,
            status="pending"
        )
        
        if not college:
            raise HTTPException(status_code=500, detail="Failed to submit application")
        
        return {
            "status": "Application submitted",
            "message": f"Your application for {request.institute_name} has been submitted.",
            "application_id": college["id"],
            "application": {
                "id": college["id"],
                "name": college["name"],
                "city": college["city"],
                "type": college["type"],
                "status": college["status"],
                "created_at": college["created_at"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/admin/organizer-applications")
def get_organizer_applications():
    try:
        applications = Database.get_pending_colleges()
        return {
            "status": "Applications retrieved",
            "total": len(applications),
            "applications": applications
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/api/admin/approve-organizer")
def approve_organizer(request: ApproveOrganizerRequest):
    try:
        if request.action not in ["approve", "reject"]:
            raise HTTPException(status_code=400, detail="Action must be 'approve' or 'reject'")
        
        status = "approved" if request.action == "approve" else "rejected"
        
        college = Database.update_college_status(request.college_id, status)
        
        if not college:
            raise HTTPException(status_code=404, detail="College not found")
        
        action_text = "approved" if request.action == "approve" else "rejected"
        
        return {
            "status": f"Application {action_text}",
            "message": f"Organizer application has been {action_text}",
            "college": college
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/api/events/create")
def create_event(request: CreateEventRequest):
    try:
        organizer = Database.get_user_by_email(request.organizer_email)
        if not organizer:
            raise HTTPException(status_code=404, detail="Organizer not found")
        
        if organizer["role"] == "admin":
            event_status = "approved"
        else:
            event_status = "pending"
        
        event = Database.create_event(
            title=request.name,
            description=request.description,
            college_id=None,
            category=request.category,
            date=request.date,
            time=request.time,
            venue=request.location,
            max_participants=request.seats,
            status=event_status
        )
        
        if not event:
            raise HTTPException(status_code=500, detail="Failed to create event")
        
        return {
            "status": "Event created successfully",
            "message": f"Event created and status is {event_status}",
            "event_id": event["id"],
            "event": event
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/events")
def get_all_events(category: str = "All", college: str = "All", search: str = ""):
    try:
        events = Database.get_all_events(status="approved")
        
        if category != "All":
            events = [e for e in events if e.get("category") == category]
        
        if search:
            events = [e for e in events if search.lower() in e.get("title", "").lower()]
        
        return {
            "status": "Events retrieved",
            "total": len(events),
            "events": events
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/events/{event_id}")
def get_event(event_id: str):
    try:
        event = Database.get_event_by_id(event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        return {
            "status": "Event found",
            "event": event
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/api/events/register")
def register_for_event(student_email: str, event_id: str):
    try:
        student = Database.get_user_by_email(student_email)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        event = Database.get_event_by_id(event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        if Database.check_registration_exists(student["id"], event_id):
            raise HTTPException(status_code=400, detail="Already registered for this event")
        
        registration = Database.register_student_for_event(student["id"], event_id)
        
        if not registration:
            raise HTTPException(status_code=500, detail="Failed to register")
        
        return {
            "status": "Successfully registered",
            "message": f"You are registered for {event['title']}",
            "event": {
                "id": event["id"],
                "name": event["title"],
                "date": event["date"],
                "time": event["time"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/events/user/{student_email}")
def get_user_events(student_email: str):
    try:
        student = Database.get_user_by_email(student_email)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        registrations = Database.get_student_registrations(student["id"])
        
        user_events = []
        for reg in registrations:
            event = Database.get_event_by_id(reg["event_id"])
            if event:
                user_events.append(event)
        
        return {
            "status": "User events retrieved",
            "total": len(user_events),
            "events": user_events
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/api/events/bookmark")
def bookmark_event(student_id: int, event_id: str):
    try:
        student = Database.get_user_by_id(student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        event = Database.get_event_by_id(event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        bookmark = Database.bookmark_event(student_id, event_id)
        
        if not bookmark:
            raise HTTPException(status_code=400, detail="Already bookmarked")
        
        return {
            "status": "Event bookmarked",
            "message": f"Event bookmarked successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/events/bookmarks/{student_email}")
def get_user_bookmarks(student_email: str):
    try:
        student = Database.get_user_by_email(student_email)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        bookmarks = Database.get_student_bookmarks(student["id"])
        
        bookmarked_events = []
        for bookmark in bookmarks:
            event = Database.get_event_by_id(bookmark["event_id"])
            if event:
                bookmarked_events.append(event)
        
        return {
            "status": "Bookmarks retrieved",
            "total": len(bookmarked_events),
            "events": bookmarked_events
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/admin/pending-events")
def get_pending_events():
    try:
        events = Database.get_pending_events()
        return {
            "status": "Pending events retrieved",
            "total": len(events),
            "events": events
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/api/admin/approve-event")
def approve_event(request: ApproveEventRequest):
    try:
        if request.action not in ["approve", "reject"]:
            raise HTTPException(status_code=400, detail="Action must be 'approve' or 'reject'")
        
        status = "approved" if request.action == "approve" else "rejected"
        
        event = Database.update_event_status(request.event_id, status)
        
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        action_text = "approved" if request.action == "approve" else "rejected"
        
        return {
            "status": f"Event {action_text}",
            "message": f"Event has been {action_text}",
            "event": event
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/admin/analytics/overview")
def get_analytics_overview():
    try:
        stats = Database.get_platform_stats()
        user_stats = Database.get_user_stats()
        
        return {
            "status": "success",
            "data": {
                **stats,
                **user_stats
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/admin/analytics/events")
def get_events_analytics():
    try:
        by_category = Database.get_events_by_category()
        top_events = Database.get_top_events()
        
        return {
            "status": "success",
            "data": {
                "by_category": by_category,
                "top_events": top_events
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/admin/analytics/registrations")
def get_registrations_analytics():
    try:
        events = Database.get_all_events(status="approved")
        
        event_registrations = {}
        for event in events:
            count = Database.get_event_registrations_count(event["id"])
            event_registrations[event["title"]] = count
        
        return {
            "status": "success",
            "data": {
                "event_registrations": event_registrations,
                "total_registrations": sum(event_registrations.values())
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("FASTAPI_PORT", 8000))
    print(f"Starting FastAPI server on http://localhost:{port}")
    print(f"API Docs available at http://localhost:{port}/docs")
    print(f"Admin Email: {ADMIN_EMAIL}")
    uvicorn.run(app, host="0.0.0.0", port=port)
