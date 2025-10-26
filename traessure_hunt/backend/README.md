# FOSS Treasure Hunt - Django Backend

🏆 **Backend API for the FOSS Treasure Hunt Game**

## 📋 Features

- ✅ User Authentication & Registration
- ✅ Game Session Management
- ✅ Level Progress Tracking
- ✅ Leaderboard System
- ✅ Achievements System
- ✅ RESTful API with Token Authentication
- ✅ SQLite Database (easy to upgrade to PostgreSQL)
- ✅ Django Admin Panel

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Create Database

```bash
# Run migrations to create database tables
python manage.py makemigrations
python manage.py migrate
```

### 3. Setup Default Data

```bash
# Create default achievements
python setup_database.py
```

### 4. Create Admin User

```bash
python manage.py createsuperuser
```

### 5. Start Development Server

```bash
python manage.py runserver
```

The API will be available at: `http://localhost:8000`

## 📡 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register/` | Register new user | No |
| POST | `/api/auth/login/` | Login user | No |
| POST | `/api/auth/logout/` | Logout user | Yes |
| GET | `/api/auth/profile/` | Get user profile | Yes |

### Game Management

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/game/start/` | Start new game session | Yes |
| GET | `/api/auth/game/session/` | Get active session | Yes |
| PUT | `/api/auth/game/session/<id>/` | Update session | Yes |
| POST | `/api/auth/game/level/` | Save level progress | Yes |
| GET | `/api/auth/game/session/<id>/progress/` | Get session progress | Yes |

### Leaderboard

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/auth/leaderboard/` | Get top players | No |
| POST | `/api/auth/leaderboard/submit/` | Submit score | Yes |

### Achievements

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/auth/achievements/` | Get user achievements | Yes |
| GET | `/api/auth/achievements/all/` | List all achievements | No |

## 🔑 Authentication

The API uses Token Authentication. After login, include the token in requests:

```
Authorization: Token <your-token-here>
```

## 📊 Database Models

### User
- Custom user model extending Django's AbstractUser
- Tracks total score, games played, best streak, rank

### GameSession
- Tracks individual game sessions
- Stores current progress, score, streaks, combo multiplier

### LevelProgress
- Tracks progress for each level in a session
- Records attempts, hints used, time spent

### Achievement
- Defines available achievements
- Contains name, description, icon, points

### UserAchievement
- Links users to unlocked achievements
- Tracks when achievements were earned

### Leaderboard
- Stores completed game scores
- Ranks players by score and time

## 🎮 Example API Usage

### Register User
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "player1",
    "email": "player1@example.com",
    "password": "foss2024",
    "password_confirm": "foss2024"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "player1",
    "password": "foss2024"
  }'
```

### Start Game Session
```bash
curl -X POST http://localhost:8000/api/auth/game/start/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

## 🔧 Admin Panel

Access the Django admin panel at: `http://localhost:8000/admin/`

You can manage:
- Users
- Game Sessions
- Level Progress
- Achievements
- Leaderboard

## 🗄️ Database Location

SQLite database is stored at: `backend/treasure_hunt.db`

## 🔄 Database Reset

To reset the database:

```bash
# Delete the database file
rm treasure_hunt.db

# Delete migrations (optional)
rm authentication/migrations/0*.py

# Recreate migrations and database
python manage.py makemigrations
python manage.py migrate
python setup_database.py
python manage.py createsuperuser
```

## 🛠️ Development

### Run Tests
```bash
python manage.py test
```

### Create Migrations
```bash
python manage.py makemigrations
```

### Apply Migrations
```bash
python manage.py migrate
```

## 📦 Project Structure

```
backend/
├── manage.py                          # Django management script
├── requirements.txt                    # Python dependencies
├── setup_database.py                   # Database initialization script
├── treasure_hunt.db                    # SQLite database (created after migration)
├── treasure_hunt_backend/
│   ├── __init__.py
│   ├── settings.py                     # Django settings
│   ├── urls.py                         # Main URL configuration
│   ├── asgi.py
│   └── wsgi.py
└── authentication/
    ├── __init__.py
    ├── models.py                       # Database models
    ├── views.py                        # API views
    ├── serializers.py                  # DRF serializers
    ├── urls.py                         # App URL configuration
    ├── admin.py                        # Admin panel configuration
    └── apps.py
```

## 🌐 CORS Configuration

The backend is configured to accept requests from Streamlit (port 8501).
Modify `settings.py` to add more origins if needed.

## 🔐 Security Notes

**⚠️ For Production:**
- Change `SECRET_KEY` in settings.py
- Set `DEBUG = False`
- Use PostgreSQL instead of SQLite
- Configure proper `ALLOWED_HOSTS`
- Use environment variables for sensitive data
- Enable HTTPS
- Use secure password hashing

## 📝 License

Created for Software Freedom Day 2024 🎉

## 🤝 Integration with Streamlit

The backend is designed to work with the Streamlit frontend.
See the updated Streamlit app for integration code.

---

Made with ❤️ for FOSS Community
