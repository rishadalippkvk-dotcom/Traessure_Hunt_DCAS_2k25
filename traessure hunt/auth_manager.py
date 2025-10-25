"""
JSON-based Authentication Manager
Handles user registration and login with local JSON storage
"""

import json
import hashlib
import os
from typing import Tuple, Optional, Dict
from datetime import datetime


class JSONAuthManager:
    """Manages user authentication with JSON file storage"""
    
    def __init__(self, json_file: str = "users.json"):
        self.json_file = json_file
        self._initialize_file()
    
    def _initialize_file(self):
        """Initialize the JSON file if it doesn't exist"""
        if not os.path.exists(self.json_file):
            with open(self.json_file, 'w') as f:
                json.dump({"users": []}, f, indent=2)
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _load_users(self) -> Dict:
        """Load users from JSON file"""
        try:
            with open(self.json_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"users": []}
    
    def _save_users(self, data: Dict):
        """Save users to JSON file"""
        with open(self.json_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def register_user(self, username: str, password: str, email: str = "") -> Tuple[bool, str, Optional[Dict]]:
        """
        Register a new user
        
        Args:
            username: User's chosen username
            password: User's password (will be hashed)
            email: User's email (optional)
        
        Returns:
            Tuple of (success: bool, message: str, user_data: dict or None)
        """
        # Validation
        if not username or len(username.strip()) < 3:
            return False, "Username must be at least 3 characters long", None
        
        if not password or len(password) < 6:
            return False, "Password must be at least 6 characters long", None
        
        username = username.strip()
        
        # Load existing users
        data = self._load_users()
        users = data.get("users", [])
        
        # Check if username already exists
        if any(user["username"].lower() == username.lower() for user in users):
            return False, "Username already exists", None
        
        # Create new user
        new_user = {
            "username": username,
            "password": self._hash_password(password),
            "email": email,
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "total_games": 0,
            "high_score": 0,
            "is_active": True  # Active by default
        }
        
        users.append(new_user)
        data["users"] = users
        self._save_users(data)
        
        # Return user data without password
        user_data = {k: v for k, v in new_user.items() if k != "password"}
        
        return True, f"Account created successfully for {username}!", user_data
    
    def login_user(self, username: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Authenticate user login
        
        Args:
            username: User's username
            password: User's password
        
        Returns:
            Tuple of (success: bool, message: str, user_data: dict or None)
        """
        if not username or not password:
            return False, "Username and password are required", None
        
        username = username.strip()
        
        # Load users
        data = self._load_users()
        users = data.get("users", [])
        
        # Find user
        user = None
        user_index = -1
        for i, u in enumerate(users):
            if u["username"].lower() == username.lower():
                user = u
                user_index = i
                break
        
        if not user:
            return False, "Invalid username or password", None
        
        # Check if account is active
        if not user.get("is_active", True):
            return False, "Account has been disabled. Please contact the administrator.", None
        
        # Verify password
        hashed_password = self._hash_password(password)
        if user["password"] != hashed_password:
            return False, "Invalid username or password", None
        
        # Update last login
        user["last_login"] = datetime.now().isoformat()
        users[user_index] = user
        data["users"] = users
        self._save_users(data)
        
        # Return user data without password
        user_data = {k: v for k, v in user.items() if k != "password"}
        
        return True, f"Welcome back, {username}!", user_data
    
    def update_user_stats(self, username: str, score: int):
        """Update user statistics after game completion"""
        data = self._load_users()
        users = data.get("users", [])
        
        for i, user in enumerate(users):
            if user["username"].lower() == username.lower():
                user["total_games"] += 1
                if score > user.get("high_score", 0):
                    user["high_score"] = score
                users[i] = user
                break
        
        data["users"] = users
        self._save_users(data)
    
    def save_progress(self, username: str, level: int, score: int, hints_used: int = 0, 
                     achievements: list = None, streak: int = 0, max_streak: int = 0,
                     combo_multiplier: float = 1.0, perfect_levels: int = 0,
                     wrong_attempts: int = 0) -> bool:
        """Save user's game progress with all stats"""
        data = self._load_users()
        users = data.get("users", [])
        
        for i, user in enumerate(users):
            if user["username"].lower() == username.lower():
                user["saved_progress"] = {
                    "level": level,
                    "score": score,
                    "hints_used": hints_used,
                    "achievements": achievements or [],
                    "streak": streak,
                    "max_streak": max_streak,
                    "combo_multiplier": combo_multiplier,
                    "perfect_levels": perfect_levels,
                    "wrong_attempts": wrong_attempts,
                    "saved_at": datetime.now().isoformat()
                }
                users[i] = user
                data["users"] = users
                self._save_users(data)
                return True
        return False
    
    def load_progress(self, username: str) -> Optional[Dict]:
        """Load user's saved game progress"""
        data = self._load_users()
        users = data.get("users", [])
        
        for user in users:
            if user["username"].lower() == username.lower():
                return user.get("saved_progress")
        return None
    
    def clear_progress(self, username: str) -> bool:
        """Clear user's saved game progress"""
        data = self._load_users()
        users = data.get("users", [])
        
        for i, user in enumerate(users):
            if user["username"].lower() == username.lower():
                if "saved_progress" in user:
                    del user["saved_progress"]
                    users[i] = user
                    data["users"] = users
                    self._save_users(data)
                return True
        return False
    
    def get_all_users(self) -> list:
        """Get all users (without passwords)"""
        data = self._load_users()
        users = data.get("users", [])
        return [{k: v for k, v in user.items() if k != "password"} for user in users]
    
    def user_exists(self, username: str) -> bool:
        """Check if a username exists"""
        data = self._load_users()
        users = data.get("users", [])
        return any(user["username"].lower() == username.lower() for user in users)
    
    def disable_user(self, username: str) -> Tuple[bool, str]:
        """Disable a user account"""
        data = self._load_users()
        users = data.get("users", [])
        
        for i, user in enumerate(users):
            if user["username"].lower() == username.lower():
                user["is_active"] = False
                user["disabled_at"] = datetime.now().isoformat()
                users[i] = user
                data["users"] = users
                self._save_users(data)
                return True, f"Account '{username}' has been disabled successfully"
        
        return False, f"User '{username}' not found"
    
    def activate_user(self, username: str) -> Tuple[bool, str]:
        """Activate a user account"""
        data = self._load_users()
        users = data.get("users", [])
        
        for i, user in enumerate(users):
            if user["username"].lower() == username.lower():
                user["is_active"] = True
                if "disabled_at" in user:
                    del user["disabled_at"]
                users[i] = user
                data["users"] = users
                self._save_users(data)
                return True, f"Account '{username}' has been activated successfully"
        
        return False, f"User '{username}' not found"
    
    def delete_user(self, username: str) -> Tuple[bool, str]:
        """Permanently delete a user account"""
        data = self._load_users()
        users = data.get("users", [])
        
        initial_count = len(users)
        users = [user for user in users if user["username"].lower() != username.lower()]
        
        if len(users) < initial_count:
            data["users"] = users
            self._save_users(data)
            return True, f"Account '{username}' has been permanently deleted"
        
        return False, f"User '{username}' not found"
    
    def create_user_admin(self, username: str, password: str, email: str = "") -> Tuple[bool, str]:
        """Create a new user account (admin function)"""
        # Reuse the register_user function
        success, message, user_data = self.register_user(username, password, email)
        
        if success:
            # Mark as active by default
            data = self._load_users()
            users = data.get("users", [])
            for i, user in enumerate(users):
                if user["username"].lower() == username.lower():
                    user["is_active"] = True
                    users[i] = user
                    break
            data["users"] = users
            self._save_users(data)
        
        return success, message
    
    def get_user_status(self, username: str) -> Optional[Dict]:
        """Get user account status"""
        data = self._load_users()
        users = data.get("users", [])
        
        for user in users:
            if user["username"].lower() == username.lower():
                return {
                    "username": user["username"],
                    "is_active": user.get("is_active", True),
                    "disabled_at": user.get("disabled_at"),
                    "created_at": user.get("created_at"),
                    "last_login": user.get("last_login")
                }
        return None
    
    def get_user_details(self, username: str) -> Optional[Dict]:
        """Get complete user details for editing"""
        data = self._load_users()
        users = data.get("users", [])
        
        for user in users:
            if user["username"].lower() == username.lower():
                # Return all fields except password
                return {k: v for k, v in user.items() if k != "password"}
        return None
    
    def update_user_email(self, username: str, new_email: str) -> Tuple[bool, str]:
        """Update user's email address"""
        data = self._load_users()
        users = data.get("users", [])
        
        for i, user in enumerate(users):
            if user["username"].lower() == username.lower():
                user["email"] = new_email
                users[i] = user
                data["users"] = users
                self._save_users(data)
                return True, f"Email updated successfully for '{username}'"
        
        return False, f"User '{username}' not found"
    
    def update_user_password(self, username: str, new_password: str) -> Tuple[bool, str]:
        """Update user's password"""
        if len(new_password) < 6:
            return False, "Password must be at least 6 characters long"
        
        data = self._load_users()
        users = data.get("users", [])
        
        for i, user in enumerate(users):
            if user["username"].lower() == username.lower():
                user["password"] = self._hash_password(new_password)
                users[i] = user
                data["users"] = users
                self._save_users(data)
                return True, f"Password updated successfully for '{username}'"
        
        return False, f"User '{username}' not found"
    
    def update_user_details(self, username: str, new_email: str = None, new_password: str = None) -> Tuple[bool, str]:
        """Update user's email and/or password"""
        data = self._load_users()
        users = data.get("users", [])
        
        user_found = False
        updates = []
        
        for i, user in enumerate(users):
            if user["username"].lower() == username.lower():
                user_found = True
                
                # Update email if provided
                if new_email is not None and new_email.strip():
                    user["email"] = new_email.strip()
                    updates.append("email")
                
                # Update password if provided
                if new_password is not None and new_password.strip():
                    if len(new_password) < 6:
                        return False, "Password must be at least 6 characters long"
                    user["password"] = self._hash_password(new_password)
                    updates.append("password")
                
                if updates:
                    users[i] = user
                    data["users"] = users
                    self._save_users(data)
                    updated_fields = " and ".join(updates)
                    return True, f"Successfully updated {updated_fields} for '{username}'"
                else:
                    return False, "No changes provided"
        
        if not user_found:
            return False, f"User '{username}' not found"
        
        return False, "Update failed"
    
    def mark_game_completed_permanently(self, username: str) -> bool:
        """Mark game as completed permanently to prevent replay"""
        data = self._load_users()
        users = data.get("users", [])
        
        for i, user in enumerate(users):
            if user["username"].lower() == username.lower():
                user["game_completed_permanently"] = True
                users[i] = user
                data["users"] = users
                self._save_users(data)
                return True
        return False


# Test the module if run directly
if __name__ == "__main__":
    print("Testing JSON Auth Manager...")
    
    auth = JSONAuthManager()
    
    # Test registration
    print("\n1. Testing Registration:")
    success, msg, user = auth.register_user("testuser", "password123", "test@example.com")
    print(f"   Result: {msg}")
    print(f"   User Data: {user}")
    
    # Test duplicate registration
    print("\n2. Testing Duplicate Registration:")
    success, msg, user = auth.register_user("testuser", "password456", "test2@example.com")
    print(f"   Result: {msg}")
    
    # Test login with correct password
    print("\n3. Testing Login (Correct):")
    success, msg, user = auth.login_user("testuser", "password123")
    print(f"   Result: {msg}")
    print(f"   User Data: {user}")
    
    # Test login with wrong password
    print("\n4. Testing Login (Wrong Password):")
    success, msg, user = auth.login_user("testuser", "wrongpassword")
    print(f"   Result: {msg}")
    
    # Test login with non-existent user
    print("\n5. Testing Login (Non-existent User):")
    success, msg, user = auth.login_user("nonexistent", "password123")
    print(f"   Result: {msg}")
    
    print("\n✅ All tests complete!")
