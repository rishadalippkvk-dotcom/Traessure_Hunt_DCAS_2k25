# 👨‍💼 Admin Dashboard - User Manual

## 📋 Table of Contents
1. [Overview](#overview)
2. [Installation & Setup](#installation--setup)
3. [Accessing the Dashboard](#accessing-the-dashboard)
4. [Dashboard Features](#dashboard-features)
5. [Using Each Tab](#using-each-tab)
6. [Data Export](#data-export)
7. [Troubleshooting](#troubleshooting)
8. [Security](#security)

---

## 🎯 Overview

The **Admin Dashboard** is a powerful monitoring tool that allows administrators to:
- 📊 Monitor all users' progress in real-time
- 🎯 Track scores, streaks, and achievements
- 📈 View analytics and statistics
- 🏆 See leaderboards and top performers
- 🔍 Inspect individual user details
- 📥 Export data for reporting

---

## 🚀 Installation & Setup

### Prerequisites
Make sure you have these packages installed:

```powershell
pip install streamlit pandas plotly
```

### Files Required
- `admin_dashboard.py` - Main dashboard application
- `auth_manager.py` - User data manager
- `users.json` - User database (auto-created)

### Verify Setup

```powershell
# Check if files exist
ls admin_dashboard.py
ls auth_manager.py
ls users.json
```

---

## 🔐 Accessing the Dashboard

### Step 1: Start the Dashboard

Open PowerShell in your project directory and run:

```powershell
streamlit run admin_dashboard.py
```

**Alternative port** (if 8501 is busy):
```powershell
streamlit run admin_dashboard.py --server.port 8502
```

### Step 2: Open in Browser

The dashboard will automatically open at:
```
http://localhost:8501
```

Or manually navigate to the URL shown in the terminal.

### Step 3: Login

**Default Admin Password:** `admin123`

⚠️ **IMPORTANT:** Change this password in production!

To change the password, edit line 24 in `admin_dashboard.py`:
```python
ADMIN_PASSWORD = "your_secure_password_here"
```

### Login Screen:
```
┌─────────────────────────────────┐
│   👨‍💼 Admin Dashboard           │
│   FOSS Treasure Hunt            │
│   Monitoring System             │
├─────────────────────────────────┤
│   🔐 Admin Authentication       │
│                                 │
│   Password: [**********]        │
│                                 │
│   [🚀 Access Dashboard]         │
└─────────────────────────────────┘
```

---

## 📊 Dashboard Features

### Top Metrics Bar

After login, you'll see 4 key metrics:

```
┌────────────────┬────────────────┬────────────────┬────────────────┐
│  👥 Total      │  🎮 Active     │  🎯 Total      │  📈 Avg High   │
│  Users         │  Players       │  Games         │  Score         │
│     15         │      8         │      42        │     67.5       │
└────────────────┴────────────────┴────────────────┴────────────────┘
```

- **Total Users**: Number of registered users
- **Active Players**: Users with saved progress
- **Total Games**: Sum of all games played
- **Avg High Score**: Average of all users' high scores

### Control Buttons

Top-right corner:
- **🔄 Refresh Data**: Reload all user data
- **🚪 Logout**: Exit admin dashboard

---

## 📑 Using Each Tab

### Tab 1: 📋 User List

**Purpose:** View all users and their current stats

#### Features:

1. **Search Bar**
   ```
   🔍 Search by username or email: [player1]
   ```
   - Type any part of username or email
   - Results update in real-time

2. **Level Filter**
   ```
   Filter by Level: [All ▼]
   ```
   - Options: All, Level 1-6
   - Shows only users at selected level

3. **User Table**
   
   Columns displayed:
   - 👤 Username
   - 📧 Email
   - 📍 Level (1-6)
   - 🎯 Current Score
   - 🏆 High Score
   - 🔥 Current Streak
   - 🏅 Max Streak
   - ⚡ Combo Multiplier
   - ⭐ Perfect Levels
   - 💡 Hints Used
   - 🎮 Total Games
   - 🕐 Last Login
   - 📅 Created Date

4. **Download Button**
   ```
   📥 Download User Data (CSV)
   ```
   - Exports filtered data to CSV
   - Filename includes timestamp
   - Use for reports or analysis

**Example Use Cases:**

✅ Find all users stuck at Level 3:
1. Set filter to "Level 3"
2. View list of users
3. Identify who needs help

✅ Search for specific user:
1. Type username in search
2. View their complete stats
3. Monitor their progress

---

### Tab 2: 📊 Analytics

**Purpose:** Visual analytics and insights

#### Charts Included:

1. **📊 User Distribution by Level**
   - Bar chart showing users per level
   - Identifies difficulty spikes
   - Shows progression bottlenecks

2. **🎯 Score Distribution**
   - Histogram of current scores
   - Shows scoring patterns
   - Identifies outliers

3. **🔥 Top 10 Users by Streak**
   - Compares current vs max streak
   - Shows most consistent players
   - Highlights engagement

4. **🎮 Most Active Users**
   - Shows games played vs hints used
   - Identifies power users
   - Measures engagement

**How to Read Charts:**

📊 **Level Distribution:**
- High bar = Many users at this level
- Low bar = Easy level or difficulty spike
- Use to balance difficulty

🎯 **Score Distribution:**
- Peak = Most common score range
- Spread = Skill variety
- Outliers = Exceptional players

🔥 **Streak Chart:**
- Blue = Current streak
- Teal = Best streak ever
- Gap = Lost momentum

🎮 **Activity Chart:**
- Purple = Games played
- Pink = Hints used
- Ratio = Player skill

**Example Analysis:**

```
Level Distribution shows:
Level 1: 5 users  ← Many starting
Level 2: 4 users  ← Normal progression
Level 3: 1 user   ← BOTTLENECK! 
Level 4: 3 users  ← Some advanced
Level 5-6: 2 users ← Elite players

Action: Level 3 may be too difficult!
```

---

### Tab 3: 🏆 Leaderboard

**Purpose:** Recognize top performers

#### Three Categories:

1. **🥇 Highest Scores**
   ```
   🥇 Alice     - 95 pts
   🥈 Bob       - 87 pts
   🥉 Charlie   - 82 pts
   4️⃣ David     - 75 pts
   5️⃣ Eve       - 68 pts
   ```

2. **🔥 Best Streaks**
   ```
   🥇 Frank     - 6x
   🥈 Grace     - 5x
   🥉 Henry     - 5x
   4️⃣ Iris      - 4x
   5️⃣ Jack      - 4x
   ```

3. **⭐ Most Perfect Levels**
   ```
   🥇 Kate      - 5 levels
   🥈 Leo       - 4 levels
   🥉 Maya      - 3 levels
   4️⃣ Noah      - 3 levels
   5️⃣ Olivia    - 2 levels
   ```

**Use Cases:**

✅ **Recognize Excellence**
- Share leaderboard with players
- Award prizes to top 3
- Motivate competition

✅ **Identify Champions**
- Find beta testers
- Recruit ambassadors
- Feature testimonials

---

### Tab 4: 🔍 User Details

**Purpose:** Deep dive into individual user performance

#### Features:

1. **User Selector**
   ```
   Select User: [Alice ▼]
   ```

2. **Profile Information**
   ```
   👤 User Profile
   ─────────────────
   Username: Alice
   Email: alice@example.com
   Created: 2025-10-20
   Last Login: 2025-10-24
   ```

3. **Game Statistics**
   ```
   🎮 Game Stats
   ─────────────────
   Current Level: 5/6
   Current Score: 85
   High Score: 95
   Total Games: 12
   ```

4. **Live Stats**
   ```
   🔥 Live Stats
   ─────────────────
   Current Streak: 4x
   Max Streak: 6x
   Combo Multiplier: 1.6x
   Perfect Levels: 4
   Hints Used: 3
   ```

5. **Progress Bar**
   ```
   📈 Progress Overview
   ████████████████░░░░ 83.3%
   Level Progress: 83.3% complete
   ```

**Example Investigation:**

Scenario: User "Bob" reports lost progress

Steps:
1. Select "Bob" from dropdown
2. Check "Last Login" date
3. View "Current Level" 
4. Compare with "High Score"
5. Review "Live Stats"

If stats are missing:
- Progress wasn't saved
- Check `users.json` file
- Verify auto-save feature

---

## 📥 Data Export

### Export User List

1. Go to **📋 User List** tab
2. Apply filters if needed
3. Click **📥 Download User Data (CSV)**
4. File downloads as: `user_data_YYYYMMDD_HHMMSS.csv`

### CSV Contents:

```csv
Username,Email,Level,Score,High Score,Streak,Max Streak,Combo,Perfect Levels,Hints Used,Total Games,Last Login,Created
Alice,alice@example.com,5,85,95,4,6,1.6x,4,3,12,2025-10-24,2025-10-20
Bob,bob@example.com,3,45,55,0,2,1.0x,1,5,8,2025-10-23,2025-10-19
```

### Use Cases:

✅ **Reporting**
- Weekly progress reports
- Monthly analytics
- Stakeholder updates

✅ **Analysis**
- Excel pivot tables
- Statistical analysis
- Trend identification

✅ **Backup**
- Archive user data
- Disaster recovery
- Historical records

---

## 🔧 Troubleshooting

### Issue 1: Dashboard Won't Start

**Error:**
```
ModuleNotFoundError: No module named 'plotly'
```

**Solution:**
```powershell
pip install plotly pandas
```

---

### Issue 2: No Users Displayed

**Symptoms:**
- Empty table in User List
- "No users found" message

**Solutions:**

1. Check if `users.json` exists:
   ```powershell
   cat users.json
   ```

2. Verify JSON format:
   ```json
   {
     "users": [
       {"username": "test", ...}
     ]
   }
   ```

3. Create test user via main game

---

### Issue 3: Charts Not Loading

**Symptoms:**
- Blank Analytics tab
- Chart errors

**Solutions:**

1. Check data availability:
   - Need at least 1 user
   - Need saved progress

2. Refresh dashboard:
   - Click 🔄 Refresh Data
   - Or restart: `Ctrl+C` then re-run

---

### Issue 4: Can't Login

**Symptoms:**
- "Invalid Password" error

**Solutions:**

1. Check password in code:
   ```python
   ADMIN_PASSWORD = "admin123"  # Line 24
   ```

2. Case-sensitive check
3. No spaces before/after

---

### Issue 5: Port Already in Use

**Error:**
```
OSError: [WinError 10048] Only one usage of each socket address
```

**Solution:**
```powershell
streamlit run admin_dashboard.py --server.port 8502
```

---

## 🔒 Security

### Best Practices

1. **Change Default Password**
   ```python
   # In admin_dashboard.py, line 24
   ADMIN_PASSWORD = "Your-Secure-P@ssw0rd-123!"
   ```

2. **Use Strong Password**
   - Minimum 12 characters
   - Mix uppercase, lowercase, numbers, symbols
   - Example: `Adm!n@FOSS#2024$Hunt`

3. **Restrict Access**
   - Only run on local network
   - Use firewall rules
   - Don't expose to internet

4. **Regular Backups**
   - Export CSV weekly
   - Backup `users.json`
   - Store securely

5. **Monitor Access**
   - Check terminal for connections
   - Log access attempts (future feature)

### Production Recommendations

For production environments:

1. **Environment Variables**
   ```python
   import os
   ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'default123')
   ```

2. **Database Authentication**
   - Use Django admin instead
   - Implement role-based access
   - Multi-factor authentication

3. **HTTPS**
   - Enable SSL/TLS
   - Use reverse proxy (nginx)
   - Secure cookies

4. **Audit Logging**
   - Log all admin actions
   - Track data exports
   - Monitor suspicious activity

---

## 📚 Quick Reference

### Starting Dashboard
```powershell
streamlit run admin_dashboard.py
```

### Default Login
- Password: `admin123`

### Refresh Data
- Click 🔄 button
- Or press `R` key in browser

### Export Data
- User List tab → Download button

### Find User
- User List tab → Search box

### View Analytics
- Analytics tab → Charts

---

## 🆘 Support

### Common Questions

**Q: How often does data refresh?**
A: Manual refresh only. Click 🔄 to update.

**Q: Can I edit user data?**
A: Not in dashboard. Edit `users.json` directly or use Django admin.

**Q: What's the difference between Score and High Score?**
A: Score = current game, High Score = best ever.

**Q: Why is Streak 0 for some users?**
A: Streak resets when hints are used or wrong answers given.

**Q: Can I run dashboard and game simultaneously?**
A: Yes! Use different ports:
```powershell
# Terminal 1: Main game
streamlit run final2.py --server.port 8501

# Terminal 2: Admin dashboard
streamlit run admin_dashboard.py --server.port 8502
```

---

## 🔄 Updates & Maintenance

### Regular Tasks

**Daily:**
- Check active players count
- Monitor stuck users
- Review top scores

**Weekly:**
- Export CSV backup
- Analyze trends
- Update difficulty if needed

**Monthly:**
- Full data export
- Statistical analysis
- User retention report

---

## 📞 Getting Help

If you encounter issues:

1. Check this manual
2. Review error messages
3. Check `users.json` integrity
4. Restart dashboard
5. Verify Python packages

---

## ✅ Checklist for Admins

Before Each Session:
- [ ] Dashboard runs without errors
- [ ] Can login with password
- [ ] User data loads correctly
- [ ] All tabs display properly
- [ ] Charts render correctly

After Each Session:
- [ ] Export data (if needed)
- [ ] Logout properly
- [ ] Close terminal/browser
- [ ] Backup users.json

---

**Admin Dashboard v1.0** | Last Updated: 2025-10-24

**Happy Monitoring!** 👨‍💼📊🎮
