# 🎉 Campus Event Hub

A full-stack web platform for discovering, creating, and managing campus events across Indian engineering colleges.

## 🚀 Live Demo
- Frontend: [Coming Soon]
- Backend API: [Coming Soon]

## 📸 Features

### 👨‍🎓 Students
- Browse and search events by category
- Register for events
- Bookmark favorite events
- Earn coins and badges
- Personal dashboard

### 🎯 Event Organizers
- Create events for admin approval
- Track registrations
- Manage event details

### ⚙️ Admin
- Approve/reject events
- Manage organizer applications
- Analytics dashboard
- User management
- Block calendar dates

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit (Python) |
| Backend | FastAPI (Python) |
| Database | Supabase (PostgreSQL) |
| Auth | JWT Tokens + Bcrypt |
| Hosting | Render + Streamlit Cloud |

## 📁 Project Structure
campus-event-hub/
├── backend/
│   ├── main.py        # FastAPI routes
│   └── database.py    # Supabase queries
├── frontend/
│   └── app.py         # Streamlit UI
├── requirements.txt
└── .env               # Environment variables

## ⚙️ Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/campus-event-hub.git
cd campus-event-hub
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create `.env` file
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
JWT_SECRET=your_jwt_secret

### 4. Run Backend
```bash
python backend/main.py
```

### 5. Run Frontend
```bash
streamlit run frontend/app.py
```

## 🔐 Demo Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | umra@jain.com | admin@123 |
| Student | demo@student.com | demo@123 |

## 👥 Team
Built with ❤️ for hackathon by Umra Jamadar

## 📄 License
MIT License