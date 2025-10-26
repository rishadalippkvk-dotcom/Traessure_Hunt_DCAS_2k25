# 🎮 Example Usage - JSON Authentication System

## 📸 Real Example: Current users.json

Here's what your `users.json` file looks like right now with some test users:

```json
{
  "users": [
    {
      "username": "testuser",
      "password": "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f",
      "email": "test@example.com",
      "created_at": "2025-10-24T15:31:43.807401",
      "last_login": "2025-10-24T15:31:43.844870",
      "total_games": 0,
      "high_score": 0
    },
    {
      "username": "alice",
      "password": "4e40e8ffe0ee32fa53e139147ed559229a5930f89c2204706fc174beb36210b3",
      "email": "alice@example.com",
      "created_at": "2025-10-24T15:32:47.807062",
      "last_login": "2025-10-24T15:32:48.062411",
      "total_games": 1,
      "high_score": 85
    },
    {
      "username": "bob",
      "password": "ed4d9437294706c60027d39427f6f5850870625544bb77722aac19f97495b2b7",
      "email": "bob@example.com",
      "created_at": "2025-10-24T15:32:47.924585",
      "last_login": null,
      "total_games": 0,
      "high_score": 0
    }
  ]
}
```

---

## 🔍 Understanding the Data

### User 1: testuser
- **Username:** `testuser`
- **Password:** `password123` → (hashed to) `ef92b778bafe771e...`
- **Email:** `test@example.com`
- **Registered:** Oct 24, 2025 at 3:31 PM
- **Last Login:** Oct 24, 2025 at 3:31 PM
- **Games Played:** 0
- **High Score:** 0
- **Status:** Registered but hasn't played yet

### User 2: alice
- **Username:** `alice`
- **Password:** `alice123` → (hashed to) `4e40e8ffe0ee32fa...`
- **Email:** `alice@example.com`
- **Registered:** Oct 24, 2025 at 3:32 PM
- **Last Login:** Oct 24, 2025 at 3:32 PM
- **Games Played:** 1
- **High Score:** 85
- **Status:** Active player with good score! 🏆

### User 3: bob
- **Username:** `bob`
- **Password:** `bob456` → (hashed to) `ed4d9437294706c6...`
- **Email:** `bob@example.com`
- **Registered:** Oct 24, 2025 at 3:32 PM
- **Last Login:** `null` (never logged in after registration)
- **Games Played:** 0
- **High Score:** 0
- **Status:** Registered but never logged back in

---

## 🎬 Step-by-Step Example

### Example 1: New User Registration

**User Action:**
```
1. Opens game
2. Clicks "Register" tab
3. Enters:
   - Username: charlie
   - Password: charlie789
   - Email: charlie@example.com
4. Clicks "CREATE ACCOUNT"
```

**What Happens Behind the Scenes:**
```python
# Step 1: Validate input
if len("charlie") >= 3:  # ✅ Valid (7 chars)
    if len("charlie789") >= 6:  # ✅ Valid (10 chars)
        # Step 2: Check if username exists
        if not user_exists("charlie"):  # ✅ New user
            # Step 3: Hash password
            hashed = sha256("charlie789")
            # Result: "a1b2c3d4e5f6..."
            
            # Step 4: Create user object
            new_user = {
                "username": "charlie",
                "password": "a1b2c3d4e5f6...",
                "email": "charlie@example.com",
                "created_at": "2025-10-24T15:35:00",
                "last_login": None,
                "total_games": 0,
                "high_score": 0
            }
            
            # Step 5: Add to users.json
            users.append(new_user)
            save_to_json()
            
            # Step 6: Auto-login
            st.session_state.logged_in = True
            st.session_state.username = "charlie"
```

**Result in users.json:**
```json
{
  "users": [
    ...existing users...,
    {
      "username": "charlie",
      "password": "a1b2c3d4e5f6...",
      "email": "charlie@example.com",
      "created_at": "2025-10-24T15:35:00",
      "last_login": null,
      "total_games": 0,
      "high_score": 0
    }
  ]
}
```

---

### Example 2: User Login

**User Action:**
```
1. Opens game
2. Clicks "Login" tab
3. Enters:
   - Username: alice
   - Password: alice123
4. Clicks "ENTER GAME"
```

**What Happens Behind the Scenes:**
```python
# Step 1: Load users from JSON
users = load_users_json()

# Step 2: Find user by username
found_user = None
for user in users:
    if user["username"].lower() == "alice".lower():
        found_user = user
        break

# Step 3: Hash entered password
entered_hash = sha256("alice123")
# Result: "4e40e8ffe0ee32fa..."

# Step 4: Compare hashes
if found_user["password"] == entered_hash:
    # ✅ Match! Login successful
    
    # Step 5: Update last_login
    found_user["last_login"] = "2025-10-24T16:00:00"
    save_to_json()
    
    # Step 6: Set session
    st.session_state.logged_in = True
    st.session_state.username = "alice"
    
    return True, "Welcome back, alice!"
```

**Result in users.json:**
```json
{
  "username": "alice",
  ...
  "last_login": "2025-10-24T16:00:00",  ← Updated!
  ...
}
```

---

### Example 3: Failed Login (Wrong Password)

**User Action:**
```
1. Opens game
2. Enters:
   - Username: alice
   - Password: wrongpassword  ❌
3. Clicks "ENTER GAME"
```

**What Happens:**
```python
# Step 1: Find user
found_user = get_user("alice")  # ✅ Found

# Step 2: Hash entered password
entered_hash = sha256("wrongpassword")
# Result: "xyz123456789..."

# Step 3: Compare hashes
stored_hash = "4e40e8ffe0ee32fa..."
if entered_hash == stored_hash:
    # ❌ No match!
    return False, "Invalid username or password"
```

**User sees:**
```
❌ Invalid username or password
```

---

### Example 4: User Completes Game

**Scenario:**
- User: bob
- Final Score: 92
- Current Stats: 0 games, 0 high score

**What Happens:**
```python
# Step 1: Game ends, calculate score
final_score = 92

# Step 2: Update user stats
update_user_stats("bob", 92)

# Step 3: Inside update_user_stats():
user = get_user("bob")
user["total_games"] += 1        # 0 → 1
if 92 > user["high_score"]:     # 92 > 0
    user["high_score"] = 92     # Update!
save_to_json()
```

**Before:**
```json
{
  "username": "bob",
  "total_games": 0,
  "high_score": 0
}
```

**After:**
```json
{
  "username": "bob",
  "total_games": 1,      ← Incremented
  "high_score": 92       ← Updated to new high
}
```

---

## 🔄 Complete User Journey

### Day 1: Registration
```
User "diana" registers:
  username: diana
  password: diana2024
  email: diana@email.com
  
→ users.json:
{
  "username": "diana",
  "password": "hashed_diana2024",
  "created_at": "2025-10-24T10:00:00",
  "last_login": null,
  "total_games": 0,
  "high_score": 0
}
```

### Day 1: First Game
```
diana logs in and plays:
  Final score: 75
  
→ users.json updated:
{
  "username": "diana",
  "last_login": "2025-10-24T10:05:00",  ← Updated
  "total_games": 1,                      ← 0 → 1
  "high_score": 75                       ← 0 → 75
}
```

### Day 2: Second Game
```
diana logs in again and plays:
  Final score: 60 (lower than before)
  
→ users.json updated:
{
  "username": "diana",
  "last_login": "2025-10-25T14:30:00",  ← Updated
  "total_games": 2,                      ← 1 → 2
  "high_score": 75                       ← Stays 75 (60 < 75)
}
```

### Day 3: New High Score
```
diana logs in and beats her record:
  Final score: 95 (new personal best!)
  
→ users.json updated:
{
  "username": "diana",
  "last_login": "2025-10-26T09:15:00",  ← Updated
  "total_games": 3,                      ← 2 → 3
  "high_score": 95                       ← 75 → 95! 🏆
}
```

---

## 🎯 Real Code Examples

### Create a New User (Python)
```python
from auth_manager import JSONAuthManager

auth = JSONAuthManager("users.json")

# Register new user
success, message, user_data = auth.register_user(
    username="player1",
    password="securepass123",
    email="player1@game.com"
)

if success:
    print(f"✅ {message}")
    print(f"User ID: {user_data['username']}")
    print(f"Created: {user_data['created_at']}")
else:
    print(f"❌ {message}")
```

### Login a User (Python)
```python
from auth_manager import JSONAuthManager

auth = JSONAuthManager("users.json")

# Attempt login
success, message, user_data = auth.login_user(
    username="player1",
    password="securepass123"
)

if success:
    print(f"✅ {message}")
    print(f"Welcome back, {user_data['username']}!")
    print(f"Games played: {user_data['total_games']}")
    print(f"High score: {user_data['high_score']}")
else:
    print(f"❌ {message}")
```

### Update Stats After Game (Python)
```python
from auth_manager import JSONAuthManager

auth = JSONAuthManager("users.json")

# Player finished game with score 88
username = "player1"
final_score = 88

auth.update_user_stats(username, final_score)
print(f"✅ Stats updated for {username}")
```

### Get All Users (Python)
```python
from auth_manager import JSONAuthManager

auth = JSONAuthManager("users.json")

all_users = auth.get_all_users()

print(f"Total users: {len(all_users)}\n")

for i, user in enumerate(all_users, 1):
    print(f"{i}. {user['username']}")
    print(f"   Email: {user['email']}")
    print(f"   Games: {user['total_games']}")
    print(f"   High Score: {user['high_score']}")
    print(f"   Last Login: {user['last_login']}\n")
```

---

## 🎨 Visual Example: Password Hashing

```
Plain Text Password Flow:
═════════════════════════

Registration:
  User enters: "mypassword123"
       ↓
  SHA-256 Hash Function
       ↓
  Hash: "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f"
       ↓
  Saved to JSON: { "password": "ef92b77..." }


Login:
  User enters: "mypassword123"
       ↓
  SHA-256 Hash Function
       ↓
  Hash: "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f"
       ↓
  Compare with stored: "ef92b77..." == "ef92b77..." ✅ MATCH!
       ↓
  LOGIN SUCCESS!


Wrong Password:
  User enters: "wrongpassword"
       ↓
  SHA-256 Hash Function
       ↓
  Hash: "abc123def456..." (different!)
       ↓
  Compare with stored: "abc123..." != "ef92b77..." ❌ NO MATCH!
       ↓
  LOGIN FAILED!
```

---

## 📊 User Statistics Example

**Sample Leaderboard (from users.json):**

| Rank | Username | Games Played | High Score | Last Login |
|------|----------|--------------|------------|------------|
| 🥇 1 | alice | 15 | 95 | 2025-10-24 16:30 |
| 🥈 2 | bob | 8 | 92 | 2025-10-24 14:15 |
| 🥉 3 | charlie | 12 | 88 | 2025-10-24 15:45 |
| 4 | diana | 3 | 75 | 2025-10-24 10:20 |
| 5 | testuser | 1 | 45 | 2025-10-24 09:10 |

---

## 🚀 Try It Yourself!

### 1️⃣ Run the Test Script
```bash
python test_json_auth.py
```

### 2️⃣ Start the Game
```bash
streamlit run final2.py
```

### 3️⃣ Register Your Account
- Create username and password
- Start playing!

### 4️⃣ Check users.json
- Open the file
- See your user data!

---

**Your authentication system is fully working!** 🎉

**Made with ❤️ for Software Freedom Day**  
*Celebrating Open Source • Building Digital Freedom*
