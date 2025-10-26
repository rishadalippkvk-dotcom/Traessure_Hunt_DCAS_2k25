# 🔧 How to Fix the Backend Connection Error

## 📋 Problem Description
You're seeing this error:
```
❌ Error loading questions: HTTPConnectionPool(host='localhost', port=8000): Max retries exceeded with url: /api/auth/questions/ (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x000001E2E70BDBA0>: Failed to establish a new connection: [WinError 10061] No connection could be made because the target machine actively refused it'))
```

This error occurs because the Streamlit frontend is trying to connect to the Django backend server at `http://localhost:8000`, but the backend server is not running.

## ✅ Solution

### Option 1: Run Both Servers (Recommended)
To fully utilize all features, you need to run both the Django backend and Streamlit frontend:

1. **Start the Django Backend Server:**
   ```powershell
   # Open PowerShell as Administrator
   cd "c:\Users\DELL\Desktop\traessure hunt"
   .\start_backend.ps1
   ```

2. **Start the Streamlit Frontend (in a new PowerShell window):**
   ```powershell
   # Open another PowerShell window
   cd "c:\Users\DELL\Desktop\traessure hunt"
   .\start_frontend.ps1
   ```

### Option 2: Run Backend Manually
If the script doesn't work, you can start the backend manually:

1. Open PowerShell and navigate to the backend directory:
   ```powershell
   cd "c:\Users\DELL\Desktop\traessure hunt\backend"
   ```

2. Activate the virtual environment:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. Start the Django server:
   ```powershell
   python manage.py runserver
   ```

4. In another PowerShell window, start the Streamlit frontend:
   ```powershell
   cd "c:\Users\DELL\Desktop\traessure hunt"
   streamlit run final2.py
   ```

### Option 3: Use Fallback Mode (Limited Features)
The application now has a fallback mode that works without the backend:
- User authentication will use a local JSON file (`users.json`)
- Game progress will be saved locally
- Questions will be loaded from the hardcoded list in the frontend
- Some features like leaderboards and admin functions won't work

## 🔄 What Was Fixed
The frontend code was updated to:
1. Gracefully handle connection errors to the backend
2. Provide clear warning messages when the backend is unavailable
3. Automatically fall back to local storage and hardcoded questions
4. Continue functioning with limited features when the backend is down

## 📝 Verification
After starting the backend server, you should see:
- No more connection errors
- Questions loaded from the database
- Full authentication and progress saving features
- Access to admin dashboard at `http://localhost:8000/admin`

## 🚀 Quick Start Commands
```powershell
# Start backend server
cd "c:\Users\DELL\Desktop\traessure hunt"
.\start_backend.ps1

# Start frontend (in new terminal)
cd "c:\Users\DELL\Desktop\traessure hunt"
.\start_frontend.ps1
```

## ❓ Need Help?
If you continue to have issues:
1. Make sure you're running PowerShell as Administrator
2. Check that port 8000 is not blocked by firewall
3. Ensure Python and required packages are installed
4. Verify the database file exists at `backend\treasure_hunt.db`