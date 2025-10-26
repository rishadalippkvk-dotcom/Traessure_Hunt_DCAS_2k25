# 🎮 How to Run the FOSS Treasure Hunt Application

## 📋 Prerequisites
- Python 3.8 or higher
- PowerShell (Windows)

## 🚀 Quick Start

### Option 1: Using Provided Scripts (Recommended)
1. **Start the complete application:**
   ```powershell
   .\start_all.ps1
   ```

2. **Or start backend and frontend separately:**
   ```powershell
   # Terminal 1: Start backend
   .\start_backend.ps1
   
   # Terminal 2: Start frontend
   .\start_frontend.ps1
   ```

### Option 2: Manual Start
1. **Start the Django backend:**
   ```powershell
   cd backend
   python manage.py runserver
   ```

2. **Start the Streamlit frontend (in another terminal):**
   ```powershell
   streamlit run final2.py
   ```

## 🔧 Troubleshooting

### If you see connection errors:
1. Make sure the backend server is running on port 8000
2. Check that no firewall is blocking the connection
3. Verify that the database file exists (`backend\treasure_hunt.db`)

### If packages are missing:
```powershell
pip install django djangorestframework streamlit requests
```

## 🌐 Access the Application
- **Game Interface:** http://localhost:8501
- **Admin Panel:** http://localhost:8000/admin
  - Username: admin
  - Password: admin123

## 📁 Project Structure
```
├── final2.py              # Streamlit frontend application
├── backend/               # Django backend
│   ├── manage.py          # Django management script
│   ├── treasure_hunt.db   # SQLite database
│   └── authentication/    # Authentication and game logic
├── start_all.ps1          # Start both servers
├── start_backend.ps1      # Start Django backend
└── start_frontend.ps1     # Start Streamlit frontend
```

## 🎯 Features
- **Full Game:** 6 levels of FOSS riddles
- **Two-Phase System:** Riddle solving + security challenges
- **Progress Tracking:** Save and load game progress
- **Achievements:** Unlock badges as you play
- **Leaderboard:** Compete with other players
- **Admin Dashboard:** Manage questions and users

## 🛡️ Fallback Mode
If the backend is not available, the application will:
- Use local JSON file for user authentication
- Load questions from hardcoded data
- Save progress locally
- Continue with limited functionality

For full features, always run both backend and frontend servers.