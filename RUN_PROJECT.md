# 🚀 HOW TO RUN THE PROJECT

## ✅ Status Check
- Backend: ✅ Working
- Frontend: ✅ Working
- Database: ✅ Connected to Supabase

---

## 🏃 Quick Start (2 Steps)

### Step 1: Start Backend (Terminal 1)
```bash
cd campus-event-hub
python backend/main.py
```

**Expected Output:**
```
🚀 Starting FastAPI server on http://localhost:8000
📚 API Docs available at http://localhost:8000/docs
👤 Admin Email: umra@jain.com
```

### Step 2: Start Frontend (Terminal 2)
```bash
cd campus-event-hub
streamlit run frontend/app.py
```

**Expected Output:**
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

---

## 🌐 Access URLs

| Component | URL |
|-----------|-----|
| Frontend | http://localhost:8501 |
| Backend | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |

---

## 🧪 Quick Test

### Test 1: Admin Registration
```bash
curl -X POST http://localhost:8000/api/auth/admin-register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Umra",
    "email": "umra@jain.com",
    "password": "admin@123",
    "admin_code": "admin123"
  }'
```

### Test 2: Student Registration
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John",
    "email": "john@example.com",
    "password": "student@123",
    "college": "MIT",
    "year": 2,
    "branch": "CSE"
  }'
```

---

## 📋 What You Can Do Now

### In Frontend (http://localhost:8501)
1. ✅ Register as student
2. ✅ Login
3. ✅ Browse events
4. ✅ View dashboard
5. ✅ See admin panel

### In Backend (http://localhost:8000/docs)
1. ✅ Test all 14 API endpoints
2. ✅ Register admin
3. ✅ Register student
4. ✅ Create events
5. ✅ Approve events

---

## ⚠️ If You Get Errors

### Error: "Connection refused"
- Make sure backend is running on Terminal 1
- Check if port 8000 is free

### Error: "Supabase connection failed"
- Check .env file has correct credentials
- Verify SUPABASE_URL and SUPABASE_KEY

### Error: "Port already in use"
- Backend: Change FASTAPI_PORT in .env
- Frontend: Use `streamlit run app.py --server.port 8502`

---

## 🎯 Next Steps

1. ✅ Start backend
2. ✅ Start frontend
3. ✅ Test registration
4. ✅ Test login
5. ✅ Test event creation
6. ✅ Test event approval

---

## 📞 Quick Reference

### Admin Credentials
```
Email: umra@jain.com
Code: admin123
```

### Test Student
```
Email: john@example.com
Password: student@123
```

---

## ✅ Everything Working?

If you see:
- ✅ Backend running on http://localhost:8000
- ✅ Frontend running on http://localhost:8501
- ✅ Can register and login
- ✅ Can create events

**Then you're ready for Phase 3!**

---

## 🚀 Ready?

Start the backend and frontend now!
