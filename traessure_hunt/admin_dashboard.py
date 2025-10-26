"""
Admin Dashboard for FOSS Treasure Hunt - PROFESSIONAL UI/UX
Monitor all users' progress, scores, and live statistics
"""

import streamlit as st
import json
import pandas as pd
from datetime import datetime
from typing import List, Dict

# Try to import plotly, but handle the case where it's not available
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    # Create mock objects to prevent crashes
    class MockFigure:
        def __init__(self, *args, **kwargs):
            pass
    
    class MockPx:
        def __getattr__(self, name):
            return lambda *args, **kwargs: MockFigure()
    
    class MockGo:
        def __getattr__(self, name):
            return type(name, (), {'__getattr__': lambda self, name: lambda *args, **kwargs: MockFigure()})()
    
    px = MockPx()
    go = MockGo()

from auth_manager import JSONAuthManager
import time

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Admin Dashboard - FOSS Treasure Hunt",
    page_icon="👨‍💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Auth Manager
auth_manager = JSONAuthManager("users.json")

# ═══════════════════════════════════════════════════════════════════════════════
# PROFESSIONAL STYLING
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Global Theme */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Professional Header */
    .admin-hero {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15));
        border: 2px solid rgba(102, 126, 234, 0.3);
        border-radius: 20px;
        padding: 40px;
        margin-bottom: 30px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
    }
    
    .admin-hero::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(102, 126, 234, 0.1), transparent);
        animation: shimmer 3s linear infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) rotate(45deg); }
        100% { transform: translateX(100%) rotate(45deg); }
    }
    
    .admin-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        animation: titleGlow 3s ease-in-out infinite;
    }
    
    @keyframes titleGlow {
        0%, 100% { filter: drop-shadow(0 0 20px rgba(102, 126, 234, 0.5)); }
        50% { filter: drop-shadow(0 0 40px rgba(118, 75, 162, 0.8)); }
    }
    
    /* Premium Metric Cards */
    .premium-metric {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.03));
        backdrop-filter: blur(20px);
        border: 2px solid rgba(102, 126, 234, 0.3);
        border-radius: 16px;
        padding: 25px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
    
    .premium-metric::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .premium-metric:hover::before {
        left: 100%;
    }
    
    .premium-metric:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: rgba(102, 126, 234, 0.6);
        box-shadow: 0 16px 48px rgba(102, 126, 234, 0.3);
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00ffff, #00ff88);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 15px 0;
        line-height: 1;
    }
    
    .metric-label {
        color: rgba(255, 255, 255, 0.8);
        font-size: 1rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 10px;
    }
    
    .metric-icon {
        font-size: 2.5rem;
        filter: drop-shadow(0 0 10px currentColor);
    }
    
    /* Enhanced Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 12px;
        padding: 12px 32px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.6);
    }
    
    /* Professional Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 10px;
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 16px 28px;
        font-size: 1.05rem;
        font-weight: 600;
        transition: all 0.3s;
        border: 2px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.3), rgba(118, 75, 162, 0.3));
        border-color: rgba(102, 126, 234, 0.5);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Data Table Enhancement */
    .stDataFrame {
        border: 2px solid rgba(102, 126, 234, 0.3);
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #667eea;
        margin: 30px 0 20px;
        padding-bottom: 15px;
        border-bottom: 3px solid rgba(102, 126, 234, 0.3);
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    /* Info Cards */
    .info-card {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.08), rgba(255, 0, 255, 0.08));
        border: 2px solid rgba(0, 255, 255, 0.2);
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        transition: all 0.3s;
    }
    
    .info-card:hover {
        border-color: rgba(0, 255, 255, 0.5);
        transform: translateX(5px);
    }
    
    /* Loading Animation */
    .stSpinner > div {
        border-color: #667eea transparent transparent transparent;
    }
    
    /* Search Box */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.08);
        border: 2px solid rgba(102, 126, 234, 0.3);
        border-radius: 12px;
        color: white;
        padding: 12px 20px;
        font-size: 1rem;
        transition: all 0.3s;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: rgba(102, 126, 234, 0.6);
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
    }
    
    /* Leaderboard Styling */
    .leaderboard-item {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.02));
        border-left: 4px solid;
        padding: 15px 20px;
        margin: 10px 0;
        border-radius: 8px;
        transition: all 0.3s;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .leaderboard-item:hover {
        transform: translateX(10px);
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
    }
    
    .rank-medal {
        font-size: 2rem;
        filter: drop-shadow(0 0 10px currentColor);
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ADMIN AUTHENTICATION
# ═══════════════════════════════════════════════════════════════════════════════
ADMIN_PASSWORD = "admin123"  # Change this in production!

def check_admin_access():
    """Check if admin is authenticated - Professional UI"""
    if "admin_authenticated" not in st.session_state:
        st.session_state.admin_authenticated = False
    
    if not st.session_state.admin_authenticated:
        # Professional Login Screen
        st.markdown('''
        <div class="admin-hero" style="text-align: center;">
            <div style="font-size: 5rem; margin-bottom: 20px; animation: iconFloat 3s ease-in-out infinite;">
                👨‍💼
            </div>
            <h1 class="admin-title">Admin Control Center</h1>
            <p style="font-size: 1.3rem; color: rgba(255,255,255,0.8); font-weight: 500;">
                🎯 FOSS Treasure Hunt Monitoring System
            </p>
            <div style="margin-top: 20px; display: flex; justify-content: center; gap: 30px;">
                <span style="color: rgba(255,255,255,0.6);">✓ Real-Time Analytics</span>
                <span style="color: rgba(255,255,255,0.6);">✓ User Management</span>
                <span style="color: rgba(255,255,255,0.6);">✓ Secure Access</span>
            </div>
        </div>
        <style>
            @keyframes iconFloat {
                0%, 100% { transform: translateY(0) rotate(0deg); }
                50% { transform: translateY(-15px) rotate(10deg); }
            }
        </style>
        ''', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('''
            <div style="background: rgba(255,255,255,0.05); backdrop-filter: blur(20px);
                        border: 2px solid rgba(102,126,234,0.3); border-radius: 16px;
                        padding: 40px; margin-top: 30px;">
                <h3 style="text-align: center; color: #667eea; font-size: 1.8rem; margin-bottom: 25px;">
                    🔐 Secure Authentication
                </h3>
            </div>
            ''', unsafe_allow_html=True)
            
            with st.form("admin_login"):
                st.markdown('<p style="font-weight: 600; margin-bottom: 8px; color: #667eea;">🔑 Admin Password</p>', unsafe_allow_html=True)
                password = st.text_input(
                    "Password", 
                    type="password",
                    placeholder="Enter admin password",
                    key="admin_pass",
                    label_visibility="collapsed"
                )
                
                st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
                
                submit = st.form_submit_button(
                    "🚀 ACCESS DASHBOARD",
                    use_container_width=True,
                    type="primary"
                )
                
                if submit:
                    if password == ADMIN_PASSWORD:
                        st.session_state.admin_authenticated = True
                        st.success("✅ Access Granted! Redirecting...")
                        st.balloons()
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Invalid Password! Access Denied.")
            
            st.markdown('''
            <div style="margin-top: 30px; padding: 20px; background: rgba(255,0,85,0.1);
                        border-left: 4px solid #ff0055; border-radius: 8px;">
                <p style="color: rgba(255,255,255,0.8); font-size: 0.95rem; margin: 0;">
                    ⚠️ <strong>Security Notice:</strong> Unauthorized access is prohibited.
                    All login attempts are monitored and logged.
                </p>
            </div>
            ''', unsafe_allow_html=True)
        
        return False
    return True

# ═══════════════════════════════════════════════════════════════════════════════
# DATA LOADING FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def load_user_data() -> List[Dict]:
    """Load all user data from JSON"""
    return auth_manager.get_all_users()

def get_user_statistics() -> Dict:
    """Calculate overall statistics"""
    users = load_user_data()
    
    total_users = len(users)
    active_users = sum(1 for u in users if u.get('saved_progress'))
    total_games = sum(u.get('total_games', 0) for u in users)
    avg_score = sum(u.get('high_score', 0) for u in users) / max(total_users, 1)
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "total_games": total_games,
        "avg_high_score": round(avg_score, 2)
    }


def get_level_progress_data() -> List[Dict]:
    """Get level progress data from backend API"""
    try:
        import requests
        response = requests.get("http://localhost:8000/api/auth/game/session/progress/", timeout=5)
        if response.status_code == 200:
            return response.json().get('progress', [])
    except Exception as e:
        pass
    return []

def create_users_dataframe() -> pd.DataFrame:
    """Create DataFrame from user data"""
    users = load_user_data()
    
    data = []
    for user in users:
        progress = user.get('saved_progress', {})
        data.append({
            'Username': user.get('username', 'N/A'),
            'Email': user.get('email', 'N/A'),
            'Level': progress.get('level', 0) + 1 if progress else 1,
            'Score': progress.get('score', 0),
            'High Score': user.get('high_score', 0),
            'Streak': progress.get('streak', 0),
            'Max Streak': progress.get('max_streak', 0),
            'Combo': f"{progress.get('combo_multiplier', 1.0):.1f}x",
            'Perfect Levels': progress.get('perfect_levels', 0),
            'Hints Used': progress.get('hints_used', 0),
            'Total Games': user.get('total_games', 0),
            'Last Login': user.get('last_login', 'Never'),
            'Created': user.get('created_at', 'N/A')
        })
    
    return pd.DataFrame(data)

# ═══════════════════════════════════════════════════════════════════════════════
# VISUALIZATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def create_level_distribution_chart(df: pd.DataFrame):
    """Create level distribution chart with dark theme"""
    # Check if plotly is available
    if not PLOTLY_AVAILABLE:
        st.warning("📊 Chart visualization requires plotly library. Please install plotly to enable charts.")
        return None
    
    # Check if DataFrame is empty or doesn't have the required column
    if df.empty or 'Level' not in df.columns:
        st.warning("📊 No data available for level distribution chart.")
        return None
    
    level_counts = df['Level'].value_counts().sort_index()
    
    fig = px.bar(
        x=level_counts.index,
        y=level_counts.values,
        labels={'x': 'Level', 'y': 'Number of Users'},
        title='📊 User Distribution by Level',
        color=level_counts.values,
        color_continuous_scale=['#667eea', '#764ba2', '#f093fb']
    )
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=14, family='Inter'),
        title_font=dict(size=20, color='#667eea'),
        xaxis=dict(gridcolor='rgba(102, 126, 234, 0.1)', showgrid=True),
        yaxis=dict(gridcolor='rgba(102, 126, 234, 0.1)', showgrid=True),
        margin=dict(l=20, r=20, t=60, b=20)
    )
    return fig

def create_score_distribution_chart(df: pd.DataFrame):
    """Create score distribution chart with dark theme"""
    # Check if plotly is available
    if not PLOTLY_AVAILABLE:
        st.warning("🎯 Chart visualization requires plotly library. Please install plotly to enable charts.")
        return None
    
    # Check if DataFrame is empty or doesn't have the required column
    if df.empty or 'Score' not in df.columns:
        st.warning("🎯 No data available for score distribution chart.")
        return None
    
    fig = px.histogram(
        df,
        x='Score',
        nbins=20,
        title='🎯 Score Distribution',
        labels={'Score': 'Current Score', 'count': 'Number of Users'},
        color_discrete_sequence=['#667eea']
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=14, family='Inter'),
        title_font=dict(size=20, color='#667eea'),
        xaxis=dict(gridcolor='rgba(102, 126, 234, 0.1)', showgrid=True),
        yaxis=dict(gridcolor='rgba(102, 126, 234, 0.1)', showgrid=True),
        margin=dict(l=20, r=20, t=60, b=20),
        bargap=0.1
    )
    return fig

def create_streak_chart(df: pd.DataFrame):
    """Create streak comparison chart with dark theme"""
    # Check if plotly is available
    if not PLOTLY_AVAILABLE:
        st.warning("🔥 Chart visualization requires plotly library. Please install plotly to enable charts.")
        return None
    
    # Check if DataFrame is empty or doesn't have the required columns
    required_columns = ['Username', 'Streak', 'Max Streak']
    if df.empty or not all(col in df.columns for col in required_columns):
        st.warning("🔥 No data available for streak chart.")
        return None
    
    top_users = df.nlargest(10, 'Max Streak')[['Username', 'Streak', 'Max Streak']]
    
    fig = go.Figure(data=[
        go.Bar(name='Current Streak', x=top_users['Username'], y=top_users['Streak'], 
               marker_color='#4facfe', marker_line=dict(width=2, color='rgba(79, 172, 254, 0.3)')),
        go.Bar(name='Max Streak', x=top_users['Username'], y=top_users['Max Streak'], 
               marker_color='#00f2fe', marker_line=dict(width=2, color='rgba(0, 242, 254, 0.3)'))
    ])
    
    fig.update_layout(
        title='🔥 Top 10 Users by Streak',
        xaxis_title='Username',
        yaxis_title='Streak Count',
        barmode='group',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=14, family='Inter'),
        title_font=dict(size=20, color='#667eea'),
        xaxis=dict(gridcolor='rgba(102, 126, 234, 0.1)', showgrid=True),
        yaxis=dict(gridcolor='rgba(102, 126, 234, 0.1)', showgrid=True),
        legend=dict(bgcolor='rgba(255,255,255,0.05)', bordercolor='rgba(102, 126, 234, 0.3)', borderwidth=2),
        margin=dict(l=20, r=20, t=60, b=20)
    )
    return fig

def create_engagement_chart(df: pd.DataFrame):
    """Create user engagement chart with dark theme"""
    # Check if plotly is available
    if not PLOTLY_AVAILABLE:
        st.warning("🎮 Chart visualization requires plotly library. Please install plotly to enable charts.")
        return None
    
    # Check if DataFrame is empty or doesn't have the required columns
    required_columns = ['Username', 'Total Games', 'Hints Used']
    if df.empty or not all(col in df.columns for col in required_columns):
        st.warning("🎮 No data available for engagement chart.")
        return None
    
    engagement_data = df[['Username', 'Total Games', 'Hints Used']].nlargest(10, 'Total Games')
    
    fig = go.Figure(data=[
        go.Bar(name='Games Played', x=engagement_data['Username'], y=engagement_data['Total Games'], 
               marker_color='#667eea', marker_line=dict(width=2, color='rgba(102, 126, 234, 0.3)')),
        go.Bar(name='Hints Used', x=engagement_data['Username'], y=engagement_data['Hints Used'], 
               marker_color='#f093fb', marker_line=dict(width=2, color='rgba(240, 147, 251, 0.3)'))
    ])
    
    fig.update_layout(
        title='🎮 Most Active Users',
        xaxis_title='Username',
        yaxis_title='Count',
        barmode='group',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=14, family='Inter'),
        title_font=dict(size=20, color='#667eea'),
        xaxis=dict(gridcolor='rgba(102, 126, 234, 0.1)', showgrid=True),
        yaxis=dict(gridcolor='rgba(102, 126, 234, 0.1)', showgrid=True),
        legend=dict(bgcolor='rgba(255,255,255,0.05)', bordercolor='rgba(102, 126, 234, 0.3)', borderwidth=2),
        margin=dict(l=20, r=20, t=60, b=20)
    )
    return fig

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
if not check_admin_access():
    st.stop()

# Admin is authenticated - show dashboard
# Professional Dashboard Header
st.markdown("""
<div class="admin-hero">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 class="admin-title" style="font-size: 2.8rem; margin: 0;">👨‍💼 Admin Control Center</h1>
            <p style="font-size: 1.2rem; color: rgba(255,255,255,0.7); margin-top: 10px; font-weight: 500;">
                🎯 Real-time FOSS Treasure Hunt Monitoring Dashboard
            </p>
        </div>
        <div style="font-size: 4rem; opacity: 0.2;">
            📊
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Control Buttons
col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
with col1:
    st.markdown(f'<p style="color: rgba(255,255,255,0.6); font-size: 0.95rem; margin-top: 15px;">🕐 Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>', unsafe_allow_html=True)
with col2:
    pass  # Spacer
with col3:
    if st.button("🔄 Refresh Data", use_container_width=True, key="refresh_btn"):
        st.rerun()
with col4:
    if st.button("🚪 Logout", use_container_width=True, key="logout_btn", type="primary"):
        st.session_state.admin_authenticated = False
        st.rerun()

st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)

# Load Data
stats = get_user_statistics()
df = create_users_dataframe()

# ═══════════════════════════════════════════════════════════════════════════════
# OVERVIEW METRICS - PREMIUM CARDS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<h2 class="section-header"><span>📊</span> Overview Metrics</h2>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="premium-metric" style="border-color: rgba(102, 126, 234, 0.5);">
        <div class="metric-icon" style="color: #667eea;">👥</div>
        <div class="metric-value">{stats['total_users']}</div>
        <div class="metric-label">Total Users</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="premium-metric" style="border-color: rgba(240, 147, 251, 0.5);">
        <div class="metric-icon" style="color: #f093fb;">🎮</div>
        <div class="metric-value">{stats['active_users']}</div>
        <div class="metric-label">Active Players</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="premium-metric" style="border-color: rgba(79, 172, 254, 0.5);">
        <div class="metric-icon" style="color: #4facfe;">🎯</div>
        <div class="metric-value">{stats['total_games']}</div>
        <div class="metric-label">Total Games</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="premium-metric" style="border-color: rgba(67, 233, 123, 0.5);">
        <div class="metric-icon" style="color: #43e97b;">📈</div>
        <div class="metric-value">{stats['avg_high_score']}</div>
        <div class="metric-label">Avg High Score</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TABS FOR DIFFERENT VIEWS
# ═══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["📋 User List", "📊 Analytics", "🏆 Leaderboard", "🔍 User Details", "⚙️ Account Management", "❓ Question Management", "📈 Level Progress"])

# TAB 1: User List
with tab1:
    st.markdown('<h2 class="section-header"><span>📋</span> All Users Progress</h2>', unsafe_allow_html=True)
    
    # Search and filter
    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input("🔍 Search by username or email", "", placeholder="Type to search...")
    with col2:
        level_filter = st.selectbox("📍 Filter by Level", ["All"] + [f"Level {i}" for i in range(1, 7)])
    
    # Apply filters
    filtered_df = df.copy()
    if search:
        filtered_df = filtered_df[
            filtered_df['Username'].str.contains(search, case=False) | 
            filtered_df['Email'].str.contains(search, case=False)
        ]
    if level_filter != "All":
        level_num = int(level_filter.split()[1])
        filtered_df = filtered_df[filtered_df['Level'] == level_num]
    
    # Display table
    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=400,
        column_config={
            "Username": st.column_config.TextColumn("👤 Username", width="medium"),
            "Level": st.column_config.NumberColumn("📍 Level", format="%d"),
            "Score": st.column_config.NumberColumn("🎯 Score", format="%d"),
            "Streak": st.column_config.NumberColumn("🔥 Streak", format="%d"),
            "Combo": st.column_config.TextColumn("⚡ Combo"),
        }
    )
    
    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download User Data (CSV)",
        data=csv,
        file_name=f"user_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

# TAB 2: Analytics
with tab2:
    st.markdown('<h2 class="section-header"><span>📊</span> Analytics Dashboard</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        level_chart = create_level_distribution_chart(df)
        if level_chart is not None:
            st.plotly_chart(level_chart, use_container_width=True)
        streak_chart = create_streak_chart(df)
        if streak_chart is not None:
            st.plotly_chart(streak_chart, use_container_width=True)
    
    with col2:
        score_chart = create_score_distribution_chart(df)
        if score_chart is not None:
            st.plotly_chart(score_chart, use_container_width=True)
        engagement_chart = create_engagement_chart(df)
        if engagement_chart is not None:
            st.plotly_chart(engagement_chart, use_container_width=True)

# TAB 3: Leaderboard
with tab3:
    st.markdown('<h2 class="section-header"><span>🏆</span> Top Performers Leaderboard</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<h3 style="color: #667eea; font-size: 1.5rem; margin-bottom: 20px;">🥇 Highest Scores</h3>', unsafe_allow_html=True)
        # Check if required columns exist
        if not df.empty and 'High Score' in df.columns and 'Username' in df.columns:
            top_scores = df.nlargest(5, 'High Score')[['Username', 'High Score']]
            for idx, row in top_scores.iterrows():
                rank = top_scores.index.get_loc(idx)
                medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
                colors = ["#FFD700", "#C0C0C0", "#CD7F32", "rgba(102, 126, 234, 0.5)", "rgba(118, 75, 162, 0.5)"]
                st.markdown(f"""
                <div class="leaderboard-item" style="border-left-color: {colors[rank]};">
                    <span class="rank-medal">{medals[rank]}</span>
                    <div style="flex: 1;">
                        <strong style="font-size: 1.1rem; color: white;">{row['Username']}</strong>
                        <div style="color: rgba(255,255,255,0.6); font-size: 0.9rem;">{row['High Score']} points</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No data available for highest scores leaderboard")
    
    with col2:
        st.markdown('<h3 style="color: #f093fb; font-size: 1.5rem; margin-bottom: 20px;">🔥 Best Streaks</h3>', unsafe_allow_html=True)
        # Check if required columns exist
        if not df.empty and 'Max Streak' in df.columns and 'Username' in df.columns:
            top_streaks = df.nlargest(5, 'Max Streak')[['Username', 'Max Streak']]
            for idx, row in top_streaks.iterrows():
                rank = top_streaks.index.get_loc(idx)
                medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
                colors = ["#FFD700", "#C0C0C0", "#CD7F32", "rgba(240, 147, 251, 0.5)", "rgba(245, 87, 108, 0.5)"]
                st.markdown(f"""
                <div class="leaderboard-item" style="border-left-color: {colors[rank]};">
                    <span class="rank-medal">{medals[rank]}</span>
                    <div style="flex: 1;">
                        <strong style="font-size: 1.1rem; color: white;">{row['Username']}</strong>
                        <div style="color: rgba(255,255,255,0.6); font-size: 0.9rem;">{row['Max Streak']}x streak</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No data available for best streaks leaderboard")
    
    with col3:
        st.markdown('<h3 style="color: #43e97b; font-size: 1.5rem; margin-bottom: 20px;">⭐ Most Perfect Levels</h3>', unsafe_allow_html=True)
        # Check if required columns exist
        if not df.empty and 'Perfect Levels' in df.columns and 'Username' in df.columns:
            top_perfect = df.nlargest(5, 'Perfect Levels')[['Username', 'Perfect Levels']]
            for idx, row in top_perfect.iterrows():
                rank = top_perfect.index.get_loc(idx)
                medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
                colors = ["#FFD700", "#C0C0C0", "#CD7F32", "rgba(67, 233, 123, 0.5)", "rgba(56, 249, 215, 0.5)"]
                st.markdown(f"""
                <div class="leaderboard-item" style="border-left-color: {colors[rank]};">
                    <span class="rank-medal">{medals[rank]}</span>
                    <div style="flex: 1;">
                        <strong style="font-size: 1.1rem; color: white;">{row['Username']}</strong>
                        <div style="color: rgba(255,255,255,0.6); font-size: 0.9rem;">{row['Perfect Levels']} perfect levels</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No data available for perfect levels leaderboard")

# TAB 4: User Details
with tab4:
    st.markdown('<h2 class="section-header"><span>🔍</span> Detailed User Information</h2>', unsafe_allow_html=True)
    
    if not df.empty:
        selected_user = st.selectbox("👤 Select User to View Details", df['Username'].tolist(), key="user_detail_select")
        
        if selected_user:
            user_row = df[df['Username'] == selected_user].iloc[0]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                <div class="info-card" style="border-color: rgba(102, 126, 234, 0.4);">
                    <h3 style="color: #667eea; margin-top: 0;">👤 User Profile</h3>
                    <div style="color: rgba(255,255,255,0.9); line-height: 2;">
                        <div><strong>Username:</strong> {}</div>
                        <div><strong>Email:</strong> {}</div>
                        <div><strong>Created:</strong> {}</div>
                        <div><strong>Last Login:</strong> {}</div>
                    </div>
                </div>
                """.format(
                    user_row['Username'],
                    user_row['Email'],
                    user_row['Created'][:10] if user_row['Created'] and user_row['Created'] != 'N/A' else 'N/A',
                    user_row['Last Login'][:10] if user_row['Last Login'] and user_row['Last Login'] != 'Never' else 'Never'
                ), unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="info-card" style="border-color: rgba(240, 147, 251, 0.4);">
                    <h3 style="color: #f093fb; margin-top: 0;">🎮 Game Stats</h3>
                    <div style="color: rgba(255,255,255,0.9); line-height: 2;">
                        <div><strong>Current Level:</strong> {}/6</div>
                        <div><strong>Current Score:</strong> {}</div>
                        <div><strong>High Score:</strong> {}</div>
                        <div><strong>Total Games:</strong> {}</div>
                    </div>
                </div>
                """.format(
                    user_row['Level'],
                    user_row['Score'],
                    user_row['High Score'],
                    user_row['Total Games']
                ), unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div class="info-card" style="border-color: rgba(67, 233, 123, 0.4);">
                    <h3 style="color: #43e97b; margin-top: 0;">🔥 Live Stats</h3>
                    <div style="color: rgba(255,255,255,0.9); line-height: 2;">
                        <div><strong>Current Streak:</strong> {}x</div>
                        <div><strong>Max Streak:</strong> {}x</div>
                        <div><strong>Combo:</strong> {}</div>
                        <div><strong>Perfect Levels:</strong> {}</div>
                        <div><strong>Hints Used:</strong> {}</div>
                    </div>
                </div>
                """.format(
                    user_row['Streak'],
                    user_row['Max Streak'],
                    user_row['Combo'],
                    user_row['Perfect Levels'],
                    user_row['Hints Used']
                ), unsafe_allow_html=True)
            
            # Progress visualization
            st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
            st.markdown('<h3 style="color: #667eea; font-size: 1.5rem;">📈 Progress Overview</h3>', unsafe_allow_html=True)
            
            progress_pct = (user_row['Level'] / 6) * 100
            st.progress(progress_pct / 100)
            st.markdown(f'<p style="color: rgba(255,255,255,0.7); font-size: 1.1rem; margin-top: 10px;">Level Progress: <strong style="color: #00ff88;">{progress_pct:.1f}%</strong> complete ({user_row["Level"]}/6 levels)</p>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-card" style="text-align: center; padding: 60px;">
            <div style="font-size: 4rem; margin-bottom: 20px;">📭</div>
            <h3 style="color: rgba(255,255,255,0.8);">No Users Found</h3>
            <p style="color: rgba(255,255,255,0.6);">The system currently has no registered users.</p>
        </div>
        """, unsafe_allow_html=True)

# TAB 5: Account Management
with tab5:
    st.markdown('<h2 class="section-header"><span>⚙️</span> Account Management</h2>', unsafe_allow_html=True)
    
    # Get all users for the entire tab
    all_users = auth_manager.get_all_users()
    user_options = [u['username'] for u in all_users] if all_users else []
    
    # Create four columns for different actions
    action_col1, action_col2, action_col3, action_col4 = st.columns(4)
    
    with action_col1:
        st.markdown("""
        <div class="info-card" style="border-color: rgba(67, 233, 123, 0.4);">
            <h3 style="color: #43e97b; margin-top: 0;">➕ Create New Account</h3>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("create_user_form"):
            new_username = st.text_input("👤 Username", placeholder="Enter username (min 3 chars)")
            new_email = st.text_input("📧 Email", placeholder="user@example.com")
            new_password = st.text_input("🔑 Password", type="password", placeholder="Enter password (min 6 chars)")
            
            submit_create = st.form_submit_button("➕ Create Account", use_container_width=True, type="primary")
            
            if submit_create:
                if new_username and new_password:
                    success, message = auth_manager.create_user_admin(new_username, new_password, new_email)
                    if success:
                        st.success(f"✅ {message}")
                        st.balloons()
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.warning("⚠️ Please fill in all required fields")
    
    with action_col2:
        st.markdown("""
        <div class="info-card" style="border-color: rgba(240, 147, 251, 0.4);">
            <h3 style="color: #f093fb; margin-top: 0;">🔄 Activate/Disable Account</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Check if users are available
        if all_users and user_options:
            
            with st.form("toggle_user_form"):
                selected_toggle_user = st.selectbox("👤 Select User", user_options, key="toggle_user_select")
                
                # Get user status
                user_status = auth_manager.get_user_status(selected_toggle_user)
                is_active = user_status.get('is_active', True) if user_status else True
                
                if is_active:
                    st.info(f"✅ Account '{selected_toggle_user}' is currently **ACTIVE**")
                else:
                    st.warning(f"⛔ Account '{selected_toggle_user}' is currently **DISABLED**")
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    submit_activate = st.form_submit_button(
                        "✅ Activate", 
                        use_container_width=True,
                        disabled=is_active
                    )
                
                with col_b:
                    submit_disable = st.form_submit_button(
                        "⛔ Disable", 
                        use_container_width=True,
                        disabled=not is_active
                    )
                
                if submit_activate:
                    success, message = auth_manager.activate_user(selected_toggle_user)
                    if success:
                        st.success(f"✅ {message}")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
                
                if submit_disable:
                    success, message = auth_manager.disable_user(selected_toggle_user)
                    if success:
                        st.warning(f"⚠️ {message}")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
        else:
            st.info("📭 No users available for management")
    
    with action_col3:
        st.markdown("""
        <div class="info-card" style="border-color: rgba(255, 0, 85, 0.4);">
            <h3 style="color: #ff0055; margin-top: 0;">🗑️ Delete Account</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if all_users and user_options:
            with st.form("delete_user_form"):
                selected_delete_user = st.selectbox("👤 Select User to Delete", user_options, key="delete_user_select")
                
                st.markdown("""
                <div style="background: rgba(255,0,85,0.1); border-left: 4px solid #ff0055; 
                            padding: 15px; margin: 15px 0; border-radius: 8px;">
                    <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 0.9rem;">
                        ⚠️ <strong>WARNING:</strong> This action is permanent and cannot be undone!
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                confirm_delete = st.checkbox("✅ I understand this action is permanent", key="confirm_delete_checkbox")
                
                submit_delete = st.form_submit_button(
                    "🗑️ DELETE ACCOUNT",
                    use_container_width=True,
                    type="primary"
                )
                
                if submit_delete:
                    if confirm_delete:
                        success, message = auth_manager.delete_user(selected_delete_user)
                        if success:
                            st.success(f"✅ {message}")
                            time.sleep(1.5)
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
                    else:
                        st.error("❌ Please check the confirmation box to delete this account")
        else:
            st.info("📭 No users available for deletion")
    
    with action_col4:
        st.markdown("""
        <div class="info-card" style="border-color: rgba(102, 126, 234, 0.4);">
            <h3 style="color: #667eea; margin-top: 0;">✏️ Edit Account Details</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if all_users and user_options:
            with st.form("edit_user_form"):
                selected_edit_user = st.selectbox("👤 Select User to Edit", user_options, key="edit_user_select")
                
                # Get current user details
                user_details = auth_manager.get_user_details(selected_edit_user)
                current_email = user_details.get('email', '') if user_details else ''
                
                st.markdown(f'<p style="color: rgba(255,255,255,0.6); font-size: 0.85rem; margin-bottom: 10px;">Current Email: <strong>{current_email if current_email else "Not set"}</strong></p>', unsafe_allow_html=True)
                
                new_email_edit = st.text_input("📧 New Email (optional)", placeholder="Leave blank to keep current")
                new_password_edit = st.text_input("🔑 New Password (optional)", type="password", placeholder="Leave blank to keep current")
                
                st.markdown("""
                <div style="background: rgba(102,126,234,0.1); border-left: 4px solid #667eea; 
                            padding: 12px; margin: 10px 0; border-radius: 8px;">
                    <p style="color: rgba(255,255,255,0.8); margin: 0; font-size: 0.85rem;">
                        💡 <strong>Tip:</strong> Fill in only the fields you want to update
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                submit_edit = st.form_submit_button(
                    "✏️ UPDATE ACCOUNT",
                    use_container_width=True,
                    type="primary"
                )
                
                if submit_edit:
                    # Check if at least one field is filled
                    if new_email_edit or new_password_edit:
                        success, message = auth_manager.update_user_details(
                            selected_edit_user,
                            new_email=new_email_edit if new_email_edit else None,
                            new_password=new_password_edit if new_password_edit else None
                        )
                        if success:
                            st.success(f"✅ {message}")
                            time.sleep(1.5)
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
                    else:
                        st.warning("⚠️ Please enter at least one field to update")
        else:
            st.info("📭 No users available for editing")
    
    # Account Management Statistics
    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #667eea; font-size: 1.5rem; margin-bottom: 20px;">📊 Account Status Overview</h3>', unsafe_allow_html=True)
    
    if all_users:
        # Calculate statistics
        total_accounts = len(all_users)
        active_accounts = sum(1 for u in all_users if u.get('is_active', True))
        disabled_accounts = total_accounts - active_accounts
        
        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
        
        with stat_col1:
            st.markdown(f"""
            <div class="premium-metric" style="border-color: rgba(102, 126, 234, 0.5);">
                <div class="metric-icon" style="color: #667eea;">👥</div>
                <div class="metric-value">{total_accounts}</div>
                <div class="metric-label">Total Accounts</div>
            </div>
            """, unsafe_allow_html=True)
        
        with stat_col2:
            st.markdown(f"""
            <div class="premium-metric" style="border-color: rgba(67, 233, 123, 0.5);">
                <div class="metric-icon" style="color: #43e97b;">✅</div>
                <div class="metric-value">{active_accounts}</div>
                <div class="metric-label">Active Accounts</div>
            </div>
            """, unsafe_allow_html=True)
        
        with stat_col3:
            st.markdown(f"""
            <div class="premium-metric" style="border-color: rgba(255, 0, 85, 0.5);">
                <div class="metric-icon" style="color: #ff0055;">⛔</div>
                <div class="metric-value">{disabled_accounts}</div>
                <div class="metric-label">Disabled Accounts</div>
            </div>
            """, unsafe_allow_html=True)
        
        with stat_col4:
            active_pct = (active_accounts / total_accounts * 100) if total_accounts > 0 else 0
            st.markdown(f"""
            <div class="premium-metric" style="border-color: rgba(240, 147, 251, 0.5);">
                <div class="metric-icon" style="color: #f093fb;">📈</div>
                <div class="metric-value">{active_pct:.1f}%</div>
                <div class="metric-label">Active Rate</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Detailed account list
        st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #667eea; font-size: 1.5rem; margin-bottom: 20px;">📝 Account Details</h3>', unsafe_allow_html=True)
        
        # Create DataFrame for account status
        account_data = []
        for user in all_users:
            status = auth_manager.get_user_status(user['username'])
            account_data.append({
                'Username': user['username'],
                'Email': user.get('email', 'N/A'),
                'Status': '✅ Active' if status.get('is_active', True) else '⛔ Disabled',
                'Created': user.get('created_at', 'N/A')[:10] if user.get('created_at') and user.get('created_at') != 'N/A' else 'N/A',
                'Last Login': user.get('last_login', 'Never')[:10] if user.get('last_login') and user.get('last_login') != 'Never' else 'Never',
                'Total Games': user.get('total_games', 0),
                'High Score': user.get('high_score', 0)
            })
        
        accounts_df = pd.DataFrame(account_data)
        st.dataframe(
            accounts_df,
            use_container_width=True,
            height=400,
            column_config={
                "Username": st.column_config.TextColumn("👤 Username", width="medium"),
                "Email": st.column_config.TextColumn("📧 Email", width="medium"),
                "Status": st.column_config.TextColumn("🟢 Status", width="small"),
                "Created": st.column_config.TextColumn("📅 Created", width="small"),
                "Last Login": st.column_config.TextColumn("🕐 Last Login", width="small"),
                "Total Games": st.column_config.NumberColumn("🎮 Games", format="%d"),
                "High Score": st.column_config.NumberColumn("🏆 High Score", format="%d")
            }
        )
    else:
        st.info("📭 No accounts to display")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 6: QUESTION MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════
with tab6:
    st.markdown('<h2 class="section-header"><span>❓</span> Question Management</h2>', unsafe_allow_html=True)
    
    # Admin authentication for API access
    if st.session_state.get("admin_authenticated", False):
        # Show login form for Django admin API access
        st.markdown("### 🔐 Django Admin API Access")
        st.info("Enter Django superuser credentials to manage questions")
        
        if "django_token" not in st.session_state:
            st.session_state.django_token = None
            
        with st.form("django_admin_login_questions"):
            django_username = st.text_input("👤 Django Username", placeholder="Enter Django superuser username")
            django_password = st.text_input("🔑 Django Password", type="password", placeholder="Enter Django superuser password")
            submit_django_login = st.form_submit_button("🔓 Authenticate with Django")
            
            if submit_django_login:
                if django_username and django_password:
                    # Try to authenticate with Django backend
                    try:
                        import requests
                        login_data = {
                            "username": django_username,
                            "password": django_password
                        }
                        response = requests.post("http://localhost:8000/api/auth/login/", json=login_data, timeout=5)
                        
                        if response.status_code == 200:
                            login_result = response.json()
                            if login_result.get("success"):
                                st.session_state.django_token = login_result.get("token")
                                st.success("✅ Django authentication successful!")
                                st.rerun()
                            else:
                                st.error("❌ Django authentication failed: " + login_result.get("message", "Unknown error"))
                        else:
                            st.error(f"❌ Django authentication failed with status code: {response.status_code}")
                    except Exception as e:
                        st.error(f"❌ Error during Django authentication: {str(e)}")
                else:
                    st.warning("⚠️ Please enter both username and password")
        
        # If we have a token, show the question management interface
        if st.session_state.django_token:
            st.success("✅ Authenticated with Django backend")
            st.markdown("---")
            
            # Create tabs for different question management operations
            question_tabs = st.tabs(["📋 View Questions", "➕ Add Question", "✏️ Edit Question", "🗑️ Delete Question"])
            
            # Tab 1: View Questions
            with question_tabs[0]:
                st.markdown("### 📋 All Questions")
                
                # Load questions from database
                try:
                    import requests
                    response = requests.get("http://localhost:8000/api/auth/questions/", timeout=5)
                    if response.status_code == 200:
                        questions_data = response.json().get('questions', [])
                        if questions_data:
                            questions_df = pd.DataFrame(questions_data)
                            st.dataframe(
                                questions_df,
                                use_container_width=True,
                                height=400,
                                column_config={
                                    "level_number": st.column_config.NumberColumn("Level", format="%d"),
                                    "category": st.column_config.TextColumn("Category"),
                                    "difficulty": st.column_config.TextColumn("Difficulty"),
                                    "points": st.column_config.NumberColumn("Points", format="%d"),
                                    "question": st.column_config.TextColumn("Question", width="large"),
                                    "answer": st.column_config.TextColumn("Answer"),
                                    "security_riddle": st.column_config.TextColumn("Security Riddle", width="medium"),
                                    "security_key": st.column_config.TextColumn("Security Key")
                                }
                            )
                        else:
                            st.info("📭 No questions found in the database.")
                    else:
                        st.error("❌ Failed to load questions from database.")
                except Exception as e:
                    st.error(f"❌ Error loading questions: {str(e)}")
            
            # Tab 2: Add Question
            with question_tabs[1]:
                st.markdown("### ➕ Add New Question")
                
                with st.form("add_question_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        level_number = st.number_input("Level Number", min_value=0, step=1)
                        category = st.text_input("Category")
                        difficulty = st.selectbox("Difficulty", ["easy", "medium", "hard"])
                        points = st.number_input("Points", min_value=1, value=10)
                        is_active = st.checkbox("Active", value=True)
                    
                    with col2:
                        question_text = st.text_area("Question Text", height=100)
                        answer = st.text_input("Answer")
                        hint = st.text_area("Hint", height=60)
                    
                    st.markdown("### 🔐 Security Challenge")
                    security_riddle = st.text_area("Security Riddle", height=80)
                    security_key = st.text_input("Security Key")
                    security_hint = st.text_area("Security Hint", height=60)
                    
                    submit_add = st.form_submit_button("➕ Add Question")
                    
                    if submit_add:
                        # Validate required fields
                        if question_text and answer and security_riddle and security_key:
                            # Prepare question data
                            question_data = {
                                "level_number": level_number,
                                "question": question_text,
                                "answer": answer,
                                "security_riddle": security_riddle,
                                "security_key": security_key,
                                "hint": hint,
                                "security_hint": security_hint,
                                "category": category,
                                "difficulty": difficulty,
                                "points": points,
                                "is_active": is_active
                            }
                            
                            # Send request to create question
                            try:
                                import requests
                                headers = {
                                    "Authorization": f"Token {st.session_state.django_token}",
                                    "Content-Type": "application/json"
                                }
                                response = requests.post(
                                    "http://localhost:8000/api/auth/questions/create/",
                                    json=question_data,
                                    headers=headers,
                                    timeout=10
                                )
                                
                                if response.status_code == 201:
                                    result = response.json()
                                    if result.get("success"):
                                        st.success("✅ Question added successfully!")
                                        st.rerun()
                                    else:
                                        st.error("❌ Failed to add question: " + result.get("message", "Unknown error"))
                                else:
                                    st.error(f"❌ Failed to add question. Status code: {response.status_code}")
                                    try:
                                        error_data = response.json()
                                        if "errors" in error_data:
                                            for field, errors in error_data["errors"].items():
                                                st.error(f"{field}: {', '.join(errors)}")
                                    except:
                                        st.error("Response: " + response.text[:200])
                            except Exception as e:
                                st.error(f"❌ Error adding question: {str(e)}")
                        else:
                            st.warning("⚠️ Please fill in all required fields (Question Text, Answer, Security Riddle, Security Key)")
            
            # Tab 3: Edit Question
            with question_tabs[2]:
                st.markdown("### ✏️ Edit Question")
                
                # First, get list of existing questions
                try:
                    import requests
                    response = requests.get("http://localhost:8000/api/auth/questions/", timeout=5)
                    if response.status_code == 200:
                        questions_data = response.json().get('questions', [])
                        if questions_data:
                            # Create a select box with question levels
                            question_levels = [q['level_number'] for q in questions_data]
                            selected_level = st.selectbox("Select Question to Edit", question_levels)
                            
                            # Find the selected question
                            selected_question = next((q for q in questions_data if q['level_number'] == selected_level), None)
                            
                            if selected_question:
                                st.markdown(f"#### Editing Level {selected_level}")
                                
                                with st.form("edit_question_form"):
                                    col1, col2 = st.columns(2)
                                    
                                    with col1:
                                        category = st.text_input("Category", value=selected_question.get('category', ''))
                                        difficulty = st.selectbox("Difficulty", ["easy", "medium", "hard"], 
                                                                index=["easy", "medium", "hard"].index(selected_question.get('difficulty', 'medium')))
                                        points = st.number_input("Points", min_value=1, value=selected_question.get('points', 10))
                                        is_active = st.checkbox("Active", value=selected_question.get('is_active', True))
                                    
                                    with col2:
                                        question_text = st.text_area("Question Text", value=selected_question.get('question', ''), height=100)
                                        answer = st.text_input("Answer", value=selected_question.get('answer', ''))
                                        hint = st.text_area("Hint", value=selected_question.get('hint', ''), height=60)
                                    
                                    st.markdown("### 🔐 Security Challenge")
                                    security_riddle = st.text_area("Security Riddle", value=selected_question.get('security_riddle', ''), height=80)
                                    security_key = st.text_input("Security Key", value=selected_question.get('security_key', ''))
                                    security_hint = st.text_area("Security Hint", value=selected_question.get('security_hint', ''), height=60)
                                    
                                    submit_edit = st.form_submit_button("💾 Save Changes")
                                    
                                    if submit_edit:
                                        # Validate required fields
                                        if question_text and answer and security_riddle and security_key:
                                            # Prepare question data
                                            question_data = {
                                                "question": question_text,
                                                "answer": answer,
                                                "security_riddle": security_riddle,
                                                "security_key": security_key,
                                                "hint": hint,
                                                "security_hint": security_hint,
                                                "category": category,
                                                "difficulty": difficulty,
                                                "points": points,
                                                "is_active": is_active
                                            }
                                            
                                            # Send request to update question
                                            try:
                                                import requests
                                                headers = {
                                                    "Authorization": f"Token {st.session_state.django_token}",
                                                    "Content-Type": "application/json"
                                                }
                                                response = requests.put(
                                                    f"http://localhost:8000/api/auth/questions/{selected_level}/update/",
                                                    json=question_data,
                                                    headers=headers,
                                                    timeout=10
                                                )
                                                
                                                if response.status_code == 200:
                                                    result = response.json()
                                                    if result.get("success"):
                                                        st.success("✅ Question updated successfully!")
                                                        st.rerun()
                                                    else:
                                                        st.error("❌ Failed to update question: " + result.get("message", "Unknown error"))
                                                else:
                                                    st.error(f"❌ Failed to update question. Status code: {response.status_code}")
                                                    try:
                                                        error_data = response.json()
                                                        if "errors" in error_data:
                                                            for field, errors in error_data["errors"].items():
                                                                st.error(f"{field}: {', '.join(errors)}")
                                                    except:
                                                        st.error("Response: " + response.text[:200])
                                            except Exception as e:
                                                st.error(f"❌ Error updating question: {str(e)}")
                                        else:
                                            st.warning("⚠️ Please fill in all required fields (Question Text, Answer, Security Riddle, Security Key)")
                        else:
                            st.info("📭 No questions found in the database.")
                    else:
                        st.error("❌ Failed to load questions from database.")
                except Exception as e:
                    st.error(f"❌ Error loading questions: {str(e)}")
            
            # Tab 4: Delete Question
            with question_tabs[3]:
                st.markdown("### 🗑️ Delete Question")
                
                # Get list of existing questions
                try:
                    import requests
                    response = requests.get("http://localhost:8000/api/auth/questions/", timeout=5)
                    if response.status_code == 200:
                        questions_data = response.json().get('questions', [])
                        if questions_data:
                            # Create a select box with question levels
                            question_levels = [q['level_number'] for q in questions_data]
                            selected_level_delete = st.selectbox("Select Question to Delete", question_levels)
                            
                            # Find the selected question
                            selected_question = next((q for q in questions_data if q['level_number'] == selected_level_delete), None)
                            
                            if selected_question:
                                st.markdown(f"#### Question Details (Level {selected_level_delete})")
                                st.info(f"**Category:** {selected_question.get('category', '')}")
                                st.info(f"**Difficulty:** {selected_question.get('difficulty', '')}")
                                st.info(f"**Points:** {selected_question.get('points', 0)}")
                                st.warning(f"**Question:** {selected_question.get('question', '')}")
                                
                                # Confirmation checkbox
                                confirm_delete = st.checkbox("⚠️ I confirm that I want to delete this question")
                                
                                if st.button("🗑️ Delete Question", disabled=not confirm_delete):
                                    # Send request to delete question
                                    try:
                                        import requests
                                        headers = {
                                            "Authorization": f"Token {st.session_state.django_token}"
                                        }
                                        response = requests.delete(
                                            f"http://localhost:8000/api/auth/questions/{selected_level_delete}/delete/",
                                            headers=headers,
                                            timeout=10
                                        )
                                        
                                        if response.status_code == 200:
                                            result = response.json()
                                            if result.get("success"):
                                                st.success("✅ Question deleted successfully!")
                                                st.rerun()
                                            else:
                                                st.error("❌ Failed to delete question: " + result.get("message", "Unknown error"))
                                        else:
                                            st.error(f"❌ Failed to delete question. Status code: {response.status_code}")
                                    except Exception as e:
                                        st.error(f"❌ Error deleting question: {str(e)}")
                        else:
                            st.info("📭 No questions found in the database.")
                    else:
                        st.error("❌ Failed to load questions from database.")
                except Exception as e:
                    st.error(f"❌ Error loading questions: {str(e)}")
        else:
            st.info("🔒 Please authenticate with Django admin credentials to manage questions")
    else:
        st.warning("⚠️ Please login to the admin dashboard first")
    
    st.markdown("""
    <div class="info-card">
        <h4 style="color: #667eea; margin-top: 0;">🔒 Admin-Only Access</h4>
        <p style="margin-bottom: 0; line-height: 1.6;">
            Questions are stored permanently in the database and can only be managed by administrators with proper credentials.
            This ensures game integrity and prevents unauthorized modifications.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 7: LEVEL PROGRESS
# ═══════════════════════════════════════════════════════════════════════════════
with tab7:
    st.markdown('<h2 class="section-header"><span>📈</span> Level Progress Tracking</h2>', unsafe_allow_html=True)
    
    # Admin authentication for API access
    if st.session_state.get("admin_authenticated", False):
        # Show login form for Django admin API access
        st.markdown("### 🔐 Django Admin API Access")
        st.info("Enter Django superuser credentials to access level progress data")
        
        if "django_token" not in st.session_state:
            st.session_state.django_token = None
            
        with st.form("django_admin_login"):
            django_username = st.text_input("👤 Django Username", placeholder="Enter Django superuser username")
            django_password = st.text_input("🔑 Django Password", type="password", placeholder="Enter Django superuser password")
            submit_django_login = st.form_submit_button("🔓 Authenticate with Django")
            
            if submit_django_login:
                if django_username and django_password:
                    # Try to authenticate with Django backend
                    try:
                        import requests
                        login_data = {
                            "username": django_username,
                            "password": django_password
                        }
                        response = requests.post("http://localhost:8000/api/auth/login/", json=login_data, timeout=5)
                        
                        if response.status_code == 200:
                            login_result = response.json()
                            if login_result.get("success"):
                                st.session_state.django_token = login_result.get("token")
                                st.success("✅ Django authentication successful!")
                                st.rerun()
                            else:
                                st.error("❌ Django authentication failed: " + login_result.get("message", "Unknown error"))
                        else:
                            st.error(f"❌ Django authentication failed with status code: {response.status_code}")
                    except Exception as e:
                        st.error(f"❌ Error during Django authentication: {str(e)}")
                else:
                    st.warning("⚠️ Please enter both username and password")
        
        # If we have a token, show the level progress data
        if st.session_state.django_token:
            st.success("✅ Authenticated with Django backend")
            st.markdown("---")
            
            # Load level progress data from backend
            try:
                import requests
                
                # Make authenticated request
                headers = {
                    "Authorization": f"Token {st.session_state.django_token}"
                }
                response = requests.get("http://localhost:8000/api/auth/game/progress/all/", headers=headers, timeout=5)
                
                if response.status_code == 200:
                    progress_data = response.json().get('progress', [])
                    if progress_data:
                        # Convert to DataFrame for display
                        import pandas as pd
                        progress_df = pd.DataFrame(progress_data)
                        
                        # Display filters
                        col1, col2 = st.columns(2)
                        with col1:
                            # Get unique levels for filter
                            if 'level_number' in progress_df.columns:
                                level_filter = st.selectbox("📍 Filter by Level", ["All"] + sorted(progress_df['level_number'].unique().tolist()))
                            else:
                                level_filter = "All"
                        with col2:
                            user_filter = st.text_input("👤 Filter by Username", "")
                        
                        # Apply filters
                        filtered_df = progress_df.copy()
                        if level_filter != "All" and 'level_number' in filtered_df.columns:
                            filtered_df = filtered_df[filtered_df['level_number'] == int(level_filter)]
                        if user_filter and 'username' in filtered_df.columns:
                            filtered_df = filtered_df[filtered_df['username'].str.contains(user_filter, case=False, na=False)]
                        
                        # Display data
                        st.dataframe(
                            filtered_df,
                            use_container_width=True,
                            height=400,
                            column_config={
                                "id": st.column_config.NumberColumn("ID", format="%d"),
                                "level_number": st.column_config.NumberColumn("Level", format="%d"),
                                "username": st.column_config.TextColumn("Player"),
                                "question_category": st.column_config.TextColumn("Category"),
                                "difficulty": st.column_config.TextColumn("Difficulty"),
                                "points_earned": st.column_config.NumberColumn("Points", format="%d"),
                                "riddle_solved": st.column_config.CheckboxColumn("Solved"),
                                "level_completed": st.column_config.CheckboxColumn("Completed"),
                                "hint_used": st.column_config.CheckboxColumn("Hint Used"),
                                "completed_at": st.column_config.DatetimeColumn("Completed At")
                            }
                        )
                        
                        # Summary statistics
                        st.markdown('<h3 style="color: #667eea; margin-top: 30px;">📊 Progress Summary</h3>', unsafe_allow_html=True)
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.markdown(f"""
                            <div class="premium-metric" style="border-color: rgba(102, 126, 234, 0.5);">
                                <div class="metric-icon" style="color: #667eea;">🏁</div>
                                <div class="metric-value">{len(progress_data)}</div>
                                <div class="metric-label">Total Levels</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with col2:
                            completed_count = len([p for p in progress_data if p.get('level_completed')]) if isinstance(progress_data, list) else 0
                            st.markdown(f"""
                            <div class="premium-metric" style="border-color: rgba(79, 172, 254, 0.5);">
                                <div class="metric-icon" style="color: #4facfe;">✅</div>
                                <div class="metric-value">{completed_count}</div>
                                <div class="metric-label">Completed</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with col3:
                            player_count = len(set([p.get('username') for p in progress_data if p.get('username')])) if isinstance(progress_data, list) else 0
                            st.markdown(f"""
                            <div class="premium-metric" style="border-color: rgba(240, 147, 251, 0.5);">
                                <div class="metric-icon" style="color: #f093fb;">👥</div>
                                <div class="metric-value">{player_count}</div>
                                <div class="metric-label">Players</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with col4:
                            hints_count = len([p for p in progress_data if p.get('hint_used')]) if isinstance(progress_data, list) else 0
                            st.markdown(f"""
                            <div class="premium-metric" style="border-color: rgba(67, 233, 123, 0.5);">
                                <div class="metric-icon" style="color: #43e97b;">💡</div>
                                <div class="metric-value">{hints_count}</div>
                                <div class="metric-label">Hints Used</div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("📭 No level progress data found.")
                elif response.status_code == 403:
                    st.warning("⚠️ Admin access required. The level progress endpoint requires admin privileges.")
                    st.info("💡 Please authenticate with a Django superuser account that has staff privileges.")
                    # Clear token to force re-authentication
                    st.session_state.django_token = None
                else:
                    st.error(f"❌ Failed to load level progress data from database. Status code: {response.status_code}")
                    st.info("💡 Make sure the Django backend server is running and accessible.")
            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to the backend server.")
                st.info("💡 Please ensure the Django backend server is running on http://localhost:8000")
            except Exception as e:
                st.error(f"❌ Error loading level progress data: {str(e)}")
                # Show raw response for debugging
                try:
                    st.write("Debug info:", response.text if 'response' in locals() else "No response available")
                except:
                    pass
        else:
            st.info("🔒 Please authenticate with Django admin credentials to view level progress data")
    else:
        st.warning("⚠️ Please login to the admin dashboard first")
    
    st.markdown("""
    <div class="info-card">
        <h4 style="color: #667eea; margin-top: 0;">📈 Real-time Progress Tracking</h4>
        <p style="margin-bottom: 0; line-height: 1.6;">
            Level progress is automatically saved when players complete each level. This dashboard shows real-time progress data
            for all players, allowing administrators to monitor game activity and player engagement.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
            border: 2px solid rgba(102, 126, 234, 0.2);
            border-radius: 16px;
            padding: 30px;
            text-align: center;
            margin-top: 40px;">
    <div style="display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap; gap: 20px;">
        <div>
            <div style="font-size: 1.5rem; color: #667eea;">🕐</div>
            <div style="color: rgba(255,255,255,0.6); font-size: 0.9rem; margin-top: 5px;">Last Updated</div>
            <div style="color: white; font-weight: 600; margin-top: 3px;">{}</div>
        </div>
        <div>
            <div style="font-size: 1.5rem; color: #f093fb;">👨‍💻</div>
            <div style="color: rgba(255,255,255,0.6); font-size: 0.9rem; margin-top: 5px;">Admin Dashboard</div>
            <div style="color: white; font-weight: 600; margin-top: 3px;">v3.0 Professional</div>
        </div>
        <div>
            <div style="font-size: 1.5rem; color: #43e97b;">✅</div>
            <div style="color: rgba(255,255,255,0.6); font-size: 0.9rem; margin-top: 5px;">System Status</div>
            <div style="color: #00ff88; font-weight: 600; margin-top: 3px;">All Systems Online</div>
        </div>
        <div>
            <div style="font-size: 1.5rem; color: #4facfe;">🎯</div>
            <div style="color: rgba(255,255,255,0.6); font-size: 0.9rem; margin-top: 5px;">FOSS Treasure Hunt</div>
            <div style="color: white; font-weight: 600; margin-top: 3px;">Monitoring Active</div>
        </div>
    </div>
</div>
""".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), unsafe_allow_html=True)
