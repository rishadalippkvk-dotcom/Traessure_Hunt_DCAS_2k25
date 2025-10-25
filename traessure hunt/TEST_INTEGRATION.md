# 🧪 Testing Django Integration - Step by Step

## 🎯 Quick Test Guide

This guide will help you verify that the Django backend and Streamlit frontend are properly integrated.

---

## ✅ Pre-Test Checklist

Before testing, make sure you have:
- [ ] Django backend installed (`backend/` directory exists)
- [ ] Virtual environment created in `backend/venv/`
- [ ] Database file created (`backend/treasure_hunt.db`)
- [ ] Streamlit installed
- [ ] Both terminals ready

---

## 🚀 Test 1: Start Django Backend

### Step 1.1: Open Terminal
```powershell
cd "c:\Users\DELL\Desktop\traessure hunt\backend"
```

### Step 1.2: Activate Virtual Environment
```powershell
.\venv\Scripts\Activate
```
**Expected:** Your prompt should show `(venv)` prefix

### Step 1.3: Start Django Server
```powershell
python manage.py runserver
```

**Expected Output:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
December 24, 2024 - 12:00:00
Django version 5.0.1, using settings 'treasure_hunt.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Step 1.4: Verify Backend is Running
Open browser and go to: `http://localhost:8000/admin`

**Expected:** Django admin login page appears

✅ **If you see the admin page, backend is running correctly!**

---

## 🎨 Test 2: Start Streamlit Frontend

### Step 2.1: Open NEW Terminal (keep Django running)
```powershell
cd "c:\Users\DELL\Desktop\traessure hunt"
```

### Step 2.2: Run Streamlit
```powershell
streamlit run final2.py
```

**Expected Output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

### Step 2.3: Browser Opens Automatically
Should show the FOSS Treasure Hunt login page

✅ **If the app opens, frontend is working!**

---

## 🧑‍💻 Test 3: Register New User

### Step 3.1: Click "Register" Tab
In the Streamlit app, click the second tab labeled "Register"

### Step 3.2: Fill Registration Form
```
Username: testuser1
Email: test1@example.com
Password: test123456
Confirm Password: test123456
```

### Step 3.3: Click "CREATE ACCOUNT"

**Expected Behavior:**
1. Spinner appears: "🔄 Creating your account in database..."
2. Success message: "✅ Registration successful! Welcome, testuser1!"
3. Balloons animation appears
4. Celebration GIF shows
5. Message: "🎮 Starting your FOSS adventure..."
6. Page reloads and you're logged in
7. Game starts

✅ **If you see success message and auto-login, registration works!**

---

## 🔐 Test 4: Verify User in Database

### Step 4.1: Check Django Admin
1. Go to `http://localhost:8000/admin`
2. Login with superuser (if you created one)
3. Click "Users" under "AUTHENTICATION"
4. Look for "testuser1" in the list

**OR use Django shell:**

### Step 4.2: Use Django Shell
In the Django terminal (not Streamlit):
```powershell
python manage.py shell
```

Then run:
```python
from authentication.models import User
User.objects.all()
# Should show: <QuerySet [<User: testuser1>]>

user = User.objects.get(username='testuser1')
print(f"Username: {user.username}")
print(f"Email: {user.email}")
print(f"Score: {user.total_score}")
print(f"Rank: {user.rank}")
```

**Expected Output:**
```
Username: testuser1
Email: test1@example.com
Score: 0
Rank: 🔰 BEGINNER CODER
```

✅ **If you see the user, database integration works!**

---

## 🔑 Test 5: Login with Existing User

### Step 5.1: Logout (if logged in)
Click "Logout" button in the sidebar

### Step 5.2: Click "Login" Tab
Switch to the first tab

### Step 5.3: Enter Credentials
```
Username: testuser1
Password: test123456
```

### Step 5.4: Click "LOGIN"

**Expected Behavior:**
1. Spinner: "🔄 Authenticating with database..."
2. Success message: "✅ Welcome, testuser1!"
3. Balloons animation
4. Celebration GIF
5. Auto-login to game

✅ **If login succeeds, authentication works!**

---

## ⚠️ Test 6: Test Error Handling

### Test 6.1: Duplicate Username
Try to register again with:
```
Username: testuser1  (same as before)
Email: another@example.com
Password: test123456
```

**Expected:**
❌ Error message: "A user with that username already exists."

### Test 6.2: Invalid Email
Try to register with:
```
Username: testuser2
Email: notanemail  (missing @ and .)
Password: test123456
```

**Expected:**
❌ Error message: "⚠️ Please enter a valid email address!"

### Test 6.3: Password Mismatch
Try to register with:
```
Username: testuser2
Email: test2@example.com
Password: test123456
Confirm Password: different123  (different)
```

**Expected:**
❌ Error message: "⚠️ Passwords do not match!"

### Test 6.4: Wrong Login Password
Try to login with:
```
Username: testuser1
Password: wrongpassword
```

**Expected:**
❌ Error message: "❌ Invalid username or password"

✅ **If all errors show correctly, validation works!**

---

## 🔌 Test 7: Offline Mode (Backend Down)

### Step 7.1: Stop Django Backend
In Django terminal, press `Ctrl+C`

### Step 7.2: Try to Register
Try registering a new user in Streamlit

**Expected:**
⚠️ Warning message: "Backend offline. Account created in offline mode only."
💡 Info: "Your progress won't be saved to database until backend is running."

### Step 7.3: Try to Login
Use fallback password: `foss2024`

**Expected:**
⚠️ Warning: "Backend offline. Logged in offline mode."

✅ **If offline mode works, fallback is functioning!**

---

## 📊 Test 8: Check Backend Logs

### Step 8.1: Watch Django Terminal
While registering/logging in, watch the Django terminal

**Expected Log Entries:**
```
[24/Dec/2024 12:30:15] "POST /api/auth/register/ HTTP/1.1" 201 256
[24/Dec/2024 12:30:45] "POST /api/auth/login/ HTTP/1.1" 200 198
```

The `201` and `200` status codes mean success!

✅ **If you see these logs, API is communicating!**

---

## 🎯 Success Criteria

All tests passed if you see:

- ✅ Django backend starts without errors
- ✅ Streamlit frontend loads the login page
- ✅ New user registration succeeds
- ✅ User appears in Django database
- ✅ Login with registered user works
- ✅ Invalid inputs show error messages
- ✅ Offline mode works when backend is down
- ✅ Backend logs show API requests

---

## 🐛 Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'rest_framework'"
**Solution:**
```powershell
cd backend
.\venv\Scripts\Activate
pip install djangorestframework
```

### Issue: "Port 8000 is already in use"
**Solution:**
```powershell
# Find and kill process using port 8000
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

### Issue: "Cannot connect to backend"
**Solution:**
1. Make sure Django is running on http://localhost:8000
2. Check firewall isn't blocking port 8000
3. Try accessing http://localhost:8000/admin manually

### Issue: "streamlit: command not found"
**Solution:**
```powershell
pip install streamlit
```

### Issue: Registration succeeds but user not in database
**Solution:**
1. Check Django terminal for errors
2. Verify database file exists: `backend/treasure_hunt.db`
3. Try: `python manage.py migrate`

---

## 📈 Advanced Testing

### Test API Directly with cURL
```powershell
# Test Registration
curl -X POST http://localhost:8000/api/auth/register/ ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"curltest\",\"email\":\"curl@test.com\",\"password\":\"test123\",\"password_confirm\":\"test123\"}"

# Test Login
curl -X POST http://localhost:8000/api/auth/login/ ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"curltest\",\"password\":\"test123\"}"
```

### Test with Python Requests
```python
import requests

# Register
response = requests.post('http://localhost:8000/api/auth/register/', json={
    'username': 'pythontest',
    'email': 'python@test.com',
    'password': 'test123',
    'password_confirm': 'test123'
})
print(response.json())

# Login
response = requests.post('http://localhost:8000/api/auth/login/', json={
    'username': 'pythontest',
    'password': 'test123'
})
print(response.json())
```

---

## 🎊 Integration Complete!

If all tests pass, your Django backend is fully integrated with the Streamlit frontend!

**You now have:**
- ✅ Persistent user accounts
- ✅ Secure authentication
- ✅ Database storage
- ✅ Token-based sessions
- ✅ Error handling
- ✅ Offline fallback

**Ready to play the FOSS Treasure Hunt!** 🎮

---

**Need Help?**
- Check `DJANGO_INTEGRATION_COMPLETE.md` for full documentation
- Check `backend/API_DOCUMENTATION.md` for API reference
- Check Django logs for error details
