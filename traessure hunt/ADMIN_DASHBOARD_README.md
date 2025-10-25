# 👨‍💼 Admin Dashboard - Quick Start Guide

## 🚀 Quick Start (30 seconds)

### Step 1: Install Dependencies
```powershell
pip install plotly pandas
```

### Step 2: Start Dashboard
```powershell
./start_admin_dashboard.ps1
```

### Step 3: Login
- Open: http://localhost:8502
- Password: `admin123`

**That's it! You're monitoring!** 🎉

---

## 📋 What Can You Do?

### ✅ Real-Time Monitoring
- 👥 See all registered users
- 📊 Track progress across 6 levels
- 🎯 Monitor scores and achievements
- 🔥 View streaks and combos
- 📈 Analyze user engagement

### ✅ Visual Analytics
- 📊 Level distribution charts
- 🎯 Score distribution graphs
- 🔥 Streak leaderboards
- 🎮 Activity heatmaps

### ✅ Data Export
- 📥 Download CSV reports
- 📊 Excel-ready format
- 🕐 Timestamped exports

---

## 🖥️ Dashboard Tabs

### 1. 📋 User List
View all users in a sortable table:
- Search by name/email
- Filter by level
- See complete stats
- Export to CSV

### 2. 📊 Analytics
Beautiful visualizations:
- User distribution
- Score patterns
- Streak analysis
- Engagement metrics

### 3. 🏆 Leaderboard
Top performers:
- Highest scores
- Best streaks
- Most perfect levels

### 4. 🔍 User Details
Deep dive per user:
- Complete profile
- Game statistics
- Live stats
- Progress visualization

---

## 📊 Metrics Explained

### Overview Metrics (Top Bar)

| Metric | Description | Example |
|--------|-------------|---------|
| 👥 Total Users | All registered accounts | 15 |
| 🎮 Active Players | Users with saved progress | 8 |
| 🎯 Total Games | Sum of all games played | 42 |
| 📈 Avg High Score | Average best score | 67.5 |

### User Statistics

| Column | Description | Range |
|--------|-------------|-------|
| 📍 Level | Current progress | 1-6 |
| 🎯 Score | Current game score | 0-120 |
| 🏆 High Score | Best score ever | 0-120 |
| 🔥 Streak | Current win streak | 0-6 |
| 🏅 Max Streak | Best streak achieved | 0-6 |
| ⚡ Combo | Point multiplier | 1.0x-3.0x |
| ⭐ Perfect Levels | No-hint completions | 0-6 |
| 💡 Hints Used | Total hints consumed | 0+ |

---

## 🎯 Common Use Cases

### Use Case 1: Daily Health Check
```
1. Start dashboard
2. Check "Active Players" count
3. Review Analytics tab
4. Identify stuck users
5. Take action if needed
```

### Use Case 2: Weekly Report
```
1. Go to User List tab
2. Click "Download CSV"
3. Open in Excel
4. Create pivot tables
5. Share with stakeholders
```

### Use Case 3: Player Support
```
Player: "I lost my progress!"

1. Go to User Details tab
2. Select their username
3. Check "Last Login" date
4. Review "Current Level"
5. Compare with "High Score"
6. Diagnose issue
```

### Use Case 4: Game Balance
```
1. Go to Analytics tab
2. Check "Level Distribution"
3. Find bottleneck levels
4. Adjust difficulty
5. Monitor improvements
```

---

## 🔧 Configuration

### Change Admin Password

Edit `admin_dashboard.py` line 24:
```python
ADMIN_PASSWORD = "your_secure_password_here"
```

### Change Port

Run with custom port:
```powershell
streamlit run admin_dashboard.py --server.port 9000
```

### Theme Customization

Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#0e1117"
secondaryBackgroundColor = "#262730"
textColor = "#fafafa"
font = "sans serif"
```

---

## 📥 Data Export Format

### CSV Structure
```csv
Username,Email,Level,Score,High Score,Streak,Max Streak,Combo,Perfect Levels,Hints Used,Total Games,Last Login,Created
alice,alice@test.com,5,85,95,4,6,1.6x,4,3,12,2025-10-24,2025-10-20
bob,bob@test.com,3,45,55,0,2,1.0x,1,5,8,2025-10-23,2025-10-19
```

### Import to Excel
1. Open Excel
2. Data → From Text/CSV
3. Select exported file
4. Click Import
5. Create pivot tables, charts

---

## 🔒 Security Checklist

- [ ] Changed default password
- [ ] Using strong password (12+ chars)
- [ ] Only running on local network
- [ ] Regular backups of users.json
- [ ] Monitoring access logs
- [ ] Not exposing to internet
- [ ] Using HTTPS in production

---

## ⚠️ Troubleshooting

### Dashboard won't start
```powershell
# Install dependencies
pip install streamlit pandas plotly

# Try different port
streamlit run admin_dashboard.py --server.port 8503
```

### No users showing
```powershell
# Check users.json exists
cat users.json

# Create test user in main game
streamlit run final2.py
```

### Charts not loading
```powershell
# Reinstall plotly
pip uninstall plotly
pip install plotly
```

---

## 🎓 Best Practices

### Daily Tasks
- Check active players count
- Monitor for stuck users
- Review top scores

### Weekly Tasks
- Export CSV backup
- Analyze trends
- Adjust game difficulty

### Monthly Tasks
- Full data export
- Statistical analysis
- User retention report

---

## 📚 Files Overview

```
.
├── admin_dashboard.py           # Main dashboard app
├── start_admin_dashboard.ps1    # Startup script
├── ADMIN_DASHBOARD_MANUAL.md    # Detailed manual
├── ADMIN_DASHBOARD_README.md    # This file
├── auth_manager.py              # User data handler
└── users.json                   # User database
```

---

## 🆘 Need Help?

### Documentation
- 📖 Full Manual: `ADMIN_DASHBOARD_MANUAL.md`
- 🎮 Game Docs: `README.md`
- 💾 Progress Feature: `PROGRESS_SAVE_FEATURE.md`

### Quick Commands
```powershell
# Start dashboard
./start_admin_dashboard.ps1

# Or manually
streamlit run admin_dashboard.py --server.port 8502

# Check dependencies
pip list | Select-String "streamlit|pandas|plotly"

# View users
cat users.json
```

---

## 📊 Sample Dashboard Views

### Overview Metrics
```
┌────────────────┬────────────────┬────────────────┬────────────────┐
│  👥 Total      │  🎮 Active     │  🎯 Total      │  📈 Avg High   │
│  Users: 15     │  Players: 8    │  Games: 42     │  Score: 67.5   │
└────────────────┴────────────────┴────────────────┴────────────────┘
```

### User Table (Sample)
```
┌──────────┬─────────┬───────┬─────────┬────────┐
│ Username │ Level   │ Score │ Streak  │ Combo  │
├──────────┼─────────┼───────┼─────────┼────────┤
│ Alice    │ 5/6     │ 85    │ 4x      │ 1.6x   │
│ Bob      │ 3/6     │ 45    │ 0x      │ 1.0x   │
│ Charlie  │ 6/6 ✓   │ 120   │ 6x      │ 3.0x   │
└──────────┴─────────┴───────┴─────────┴────────┘
```

### Leaderboard
```
🏆 TOP SCORES
─────────────
🥇 Charlie - 120 pts
🥈 Alice   - 95 pts
🥉 David   - 82 pts
```

---

## 🚀 Advanced Usage

### Run Both Game and Dashboard
```powershell
# Terminal 1: Main game
streamlit run final2.py --server.port 8501

# Terminal 2: Admin dashboard
streamlit run admin_dashboard.py --server.port 8502

# Terminal 3: Django backend (optional)
cd backend
python manage.py runserver
```

### Auto-Refresh Setup
Add to `admin_dashboard.py`:
```python
import time

# Auto-refresh every 30 seconds
if st.button("Enable Auto-Refresh"):
    time.sleep(30)
    st.rerun()
```

### Custom Alerts
Add notifications for specific events:
```python
# Alert if user stuck for 24+ hours
stuck_users = df[df['Last Login'] < yesterday]
if len(stuck_users) > 0:
    st.warning(f"⚠️ {len(stuck_users)} users inactive for 24+ hours")
```

---

## 📈 Metrics to Track

### Engagement Metrics
- Daily Active Users (DAU)
- Weekly Active Users (WAU)
- Average session length
- Completion rate

### Performance Metrics
- Level completion time
- Hint usage rate
- Wrong answer frequency
- Streak achievement rate

### Business Metrics
- User retention
- Churn rate
- Virality coefficient
- User satisfaction score

---

## ✨ Tips & Tricks

1. **Keyboard Shortcuts**
   - `R` - Refresh page
   - `Ctrl + K` - Search commands
   - `Ctrl + /` - Toggle sidebar

2. **Quick Export**
   - Use filters before export
   - Include only needed columns
   - Add timestamps to filenames

3. **Performance**
   - Limit table to 100 rows
   - Use pagination for large datasets
   - Cache expensive calculations

4. **Monitoring**
   - Set up daily check routine
   - Create anomaly alerts
   - Track trends over time

---

## 🎯 Success Criteria

Your dashboard is working when you can:
- ✅ View all users and their stats
- ✅ See real-time progress updates
- ✅ Export data for reports
- ✅ Identify stuck or struggling users
- ✅ Track game engagement metrics
- ✅ Make data-driven decisions

---

## 🔄 Version History

**v1.0** (2025-10-24)
- Initial release
- 4 main tabs
- CSV export
- Real-time monitoring
- Visual analytics

---

**Admin Dashboard v1.0** | Made with ❤️ for FOSS Treasure Hunt

**Start Monitoring Now!** 🚀
```powershell
./start_admin_dashboard.ps1
```
