# 📍 Where Are My Registration Details Stored?

## 🎯 Quick Answer

Your registration details are stored in **TWO different places** depending on whether the Django backend is running:

| Backend Status | Storage Location | Persistence | Can Login Later? |
|----------------|------------------|-------------|------------------|
| ✅ **Running** | Django Database | **PERMANENT** | ✅ **YES** |
| ❌ **Offline** | Session State | **TEMPORARY** | ❌ **NO** |

---

## 📊 Storage Location Details

### **1. Django Database (When Backend is Running) ✅**

**File Location:**
```
c:\Users\DELL\Desktop\traessure hunt\backend\treasure_hunt.db
```

**Database Type:** SQLite

**Table Name:** `authentication_user`

**Your Data Stored:**
```sql
CREATE TABLE authentication_user (
    id INTEGER PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(254),
    password VARCHAR(128),          -- Hashed with PBKDF2
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    is_staff BOOLEAN,
    is_active BOOLEAN,
    date_joined DATETIME,
    
    -- Custom fields
    total_score INTEGER DEFAULT 0,
    games_played INTEGER DEFAULT 0,
    best_streak INTEGER DEFAULT 0,
    rank VARCHAR(100) DEFAULT '🔰 BEGINNER CODER',
    created_at DATETIME,
    last_login_at DATETIME
);
```

**Example Data:**
```
id: 1
username: "rishad"
email: "rishadalippkvk@gmail.com"
password: "pbkdf2_sha256$600000$abc123...$def456..."  (HASHED, not plain text)
total_score: 0
games_played: 0
best_streak: 0
rank: "🔰 BEGINNER CODER"
created_at: "2024-12-24 10:30:45"
last_login_at: NULL
```

**Persistence:** ✅ **PERMANENT**
- Survives browser close
- Survives app restart
- Survives computer restart
- Data is FOREVER (until manually deleted)

---

### **2. Session State (When Backend is Offline) ❌**

**Location:** In-memory Python dictionary in Streamlit

**Code Location:** `final2.py` (in memory, not a file)

**Data Structure:**
```python
st.session_state = {
    'logged_in': True,
    'username': 'rishad',
    'start_time': datetime(2024, 12, 24, 10, 30, 45),
    # NO email stored
    # NO password stored
    # NO other user details
}
```

**Persistence:** ❌ **TEMPORARY**
- Lost on browser refresh
- Lost on browser close
- Lost on app restart
- Data is GONE when session ends

---

## 🔍 How to Check Where YOUR Data is Stored

### **Method 1: Check if Backend Was Running**

**Look for this message when you registered:**

✅ **Backend was RUNNING:**
```
🔄 Creating your account in database...
✅ Registration successful! Welcome, [username]!
🎮 Starting your FOSS adventure...
```

❌ **Backend was OFFLINE:**
```
⚠️ Backend offline. Account created in offline mode only.
💡 Your progress won't be saved to database until backend is running.
```

### **Method 2: Try to Login After Closing Browser**

1. **Close your browser completely**
2. **Reopen and go to** http://localhost:8501
3. **Try to login with your credentials**

**Result:**
- ✅ **Login works** → Data is in database
- ❌ **Login fails** → Data was in session state (now lost)

### **Method 3: Check Database Directly**

#### **Step 1: Open PowerShell**
```powershell
cd "c:\Users\DELL\Desktop\traessure hunt\backend"
.\venv\Scripts\Activate
python manage.py shell
```

#### **Step 2: Query Users**
```python
from authentication.models import User

# List all users
User.objects.all()
# Output: <QuerySet [<User: rishad>, <User: testuser>]>

# Count users
User.objects.count()
# Output: 2

# Check specific user
user = User.objects.get(username='rishad')
print(f"Username: {user.username}")
print(f"Email: {user.email}")
print(f"ID: {user.id}")
print(f"Score: {user.total_score}")
print(f"Rank: {user.rank}")
print(f"Created: {user.created_at}")
```

#### **Step 3: Exit Shell**
```python
exit()
```

### **Method 4: Use Database Browser**

1. **Download DB Browser for SQLite:**
   - https://sqlitebrowser.org/dl/

2. **Open Database:**
   - File → Open Database
   - Navigate to: `c:\Users\DELL\Desktop\traessure hunt\backend\treasure_hunt.db`

3. **Browse Data:**
   - Click "Browse Data" tab
   - Select table: `authentication_user`
   - See all registered users

---

## 🎯 Current Situation Analysis

### **Your Problem:**
> "why registed user can't idenfying"

### **Most Likely Cause:**

You registered when **Django backend was OFFLINE**, so:

```
Registration Flow (Backend Offline):
User fills form
    ↓
Frontend validates
    ↓
Tries to connect to Django → ❌ Connection Failed
    ↓
Falls back to offline mode
    ↓
❌ Saves ONLY to st.session_state (temporary)
    ↓
✅ Shows success message (misleading!)
    ↓
User closes browser
    ↓
❌ ALL DATA LOST (session state cleared)
```

### **Solution:**

1. **Start Django backend:**
   ```powershell
   cd "c:\Users\DELL\Desktop\traessure hunt\backend"
   .\venv\Scripts\Activate
   python manage.py runserver
   ```

2. **Register AGAIN** (with NEW username)
   - Now it will save to database permanently

3. **Verify in database:**
   ```python
   python manage.py shell
   from authentication.models import User
   User.objects.get(username='your_new_username')
   ```

---

## 📂 Complete Storage Structure

```
Registration Data Storage Hierarchy:

1️⃣ PRIMARY STORAGE (Persistent):
   📁 c:\Users\DELL\Desktop\traessure hunt\backend\
       └── 🗄️ treasure_hunt.db (208 KB)
           └── 📊 authentication_user table
               ├── username (indexed, unique)
               ├── email
               ├── password (hashed)
               ├── total_score
               ├── games_played
               ├── best_streak
               ├── rank
               └── timestamps

2️⃣ TEMPORARY STORAGE (Volatile):
   💾 Python Memory (Streamlit Process)
       └── 🔑 st.session_state dictionary
           ├── logged_in
           ├── username
           └── start_time
           ❌ Cleared on browser close

3️⃣ AUTHENTICATION TOKENS:
   📁 backend/treasure_hunt.db
       └── 📊 authtoken_token table
           ├── key (40-char hex token)
           ├── user_id (foreign key)
           └── created timestamp
```

---

## 🔐 Password Storage Details

### **In Database:**
```
Plain Password: "rishad123"
        ↓
PBKDF2 Algorithm
        ↓
Stored Hash: "pbkdf2_sha256$600000$randomsalt$hashedvalue"
```

**Components:**
- `pbkdf2_sha256` - Algorithm used
- `600000` - Number of iterations
- `randomsalt` - Random salt (unique per user)
- `hashedvalue` - Actual password hash

**Security:**
- ✅ Cannot be reversed
- ✅ Unique salt per user
- ✅ 600,000 iterations (very slow to crack)
- ✅ Industry standard

### **In Session State:**
❌ **Password is NOT stored at all** (for security)

---

## 📊 Data Comparison

| Field | Database Storage | Session Storage |
|-------|------------------|-----------------|
| Username | ✅ Stored | ✅ Stored |
| Email | ✅ Stored | ❌ Not stored |
| Password | ✅ Hashed | ❌ Not stored |
| User ID | ✅ Auto-generated | ❌ Not stored |
| Total Score | ✅ Stored (0) | ❌ Not stored |
| Games Played | ✅ Stored (0) | ❌ Not stored |
| Rank | ✅ Stored | ❌ Not stored |
| Created At | ✅ Timestamp | ❌ Not stored |
| Last Login | ✅ Updated | ❌ Not stored |
| Auth Token | ✅ Generated | ✅ Stored (temporary) |

---

## 🧪 Quick Test: Where Is My Data?

Run this test to find out:

### **Test 1: Check Database**
```powershell
cd "c:\Users\DELL\Desktop\traessure hunt\backend"
.\venv\Scripts\Activate
python manage.py shell
```
```python
from authentication.models import User
User.objects.filter(username='your_username').exists()
# True = In database ✅
# False = Not in database ❌
```

### **Test 2: Check Session State**
In your Streamlit app, add this temporarily:
```python
st.write("Session State:", st.session_state)
```

Look for:
- `logged_in: True` = In session ✅
- `username: 'your_username'` = In session ✅

---

## ✅ Best Practice

### **Always Register with Backend Running:**

1. **Terminal 1:**
   ```powershell
   cd "c:\Users\DELL\Desktop\traessure hunt\backend"
   .\venv\Scripts\Activate
   python manage.py runserver
   ```

2. **Terminal 2:**
   ```powershell
   cd "c:\Users\DELL\Desktop\traessure hunt"
   streamlit run final2.py
   ```

3. **Register:**
   - Go to http://localhost:8501
   - Click "Register" tab
   - Fill form and submit
   - Look for: "🔄 Creating your account in database..."
   - ✅ **This confirms database storage!**

---

## 🎯 Summary

**Where Registration Details Are Stored:**

| Scenario | Location | File/Memory | Persistent? |
|----------|----------|-------------|-------------|
| Backend Running | Django Database | `backend/treasure_hunt.db` → `authentication_user` table | ✅ YES |
| Backend Offline | Session State | Python memory → `st.session_state` dictionary | ❌ NO |

**How to Check:**
1. Look at registration message ("Creating in database" vs "Offline mode")
2. Try login after browser restart
3. Query database with Django shell
4. Use SQLite browser tool

**Your Issue:**
- Registered when backend was offline
- Data saved to session state (temporary)
- Browser closed = data lost
- Login fails because database is empty

**Fix:**
- Start Django backend
- Register again (new username)
- Data will save permanently
- Login will work forever

---

**Need Help?** See [`QUICK_START.md`](QUICK_START.md) for startup instructions!
