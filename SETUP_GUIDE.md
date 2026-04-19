# Campus Event Hub - Setup & Implementation Guide

## ✅ What We've Completed

### Phase 1 & 2: Skeleton + Auth (DONE)
- Project structure created
- Packages installed
- Supabase database configured
- Student registration & login
- JWT token authentication

### Phase 2.5: NEW - Supabase Migration + Admin System (JUST COMPLETED)

---

## 🔄 SUPABASE MIGRATION - What Changed

### Before (In-Memory):
```python
users_db = {}  # Data lost on server restart
events_db = {}  # Data lost on server restart
```

### After (Supabase):
```python
Database.create_user(...)  # Saved to cloud database
Database.get_user_by_email(...)  # Retrieved from cloud
```

**Benefits:**
- ✅ Data persists permanently
- ✅ Can access from multiple servers
- ✅ Real production-ready database
- ✅ Automatic backups

---

## 👤 ADMIN REGISTRATION - How It Works

### 3 User Roles Now:

#### 1. **STUDENT** (Regular User)
- Registers with: name, email, password, college, year, branch
- Can browse and register for events
- Cannot create events

#### 2. **ORGANIZER** (College/Company)
- Must apply first (pending status)
- Admin reviews and approves
- After approval, can create events
- Events go to pending for admin approval

#### 3. **ADMIN** (Super Admin)
- Special registration with email: `umra@jain.com`
- Requires admin code: `admin123` (in .env file)
- Can approve/reject organizer applications
- Can approve/reject events
- Events created by admin are auto-approved

---

## 🔐 Admin Registration Flow

### Step 1: Admin Registers
```
POST /api/auth/admin-register
{
  "name": "Umra",
  "email": "umra@jain.com",
  "password": "securepassword",
  "admin_code": "admin123"
}
```

### Step 2: System Checks
- ✅ Email must be `umra@jain.com`
- ✅ Admin code must match (from .env)
- ✅ Creates user with role="admin"
- ✅ Returns JWT token

---

## 📋 Event Approval Workflow

### Scenario 1: Admin Creates Event
```
POST /api/events/create
{
  "name": "Tech Talk",
  "organizer_email": "umra@jain.com",  ← Admin email
  ...
}
```
**Result:** Event status = "approved" (auto-approved)

### Scenario 2: Organizer Creates Event
```
POST /api/events/create
{
  "name": "Workshop",
  "organizer_email": "college@example.com",  ← Organizer email
  ...
}
```
**Result:** Event status = "pending" (needs admin approval)

### Scenario 3: Admin Approves Event
```
POST /api/admin/approve-event
{
  "event_id": 1,
  "action": "approve"  ← or "reject"
}
```
**Result:** Event status changes to "approved" or "rejected"

---

## 🏢 Organizer Application Workflow

### Step 1: College Applies
```
POST /api/organizer/apply
{
  "institute_name": "MIT",
  "city": "Bangalore",
  "type_": "College",
  "contact_email": "mit@example.com",
  "reason": "We want to host events"
}
```
**Result:** Application saved with status="pending"

### Step 2: Admin Reviews
```
GET /api/admin/organizer-applications
```
**Result:** List of all pending applications

### Step 3: Admin Approves/Rejects
```
POST /api/admin/approve-organizer
{
  "college_id": 1,
  "action": "approve"  ← or "reject"
}
```
**Result:** College status changes to "approved" or "rejected"

---

## 📊 Database Tables (Supabase)

### users
```
id, name, email, password_hash, college, year, branch, 
role (student/organizer/admin), coins, badge, created_at
```

### events
```
id, title, description, college_id, category, date, time, 
venue, max_participants, status (pending/approved/rejected), created_at
```

### registrations
```
id, student_id, event_id, status (registered/participated/won), created_at
```

### colleges
```
id, name, city, type, contact_email, 
status (pending/approved/rejected), created_at
```

### bookmarks
```
id, student_id, event_id, created_at
```

---

## 🚀 How to Test

### 1. Register as Admin
```
Email: umra@jain.com
Password: anypassword
Admin Code: admin123
```

### 2. Register as Student
```
Email: student@example.com
Password: anypassword
College: MIT
Year: 2
Branch: CSE
```

### 3. Apply as Organizer
```
Institute: IIT
City: Bangalore
Type: College
Contact: iit@example.com
```

### 4. Admin Approves Organizer
- Go to admin panel
- See pending applications
- Click approve

### 5. Organizer Creates Event
```
Event Name: Python Workshop
Date: 2026-04-20
Time: 10:00
Seats: 50
```
**Status:** pending (waiting for admin approval)

### 6. Admin Approves Event
- Go to admin panel
- See pending events
- Click approve

### 7. Student Registers for Event
- Browse events
- Click register
- Event appears in dashboard

---

## 🔑 Key Differences: Student vs Admin Registration

| Feature | Student | Admin |
|---------|---------|-------|
| Email | Any email | Must be umra@jain.com |
| College | Required | Set to "Admin" |
| Year | Required (1-4) | Set to 0 |
| Branch | Required | Set to "Admin" |
| Admin Code | Not needed | Required (admin123) |
| Event Creation | No | Yes (auto-approved) |
| Can Approve Events | No | Yes |
| Can Approve Organizers | No | Yes |

---

## 📝 Next Steps (Phase 3)

1. Update frontend to show admin registration page
2. Update frontend to show organizer application form
3. Update frontend admin panel to show pending events
4. Update frontend admin panel to show pending organizers
5. Add event approval buttons in admin panel
6. Add organizer approval buttons in admin panel

---

## ⚠️ Important Notes

1. **Admin Code:** Change `admin123` in .env file for production
2. **Admin Email:** Only `umra@jain.com` can register as admin
3. **Event Status:** 
   - Admin events: auto-approved
   - Organizer events: pending (need approval)
4. **Supabase:** Make sure tables exist in your Supabase project
5. **JWT Token:** Valid for 24 hours

---

## 🐛 Troubleshooting

### Error: "Email already registered"
- User already exists in database
- Try different email

### Error: "Invalid admin code"
- Admin code doesn't match .env file
- Check ADMIN_CODE in .env

### Error: "Only authorized email can register as admin"
- Email is not umra@jain.com
- Only this email can be admin

### Error: "Failed to create user"
- Supabase connection issue
- Check SUPABASE_URL and SUPABASE_KEY in .env

---

## 📞 Support

If you have questions about:
- Admin registration: Check ADMIN_EMAIL and ADMIN_CODE in .env
- Event approval: Check event status in database
- Organizer applications: Check colleges table status
