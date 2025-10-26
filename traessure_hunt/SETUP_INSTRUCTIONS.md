# 🏆 FOSS Treasure Hunt - Complete Setup Guide

## 📋 Table of Contents
1. [Backend Setup](#backend-setup)
2. [Database Creation](#database-creation)
3. [Frontend Integration](#frontend-integration)
4. [Running the Application](#running-the-application)

---

## 🔧 Backend Setup

### Step 1: Navigate to Backend Directory

```bash
cd "c:\Users\DELL\Desktop\traessure hunt\backend"
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- Django 5.0.1
- djangorestframework 3.14.0
- django-cors-headers 4.3.1
- djangorestframework-simplejwt 5.3.1
- python-dotenv 1.0.0

### Step 3: Create Database Tables

```bash
# Generate migration files
python manage.py makemigrations authentication

# Apply migrations to create database
python manage.py migrate
```

This will create `treasure_hunt.db` (SQLite database) in the backend directory.

### Step 4: Load Default Data

```bash
# Create default achievements
python setup_database.py
```

### Step 5: Create Admin Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create:
- Username: (your choice)
- Email: (optional)
- Password: (your choice)

### Step 6: Start Django Backend Server

```bash
python manage.py runserver
```

The backend API will be running at: **http://localhost:8000**

---

## 🗄️ Database Creation

### What Gets Created:

The database (`treasure_hunt.db`) includes the following tables:

1. **users** - Player accounts with stats
   - username, email, password (hashed)
   - total_score, games_played, best_streak
   - rank, created_at, last_login_at

2. **game_sessions** - Individual game sessions
   - user, session_token
   - current_level, score, hints_used
   - streak, combo_multiplier
   - riddle_solved, finished status

3. **level_progress** - Progress for each level
   - session, level_number
   - category, difficulty, points_earned
   - attempts, hints_used
   - completion status, time_spent

4. **achievements** - Available achievements
   - name, description, icon, points

5. **user_achievements** - Unlocked achievements
   - user, achievement, unlocked_at

6. **leaderboard** - Top player scores
   - user, session, final_score
   - total_time, rank_achieved
   - accuracy, speed_score

### Verify Database Creation:

```bash
# Check if database file exists
dir treasure_hunt.db

# Or open Django shell to inspect
python manage.py shell
```

In the shell:
```python
from authentication.models import User, Achievement
print(f"Users: {User.objects.count()}")
print(f"Achievements: {Achievement.objects.count()}")
```

---

## 🎮 Frontend Integration

The Streamlit frontend (final2.py) is already set up with login functionality.

### Current Features:
✅ Login page with authentication
✅ Session state management
✅ User tracking
✅ Password protection (default: foss2024)

### To Integrate with Django Backend:

You would need to modify `final2.py` to make API calls to Django. This involves:

1. Adding `requests` library to make HTTP calls
2. Replacing Streamlit session state with Django API calls
3. Storing authentication tokens
4. Syncing game progress to the database

**Example integration** (for reference):

```python
import requests

API_URL = "http://localhost:8000/api/auth"

def django_login(username, password):
    response = requests.post(
        f"{API_URL}/login/",
        json={"username": username, "password": password}
    )
    if response.status_code == 200:
        data = response.json()
        return data['token'], data['user']
    return None, None
```

---

## 🚀 Running the Application

### Option 1: Streamlit Only (Current Setup)

```bash
# From main directory
streamlit run final2.py
```

Access at: **http://localhost:8501**

**Features:**
- ✅ Login page with hardcoded password
- ✅ Full treasure hunt game
- ✅ Session-based state management
- ❌ No persistent database
- ❌ No user registration

### Option 2: Django Backend + Streamlit Frontend

**Terminal 1 - Start Django Backend:**
```bash
cd backend
python manage.py runserver
```

**Terminal 2 - Start Streamlit Frontend:**
```bash
streamlit run final2.py
```

**To enable full integration**, you'll need to modify `final2.py` to use the Django API.

---

## 🔑 API Testing

### Test with PowerShell:

#### 1. Register a New User
```powershell
$body = @{
    username = "player1"
    email = "player1@example.com"
    password = "foss2024"
    password_confirm = "foss2024"
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/auth/register/" -Body $body -ContentType "application/json"
```

#### 2. Login
```powershell
$body = @{
    username = "player1"
    password = "foss2024"
} | ConvertTo-Json

$response = Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/auth/login/" -Body $body -ContentType "application/json"
$token = $response.token
Write-Host "Token: $token"
```

#### 3. Get User Profile
```powershell
$headers = @{
    "Authorization" = "Token $token"
}

Invoke-RestMethod -Method Get -Uri "http://localhost:8000/api/auth/profile/" -Headers $headers
```

#### 4. Start Game Session
```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/auth/game/start/" -Headers $headers
```

---

## 📊 Admin Panel

Access Django admin panel at: **http://localhost:8000/admin/**

**Login with superuser credentials** created in Step 5.

### What You Can Do:
- ✅ View all users and their stats
- ✅ Monitor game sessions
- ✅ Track level progress
- ✅ Manage achievements
- ✅ View leaderboard
- ✅ Create/edit/delete data

---

## 🛠️ Troubleshooting

### Issue: Migrations not creating tables

```bash
# Force create tables
python manage.py migrate --run-syncdb

# Or reset database
del treasure_hunt.db
python manage.py makemigrations authentication
python manage.py migrate
```

### Issue: Port already in use

```bash
# Django on different port
python manage.py runserver 8001

# Streamlit on different port
streamlit run final2.py --server.port 8502
```

### Issue: CORS errors

Edit `backend/treasure_hunt_backend/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8501",
    "http://localhost:8502",  # Add your port
]
```

### Issue: Authentication errors

```bash
# Create new token for user
python manage.py shell

>>> from rest_framework.authtoken.models import Token
>>> from authentication.models import User
>>> user = User.objects.get(username='yourname')
>>> Token.objects.filter(user=user).delete()
>>> token = Token.objects.create(user=user)
>>> print(token.key)
```

---

## 📁 Project Structure

```
traessure hunt/
├── final2.py                          # Streamlit frontend
├── backend/
│   ├── manage.py                      # Django management
│   ├── requirements.txt               # Dependencies
│   ├── setup.bat                      # Windows setup script
│   ├── setup_database.py              # Database initialization
│   ├── treasure_hunt.db               # SQLite database (created after setup)
│   ├── treasure_hunt_backend/         # Django project
│   │   ├── settings.py                # Configuration
│   │   ├── urls.py                    # URL routing
│   │   ├── wsgi.py, asgi.py
│   │   └── __init__.py
│   └── authentication/                # Django app
│       ├── models.py                  # Database models
│       ├── views.py                   # API endpoints
│       ├── serializers.py             # Data serialization
│       ├── urls.py                    # App URLs
│       ├── admin.py                   # Admin config
│       ├── apps.py
│       └── migrations/                # Database migrations
└── SETUP_INSTRUCTIONS.md              # This file
```

---

## ✅ Quick Start Checklist

- [ ] Navigate to backend directory
- [ ] Install requirements: `pip install -r requirements.txt`
- [ ] Create migrations: `python manage.py makemigrations authentication`
- [ ] Apply migrations: `python manage.py migrate`
- [ ] Setup data: `python setup_database.py`
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Start Django: `python manage.py runserver`
- [ ] (In another terminal) Start Streamlit: `streamlit run final2.py`
- [ ] Access admin panel: http://localhost:8000/admin/
- [ ] Access game: http://localhost:8501/

---

## 🎯 Next Steps

1. **Test the Backend API** using the PowerShell commands above
2. **Create some test users** via the API or admin panel
3. **Modify final2.py** to integrate with Django backend (optional)
4. **Play the game!** 🎮

---

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all dependencies are installed
3. Ensure both ports (8000, 8501) are available
4. Check Django logs for errors

---

Made with ❤️ for Software Freedom Day 2024! 🎉
