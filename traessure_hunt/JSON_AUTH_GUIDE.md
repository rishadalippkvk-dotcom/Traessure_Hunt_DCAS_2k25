# 🔐 JSON-Based Authentication System

## Overview
This treasure hunt game now features a **dual authentication system**:
- **Primary**: Django backend database (when available)
- **Fallback**: JSON file-based authentication (when backend is offline)

## Features ✨

### 1. **Automatic Fallback**
- Automatically uses Django backend when available
- Seamlessly switches to JSON storage when backend is offline
- No manual configuration needed

### 2. **Secure Password Storage**
- Passwords are hashed using SHA-256 encryption
- Original passwords are never stored in plain text
- Secure against common security vulnerabilities

### 3. **User Data Management**
- Username (unique identifier)
- Password (hashed)
- Email (optional)
- Registration date
- Last login timestamp
- Game statistics (total games, high score)

## File Structure 📁

```
treasure hunt/
├── final2.py              # Main game file
├── auth_manager.py        # JSON authentication manager
├── users.json            # User data storage (auto-created)
└── JSON_AUTH_GUIDE.md    # This file
```

## How It Works 🔧

### Registration Process

1. User enters username, password, and email
2. System validates input (username ≥3 chars, password ≥6 chars)
3. System tries Django backend first
4. If backend fails, saves to `users.json`
5. Password is hashed before storage
6. User is automatically logged in

### Login Process

1. User enters username and password
2. System tries Django backend authentication first
3. If backend fails, checks `users.json`
4. Password is hashed and compared with stored hash
5. On success, user gains access to the game

## JSON Data Format 📋

The `users.json` file stores user data in this format:

```json
{
  "users": [
    {
      "username": "player1",
      "password": "hashed_password_here",
      "email": "player1@example.com",
      "created_at": "2025-10-24T10:30:00",
      "last_login": "2025-10-24T14:45:00",
      "total_games": 5,
      "high_score": 95
    }
  ]
}
```

## Security Features 🔒

1. **Password Hashing**: SHA-256 algorithm
2. **No Plain Text Storage**: Original passwords never stored
3. **Input Validation**: Prevents empty or short passwords
4. **Unique Usernames**: Prevents duplicate accounts
5. **Case-Insensitive Login**: Usernames are case-insensitive

## API Reference 🛠️

### JSONAuthManager Class

#### Methods:

**`register_user(username, password, email="")`**
- Registers a new user
- Returns: `(success: bool, message: str, user_data: dict)`

**`login_user(username, password)`**
- Authenticates user login
- Returns: `(success: bool, message: str, user_data: dict)`

**`update_user_stats(username, score)`**
- Updates user game statistics
- Called after game completion

**`get_all_users()`**
- Returns list of all users (without passwords)

**`user_exists(username)`**
- Checks if username already exists

## Usage Examples 💻

### Testing the Auth System

Run the standalone test:
```bash
python auth_manager.py
```

### Integration in Game

```python
from auth_manager import JSONAuthManager

# Initialize
auth = JSONAuthManager("users.json")

# Register new user
success, msg, user = auth.register_user("player1", "mypassword123", "email@test.com")

# Login
success, msg, user = auth.login_user("player1", "mypassword123")

# Update stats after game
auth.update_user_stats("player1", score=85)
```

## Advantages ✅

1. **Works Offline**: No internet or backend required
2. **Easy Setup**: No database configuration needed
3. **Portable**: Single JSON file contains all user data
4. **Transparent**: Data is human-readable
5. **Automatic Backup**: When backend is used, data is also saved to JSON

## Limitations ⚠️

1. **Not for Production**: Use Django backend for production apps
2. **Single File**: All users in one file (scalability limit)
3. **No Encryption**: File is not encrypted (hashing protects passwords)
4. **No Email Verification**: Emails are stored but not verified

## Migration to Backend 🔄

When the Django backend becomes available:
1. Existing JSON users can still login
2. New registrations are saved to both JSON and database
3. No data loss occurs
4. Seamless transition for users

## Troubleshooting 🔍

### Issue: "Cannot create users.json"
**Solution**: Check file permissions in the directory

### Issue: "User already exists"
**Solution**: Choose a different username or check `users.json`

### Issue: "Invalid password"
**Solution**: Passwords are case-sensitive, try again carefully

### Issue: File corruption
**Solution**: Delete `users.json` (will recreate with empty user list)

## Best Practices 📝

1. **Backup users.json**: Regularly backup to prevent data loss
2. **Use Strong Passwords**: Minimum 6 characters, use mix of letters/numbers
3. **Unique Usernames**: Choose memorable but unique usernames
4. **Test Offline Mode**: Verify game works without backend

## Future Enhancements 🚀

Potential improvements:
- File encryption for enhanced security
- Password reset functionality
- Email verification
- Session management
- User profiles and avatars
- Statistics dashboard
- Leaderboard integration

## Support 💬

For issues or questions:
1. Check this guide first
2. Test with `python auth_manager.py`
3. Verify `users.json` format
4. Check console for error messages

---

**Made with ❤️ for Software Freedom Day**

*Celebrating Open Source • Building Digital Freedom*
