"""
Demo script to test the JSON Authentication System
This shows how the authentication works independently
"""

from auth_manager import JSONAuthManager
import json

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def view_users_file():
    """Display current contents of users.json"""
    try:
        with open("users.json", 'r') as f:
            data = json.load(f)
            print(json.dumps(data, indent=2))
    except FileNotFoundError:
        print("users.json not found (will be created on first use)")

# Initialize the authentication manager
auth = JSONAuthManager("users.json")

print_section("🔐 JSON Authentication System Demo")
print("This demo shows how user registration and login work")

# Show initial state
print_section("📄 Current users.json content")
view_users_file()

# Demo 1: Register first user
print_section("📝 Demo 1: Register New User")
print("Registering user: 'alice' with password 'alice123'")
success, msg, user_data = auth.register_user("alice", "alice123", "alice@example.com")
print(f"✅ Success: {success}")
print(f"📝 Message: {msg}")
if user_data:
    print(f"👤 User Data: {user_data}")

# Demo 2: Try duplicate registration
print_section("📝 Demo 2: Try Duplicate Registration")
print("Trying to register 'alice' again...")
success, msg, user_data = auth.register_user("alice", "different_password", "alice2@example.com")
print(f"✅ Success: {success}")
print(f"📝 Message: {msg}")

# Demo 3: Register second user
print_section("📝 Demo 3: Register Another User")
print("Registering user: 'bob' with password 'bob456'")
success, msg, user_data = auth.register_user("bob", "bob456", "bob@example.com")
print(f"✅ Success: {success}")
print(f"📝 Message: {msg}")

# Show updated users
print_section("📄 Updated users.json content")
view_users_file()

# Demo 4: Successful login
print_section("🔑 Demo 4: Login with Correct Password")
print("Logging in as 'alice' with password 'alice123'")
success, msg, user_data = auth.login_user("alice", "alice123")
print(f"✅ Success: {success}")
print(f"📝 Message: {msg}")
if user_data:
    print(f"👤 User Data: {user_data}")

# Demo 5: Failed login - wrong password
print_section("🔑 Demo 5: Login with Wrong Password")
print("Trying to login as 'alice' with wrong password")
success, msg, user_data = auth.login_user("alice", "wrong_password")
print(f"✅ Success: {success}")
print(f"📝 Message: {msg}")

# Demo 6: Failed login - non-existent user
print_section("🔑 Demo 6: Login with Non-existent User")
print("Trying to login as 'charlie' (doesn't exist)")
success, msg, user_data = auth.login_user("charlie", "anypassword")
print(f"✅ Success: {success}")
print(f"📝 Message: {msg}")

# Demo 7: Update user stats
print_section("📊 Demo 7: Update User Statistics")
print("Updating alice's game stats (score: 85)")
auth.update_user_stats("alice", 85)
print("Stats updated!")

# Demo 8: Login again to see updated stats
print_section("🔑 Demo 8: Login Again (Check Updated Stats)")
print("Logging in as 'alice' to see updated data")
success, msg, user_data = auth.login_user("alice", "alice123")
if user_data:
    print(f"👤 Total Games: {user_data.get('total_games', 0)}")
    print(f"🏆 High Score: {user_data.get('high_score', 0)}")
    print(f"🕒 Last Login: {user_data.get('last_login', 'N/A')}")

# Demo 9: Get all users
print_section("👥 Demo 9: Get All Users")
all_users = auth.get_all_users()
print(f"Total registered users: {len(all_users)}")
for i, user in enumerate(all_users, 1):
    print(f"\n{i}. Username: {user['username']}")
    print(f"   Email: {user['email']}")
    print(f"   Games Played: {user['total_games']}")
    print(f"   High Score: {user['high_score']}")

# Final users.json state
print_section("📄 Final users.json content")
view_users_file()

print_section("✅ Demo Complete!")
print("All authentication features have been demonstrated.")
print("\nKey Points:")
print("  ✓ Passwords are hashed (not stored in plain text)")
print("  ✓ Duplicate usernames are prevented")
print("  ✓ Login validates against hashed passwords")
print("  ✓ User statistics are tracked and updated")
print("  ✓ Last login timestamp is automatically recorded")
print("\nYou can now use this system in your treasure hunt game!")
print("="*60)
