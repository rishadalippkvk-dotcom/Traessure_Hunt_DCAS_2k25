# 🚀 Quick Start Guide - FOSS Treasure Hunt

## ⚡ Start Both Servers (Recommended)

### Option 1: Using PowerShell Scripts (Easiest!)

**Terminal 1 - Start Backend:**
```powershell
.\start_backend.ps1
```

**Terminal 2 - Start Frontend:**
```powershell
.\start_frontend.ps1
```

### Option 2: Manual Commands

**Terminal 1 - Django Backend:**
```powershell
cd backend
.\venv\Scripts\Activate
python manage.py runserver
```

**Terminal 2 - Streamlit Frontend:**
```powershell
streamlit run final2.py
```

---

## 🎮 Access the Application

Once both servers are running:

- **Streamlit App:** http://localhost:8501 (opens automatically)
- **Django Admin:** http://localhost:8000/admin
- **API Base:** http://localhost:8000/api/auth/

---

## 👤 Create Your First Account

1. Open http://localhost:8501
2. Click **"Register"** tab
3. Fill in:
   - Username: `your_username` (minimum 3 characters)
   - Email: `your@email.com` (valid format)
   - Password: `your_password` (minimum 6 characters)
   - Confirm Password: (same as above)
4. Click **"CREATE ACCOUNT"** 🌟
5. You'll be automatically logged in!

---

## 🔑 Login with Existing Account

1. Click **"Login"** tab
2. Enter your username and password
3. Click **"LOGIN"** ✨
4. Start playing!

---

## 📋 What's Integrated?

✅ **Full Django Backend**
- User authentication with secure password hashing
- SQLite database for persistent storage
- Token-based authentication
- 13 REST API endpoints

✅ **Streamlit Frontend**
- Beautiful login/registration interface
- Real-time backend integration
- Offline fallback mode
- Auto-login after registration

✅ **Features**
- Secure user accounts
- Password validation
- Email validation
- Duplicate username detection
- Error handling with helpful messages

---

## 🛠️ Troubleshooting

### "Cannot connect to backend"
**Fix:** Start Django backend first
```powershell
cd backend
.\venv\Scripts\Activate
python manage.py runserver
```

### "ModuleNotFoundError"
**Fix:** Install dependencies
```powershell
cd backend
.\venv\Scripts\Activate
pip install django djangorestframework django-cors-headers
```

### "Streamlit command not found"
**Fix:** Install Streamlit
```powershell
pip install streamlit requests
```

---

## 📚 Documentation Files

- **DJANGO_INTEGRATION_COMPLETE.md** - Complete integration guide
- **TEST_INTEGRATION.md** - Step-by-step testing guide
- **backend/API_DOCUMENTATION.md** - Full API reference
- **backend/CREATE_USER_MANUAL.txt** - User creation methods

---

## 🎯 Test Users

You can create test users with these credentials:

```
Username: alice
Email: alice@example.com
Password: alice123

Username: bob
Email: bob@example.com
Password: bob12345

Username: charlie
Email: charlie@example.com
Password: charlie789
```

---

## 💡 Tips

1. **Always start Django backend first** before Streamlit
2. **Keep both terminals open** while playing
3. **Check Django logs** in Terminal 1 for API requests
4. **Use offline mode** if backend is unavailable (password: `foss2024`)
5. **Registered users are saved permanently** in the database

---

## 🔐 Default Credentials

**Offline Mode (when backend is down):**
- Any username
- Password: `foss2024`

**Backend Mode (normal):**
- Use your registered username and password

---

## 🎊 You're All Set!

Start playing the FOSS Treasure Hunt and test your open-source knowledge! 🎮

**Made with ❤️ for Software Freedom Day**
