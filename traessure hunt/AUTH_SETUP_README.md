# 🎮 Treasure Hunt - JSON Authentication System

## ✅ Setup Complete!

Your treasure hunt game now has a **JSON-based authentication system** that stores user registration data (username and password) in a local file.

---

## 🚀 Quick Start

### 1️⃣ **Run the Game**
```bash
streamlit run final2.py
```

### 2️⃣ **Register a New Account**
- Click the **"Register"** tab
- Enter a username (minimum 3 characters)
- Enter a password (minimum 6 characters)
- Confirm your password
- Click **"CREATE ACCOUNT"**

### 3️⃣ **Login**
- Click the **"Login"** tab
- Enter your username
- Enter your password
- Click **"ENTER GAME"**

---

## 📁 Files Created

| File | Purpose |
|------|---------|
| [`users.json`](file://c:\Users\DELL\Desktop\traessure%20hunt\users.json) | Stores all user accounts (username, hashed password, email, stats) |
| [`auth_manager.py`](file://c:\Users\DELL\Desktop\traessure%20hunt\auth_manager.py) | Authentication logic (register, login, password hashing) |
| [`test_json_auth.py`](file://c:\Users\DELL\Desktop\traessure%20hunt\test_json_auth.py) | Demo script to test authentication |
| [`JSON_AUTH_GUIDE.md`](file://c:\Users\DELL\Desktop\traessure%20hunt\JSON_AUTH_GUIDE.md) | Detailed documentation |

---

## 🔐 How It Works

### **Registration Flow**
```
User enters credentials
     ↓
System validates (username ≥3 chars, password ≥6 chars)
     ↓
Password is hashed with SHA-256
     ↓
Data saved to users.json
     ↓
User automatically logged in
```

### **Login Flow**
```
User enters username & password
     ↓
System hashes the entered password
     ↓
Compares hash with stored hash in users.json
     ↓
If match → Login successful ✅
If no match → Login failed ❌
```

---

## 🔍 View Your Users

Check the `users.json` file to see all registered users:

```json
{
  "users": [
    {
      "username": "player1",
      "password": "hashed_password_here",
      "email": "player1@example.com",
      "created_at": "2025-10-24T15:32:47",
      "last_login": "2025-10-24T15:32:48",
      "total_games": 1,
      "high_score": 85
    }
  ]
}
```

> **Note:** Passwords are stored as SHA-256 hashes (not plain text) for security!

---

## 🧪 Test the Authentication

Run the test script to see how registration and login work:

```bash
python test_json_auth.py
```

This will:
- ✅ Create test users
- ✅ Test login with correct password
- ✅ Test login with wrong password
- ✅ Show user statistics
- ✅ Display the users.json contents

---

## 🛡️ Security Features

| Feature | Description |
|---------|-------------|
| **Password Hashing** | SHA-256 encryption (passwords never stored in plain text) |
| **Unique Usernames** | System prevents duplicate accounts |
| **Input Validation** | Minimum length requirements enforced |
| **Case-Insensitive** | Usernames are case-insensitive for login |
| **Auto Timestamps** | Registration and login times tracked |

---

## 🎯 Dual Authentication System

The game supports **two modes**:

### 1️⃣ **Django Backend Mode** (Online)
- Uses Django database when backend is running
- Full features including achievements and leaderboards
- Data is also backed up to `users.json`

### 2️⃣ **JSON Offline Mode** (Offline)
- Works without internet or backend
- Stores everything in local `users.json` file
- Perfect for offline play

**The system automatically chooses the right mode!** ✨

---

## 📊 Features

✅ **User Registration** - Create new accounts  
✅ **User Login** - Authenticate with username/password  
✅ **Password Security** - SHA-256 hashing  
✅ **Stats Tracking** - Games played and high scores  
✅ **Last Login** - Timestamp of last login  
✅ **Duplicate Prevention** - No duplicate usernames  
✅ **Auto-Login** - Login immediately after registration  

---

## 🔧 Customization

### Change Password Requirements
Edit [`auth_manager.py`](file://c:\Users\DELL\Desktop\traessure%20hunt\auth_manager.py) lines 48-51:

```python
# Current: minimum 6 characters
if not password or len(password) < 6:
    return False, "Password must be at least 6 characters long", None

# Change to minimum 8 characters:
if not password or len(password) < 8:
    return False, "Password must be at least 8 characters long", None
```

### Change Username Requirements
Edit [`auth_manager.py`](file://c:\Users\DELL\Desktop\traessure%20hunt\auth_manager.py) lines 45-46:

```python
# Current: minimum 3 characters
if not username or len(username.strip()) < 3:
    return False, "Username must be at least 3 characters long", None

# Change to minimum 5 characters:
if not username or len(username.strip()) < 5:
    return False, "Username must be at least 5 characters long", None
```

---

## 🐛 Troubleshooting

### ❌ "Username already exists"
**Solution:** Choose a different username or check `users.json` to see existing users

### ❌ "Invalid username or password"
**Solution:** Double-check your password (case-sensitive) and username (case-insensitive)

### ❌ "Cannot create users.json"
**Solution:** Check that you have write permissions in the game directory

### ❌ File appears corrupted
**Solution:** Delete `users.json` (it will be recreated automatically - but you'll lose user data!)

---

## 📚 Additional Resources

- **Full Documentation:** [`JSON_AUTH_GUIDE.md`](file://c:\Users\DELL\Desktop\traessure%20hunt\JSON_AUTH_GUIDE.md)
- **Test Script:** [`test_json_auth.py`](file://c:\Users\DELL\Desktop\traessure%20hunt\test_json_auth.py)
- **Auth Manager:** [`auth_manager.py`](file://c:\Users\DELL\Desktop\traessure%20hunt\auth_manager.py)

---

## 🎮 Example Usage

### **Register and Play:**
```bash
# Step 1: Start the game
streamlit run final2.py

# Step 2: Create account
# - Username: awesome_player
# - Password: mypassword123

# Step 3: Play the game!
```

### **Login Next Time:**
```bash
# Step 1: Start the game
streamlit run final2.py

# Step 2: Login
# - Username: awesome_player
# - Password: mypassword123

# Step 3: Continue where you left off!
```

---

## 🎉 Summary

You now have a **fully functional authentication system** that:

✅ Stores usernames and passwords in `users.json`  
✅ Hashes passwords for security (SHA-256)  
✅ Validates user input  
✅ Tracks user statistics  
✅ Works offline (no backend required)  
✅ Automatically falls back from Django to JSON  

**Enjoy your treasure hunt game!** 🏆

---

**Made with ❤️ for Software Freedom Day**  
*Celebrating Open Source • Building Digital Freedom*
