import streamlit as st
import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# ============================================
# CONFIGURATION
# ============================================

BACKEND_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Campus Event Hub",
    page_icon="🎉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS STYLING
# ============================================

st.markdown("""
    <style>
    /* Main background - Modern Dark Navy */
    .stApp {
        background: linear-gradient(135deg, #0A1428 0%, #0D0E1A 100%);
    }
    
    /* Sidebar styling - Pure Black Premium */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #000000 0%, #0A0E1A 100%) !important;
    }
    
    /* Header styling - Bold Cyan */
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
    
    /* Text styling - Pure White */
    p, div {
        color: #FFFFFF;
    }
    
    /* Card styling - Single Blue */
    .stMetric {
        background: #1A4A8F;
        border-radius: 15px;
        padding: 25px;
        border: 2px solid #00D9FF;
        box-shadow: 0px 10px 40px rgba(0, 217, 255, 0.15), 0px 0px 30px rgba(26, 74, 143, 0.2);
    }
    
    /* Button styling - Cyan only */
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
    
    /* Input styling - Dark navy with cyan border */
    .stTextInput>div>div>input, .stSelectbox>div>div>select {
        background-color: #16213e !important;
        border: 2px solid #00D9FF !important;
        border-radius: 10px !important;
        padding: 12px !important;
        color: #FFFFFF !important;
        font-weight: 500;
    }
    
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>select:focus {
        box-shadow: 0px 0px 20px rgba(0, 217, 255, 0.4) !important;
    }
    
    /* Info box styling */
    .stInfo, [data-testid="stAlert"] {
        background: #1A4A8F !important;
        border-left: 5px solid #00D9FF !important;
        border: 2px solid #00D9FF !important;
        border-radius: 10px !important;
    }
    
    /* Success box - Blue */
    .stSuccess {
        background: #1A4A8F !important;
        border-left: 5px solid #00D9FF !important;
        border: 2px solid #00D9FF !important;
    }
    
    /* Warning box - Blue */
    .stWarning {
        background: #1A4A8F !important;
        border-left: 5px solid #00D9FF !important;
        border: 2px solid #00D9FF !important;
    }
    
    /* Radio button and selectbox */
    .stRadio>div, label {
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE MANAGEMENT
# ============================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.token = None

# ============================================
# SIDEBAR NAVIGATION
# ============================================

st.sidebar.title("Campus Event Hub")

if st.session_state.authenticated:
    st.sidebar.markdown(f"✅ **Logged in as:** {st.session_state.user['name']}")
    st.sidebar.markdown(f"📍 **Role:** {st.session_state.user['role'].upper()}")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Navigation",
        ["🏠 Home", "📋 Events", "👤 Dashboard", "⚙️ Admin", "📊 Analytics", "🏢 Apply Organizer"],
        key="nav_authenticated"
    )
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
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
        ["🏠 Home", "🔐 Login", "📝 Sign Up", "👑 Admin Register"],
        key="nav_unauthenticated"
    )

# ============================================
# HOME PAGE
# ============================================

if page == "🏠 Home":
    # Hero Section
    st.markdown("<h1 style='text-align: center; color: #00D9FF;'>🎉 Campus Event Hub</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2em; color: #FFFFFF;'>Discover Amazing Events in Your City</p>", unsafe_allow_html=True)
    
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
    
    # Features Section
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
            <p style='color: #FFFFFF;'>Find events tailored to your interests with powerful search and filters</p>
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
            <p style='color: #FFFFFF;'>Collect coins and badges as you participate in more events</p>
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
            <p style='color: #FFFFFF;'>Meet students and professionals from colleges across your city</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # Call to Action
    st.markdown("""
    <div style='background: #1A4A8F;
                padding: 40px;
                border-radius: 15px;
                text-align: center;
                color: #FFFFFF;
                box-shadow: 0px 10px 40px rgba(0, 217, 255, 0.3), 0px 0px 20px rgba(26, 74, 143, 0.3);
                border: 3px solid #00D9FF;'>
        <h2 style='color: #FFFFFF;'>👉 Ready to Join?</h2>
        <p style='color: #FFFFFF; font-weight: bold; font-size: 1.1em;'>Sign up today and start discovering amazing events!</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================
# EVENTS PAGE
# ============================================

elif page == "📋 Events":
    st.markdown("<h1 style='color: #FFFFFF;'>📋 Browse Events</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #00D9FF;'>Find and register for amazing events happening in your city!</p>", unsafe_allow_html=True)
    
    # Search and filter
    col1, col2, col3 = st.columns(3)
    with col1:
        search = st.text_input("🔍 Search events by name...")
    with col2:
        category = st.selectbox("📂 Filter by Category", ["All", "Tech", "Sports", "Workshop", "Seminar", "Cultural", "Hackathon"])
    with col3:
        college = st.selectbox("🏛️ Filter by College", ["All", "MIT", "IIT", "NIT", "BITS", "VIT"])
    
    st.markdown("")
    
    # Fetch events from backend
    try:
        params = {"search": search}
        if category != "All":
            params["category"] = category
        if college != "All":
            params["college"] = college
        
        response = requests.get(f"{BACKEND_URL}/api/events", params=params)
        
        if response.status_code == 200:
            data = response.json()
            events = data.get("events", [])
            
            if events:
                st.success(f"✅ Found {len(events)} event(s)")
                
                # Display events as cards
                for event in events:
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"""
                            <div style='background: #1A4A8F;
                                        padding: 20px;
                                        border-radius: 15px;
                                        color: #FFFFFF;
                                        margin-bottom: 15px;
                                        border: 3px solid #00D9FF;
                                        box-shadow: 0px 8px 30px rgba(0, 217, 255, 0.3), 0px 0px 20px rgba(26, 74, 143, 0.2);'>
                                <h3 style='color: #FFFFFF;'>{event['name']}</h3>
                                <p style='color: #FFFFFF;'><b>🏛️ College:</b> {event['college']} | <b>📂 Category:</b> {event['category']}</p>
                                <p style='color: #FFFFFF;'><b>📅 Date:</b> {event['date']} | <b>⏰ Time:</b> {event['time']}</p>
                                <p style='color: #FFFFFF;'><b>📍 Location:</b> {event['location']}</p>
                                <p style='color: #FFFFFF;'><b>👥 Seats:</b> {event['registered']}/{event['seats']} registered</p>
                                <p style='color: #FFFFFF;'><b>👤 Organizer:</b> {event['organizer_name']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            if st.session_state.authenticated:
                                if st.button("📋 Register", key=f"event_{event['id']}"):
                                    try:
                                        register_response = requests.post(
                                            f"{BACKEND_URL}/api/events/register",
                                            json={
                                                "student_email": st.session_state.user['email'],
                                                "event_id": event['id']
                                            }
                                        )
                                        
                                        if register_response.status_code == 200:
                                            st.success(f"✅ {register_response.json()['message']}")
                                            st.rerun()
                                        else:
                                            st.error(f"❌ {register_response.json()['detail']}")
                                    except Exception as e:
                                        st.error(f"❌ Error: {str(e)}")
                            else:
                                st.warning("🔐 Login to register")
            else:
                st.info("📭 No events found. Try adjusting your filters!")
        else:
            st.error("❌ Could not fetch events from backend")
    except Exception as e:
        st.error(f"❌ Connection error: {str(e)}")
    
    st.markdown("")
    st.markdown("💡 Create events as an organizer by updating your role!")

# ============================================
# DASHBOARD PAGE

# ============================================
# DASHBOARD PAGE
# ============================================

elif page == "👤 Dashboard":
    st.markdown("<h1 style='color: #00D9FF;'>👤 My Dashboard</h1>", unsafe_allow_html=True)
    
    # Tabs for different dashboard sections
    tab1, tab2 = st.tabs(["📊 My Events", "🎯 Create Event"])
    
    with tab1:
        # User Stats
        st.markdown("<h2 style='color: #00D9FF;'>📊 Your Stats</h2>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📋 Events Registered", "12", "+2 this month")
        
        with col2:
            st.metric("✅ Events Attended", "8", "67% attendance")
        
        with col3:
            st.metric("🏆 Events Won", "2", "Great job!")
        
        with col4:
            st.metric("💰 Total Coins", "850", "+150 this month")
        
        st.markdown("")
        
        # Badge Section
        st.markdown("<h2 style='color: #FFFFFF;'>🏅 Your Badge</h2>", unsafe_allow_html=True)
        
        badge_col1, badge_col2, badge_col3 = st.columns([1, 2, 1])
        
        with badge_col2:
            st.markdown("""
            <div style='background: #1A4A8F;
                        padding: 30px;
                        border-radius: 15px;
                        text-align: center;
                        color: #FFFFFF;
                        border: 3px solid #00D9FF;
                        box-shadow: 0px 10px 40px rgba(0, 217, 255, 0.3), 0px 0px 30px rgba(26, 74, 143, 0.2);'>
                <h1 style='font-size: 4em;'>🥇</h1>
                <h2 style='color: #FFFFFF;'>GOLD Member</h2>
                <p style='color: #FFFFFF; font-weight: 500;'>You've registered for 10+ events! You're a true event enthusiast!</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("")
        
        # Upcoming Events
        st.markdown("<h2 style='color: #00D9FF;'>📅 My Upcoming Events</h2>", unsafe_allow_html=True)
        
        try:
            response = requests.get(f"{BACKEND_URL}/api/events/user/{st.session_state.user['email']}")
            if response.status_code == 200:
                data = response.json()
                events = data.get("events", [])
                
                if events:
                    for event in events:
                        st.markdown(f"""
                        <div style='background: #1A4A8F;
                                    padding: 15px;
                                    border-radius: 15px;
                                    border: 2px solid #00D9FF;
                                    margin-bottom: 10px;
                                    box-shadow: 0px 4px 15px rgba(0, 217, 255, 0.2);'>
                            <b style='color: #FFFFFF;'>📅 {event['name']}</b> - <span style='color: #FFFFFF;'>{event['date']} ✅ Registered</span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("📭 You're not registered for any events yet!")
            else:
                st.error("❌ Could not fetch your events")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    with tab2:
        st.markdown("<h2 style='color: #00D9FF;'>🎯 Create New Event</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #FFFFFF;'>Share your event with the campus community!</p>", unsafe_allow_html=True)
        
        st.markdown("")
        
        with st.form("create_event_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                event_name = st.text_input("📋 Event Name", placeholder="e.g., Web Dev Workshop")
                event_date = st.date_input("📅 Event Date")
                event_location = st.text_input("📍 Location", placeholder="e.g., Building A, Room 101")
                event_seats = st.number_input("👥 Available Seats", min_value=10, max_value=1000, value=50)
            
            with col2:
                event_category = st.selectbox("📂 Category", ["Tech", "Sports", "Workshop", "Seminar", "Cultural", "Hackathon"])
                event_time = st.time_input("⏰ Event Time")
                event_college = st.selectbox("🏛️ College", ["MIT", "IIT", "NIT", "BITS", "VIT"])
                event_desc = st.text_area("📝 Description", placeholder="Describe your event...", height=100)
            
            st.markdown("")
            
            if st.form_submit_button("✅ Create Event", use_container_width=True):
                if not all([event_name, event_date, event_location, event_category, event_time]):
                    st.error("❌ Please fill in all required fields")
                else:
                    try:
                        event_date_str = str(event_date)
                        event_time_str = str(event_time)
                        
                        response = requests.post(
                            f"{BACKEND_URL}/api/events/create",
                            json={
                                "name": event_name,
                                "description": event_desc,
                                "category": event_category,
                                "college": event_college,
                                "date": event_date_str,
                                "time": event_time_str,
                                "location": event_location,
                                "seats": event_seats,
                                "organizer_email": st.session_state.user['email']
                            }
                        )
                        
                        if response.status_code == 200:
                            st.success("✅ Event created successfully!")
                            st.balloons()
                        else:
                            st.error(f"❌ {response.json().get('detail', 'Failed to create event')}")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

# ============================================
# DASHBOARD PAGE (PLACEHOLDER)
# ============================================

elif page == "👤 Dashboard":
    st.markdown("<h1 style='color: #00D9FF;'>👤 My Dashboard</h1>", unsafe_allow_html=True)
    
    # User Stats
    st.markdown("<h2 style='color: #00D9FF;'>📊 Your Stats</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📋 Events Registered", "12", "+2 this month")
    
    with col2:
        st.metric("✅ Events Attended", "8", "67% attendance")
    
    with col3:
        st.metric("🏆 Events Won", "2", "Great job!")
    
    with col4:
        st.metric("💰 Total Coins", "850", "+150 this month")
    
    st.markdown("")
    
    # Badge Section
    st.markdown("<h2 style='color: #FFFFFF;'>🏅 Your Badge</h2>", unsafe_allow_html=True)
    
    badge_col1, badge_col2, badge_col3 = st.columns([1, 2, 1])
    
    with badge_col2:
        st.markdown("""
        <div style='background: #1A4A8F;
                    padding: 30px;
                    border-radius: 15px;
                    text-align: center;
                    color: #FFFFFF;
                    border: 3px solid #00D9FF;
                    box-shadow: 0px 10px 40px rgba(0, 217, 255, 0.3), 0px 0px 30px rgba(26, 74, 143, 0.2);'>
            <h1 style='font-size: 4em;'>🥇</h1>
            <h2 style='color: #FFFFFF;'>GOLD Member</h2>
            <p style='color: #FFFFFF; font-weight: 500;'>You've registered for 10+ events! You're a true event enthusiast!</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # Upcoming Events
    st.markdown("<h2 style='color: #00D9FF;'>📅 My Upcoming Events</h2>", unsafe_allow_html=True)
    
    upcoming = [
        {"name": "AI/ML Hackathon", "date": "2026-04-18", "status": "Registered"},
        {"name": "Tech Talk: Cloud Computing", "date": "2026-04-20", "status": "Registered"}
    ]
    
    for event in upcoming:
        st.markdown(f"""
        <div style='background: #1A4A8F;
                    padding: 15px;
                    border-left: 5px solid #00D9FF;
                    border-radius: 10px;
                    margin-bottom: 10px;
                    border: 2px solid #00D9FF;
                    box-shadow: 0px 4px 15px rgba(0, 217, 255, 0.2);'>
            <b style='color: #FFFFFF;'>📅 {event['name']}</b> - <span style='color: #FFFFFF;'>{event['date']} ✅ {event['status']}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Bookmarked Events
    st.markdown("<h2 style='color: #FFFFFF;'>❤️ My Bookmarked Events</h2>", unsafe_allow_html=True)
    
    bookmarked = [
        {"name": "Web Dev Workshop", "date": "2026-04-15"}
    ]
    
    for event in bookmarked:
        st.markdown(f"""
        <div style='background: #1A4A8F;
                    padding: 15px;
                    border-left: 5px solid #00D9FF;
                    border-radius: 10px;
                    margin-bottom: 10px;
                    border: 2px solid #00D9FF;
                    box-shadow: 0px 4px 15px rgba(0, 217, 255, 0.2);'>
            <b style='color: #FFFFFF;'>❤️ {event['name']}</b> - <span style='color: #FFFFFF;'>{event['date']}</span>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# ADMIN PAGE
# ============================================

elif page == "⚙️ Admin":
    st.markdown("<h1 style='color: #FFFFFF;'>⚙️ Admin Control Panel</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #00D9FF;'>Manage applications, events, and users</p>", unsafe_allow_html=True)
    
    admin_section = st.radio(
        "📋 Admin Section",
        ["🔔 Organizer Applications", "✅ Event Approvals", "👥 User Management", "📅 Block Dates"]
    )
    
    if admin_section == "🔔 Organizer Applications":
        st.markdown("<h2 style='color: #00D9FF;'>🔔 Pending Organizer Applications</h2>", unsafe_allow_html=True)
        
        sample_apps = [
            {"name": "Tech Club IIT", "city": "Bangalore", "type": "College Club", "date": "2026-04-10"},
            {"name": "StartUp XYZ", "city": "Bangalore", "type": "Company", "date": "2026-04-12"}
        ]
        
        for app in sample_apps:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"""
                <div style='background: #1A4A8F;
                            padding: 15px;
                            border-left: 5px solid #00D9FF;
                            border-radius: 10px;
                            border: 2px solid #FFFFFF;
                            box-shadow: 0px 4px 15px rgba(0, 217, 255, 0.2);'>
                    <b style='color: #FFFFFF;'>{app['name']}</b> | <span style='color: #FFFFFF;'>{app['type']} | {app['city']}</span>
                    <p style='font-size: 0.9em; color: #00D9FF;'>Applied: {app['date']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.button("✅ Approve", key=f"approve_{app['name']}")
            
            with col3:
                st.button("❌ Reject", key=f"reject_{app['name']}")
    
    elif admin_section == "✅ Event Approvals":
        st.markdown("<h2 style='color: #FFFFFF;'>✅ Pending Event Approvals</h2>", unsafe_allow_html=True)
        
        sample_events = [
            {"name": "Python Workshop", "college": "MIT", "date": "2026-04-25", "category": "Workshop"},
            {"name": "Data Science Seminar", "college": "IIT", "date": "2026-04-28", "category": "Seminar"}
        ]
        
        for event in sample_events:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"""
                <div style='background: #1A4A8F;
                            padding: 15px;
                            border-left: 5px solid #00D9FF;
                            border-radius: 10px;
                            border: 2px solid #FFFFFF;
                            box-shadow: 0px 4px 15px rgba(0, 217, 255, 0.2);'>
                    <b style='color: #FFFFFF;'>{event['name']}</b> by <span style='color: #FFFFFF;'>{event['college']}</span>
                    <p style='font-size: 0.9em; color: #00D9FF;'>{event['category']} | {event['date']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.button("✅ Approve", key=f"app_approve_{event['name']}")
            
            with col3:
                st.button("❌ Reject", key=f"app_reject_{event['name']}")
    
    elif admin_section == "👥 User Management":
        st.markdown("<h2 style='color: #FFFFFF;'>👥 Manage Users</h2>", unsafe_allow_html=True)
        st.info("👥 User management dashboard coming soon!")
    
    elif admin_section == "📅 Block Dates":
        st.markdown("<h2 style='color: #00D9FF;'>📅 Block Calendar Dates</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date")
        with col2:
            end_date = st.date_input("End Date")
        
        reason = st.text_input("Reason (e.g., Exam Period, Holiday)")
        
        if st.button("🔒 Block Dates"):
            st.success(f"Block Dates {start_date} to {end_date} blocked!")

# ============================================
# ANALYTICS PAGE
# ============================================

elif page == "📊 Analytics":
    st.markdown("<h1 style='color: #00D9FF;'>📊 Analytics Dashboard</h1>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='color: #00D9FF;'>📈 Platform Overview</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🏛️ Total Colleges", "15", "+3 this month")
    
    with col2:
        st.metric("📅 Total Events", "250", "+45 this month")
    
    with col3:
        st.metric("👥 Active Students", "5000", "+800 this month")
    
    with col4:
        st.metric("✅ Total Registrations", "25000", "+5000 this month")
    
    st.markdown("---")
    
    st.markdown("<h2 style='color: #FFFFFF;'>◇ Charts & Insights</h2>", unsafe_allow_html=True)
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("""
        <div style='background: #1A4A8F;
                    padding: 20px;
                    border-radius: 15px;
                    border: 3px solid #00D9FF;
                    box-shadow: 0px 8px 30px rgba(0, 217, 255, 0.3), 0px 0px 20px rgba(26, 74, 143, 0.2);'>
            <h3 style='color: #FFFFFF;'>Events by Category</h3>
            <p style='color: #FFFFFF; font-weight: 500;'>◇ Chart: Tech (40%), Sports (25%), Seminar (20%), Other (15%)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with chart_col2:
        st.markdown("""
        <div style='background: #1A4A8F;
                    padding: 20px;
                    border-radius: 15px;
                    border: 3px solid #00D9FF;
                    box-shadow: 0px 8px 30px rgba(0, 217, 255, 0.3), 0px 0px 20px rgba(26, 74, 143, 0.2);'>
            <h3 style='color: #FFFFFF;'>Top Colleges</h3>
            <p style='color: #FFFFFF; font-weight: 500;'>✦ 1. MIT - 80 events<br>✦ 2. IIT - 75 events<br>✦ 3. BITS - 60 events</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div style='background: #1A4A8F;
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                color: #FFFFFF;
                border: 3px solid #00D9FF;
                box-shadow: 0px 10px 40px rgba(0, 217, 255, 0.3), 0px 0px 30px rgba(26, 74, 143, 0.2);'>
        <h3 style='color: #FFFFFF;'>📈 Growth Trend</h3>
        <p style='color: #FFFFFF; font-weight: 500;'>Events and registrations are growing 15% month-over-month!</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# LOGIN PAGE
# ============================================

elif page == "🔐 Login":
    st.markdown("<h1 style='text-align: center; color: #00D9FF;'>🔐 Welcome Back</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #FFFFFF; font-size: 1.1em;'>Login to your Campus Event Hub account</p>", unsafe_allow_html=True)
    
    st.markdown("")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='background: #1A4A8F;
                    padding: 40px;
                    border-radius: 15px;
                    border: 3px solid #00D9FF;
                    box-shadow: 0px 10px 40px rgba(0, 217, 255, 0.3), 0px 0px 20px rgba(26, 74, 143, 0.2);'>
        """, unsafe_allow_html=True)
        
        email = st.text_input("📧 Email Address", placeholder="your.email@college.com")
        password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
        
        st.markdown("")
        
        if st.button("🔓 Login"):
            if not email or not password:
                st.error("❌ Please fill in all fields")
            else:
                try:
                    # Call backend login endpoint
                    response = requests.post(
                        f"{BACKEND_URL}/api/auth/login",
                        json={"email": email, "password": password}
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.authenticated = True
                        st.session_state.user = data["user"]
                        st.session_state.token = data["token"]
                        st.success(f"✅ {data['message']}")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"❌ {response.json().get('detail', 'Login failed')}")
                except Exception as e:
                    st.error(f"❌ Connection error: {str(e)}")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("")
        st.markdown("<p style='text-align: center; color: #FFFFFF;'>Don't have an account? <a href='#' style='color: #00D9FF; font-weight: bold;'>Sign Up Now</a></p>", unsafe_allow_html=True)

# ============================================
# SIGN UP PAGE
# ============================================

elif page == "📝 Sign Up":
    st.markdown("<h1 style='text-align: center; color: #00D9FF;'>📝 Join Us Today</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #FFFFFF; font-size: 1.1em;'>Create your Campus Event Hub account</p>", unsafe_allow_html=True)
    
    st.markdown("")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='background: #1A4A8F;
                    padding: 40px;
                    border-radius: 15px;
                    border: 3px solid #00D9FF;
                    box-shadow: 0px 10px 40px rgba(0, 217, 255, 0.3), 0px 0px 20px rgba(26, 74, 143, 0.2);'>
        """, unsafe_allow_html=True)
        
        # Personal Information
        st.markdown("<h3 style='color: #00D9FF;'>👤 Personal Information</h3>", unsafe_allow_html=True)
        name = st.text_input("📛 Full Name", placeholder="John Doe")
        email = st.text_input("📧 Email Address", placeholder="your.email@college.com")
        
        st.markdown("")
        
        # College Information
        st.markdown("<h3 style='color: #00D9FF;'>🏛️ College Information</h3>", unsafe_allow_html=True)
        college = st.selectbox("🏛️ College", ["MIT", "IIT", "NIT", "BITS", "VIT", "Other"])
        year = st.selectbox("📅 Year", ["1st Year", "2nd Year", "3rd Year", "4th Year"])
        branch = st.selectbox("⚙️ Branch", ["CSE", "ECE", "Mechanical", "Civil", "Other"])
        
        st.markdown("")
        
        # Password
        st.markdown("<h3 style='color: #00D9FF;'>🔐 Security</h3>", unsafe_allow_html=True)
        password = st.text_input("🔑 Password", type="password", placeholder="Create a strong password")
        confirm_password = st.text_input("🔑 Confirm Password", type="password", placeholder="Re-enter password")
        
        st.markdown("")
        
        if st.button("✅ Create Account"):
            if not all([name, email, college, password, confirm_password]):
                st.error("❌ Please fill in all fields")
            elif password != confirm_password:
                st.error("❌ Passwords do not match")
            elif len(password) < 6:
                st.error("❌ Password must be at least 6 characters")
            else:
                try:
                    # Call backend registration endpoint
                    response = requests.post(
                        f"{BACKEND_URL}/api/auth/register",
                        json={
                            "name": name,
                            "email": email,
                            "password": password,
                            "college": college,
                            "year": int(year[0]),
                            "branch": branch,
                            "role": "student"
                        }
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.authenticated = True
                        st.session_state.user = data["user"]
                        st.session_state.token = data["token"]
                        st.success(f"✅ {data['message']}")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"❌ {response.json().get('detail', 'Registration failed')}")
                except Exception as e:
                    st.error(f"❌ Connection error: {str(e)}")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("")
        st.markdown("<p style='text-align: center; color: #FFFFFF;'>Already have an account? <a href='#' style='color: #00D9FF; font-weight: bold;'>Login Here</a></p>", unsafe_allow_html=True)

# ============================================
# ORGANIZER APPLICATION PAGE
# ============================================

elif page == "🏢 Apply Organizer":
    st.markdown("<h1 style='color: #00D9FF;'>🏢 Apply as Organizer</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #FFFFFF;'>Apply to host events on our platform</p>", unsafe_allow_html=True)
    
    st.markdown("")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='background: #1A4A8F;
                    padding: 40px;
                    border-radius: 15px;
                    border: 3px solid #00D9FF;
                    box-shadow: 0px 10px 40px rgba(0, 217, 255, 0.3), 0px 0px 20px rgba(26, 74, 143, 0.2);'>
        """, unsafe_allow_html=True)
        
        st.info("Fill the form below to apply as an organizer. Admin will review and approve.")
        
        st.markdown("")
        
        with st.form("organizer_application"):
            institute_name = st.text_input("Institute Name", placeholder="e.g., IIT Bangalore")
            city = st.text_input("City", placeholder="e.g., Bangalore")
            institute_type = st.selectbox("Type", ["College", "Company", "Club", "NGO"])
            contact_email = st.text_input("Contact Email", placeholder="contact@institute.com")
            reason = st.text_area("Why do you want to host events?", placeholder="Tell us about your organization...", height=100)
            
            st.markdown("")
            
            if st.form_submit_button("Submit Application", use_container_width=True):
                if not all([institute_name, city, contact_email, reason]):
                    st.error("Please fill all fields")
                else:
                    try:
                        response = requests.post(
                            f"{BACKEND_URL}/api/organizer/apply",
                            json={
                                "institute_name": institute_name,
                                "city": city,
                                "type_": institute_type,
                                "contact_email": contact_email,
                                "reason": reason
                            }
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            st.success("Application submitted successfully!")
                            st.info(f"Application ID: {data['application_id']}")
                            st.balloons()
                        else:
                            st.error(f"Error: {response.json().get('detail', 'Failed to submit')}")
                    except Exception as e:
                        st.error(f"Connection error: {str(e)}")
        
        st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# ADMIN REGISTRATION PAGE
# ============================================

elif page == "👑 Admin Register":
    st.markdown("<h1 style='text-align: center; color: #00D9FF;'>👑 Admin Registration</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #FFFFFF; font-size: 1.1em;'>Register as Platform Admin</p>", unsafe_allow_html=True)
    
    st.markdown("")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='background: #1A4A8F;
                    padding: 40px;
                    border-radius: 15px;
                    border: 3px solid #00D9FF;
                    box-shadow: 0px 10px 40px rgba(0, 217, 255, 0.3), 0px 0px 20px rgba(26, 74, 143, 0.2);'>
        """, unsafe_allow_html=True)
        
        st.warning("Only umra@jain.com can register as admin")
        
        st.markdown("")
        
        name = st.text_input("Name", placeholder="Admin Name")
        email = st.text_input("Email", placeholder="umra@jain.com")
        password = st.text_input("Password", type="password", placeholder="Create password")
        admin_code = st.text_input("Admin Code", type="password", placeholder="Enter admin code")
        
        st.markdown("")
        
        if st.button("Register as Admin", use_container_width=True):
            if not all([name, email, password, admin_code]):
                st.error("Please fill all fields")
            elif email != "umra@jain.com":
                st.error("Only umra@jain.com can be admin")
            else:
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/api/auth/admin-register",
                        json={
                            "name": name,
                            "email": email,
                            "password": password,
                            "admin_code": admin_code
                        }
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.authenticated = True
                        st.session_state.user = data["user"]
                        st.session_state.token = data["token"]
                        st.success("Admin registered successfully!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Registration failed')}")
                except Exception as e:
                    st.error(f"Connection error: {str(e)}")
        
        st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #1A2741 0%, #0F1D35 100%); border-top: 3px solid #00D9FF; border-radius: 10px;'>
    <p style='color: #FFFFFF; font-size: 1.1em;'>Campus Event Hub v1.0.0 | Made by Engineers for the Engineers</p>
    <p style='font-size: 0.9em; color: #FFFFFF;'>© 2026 All Rights Reserved | Privacy Policy | Terms of Service</p>
</div>
""", unsafe_allow_html=True)
