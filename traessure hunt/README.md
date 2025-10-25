# 🏆 FOSS Treasure Hunt - Full Stack Application

## 🎮 Interactive FOSS Knowledge Game with Django Backend

A gamified treasure hunt experience to test your Free and Open Source Software (FOSS) knowledge, featuring a complete Django REST API backend for user authentication and progress tracking.

---

## ⚡ Quick Start

### Start the Application:

**Terminal 1 - Django Backend:**
```powershell
.\start_backend.ps1
```

**Terminal 2 - Streamlit Frontend:**
```powershell
.\start_frontend.ps1
```

### Access:
- **Play Game:** http://localhost:8501
- **Admin Panel:** http://localhost:8000/admin

---

## 🚀 Features

### 🎯 Game Features
- ✅ **10 Challenging Levels** with FOSS riddles
- ✅ **Security Challenges** at every stage
- ✅ **Hint System** with point deductions
- ✅ **Combo Multipliers** for consecutive correct answers
- ✅ **Achievement System** with 8 unique badges
- ✅ **Leaderboard** with ranking system
- ✅ **Beautiful Animations** and visual effects

### 🔐 Authentication Features
- ✅ **User Registration** with email validation
- ✅ **Secure Login** with password hashing (PBKDF2)
- ✅ **Token-based Authentication**
- ✅ **Persistent User Accounts** in Django database
- ✅ **Offline Fallback Mode** when backend unavailable
- ✅ **Auto-login** after registration

### 💾 Backend Features
- ✅ **Django 5.0.1** REST API
- ✅ **SQLite Database** for data persistence
- ✅ **13 API Endpoints** for game management
- ✅ **6 Database Models** (User, GameSession, LevelProgress, etc.)
- ✅ **Django Admin Panel** for user management
- ✅ **CORS Support** for frontend integration

---

## 📁 Project Structure

```
traessure hunt/
├── final2.py                          # Main Streamlit application
├── start_backend.ps1                  # Script to start Django server
├── start_frontend.ps1                 # Script to start Streamlit app
├── README.md                          # This file
├── QUICK_START.md                     # Quick reference guide
├── INTEGRATION_SUMMARY.md             # Integration details
├── DJANGO_INTEGRATION_COMPLETE.md     # Complete integration guide
├── TEST_INTEGRATION.md                # Testing guide
└── backend/
    ├── manage.py                      # Django management script
    ├── treasure_hunt.db               # SQLite database
    ├── treasure_hunt/
    │   ├── settings.py                # Django configuration
    │   └── urls.py                    # URL routing
    └── authentication/
        ├── models.py                  # Database models
        ├── views.py                   # API endpoints
        ├── serializers.py             # Data validation
        ├── urls.py                    # API routes
        └── admin.py                   # Admin panel config
```

---

## 🎯 How to Play

### 1. Create Account
- Click **"Register"** tab
- Enter username (3+ characters)
- Enter valid email address
- Create password (6+ characters)
- Click **"CREATE ACCOUNT"** 🌟

### 2. Login
- Click **"Login"** tab
- Enter your credentials
- Click **"LOGIN"** ✨

### 3. Play Game
- Solve **10 FOSS riddles** progressively
- Answer **security questions** to unlock next level
- Use **hints** if stuck (costs points)
- Build **combo streaks** for bonus points
- Earn **achievements** and climb the **leaderboard**

---

## 🛠️ Technology Stack

### Frontend
- **Streamlit 1.28+** - Web application framework
- **Python 3.13.7** - Programming language
- **HTML/CSS** - Custom styling and animations

### Backend
- **Django 5.0.1** - Web framework
- **Django REST Framework 3.14.0** - API development
- **SQLite** - Database
- **Token Authentication** - Security

### Libraries
- `requests` - HTTP client for API calls
- `django-cors-headers` - Cross-origin support
- `typing` - Type hints

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [`README.md`](README.md) | This file - Overview and quick start |
| [`QUICK_START.md`](QUICK_START.md) | Quick reference for starting servers |
| [`INTEGRATION_SUMMARY.md`](INTEGRATION_SUMMARY.md) | What was integrated and how |
| [`DJANGO_INTEGRATION_COMPLETE.md`](DJANGO_INTEGRATION_COMPLETE.md) | Complete integration guide (434 lines) |
| [`TEST_INTEGRATION.md`](TEST_INTEGRATION.md) | Step-by-step testing guide (382 lines) |
| `backend/API_DOCUMENTATION.md` | Full API reference |
| `backend/CREATE_USER_MANUAL.txt` | User creation methods |

---

## 🔐 Security

- **Password Hashing:** PBKDF2 algorithm (Django default)
- **Token Authentication:** Secure API access
- **Input Validation:** Email format, username uniqueness
- **CORS Configuration:** Controlled access
- **SQL Injection Protection:** Django ORM
- **XSS Protection:** Streamlit auto-escaping

---

## 🧪 Testing

### Run Full Test Suite
See [`TEST_INTEGRATION.md`](TEST_INTEGRATION.md) for:
- 8 comprehensive tests
- Expected outputs
- Common issues and solutions

### Quick Test
```python
# Start both servers, then:
# 1. Register: testuser1 / test1@example.com / test123456
# 2. Verify in Django shell:
from authentication.models import User
User.objects.get(username='testuser1')
```

---

## 🐛 Troubleshooting

### Backend won't start
```powershell
cd backend
.\venv\Scripts\Activate
pip install django djangorestframework django-cors-headers
python manage.py migrate
python manage.py runserver
```

### Frontend won't start
```powershell
pip install streamlit requests
streamlit run final2.py
```

### Can't register users
1. Check Django server is running on port 8000
2. Check firewall settings
3. Try offline mode (password: `foss2024`)

---

## 📊 Database Schema

### User Model
```python
username: str          # Unique, 3+ chars
email: str            # Valid email format
password: str         # Hashed with PBKDF2
total_score: int      # Cumulative score
games_played: int     # Number of games
best_streak: int      # Longest streak
rank: str            # Player rank/title
created_at: datetime  # Registration time
last_login_at: datetime  # Last login time
```

### Other Models
- **GameSession** - Individual game instances
- **LevelProgress** - Progress tracking per level
- **Achievement** - Available achievements
- **UserAchievement** - Unlocked achievements
- **Leaderboard** - Global rankings

---

## 🎨 Game Mechanics

### Scoring System
- **Correct Answer:** 10 points
- **No Hints:** +5 bonus
- **Combo Streak (3+):** +3 bonus
- **Combo Streak (5+):** +8 bonus
- **Perfect Level:** +10 bonus
- **Hint Used:** -2 points

### Achievements
🏆 **FOSS GRANDMASTER** - Perfect score, no hints
⭐ **LEGENDARY HACKER** - 85+ score, ≤1 hint
💎 **ELITE DEVELOPER** - 75+ score, ≤2 hints
🚀 **SENIOR ENGINEER** - 60+ score, 4+ streak
🐧 **LINUX ENTHUSIAST** - 45+ score
🌱 **FOSS EXPLORER** - 30+ score
🔰 **BEGINNER CODER** - Starting rank

---

## 🌐 API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user
- `POST /api/auth/logout/` - Logout user
- `GET /api/auth/profile/` - Get user profile

### Game Management
- `POST /api/auth/game/start/` - Start game session
- `GET /api/auth/game/session/` - Get active session
- `PUT /api/auth/game/session/<id>/` - Update session
- `POST /api/auth/game/level/progress/` - Save level progress

### Achievements & Leaderboard
- `GET /api/auth/achievements/all/` - List achievements
- `GET /api/auth/leaderboard/` - Get leaderboard
- `POST /api/auth/achievements/unlock/` - Unlock achievement

---

## 🎯 What's New in Latest Version

### ✅ Completed in This Session:
1. **Full Django Backend Integration**
   - Registration saves to database
   - Login validates against database
   - Token-based authentication
   
2. **Enhanced Registration**
   - Email validation required
   - Auto-login after registration
   - Clear error messages
   
3. **Improved Login**
   - Backend-first authentication
   - Offline fallback mode
   - Token storage
   
4. **Comprehensive Documentation**
   - 4 new documentation files
   - Step-by-step testing guide
   - Troubleshooting guides
   
5. **Helper Scripts**
   - PowerShell startup scripts
   - Automated environment setup

---

## 🚀 Future Enhancements

- [ ] Real-time leaderboard updates
- [ ] Save game scores to database
- [ ] Track achievements in backend
- [ ] Password reset functionality
- [ ] Email verification
- [ ] Social authentication (Google, GitHub)
- [ ] Multiplayer features
- [ ] More FOSS riddles and levels

---

## 🤝 Contributing

This is a Software Freedom Day project celebrating FOSS!

### How to Contribute:
1. Add more FOSS riddles
2. Improve game mechanics
3. Add new achievements
4. Enhance UI/UX
5. Add more backend features

---

## 📄 License

Built for Software Freedom Day - Celebrating Open Source

---

## 🎊 Credits

**Made with ❤️ for Software Freedom Day**

### Technologies Used:
- Streamlit (Frontend)
- Django (Backend)
- Python (Language)
- SQLite (Database)

### Concepts Showcased:
- Full-stack web development
- REST API architecture
- Token-based authentication
- Database ORM
- Modern UI/UX design
- Gamification principles

---

## 📞 Support

### Documentation:
- **Quick Start:** [`QUICK_START.md`](QUICK_START.md)
- **Testing Guide:** [`TEST_INTEGRATION.md`](TEST_INTEGRATION.md)
- **Integration Details:** [`DJANGO_INTEGRATION_COMPLETE.md`](DJANGO_INTEGRATION_COMPLETE.md)

### Common Issues:
See [`DJANGO_INTEGRATION_COMPLETE.md`](DJANGO_INTEGRATION_COMPLETE.md) section "🐛 Troubleshooting"

---

## 🎮 Ready to Play!

```powershell
# Terminal 1
.\start_backend.ps1

# Terminal 2  
.\start_frontend.ps1
```

Then visit http://localhost:8501 and start your FOSS adventure! 🚀

---

**🌐 Celebrating Open Source • Building Digital Freedom**
