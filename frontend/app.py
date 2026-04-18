import streamlit as st
import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

BACKEND_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Campus Event Hub",
    page_icon="🎉",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0A1428 0%, #0D0E1A 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #000000 0%, #0A0E1A 100%) !important;
    }
    
    h1 {
        color: #00D9FF;
        font-size: 2.5em !important;
        letter-spacing: 2px;
        font-weight: 800;
    }
    
    h2 {
        color: #FFFFFF;
        border-bottom: 3px solid #FFFFFF;
        padding-bottom: 10px;
        letter-spacing: 1px;
        font-weight: 700;
    }
    
    h3 {
        color: #FFFFFF;
        font-weight: 700;
    }
    
    p, div {
        color: #FFFFFF;
    }
    
    .stMetric {
        background: #1A4A8F;
        border-radius: 15px;
        padding: 25px;
        border: 2px solid #00D9FF;
        box-shadow: 0px 10px 40px rgba(0, 217, 255, 0.15), 0px 0px 30px rgba(26, 74, 143, 0.2);
    }
    
    .stButton>button {
        width: 100%;
        background: #00D9FF !important;
        color: #000000 !important;
        border: 2px solid #00D9FF !important;
        border-radius: 12px !important;
        padding: 14px !important;
        font-weight: 700 !important;
        font-size: 1.1em !important;
        transition: all 0.3s ease !important;
        box-shadow: 0px 8px 25px rgba(0, 217, 255, 0.3), inset 0px 2px 0px rgba(255, 255, 255, 0.1) !important;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        background: #00EFF6 !important;
        transform: translateY(-3px);
        box-shadow: 0px 15px 40px rgba(0, 217, 255, 0.5) !important;
    }
    
    .stTextInput>div>div>input, .stSelectbox>div>div>select, .stTextArea>div>div>textarea {
        background-color: #16213e !important;
        border: 2px solid #00D9FF !important;
        border-radius: 10px !important;
        padding: 12px !important;
        color: #FFFFFF !important;
        font-weight: 500;
    }
    
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>select:focus, .stTextArea>div>div>textarea:focus {
        box-shadow: 0px 0px 20px rgba(0, 217, 255, 0.4) !important;
    }
    
    .stInfo, [data-testid="stAlert"] {
        background: #1A4A8F !important;
        border-left: 5px solid #00D9FF !important;
        border: 2px solid #00D9FF !important;
        border-radius: 10px !important;
    }
    
    .stSuccess {
        background: #1A4A8F !important;
        border-left: 5px solid #00D9FF !important;
        border: 2px solid #00D9FF !important;
    }
    
    .stWarning {
        background: #1A4A8F !important;
        border-left: 5px solid #00D9FF !important;
        border: 2px solid #00D9FF !important;
    }
    
    .stRadio>div, label {
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.token = None

st.sidebar.title("Campus Event Hub")

if st.session_state.authenticated:
    st.sidebar.markdown(f"✅ **Logged in as:** {st.session_state.user['name']}")
    st.sidebar.markdown(f"📍 **Role:** {st.session_state.user['role'].upper()}")
    st.sidebar.markdown("---")
    
    if st.session_state.user['role'] == 'admin':
        nav_options = ["🏠 Home", "📋 Events", "⚙️ Admin Panel", "📊 Analytics"]
    else:
        nav_options = ["🏠 Home", "📋 Events", "🎯 Create Event", "👤 Dashboard", "📊 Analytics"]
    
    page = st.sidebar.radio("Navigation", nav_options, key="nav_authenticated")
    
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.token = None
        st.rerun()
else:
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Not Logged In**")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Navigation",
        ["🏠 Home", "🔐 Login", "📝 Sign Up", "👑 Admin Login"],
        key="nav_unauthenticated"
    )

# ============================================
# HOME PAGE
# ============================================

if page == "🏠 Home":
    st.markdown("<h1 style='text-align: center; color: #00D9FF;'>🎉 Campus Event Hub</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2em; color: #FFFFFF;'>Discover Amazing Events in Your City</p>", unsafe_allow_html=True)
    
    if not st.session_state.authenticated:
        if st.button("📥 Load Demo Data", use_container_width=True):
            try:
                response = requests.post(f"{BACKEND_URL}/api/demo/load-data")
                if response.status_code == 200:
                    st.success("Demo data loaded! Refresh to see events.")
                else:
                    st.error("Failed to load demo data")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    st.markdown("")
    st.markdown("<h2 style='color: #FFFFFF;'>📊 Platform Stats</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🏛️ Colleges", "10+", "Growing")
    with col2:
        st.metric("📅 Events", "50+", "This Month")
    with col3:
        st.metric("👥 Users", "1000+", "Active")
    with col4:
        st.metric("🎯 Registrations", "5000+", "Total")
    
    st.markdown("")
    st.markdown("<h2 style='color: #FFFFFF;'>✨ Why Join Us?</h2>", unsafe_allow_html=True)
    
    feature_col1, feature_col2, feature_col3 = st.columns(3)
    
    with feature_col1:
        st.markdown("""
        <div style='background: #1A4A8F;
                    padding: 20px;
                    border-radius: 15px;
                    border: 2px solid #00D9FF;
                    box-shadow: 0px 4px 15px rgba(0, 217, 255, 0.2);'>
            <h3 style='color: #00D9FF;'>🔍 Smart Discovery</h3>
            <p style='color: #FFFFFF;'>Find events tailored to your interests</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_col2:
        st.markdown("""
        <div style='background: #1A4A8F;
                    padding: 20px;
                    border-radius: 15px;
                    border: 2px solid #00D9FF;
                    box-shadow: 0px 4px 15px rgba(0, 217, 255, 0.2);'>
            <h3 style='color: #00D9FF;'>🏆 Earn Rewards</h3>
            <p style='color: #FFFFFF;'>Collect coins and badges</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_col3:
        st.markdown("""
        <div style='background: #1A4A8F;
                    padding: 20px;
                    border-radius: 15px;
                    border: 2px solid #00D9FF;
                    box-shadow: 0px 4px 15px rgba(0, 217, 255, 0.2);'>
            <h3 style='color: #00D9FF;'>🤝 Connect</h3>
            <p style='color: #FFFFFF;'>Meet students and professionals</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    st.markdown("<h2 style='color: #FFFFFF;'>🚀 Ready to Join Us?</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background: #1A4A8F;
                padding: 30px;
                border-radius: 15px;
                border: 2px solid #00D9FF;
                box-shadow: 0px 8px 30px rgba(0, 217, 255, 0.3);'>
        <h3 style='color: #00D9FF;'>Join thousands of students discovering amazing events!</h3>
        <p style='color: #FFFFFF; font-size: 1.1em;'>Create your account today and start exploring events in your city. Network with peers, learn new skills, and earn rewards.</p>
        <p style='color: #00D9FF;'><b>✨ Features:</b></p>
        <ul style='color: #FFFFFF;'>
            <li>Browse events by category and location</li>
            <li>Register for events and track attendance</li>
            <li>Bookmark your favorite events</li>
            <li>Earn coins and badges for participation</li>
            <li>Connect with other students and professionals</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    

# ============================================
# EVENTS PAGE
# ============================================

elif page == "📋 Events":
    st.markdown("<h1 style='color: #FFFFFF;'>📋 Browse Events</h1>", unsafe_allow_html=True)
    
    try:
        response = requests.get(f"{BACKEND_URL}/api/events")
        if response.status_code == 200:
            data = response.json()
            events = data.get("events", [])
            
            if events:
                st.success(f"Found {len(events)} event(s)")
                for event in events:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"""
                        <div style='background: #1A4A8F;
                                    padding: 20px;
                                    border-radius: 15px;
                                    color: #FFFFFF;
                                    margin-bottom: 15px;
                                    border: 3px solid #00D9FF;
                                    box-shadow: 0px 8px 30px rgba(0, 217, 255, 0.3);'>
                            <h3 style='color: #FFFFFF;'>{event['title']}</h3>
                            <p style='color: #FFFFFF;'><b>📂 Category:</b> {event['category']}</p>
                            <p style='color: #FFFFFF;'><b>📅 Date:</b> {event['date']} | <b>⏰ Time:</b> {event['time']}</p>
                            <p style='color: #FFFFFF;'><b>📍 Location:</b> {event['venue']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        if st.session_state.authenticated and st.session_state.user['role'] == 'student':
                            col_reg, col_bm = st.columns(2)
                            with col_reg:
                                if st.button("📋 Register", key=f"event_{event['id']}"):
                                    try:
                                        register_response = requests.post(
                                            f"{BACKEND_URL}/api/events/register",
                                            params={"student_email": st.session_state.user['email'], "event_id": event['id']}
                                        )
                                        if register_response.status_code == 200:
                                            st.success("Registered!")
                                            st.rerun()
                                        else:
                                            st.error(register_response.json().get("detail", "Failed"))
                                    except Exception as e:
                                        st.error(f"Error: {str(e)}")
                            with col_bm:
                                if st.button("🔖 Bookmark", key=f"bookmark_{event['id']}"):
                                    try:
                                        student = requests.get(f"{BACKEND_URL}/api/auth/profile/{st.session_state.user['email']}").json()["user"]
                                        bookmark_response = requests.post(
                                            f"{BACKEND_URL}/api/events/bookmark",
                                            params={"student_id": student['id'], "event_id": event['id']}
                                        )
                                        if bookmark_response.status_code == 200:
                                            st.success("Bookmarked!")
                                        else:
                                            st.info("Already bookmarked")
                                    except Exception as e:
                                        st.error(f"Error: {str(e)}")
                        elif not st.session_state.authenticated:
                            st.info("Login to register")
            else:
                st.info("No events available")
        else:
            st.error("Could not fetch events")
    except Exception as e:
        st.error(f"Connection error: {str(e)}")

# ============================================
# CREATE EVENT PAGE (STUDENTS)
# ============================================

elif page == "🎯 Create Event":
    st.markdown("<h1 style='color: #00D9FF;'>🎯 Create New Event</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #FFFFFF;'>Create an event for approval by admin</p>", unsafe_allow_html=True)
    
    with st.form("create_event_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            event_name = st.text_input("Event Name")
            event_date = st.date_input("Event Date")
            event_location = st.text_input("Location")
            event_seats = st.number_input("Available Seats", min_value=10, max_value=1000, value=50)
        
        with col2:
            event_category = st.selectbox("Category", ["Tech", "Sports", "Workshop", "Seminar", "Cultural", "Hackathon"])
            event_time = st.time_input("Event Time")
            event_college = st.text_input("College/Organization")
            event_desc = st.text_area("Description", height=100)
        
        if st.form_submit_button("Create Event"):
            if not all([event_name, event_date, event_location, event_category, event_time]):
                st.error("Please fill all required fields")
            else:
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/api/events/create",
                        json={
                            "title": event_name,
                            "description": event_desc,
                            "category": event_category,
                            "college": event_college,
                            "date": str(event_date),
                            "time": str(event_time),
                            "venue": event_location,
                            "seats": event_seats,
                            "organizer_email": st.session_state.user['email'],
                            "location": event_location,
                             "name": event_name,

                        }
                    )
                    if response.status_code == 200:
                        st.success("Event created! Waiting for admin approval.")
                        st.balloons()
                    else:
                        st.error(response.json().get("detail", "Failed to create event"))
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# ============================================
# DASHBOARD PAGE
# ============================================

elif page == "👤 Dashboard":
    st.markdown("<h1 style='color: #00D9FF;'>👤 My Dashboard</h1>", unsafe_allow_html=True)
    
    try:
        profile_response = requests.get(f"{BACKEND_URL}/api/auth/profile/{st.session_state.user['email']}")
        if profile_response.status_code == 200:
            profile = profile_response.json()["user"]
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("💰 Total Coins", profile.get("coins", 0))
            with col2:
                st.metric("🏆 Badge", profile.get("badge", "None"))
            with col3:
                st.metric("🎓 College", profile.get("college", "N/A"))
            with col4:
                st.metric("📚 Year", profile.get("year", "N/A"))
        
        st.markdown("")
        st.markdown("<h2 style='color: #00D9FF;'>📅 My Registered Events</h2>", unsafe_allow_html=True)
        
        events_response = requests.get(f"{BACKEND_URL}/api/events/user/{st.session_state.user['email']}")
        if events_response.status_code == 200:
            events_data = events_response.json()
            events = events_data.get("events", [])
            
            if events:
                st.success(f"Registered for {len(events)} event(s)")
                for event in events:
                    st.markdown(f"""
                    <div style='background: #1A4A8F;
                                padding: 15px;
                                border-radius: 10px;
                                border: 2px solid #00D9FF;
                                margin-bottom: 10px;'>
                        <b style='color: #FFFFFF;'>{event['title']}</b>
                        <p style='color: #00D9FF;'>📅 {event['date']} | ⏰ {event['time']}</p>
                        <p style='color: #FFFFFF;'>📍 {event['venue']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No registered events yet")
        else:
            st.error("Could not fetch events")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# ============================================
# ANALYTICS PAGE
# ============================================

elif page == "📊 Analytics":
    st.markdown("<h1 style='color: #00D9FF;'>📊 Analytics Dashboard</h1>", unsafe_allow_html=True)
    
    try:
        overview_response = requests.get(f"{BACKEND_URL}/api/admin/analytics/overview")
        if overview_response.status_code == 200:
            overview = overview_response.json()["data"]
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("🏛️ Total Colleges", overview.get("total_colleges", 0))
            with col2:
                st.metric("📅 Total Events", overview.get("total_events", 0))
            with col3:
                st.metric("👥 Active Students", overview.get("total_students", 0))
            with col4:
                st.metric("✅ Total Registrations", overview.get("total_registrations", 0))
            
            st.markdown("")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("<h3 style='color: #FFFFFF;'>📊 Event Status</h3>", unsafe_allow_html=True)
                status_data = {
                    "Approved": overview.get("approved_events", 0),
                    "Pending": overview.get("pending_events", 0),
                    "Rejected": overview.get("rejected_events", 0)
                }
                st.bar_chart(status_data)
            
            with col2:
                st.markdown("<h3 style='color: #FFFFFF;'>👥 User Breakdown</h3>", unsafe_allow_html=True)
                user_data = {
                    "Students": overview.get("total_students", 0),
                    "Organizers": overview.get("total_organizers", 0),
                    "Admins": overview.get("total_admins", 0)
                }
                st.bar_chart(user_data)
        
        st.markdown("")
        events_response = requests.get(f"{BACKEND_URL}/api/admin/analytics/events")
        if events_response.status_code == 200:
            events_data = events_response.json()["data"]
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("<h3 style='color: #FFFFFF;'>📂 Events by Category</h3>", unsafe_allow_html=True)
                category_data = events_data.get("by_category", {})
                if category_data:
                    st.bar_chart(category_data)
                else:
                    st.info("No category data available")
            
            with col2:
                st.markdown("<h3 style='color: #FFFFFF;'>🏆 Top Events</h3>", unsafe_allow_html=True)
                top_events = events_data.get("top_events", {})
                if top_events:
                    st.bar_chart(top_events)
                else:
                    st.info("No event data available")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# ============================================
# ADMIN PANEL
# ============================================

elif page == "⚙️ Admin Panel":
    st.markdown("<h1 style='color: #FFFFFF;'>⚙️ Admin Control Panel</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #00D9FF;'>Manage applications, events, and users</p>", unsafe_allow_html=True)
    
    admin_section = st.radio(
        "Admin Section",
        ["✅ Event Approvals", "🔔 Organizer Applications", "👥 User Management", "📅 Block Dates"]
    )
    
    if admin_section == "✅ Event Approvals":
        st.markdown("<h2 style='color: #FFFFFF;'>✅ Pending Event Approvals</h2>", unsafe_allow_html=True)
        
        try:
            response = requests.get(f"{BACKEND_URL}/api/admin/pending-events")
            if response.status_code == 200:
                data = response.json()
                events = data.get("events", [])
                
                if events:
                    st.success(f"Found {len(events)} pending event(s)")
                    for event in events:
                        col1, col2, col3 = st.columns([3, 1, 1])
                        with col1:
                            st.markdown(f"""
                            <div style='background: #1A4A8F;
                                        padding: 15px;
                                        border-left: 5px solid #00D9FF;
                                        border-radius: 10px;
                                        border: 2px solid #FFFFFF;
                                        box-shadow: 0px 4px 15px rgba(0, 217, 255, 0.2);'>
                                <b style='color: #FFFFFF;'>{event['title']}</b>
                                <p style='font-size: 0.9em; color: #00D9FF;'>{event['category']} | {event['date']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        with col2:
                            if st.button("Approve", key=f"app_approve_{event['id']}"):
                                try:
                                    requests.post(f"{BACKEND_URL}/api/admin/approve-event", json={"event_id": str(event['id']), "action": "approve"})
                                    st.success("Approved!")
                                    st.rerun()
                                except:
                                    st.error("Failed")
                        with col3:
                            if st.button("Reject", key=f"app_reject_{event['id']}"):
                                try:
                                    requests.post(f"{BACKEND_URL}/api/admin/approve-event", json={"event_id": str(event['id']), "action": "reject"})
                                    st.success("Rejected!")
                                    st.rerun()
                                except:
                                    st.error("Failed")
                else:
                    st.info("No pending events")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    elif admin_section == "🔔 Organizer Applications":
        st.markdown("<h2 style='color: #00D9FF;'>🔔 Pending Organizer Applications</h2>", unsafe_allow_html=True)
        
        try:
            response = requests.get(f"{BACKEND_URL}/api/admin/organizer-applications")
            if response.status_code == 200:
                data = response.json()
                applications = data.get("applications", [])
                
                if applications:
                    st.success(f"Found {len(applications)} pending application(s)")
                    for app in applications:
                        col1, col2, col3 = st.columns([3, 1, 1])
                        with col1:
                            st.markdown(f"""
                            <div style='background: #1A4A8F;
                                        padding: 15px;
                                        border-left: 5px solid #00D9FF;
                                        border-radius: 10px;
                                        border: 2px solid #FFFFFF;
                                        box-shadow: 0px 4px 15px rgba(0, 217, 255, 0.2);'>
                                <b style='color: #FFFFFF;'>{app['name']}</b> | {app['type']} | {app['city']}
                                <p style='font-size: 0.9em; color: #00D9FF;'>Email: {app['contact_email']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        with col2:
                            if st.button("Approve", key=f"approve_{app['id']}"):
                                try:
                                    requests.post(f"{BACKEND_URL}/api/admin/approve-organizer", json={"college_id": app['id'], "action": "approve"})
                                    st.success("Approved!")
                                    st.rerun()
                                except:
                                    st.error("Failed")
                        with col3:
                            if st.button("Reject", key=f"reject_{app['id']}"):
                                try:
                                    requests.post(f"{BACKEND_URL}/api/admin/approve-organizer", json={"college_id": app['id'], "action": "reject"})
                                    st.success("Rejected!")
                                    st.rerun()
                                except:
                                    st.error("Failed")
                else:
                    st.info("No pending applications")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    elif admin_section == "👥 User Management":
        st.markdown("<h2 style='color: #FFFFFF;'>👥 Manage Users</h2>", unsafe_allow_html=True)
        st.info("User management dashboard coming soon!")
    
    elif admin_section == "📅 Block Dates":
        st.markdown("<h2 style='color: #00D9FF;'>📅 Block Calendar Dates</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date")
        with col2:
            end_date = st.date_input("End Date")
        reason = st.text_input("Reason")
        if st.button("Block Dates"):
            st.success("Dates blocked!")

# ============================================
# LOGIN PAGE
# ============================================

elif page == "🔐 Login":
    st.markdown("<h1 style='text-align: center; color: #00D9FF;'>🔐 Student Login</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if not email or not password:
                st.error("Please fill all fields")
            else:
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/api/auth/login",
                        json={"email": email, "password": password}
                    )
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.authenticated = True
                        st.session_state.user = data["user"]
                        st.session_state.token = data["token"]
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error(response.json().get("detail", "Login failed"))
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# ============================================
# SIGN UP PAGE
# ============================================

elif page == "📝 Sign Up":
    st.markdown("<h1 style='text-align: center; color: #00D9FF;'>📝 Student Registration</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        college = st.selectbox("College", ["MIT", "IIT", "NIT", "BITS", "VIT", "Other"])
        year = st.selectbox("Year", [1, 2, 3, 4])
        branch = st.selectbox("Branch", ["CSE", "ECE", "Mechanical", "Civil", "Other"])
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        if st.button("Create Account"):
            if not all([name, email, college, password, confirm_password]):
                st.error("Please fill all fields")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters")
            else:
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/api/auth/register",
                        json={
                            "name": name,
                            "email": email,
                            "password": password,
                            "college": college,
                            "year": year,
                            "branch": branch,
                            "role": "student"
                        }
                    )
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.authenticated = True
                        st.session_state.user = data["user"]
                        st.session_state.token = data["token"]
                        st.success("Account created!")
                        st.rerun()
                    else:
                        st.error(response.json().get("detail", "Registration failed"))
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# ============================================
# ADMIN LOGIN PAGE
# ============================================

elif page == "👑 Admin Login":
    st.markdown("<h1 style='text-align: center; color: #00D9FF;'>👑 Admin Login</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("Admin Email: umra@jain.com")
        
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        
        if st.button("Admin Login"):
            if not email or not password:
                st.error("Please fill all fields")
            else:
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/api/auth/login",
                        json={"email": email, "password": password}
                    )
                    if response.status_code == 200:
                        data = response.json()
                        if data["user"]["role"] == "admin":
                            st.session_state.authenticated = True
                            st.session_state.user = data["user"]
                            st.session_state.token = data["token"]
                            st.success("Admin login successful!")
                            st.rerun()
                        else:
                            st.error("This account is not an admin account")
                    else:
                        st.error(response.json().get("detail", "Login failed"))
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        st.markdown("---")
        st.markdown("<h3 style='color: #00D9FF;'>First Time Admin?</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #FFFFFF;'>Contact system administrator to create admin account</p>", unsafe_allow_html=True)
