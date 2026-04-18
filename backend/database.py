import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Get Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

print("[OK] Supabase connection configured!")

# ============================================
# DATABASE HELPER FUNCTIONS
# ============================================

class Database:
    """Database operations for Campus Event Hub"""
    
    # ============================================
    # USER OPERATIONS
    # ============================================
    
    @staticmethod
    def create_user(name: str, email: str, password_hash: str, college: str, year: int, branch: str, role: str):
        """Create a new user"""
        try:
            response = supabase.table("users").insert({
                "name": name,
                "email": email,
                "password_hash": password_hash,
                "college": college,
                "year": year,
                "branch": branch,
                "role": role,
                "coins": 0,
                "badge": None,
                "created_at": datetime.utcnow().isoformat()
            }).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    @staticmethod
    def get_user_by_email(email: str):
        """Get user by email"""
        try:
            response = supabase.table("users").select("*").eq("email", email).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    @staticmethod
    def get_user_by_id(user_id: int):
        """Get user by ID"""
        try:
            response = supabase.table("users").select("*").eq("id", user_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    # ============================================
    # EVENT OPERATIONS
    # ============================================
    
    @staticmethod
    def create_event(title: str, description: str, college_id: int, category: str, date: str, time: str, venue: str, max_participants: int, status: str = "pending"):
        """Create a new event"""
        try:
            response = supabase.table("events").insert({
                "title": title,
                "description": description,
                "college_id": college_id,
                "category": category,
                "date": date,
                "time": time,
                "venue": venue,
                "max_participants": max_participants,
                "status": status,
                "created_at": datetime.utcnow().isoformat()
            }).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating event: {e}")
            return None
    
    @staticmethod
    def get_all_events(status: str = "approved"):
        """Get all events with optional status filter"""
        try:
            response = supabase.table("events").select("*").eq("status", status).execute()
            return response.data
        except Exception as e:
            print(f"Error getting events: {e}")
            return []
    
    @staticmethod
    def get_event_by_id(event_id: int):
        """Get event by ID"""
        try:
            response = supabase.table("events").select("*").eq("id", event_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting event: {e}")
            return None
    
    @staticmethod
    def get_event_by_title(title: str):
        """Get event by title"""
        try:
            response = supabase.table("events").select("*").eq("title", title).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting event: {e}")
            return None
    
    @staticmethod
    def update_event_status(event_id: int, status: str):
        """Update event status (pending, approved, rejected)"""
        try:
            response = supabase.table("events").update({"status": status}).eq("id", event_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error updating event: {e}")
            return None
    
    @staticmethod
    def get_pending_events():
        """Get all pending events for admin approval"""
        try:
            response = supabase.table("events").select("*").eq("status", "pending").execute()
            return response.data
        except Exception as e:
            print(f"Error getting pending events: {e}")
            return []
    
    # ============================================
    # REGISTRATION OPERATIONS
    # ============================================
    
    @staticmethod
    def register_student_for_event(student_id: int, event_id: int):
        """Register a student for an event"""
        try:
            response = supabase.table("registrations").insert({
                "student_id": student_id,
                "event_id": event_id,
                "status": "registered",
                "created_at": datetime.utcnow().isoformat()
            }).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error registering student: {e}")
            return None
    
    @staticmethod
    def get_student_registrations(student_id: int):
        """Get all events a student is registered for"""
        try:
            response = supabase.table("registrations").select("*").eq("student_id", student_id).execute()
            return response.data
        except Exception as e:
            print(f"Error getting registrations: {e}")
            return []
    
    @staticmethod
    def check_registration_exists(student_id: int, event_id: int):
        """Check if student is already registered for event"""
        try:
            response = supabase.table("registrations").select("*").eq("student_id", student_id).eq("event_id", event_id).execute()
            return len(response.data) > 0
        except Exception as e:
            print(f"Error checking registration: {e}")
            return False
    
    # ============================================
    # COLLEGE OPERATIONS
    # ============================================
    
    @staticmethod
    def create_college(name: str, city: str, type_: str, contact_email: str, status: str = "pending"):
        """Create a new college/organizer application"""
        try:
            response = supabase.table("colleges").insert({
                "name": name,
                "city": city,
                "type": type_,
                "contact_email": contact_email,
                "status": status,
                "created_at": datetime.utcnow().isoformat()
            }).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating college: {e}")
            return None
    
    @staticmethod
    def get_pending_colleges():
        """Get all pending college applications"""
        try:
            response = supabase.table("colleges").select("*").eq("status", "pending").execute()
            return response.data
        except Exception as e:
            print(f"Error getting pending colleges: {e}")
            return []
    
    @staticmethod
    def update_college_status(college_id: int, status: str):
        """Update college status (pending, approved, rejected)"""
        try:
            response = supabase.table("colleges").update({"status": status}).eq("id", college_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error updating college: {e}")
            return None
    
    # ============================================
    # BOOKMARK OPERATIONS
    # ============================================
    
    @staticmethod
    def bookmark_event(student_id: int, event_id: int):
        """Bookmark an event"""
        try:
            response = supabase.table("bookmarks").insert({
                "student_id": student_id,
                "event_id": event_id,
                "created_at": datetime.utcnow().isoformat()
            }).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error bookmarking event: {e}")
            return None
    
    @staticmethod
    def get_student_bookmarks(student_id: int):
        """Get all bookmarked events for a student"""
        try:
            response = supabase.table("bookmarks").select("*").eq("student_id", student_id).execute()
            return response.data
        except Exception as e:
            print(f"Error getting bookmarks: {e}")
            return []
    
    # ============================================
    # ANALYTICS OPERATIONS (PHASE 4)
    # ============================================
    
    @staticmethod
    def get_platform_stats():
        """Get overall platform statistics"""
        try:
            # Get counts
            events_response = supabase.table("events").select("id").execute()
            users_response = supabase.table("users").select("id").execute()
            registrations_response = supabase.table("registrations").select("id").execute()
            colleges_response = supabase.table("colleges").select("id").execute()
            
            total_events = len(events_response.data) if events_response.data else 0
            total_users = len(users_response.data) if users_response.data else 0
            total_registrations = len(registrations_response.data) if registrations_response.data else 0
            total_colleges = len(colleges_response.data) if colleges_response.data else 0
            
            # Get event status breakdown
            approved_events = supabase.table("events").select("id").eq("status", "approved").execute()
            pending_events = supabase.table("events").select("id").eq("status", "pending").execute()
            rejected_events = supabase.table("events").select("id").eq("status", "rejected").execute()
            
            return {
                "total_events": total_events,
                "approved_events": len(approved_events.data) if approved_events.data else 0,
                "pending_events": len(pending_events.data) if pending_events.data else 0,
                "rejected_events": len(rejected_events.data) if rejected_events.data else 0,
                "total_users": total_users,
                "total_registrations": total_registrations,
                "total_colleges": total_colleges
            }
        except Exception as e:
            print(f"Error getting platform stats: {e}")
            return {}
    
    @staticmethod
    def get_events_by_category():
        """Get event count by category"""
        try:
            events = supabase.table("events").select("category").eq("status", "approved").execute()
            
            category_count = {}
            if events.data:
                for event in events.data:
                    category = event.get("category", "Other")
                    category_count[category] = category_count.get(category, 0) + 1
            
            return category_count
        except Exception as e:
            print(f"Error getting events by category: {e}")
            return {}
    
    @staticmethod
    def get_top_events(limit: int = 5):
        """Get top events by registration count"""
        try:
            events = supabase.table("events").select("id, title, category").eq("status", "approved").execute()
            
            event_registrations = {}
            if events.data:
                for event in events.data:
                    event_id = event["id"]
                    regs = supabase.table("registrations").select("id").eq("event_id", event_id).execute()
                    event_registrations[event["title"]] = len(regs.data) if regs.data else 0
            
            # Sort and return top events
            sorted_events = sorted(event_registrations.items(), key=lambda x: x[1], reverse=True)
            return dict(sorted_events[:limit])
        except Exception as e:
            print(f"Error getting top events: {e}")
            return {}
    
    @staticmethod
    def get_user_stats():
        """Get user statistics"""
        try:
            students = supabase.table("users").select("id").eq("role", "student").execute()
            organizers = supabase.table("users").select("id").eq("role", "organizer").execute()
            admins = supabase.table("users").select("id").eq("role", "admin").execute()
            
            return {
                "total_students": len(students.data) if students.data else 0,
                "total_organizers": len(organizers.data) if organizers.data else 0,
                "total_admins": len(admins.data) if admins.data else 0
            }
        except Exception as e:
            print(f"Error getting user stats: {e}")
            return {}
    
    @staticmethod
    def get_event_registrations_count(event_id: int):
        """Get registration count for a specific event"""
        try:
            response = supabase.table("registrations").select("id").eq("event_id", event_id).execute()
            return len(response.data) if response.data else 0
        except Exception as e:
            print(f"Error getting event registrations: {e}")
            return 0
