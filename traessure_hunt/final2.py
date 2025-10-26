import streamlit as st
import random
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import time
import requests
import json
import toml
from auth_manager import JSONAuthManager

# ═══════════════════════════════════════════════════════════════════════════════
# DJANGO API INTEGRATION
# ═══════════════════════════════════════════════════════════════════════════════
API_BASE_URL = "http://localhost:8000/api/auth"

# Initialize JSON Auth Manager for offline mode
json_auth = JSONAuthManager("users.json")

class DjangoAPI:
    """Helper class for Django backend API integration"""
    
    @staticmethod
    def register_user(username: str, email: str, password: str) -> Tuple[bool, str, Optional[dict]]:
        """Register a new user in Django database or JSON fallback"""
        try:
            response = requests.post(
                f"{API_BASE_URL}/register/",
                json={
                    "username": username,
                    "email": email,
                    "password": password,
                    "password_confirm": password
                },
                timeout=5
            )
            
            if response.status_code == 201:
                data = response.json()
                # Also save to JSON for offline backup
                json_auth.register_user(username, password, email)
                return True, "Registration successful!", data
            else:
                error_data = response.json()
                error_msg = error_data.get('errors', {}).get('username', ['Registration failed'])[0]
                return False, str(error_msg), None
                
        except requests.exceptions.ConnectionError:
            # Fallback to JSON authentication
            return json_auth.register_user(username, password, email)
        except Exception as e:
            # Fallback to JSON authentication
            return json_auth.register_user(username, password, email)
    
    @staticmethod
    def login_user(username: str, password: str) -> Tuple[bool, str, Optional[dict]]:
        """Login user via Django backend or JSON fallback"""
        try:
            response = requests.post(
                f"{API_BASE_URL}/login/",
                json={"username": username, "password": password},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                return True, data.get('message', 'Login successful'), data
            else:
                return False, "Invalid username or password", None
                
        except requests.exceptions.ConnectionError:
            # Fallback to JSON authentication
            return json_auth.login_user(username, password)
        except Exception as e:
            # Fallback to JSON authentication
            return json_auth.login_user(username, password)
    
    @staticmethod
    def check_backend_status() -> bool:
        """Check if Django backend is running"""
        try:
            response = requests.get(f"{API_BASE_URL}/achievements/all/", timeout=2)
            return response.status_code in [200, 401, 403]  # Backend is up
        except:
            return False
    
    @staticmethod
    def get_questions() -> Optional[List[Dict]]:
        """Fetch questions from Django backend"""
        try:
            response = requests.get(f"{API_BASE_URL}/questions/", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get('questions', [])
            else:
                print(f"❌ Backend returned status code {response.status_code} when fetching questions")
                return None
        except requests.exceptions.ConnectionError as e:
            print(f"❌ Connection error when fetching questions: {e}")
            return None
        except requests.exceptions.Timeout as e:
            print(f"❌ Timeout error when fetching questions: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error when fetching questions: {e}")
            return None

    @staticmethod
    def save_progress(username: str, level: int, score: int, hints_used: int = 0, 
                     achievements: list = None, streak: int = 0, max_streak: int = 0,
                     combo_multiplier: float = 1.0, perfect_levels: int = 0,
                     wrong_attempts: int = 0) -> bool:
        """Save user's game progress with all stats to backend or JSON"""
        try:
            # Try Django backend first
            response = requests.post(
                f"{API_BASE_URL}/game/level/",
                json={
                    "username": username,
                    "level": level,
                    "score": score,
                    "hints_used": hints_used,
                    "achievements": achievements or [],
                    "streak": streak,
                    "max_streak": max_streak,
                    "combo_multiplier": combo_multiplier,
                    "perfect_levels": perfect_levels,
                    "wrong_attempts": wrong_attempts
                },
                headers={'Authorization': f'Token {st.session_state.auth_token}'} if st.session_state.get('auth_token') else {},
                timeout=5
            )
            return response.status_code == 200
        except:
            # Fallback to JSON
            return json_auth.save_progress(
                username, level, score, hints_used, achievements,
                streak, max_streak, combo_multiplier, perfect_levels, wrong_attempts
            )
    
    @staticmethod
    def mark_game_completed_permanently(username: str) -> bool:
        """Mark game as completed permanently to prevent replay"""
        try:
            # Try Django backend first
            response = requests.post(
                f"{API_BASE_URL}/game/mark_completed/",
                json={
                    "username": username
                },
                timeout=5
            )
            return response.status_code == 200
        except:
            # Fallback to JSON
            return json_auth.mark_game_completed_permanently(username)
    
    @staticmethod
    def load_progress(username: str) -> Optional[dict]:
        """Load user's saved game progress from backend or JSON"""
        try:
            # Try Django backend first
            # Get active session first
            session_response = requests.get(
                f"{API_BASE_URL}/game/session/",
                headers={'Authorization': f'Token {st.session_state.auth_token}'} if st.session_state.get('auth_token') else {},
                timeout=5
            )
            if session_response.status_code == 200:
                session_data = session_response.json()
                session_id = session_data.get('session', {}).get('id')
                if session_id:
                    # Get progress for this session
                    response = requests.get(
                        f"{API_BASE_URL}/game/session/{session_id}/progress/",
                        headers={'Authorization': f'Token {st.session_state.auth_token}'} if st.session_state.get('auth_token') else {},
                        timeout=5
                    )
                    if response.status_code == 200:
                        progress_data = response.json().get('progress', [])
                        if progress_data:
                            # Find the highest level completed
                            max_level = max([p.get('level_number', 0) for p in progress_data])
                            # Return the progress of the highest level
                            for p in progress_data:
                                if p.get('level_number') == max_level:
                                    return p
        except:
            pass
        
        # Fallback to JSON
        return json_auth.load_progress(username)
    
    @staticmethod
    def clear_progress(username: str) -> bool:
        """Clear user's saved game progress"""
        try:
            # Try Django backend first
            # Get active session first
            session_response = requests.get(
                f"{API_BASE_URL}/game/session/",
                headers={'Authorization': f'Token {st.session_state.auth_token}'} if st.session_state.get('auth_token') else {},
                timeout=5
            )
            if session_response.status_code == 200:
                session_data = session_response.json()
                session_id = session_data.get('session', {}).get('id')
                if session_id:
                    # Clear all level progress for this session
                    response = requests.delete(
                        f"{API_BASE_URL}/game/session/{session_id}/progress/clear/",
                        headers={'Authorization': f'Token {st.session_state.auth_token}'} if st.session_state.get('auth_token') else {},
                        timeout=5
                    )
                    if response.status_code == 200:
                        return True
        except:
            pass
        
        # Fallback to JSON
        return json_auth.clear_progress(username)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="FOSS Treasure Hunt",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════════════
# LEGENDARY STYLING SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;500;700&display=swap');

    :root {
        --primary-glow: #00ffff;
        --secondary-glow: #ff00ff;
        --success-glow: #00ff88;
        --danger-glow: #ff0055;
        --gold-glow: #ffd700;
    }

    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Rajdhani', sans-serif;
    }

    /* ═══════════════════════════════════════════════════════════════ */
    /* ANIMATED HERO TITLE */
    /* ═══════════════════════════════════════════════════════════════ */
    .hero-title {
        text-align: center;
        font-family: georgia;
        font-size: 4.5rem;
        font-weight: 900;
        color: blue;
        margin: 30px 0;
        letter-spacing: 3px;
    }
    
    
        .hero-title {
        text-align: center;
        font-family: 'Orbitron', monospace;
        font-size: 4.5rem;
        font-weight: 900;
        background: linear-gradient(45deg, #00ffff, #ff00ff, #00ffff);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientShift 3s ease infinite, heroGlow 2s ease-in-out infinite;
        margin: 30px 0;
        letter-spacing: 8px;
        text-transform: uppercase;
    }

    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }

    @keyframes heroGlow {
        0%, 100% { 
            filter: drop-shadow(0 0 20px var(--primary-glow)) 
                    drop-shadow(0 0 40px var(--secondary-glow)); 
        }
        50% { 
            filter: drop-shadow(0 0 40px var(--primary-glow)) 
                    drop-shadow(0 0 60px var(--secondary-glow)); 
        }
    }


    .float-title span {
        display: inline-block;
        font-size: 50px;
        animation: float 2s ease-in-out infinite;
        animation-delay: calc(var(--i) * 0.1s);
    }

    @keyframes float {
        0% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0); }
    }

    .subtitle {
        text-align: center;
        font-size: 2rem;
        color: var(--primary-glow);
        font-weight: 700;
        text-shadow: 0 0 20px var(--primary-glow);
        animation: pulse 2s ease-in-out infinite;
        margin-bottom: 30px;
    }

    /* ═══════════════════════════════════════════════════════════════ */
    /* GLASSMORPHIC CONTAINERS */
    /* ═══════════════════════════════════════════════════════════════ */
    .glass-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 8px 32px 0 rgba(0, 255, 255, 0.2);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    .glass-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 48px 0 rgba(0, 255, 255, 0.4);
        border-color: rgba(0, 255, 255, 0.3);
    }

    /* INFO BOX STYLING */
    .info-box {
        background: rgba(0, 0, 0, 0.85);
        border: 3px solid transparent;
        background-image: 
            linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)),
            linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%);
        background-origin: border-box;
        background-clip: padding-box, border-box;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        color: #FFF0F0;
        text-align: center;
        box-shadow: 0 0 30px rgba(102, 126, 234, 0.5);
        transition: all 0.4s ease;
        cursor: pointer;
    }

    .info-box:hover {
        transform: scale(1.02);
        box-shadow: 0 0 50px rgba(102, 126, 234, 0.8), 0 10px 30px rgba(118, 75, 162, 0.6);
        background-image: 
            linear-gradient(rgba(0, 0, 0, 0.9), rgba(0, 0, 0, 0.9)),
            linear-gradient(135deg, #00f2fe 0%, #4facfe 25%, #f093fb 50%, #764ba2 75%, #667eea 100%);
    }

    /* ═══════════════════════════════════════════════════════════════ */
    /* RIDDLE DISPLAY - NEON CYBERPUNK */
    /* ═══════════════════════════════════════════════════════════════ */
    .riddle-container {
        background: rgba(10, 14, 39, 0.95);
        border: 3px solid;
        border-image: linear-gradient(45deg, var(--primary-glow), var(--secondary-glow), var(--gold-glow)) 1;
        padding: 35px;
        border-radius: 15px;
        margin: 25px 0;
        position: relative;
        overflow: hidden;
        animation: borderPulse 3s ease-in-out infinite;
    }

    .riddle-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(0, 255, 255, 0.1), transparent);
        transform: rotate(45deg);
        animation: scanline 4s linear infinite;
    }

    @keyframes scanline {
        0% { transform: translateY(-100%) rotate(45deg); }
        100% { transform: translateY(100%) rotate(45deg); }
    }

    @keyframes borderPulse {
        0%, 100% { box-shadow: 0 0 20px rgba(0, 255, 255, 0.5); }
        50% { box-shadow: 0 0 40px rgba(255, 0, 255, 0.7); }
    }

    .riddle-text {
        font-size: 1.4rem;
        line-height: 2;
        color: #ffffff;
        text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
        position: relative;
        z-index: 1;
        font-weight: 500;
    }

    /* ═══════════════════════════════════════════════════════════════ */
    /* SECURITY PHASE - DANGER ZONE */
    /* ═══════════════════════════════════════════════════════════════ */
    .security-zone {
        background: linear-gradient(135deg, rgba(255, 0, 85, 0.1), rgba(255, 100, 0, 0.1));
        border: 3px solid var(--danger-glow);
        border-radius: 20px;
        padding: 30px;
        margin: 25px 0;
        position: relative;
        animation: dangerPulse 2s ease-in-out infinite;
    }

    @keyframes dangerPulse {
        0%, 100% { 
            box-shadow: 0 0 30px rgba(255, 0, 85, 0.4),
                        inset 0 0 30px rgba(255, 0, 85, 0.1); 
        }
        50% { 
            box-shadow: 0 0 50px rgba(255, 0, 85, 0.7),
                        inset 0 0 50px rgba(255, 0, 85, 0.2); 
        }
    }

    .security-title {
        font-size: 2rem;
        color: var(--danger-glow);
        text-shadow: 0 0 20px var(--danger-glow);
        font-weight: 700;
        margin-bottom: 20px;
        animation: flicker 1.5s infinite;
    }

    @keyframes flicker {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.85; }
    }

    /* ═══════════════════════════════════════════════════════════════ */
    /* PROGRESS TRACKER - HOLOGRAPHIC */
    /* ═══════════════════════════════════════════════════════════════ */
    .progress-ring {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        background: conic-gradient(
            from 0deg,
            var(--primary-glow) 0deg,
            var(--secondary-glow) calc(var(--progress) * 3.6deg),
            rgba(255, 255, 255, 0.1) calc(var(--progress) * 3.6deg)
        );
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 20px auto;
        position: relative;
        animation: rotate 3s linear infinite;
        box-shadow: 0 0 40px rgba(0, 255, 255, 0.5);
    }

    .progress-ring::before {
        content: '';
        position: absolute;
        width: 85%;
        height: 85%;
        background: #0a0e27;
        border-radius: 50%;
    }

    .progress-content {
        position: relative;
        z-index: 1;
        text-align: center;
        font-family: 'Orbitron', monospace;
    }

    @keyframes rotate {
        100% { filter: hue-rotate(360deg); }
    }

    /* ═══════════════════════════════════════════════════════════════ */
    /* NODE TRACKER - 3D EFFECT */
    /* ═══════════════════════════════════════════════════════════════ */
    .node-tracker {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-wrap: wrap;
        gap: 15px;
        margin: 30px 0;
        padding: 20px;
    }

    .node {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: linear-gradient(145deg, #1a1a2e, #16213e);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1.2rem;
        color: #666;
        position: relative;
        transition: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.3),
                    -5px -5px 15px rgba(255, 255, 255, 0.05);
    }

    .node.completed {
        background: linear-gradient(145deg, var(--success-glow), #00cc66);
        color: white;
        box-shadow: 0 0 30px var(--success-glow),
                    5px 5px 15px rgba(0, 255, 136, 0.4);
        transform: scale(1.15) rotateY(360deg);
    }

    .node.active {
        background: linear-gradient(145deg, var(--primary-glow), #0099ff);
        color: white;
        animation: activeNode 1.5s ease-in-out infinite;
        box-shadow: 0 0 40px var(--primary-glow);
    }

    @keyframes activeNode {
        0%, 100% { transform: scale(1) rotate(0deg); }
        25% { transform: scale(1.2) rotate(5deg); }
        50% { transform: scale(1.15) rotate(0deg); }
        75% { transform: scale(1.2) rotate(-5deg); }
    }

    .node-connector {
        width: 50px;
        height: 4px;
        background: linear-gradient(90deg, #1a1a2e, #16213e);
        position: relative;
    }

    .node-connector.active {
        background: linear-gradient(90deg, var(--success-glow), var(--primary-glow));
        box-shadow: 0 0 10px var(--success-glow);
        animation: flowEnergy 1s linear infinite;
    }

    @keyframes flowEnergy {
        0% { background-position: 0% 50%; }
        100% { background-position: 100% 50%; }
    }

    /* ═══════════════════════════════════════════════════════════════ */
    /* STATS CARDS - HOLOGRAPHIC */
    /* ═══════════════════════════════════════════════════════════════ */
    .stat-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(0, 255, 255, 0.3);
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }

    .stat-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(0, 255, 255, 0.1), transparent);
        transform: rotate(45deg);
        transition: all 0.6s ease;
    }

    .stat-card:hover {
        transform: translateY(-10px) scale(1.05);
        border-color: var(--primary-glow);
        box-shadow: 0 15px 40px rgba(0, 255, 255, 0.4);
    }

    .stat-card:hover::before {
        transform: rotate(45deg) translate(50%, 50%);
    }

    .stat-value {
        font-size: 3rem;
        font-weight: 900;
        font-family: 'Orbitron', monospace;
        background: linear-gradient(45deg, var(--primary-glow), var(--gold-glow));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 10px 0;
    }

    .stat-label {
        color: rgba(255, 255, 255, 0.7);
        font-size: 1.1rem;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* ═══════════════════════════════════════════════════════════════ */
    /* BADGES & ACHIEVEMENTS */
    /* ═══════════════════════════════════════════════════════════════ */
    .badge {
        display: inline-block;
        padding: 12px 24px;
        border-radius: 25px;
        font-weight: 700;
        margin: 8px;
        font-size: 1rem;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .badge-easy {
        background: linear-gradient(135deg, #00ff88, #00cc66);
        color: #0a0e27;
        box-shadow: 0 5px 20px rgba(0, 255, 136, 0.4);
    }

    .badge-medium {
        background: linear-gradient(135deg, #ffa500, #ff8c00);
        color: white;
        box-shadow: 0 5px 20px rgba(255, 165, 0, 0.4);
    }

    .badge-hard {
        background: linear-gradient(135deg, #ff0055, #cc0044);
        color: white;
        box-shadow: 0 5px 20px rgba(255, 0, 85, 0.4);
    }

    .badge:hover {
        transform: translateY(-3px) scale(1.1);
        box-shadow: 0 10px 30px rgba(255, 255, 255, 0.3);
    }

    /* ═══════════════════════════════════════════════════════════════ */
    /* HINT SYSTEM */
    /* ═══════════════════════════════════════════════════════════════ */
    .hint-container {
        background: linear-gradient(135deg, rgba(255, 193, 7, 0.1), rgba(255, 152, 0, 0.1));
        border-left: 5px solid #ffc107;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        animation: hintGlow 2s ease-in-out infinite;
    }

    @keyframes hintGlow {
        0%, 100% { box-shadow: 0 0 15px rgba(255, 193, 7, 0.3); }
        50% { box-shadow: 0 0 30px rgba(255, 193, 7, 0.6); }
    }

    /* ═══════════════════════════════════════════════════════════════ */
    /* VICTORY SCREEN - EPIC */
    /* ═══════════════════════════════════════════════════════════════ */
    .victory-container {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.1), rgba(255, 140, 0, 0.1));
        border: 5px solid var(--gold-glow);
        border-radius: 30px;
        padding: 50px;
        text-align: center;
        margin: 30px 0;
        animation: victoryShine 3s ease-in-out infinite;
        position: relative;
        overflow: hidden;
    }

    @keyframes victoryShine {
        0%, 100% { 
            box-shadow: 0 0 50px rgba(255, 215, 0, 0.5),
                        inset 0 0 50px rgba(255, 215, 0, 0.2);
        }
        50% { 
            box-shadow: 0 0 80px rgba(255, 215, 0, 0.8),
                        inset 0 0 80px rgba(255, 215, 0, 0.3);
        }
    }

    .victory-title {
        font-size: 5rem;
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        background: linear-gradient(45deg, #ffd700, #ffed4e, #ffd700);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: goldShimmer 2s ease-in-out infinite;
        margin-bottom: 30px;
    }

    @keyframes goldShimmer {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }

    /* ═══════════════════════════════════════════════════════════════ */
    /* PARTICLE EFFECTS */
    /* ═══════════════════════════════════════════════════════════════ */
    .particle {
        position: fixed;
        pointer-events: none;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        animation: float 3s ease-in-out infinite;
        z-index: 1000;
    }

    @keyframes confettiFall {
        0% { transform: translateY(-10vh) rotate(0deg); opacity: 1; }
        100% { transform: translateY(110vh) rotate(720deg); opacity: 0.8; }
    }

    .confetti-piece {
        position: fixed;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        animation: confettiFall 4s linear infinite;
        pointer-events: none;
    }

    /* FIREWORK ANIMATION */
    .firework {
        position: fixed;
        pointer-events: none;
        width: 5px;
        height: 5px;
        border-radius: 50%;
        animation: explode 1.5s ease-out forwards;
        z-index: 1000;
    }

    @keyframes explode {
        0% {
            transform: translate(var(--startX), var(--startY)) scale(1);
            opacity: 1;
        }
        50% {
            transform: translate(var(--midX), var(--midY)) scale(1.5);
            opacity: 0.8;
        }
        100% {
            transform: translate(var(--endX), var(--endY)) scale(0);
            opacity: 0;
        }
    }

    /* ═══════════════════════════════════════════════════════════════ */
    /* PHASE INDICATOR */
    /* ═══════════════════════════════════════════════════════════════ */
    .phase-banner {
        background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.2), transparent);
        border-top: 2px solid var(--primary-glow);
        border-bottom: 2px solid var(--primary-glow);
        padding: 20px;
        text-align: center;
        margin: 25px 0;
        animation: phasePulse 2s ease-in-out infinite;
    }

    @keyframes phasePulse {
        0%, 100% { border-color: var(--primary-glow); }
        50% { border-color: var(--secondary-glow); }
    }

    .phase-text {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--primary-glow);
        text-shadow: 0 0 20px var(--primary-glow);
        font-family: 'Orbitron', monospace;
        letter-spacing: 3px;
    }

    /* COMPLETED LEVEL CARD */
    .completed-level {
        background: rgba(76, 175, 80, 0.2);
        border-left: 4px solid #4CAF50;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
        color: #4CAF50;
        font-weight: bold;
    }

    /* ═══════════════════════════════════════════════════════════════ */
    /* RESPONSIVE DESIGN */
    /* ═══════════════════════════════════════════════════════════════ */
    @media (max-width: 768px) {
        .hero-title { font-size: 2.5rem; letter-spacing: 3px; }
        .subtitle { font-size: 1.5rem; }
        .riddle-text { font-size: 1.1rem; }
        .node { width: 40px; height: 40px; font-size: 1rem; }
        .stat-value { font-size: 2rem; }
        .victory-title { font-size: 3rem; }
    }

    /* ═══════════════════════════════════════════════════════════════ */
    /* STREAMLIT OVERRIDES */
    /* ═══════════════════════════════════════════════════════════════ */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-glow), var(--secondary-glow));
        color: white;
        border: none;
        border-radius: 15px;
        padding: 15px 35px;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 5px 20px rgba(0, 255, 255, 0.4);
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(0, 255, 255, 0.6);
    }

    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid rgba(0, 255, 255, 0.3);
        border-radius: 10px;
        color: white;
        padding: 15px;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }

    .stTextInput > div > div > input:focus {
        border-color: var(--primary-glow);
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ENHANCED GAME DATA WITH 6 LEVELS
# ═══════════════════════════════════════════════════════════════════════════════

# Load answers from TOML file for security
answers_data = toml.load("answers.toml")
answers = answers_data["questions"]

QUESTIONS: List[Dict] = [
    {
        "question": "🔍 The Hidden Core\n\nI am invisible but control it all,\nCPU, memory, devices—I stand tall.\nWithout me, Linux would never run,\nFind my name, and Level 2 is begun.",
        "answer": answers["level_1_answer"],
        "security_riddle": "What 3-letter command shows you where you are in the Linux filesystem?",
        "security_key": answers["level_1_security_key"],
        "hint": "💡 Think of the 'heart' of the operating system that manages hardware.",
        "security_hint": "💡 Stands for 'Print Working Directory'.",
        "category": "OS Architecture",
        "difficulty": "easy",
        "points": 10
    },
    {
        "question": "🔍 The Command Interpreter\n\nI'm not food, but I'm called a shell,\nWithout me, using the kernel is hell.\nI take your commands, one by one,\nBash, Zsh, Fish—I'm the one!",
        "answer": answers["level_2_answer"],
        "security_riddle": "What license ensures software remains free and open source? (3 letters, created by FSF)",
        "security_key": answers["level_2_security_key"],
        "hint": "💡 The interface between users and the kernel. Famous types include Bash and Zsh.",
        "security_hint": "💡 GNU _____ License. Richard Stallman's creation.",
        "category": "System Components",
        "difficulty": "medium",
        "points": 15
    },
    {
        "question": "🔍 The Ancient Ancestor\n\nBorn at Bell Labs in the 1970s,\nI shaped today's systems and realities.\nLinux is my child, that's true,\nFour letters, can you name me too?",
        "answer": answers["level_3_answer"],
        "security_riddle": "Decode: 01101100 01101001 01101110 01110101 01111000",
        "security_key": answers["level_3_security_key"],
        "hint": "💡 The operating system that inspired Linux. Starts with 'U'.",
        "security_hint": "💡 Convert binary to ASCII. Each group is 8 bits = 1 character.",
        "category": "OS History",
        "difficulty": "hard",
        "points": 20
    },
    {
        "question": "🔍 The Software Manager\n\nI fetch, install, and update with ease,\napt, yum, pacman—examples of me.\nWithout me, your software is stranded,\nWhat's my name, two words demanded?",
        "answer": answers["level_4_answer"],
        "security_riddle": "What command changes your current directory in Linux? (2 letters)",
        "security_key": answers["level_4_security_key"],
        "hint": "💡 Two words. First word is 'Package'. Manages software installation.",
        "security_hint": "💡 'Change Directory' - one of the most basic Linux commands.",
        "category": "System Tools",
        "difficulty": "medium",
        "points": 15
    },
    {
        "question": "🔍 The Permission Master\n\nI control who can read, write, execute,\nThree groups of three—that's my tribute.\nOwner, group, others—I set the law,\nWhat am I called? Answer with awe.",
        "answer": answers["level_5_answer"],
        "security_riddle": "What famous OS did Linus Torvalds create? (5 letters)",
        "security_key": answers["level_5_security_key"],
        "hint": "💡 A Linux command to change file permissions. Starts with 'ch'.",
        "security_hint": "💡 The creator's first name is Linus. OS released in 1991.",
        "category": "File System",
        "difficulty": "medium",
        "points": 15
    },
    {
        "question": "🔍 The Final Treasure\n\nI wrote the kernel back in '91,\nFor fun at first, but now it runs everyone.\nA Finnish programmer, still maintaining today,\nWho am I—can you say?",
        "answer": answers["level_6_answer"],
        "security_riddle": "What 3-letter open source version control system did Linus also create?",
        "security_key": answers["level_6_security_key"],
        "hint": "💡 His first name is Linus. Created Linux as a student project.",
        "security_hint": "💡 Rhymes with 'sit'. Used for tracking code changes.",
        "category": "Linux History",
        "difficulty": "hard",
        "points": 20
    }
]
import random
import time
from datetime import datetime
from typing import Tuple

import streamlit as st


# ═══════════════════════════════════════════════════════════════════════════════
# SESSION STATE MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════
def init_session_state():
    """Initialize all session state variables with proper defaults"""
    defaults = {
        "logged_in": False,
        "username": "",
        "backend_connected": False,
        "auth_token": None,
        "user_id": None,
        "level": 0,
        "score": 0,
        "hints_used": 0,
        "start_time": datetime.now(),
        "show_hint": False,
        "show_security_hint": False,
        "finished": False,
        "streak": 0,
        "max_streak": 0,
        "wrong_attempts": 0,
        "security_wrong_attempts": 0,
        "level_start_time": datetime.now(),
        "riddle_solved": False,
        "combo_multiplier": 1.0,
        "perfect_levels": 0,
        "total_time_spent": 0,
        "achievements": [],
        "show_riddle_animation": False,
        "show_level_animation": False,
        "game_completed_permanently": False
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    # Check backend status on first load
    if "backend_checked" not in st.session_state:
        st.session_state.backend_connected = DjangoAPI.check_backend_status()
        st.session_state.backend_checked = True
    
    # Load questions from API or use fallback
    if "questions_loaded" not in st.session_state:
        if st.session_state.backend_connected:
            api_questions = DjangoAPI.get_questions()
            if api_questions:
                # Convert API questions to the format expected by the frontend
                converted_questions = []
                for q in api_questions:
                    converted_questions.append({
                        "question": q["question"],
                        "answer": q["answer"],
                        "security_riddle": q["security_riddle"],
                        "security_key": q["security_key"],
                        "hint": q["hint"],
                        "security_hint": q["security_hint"],
                        "category": q["category"],
                        "difficulty": q["difficulty"],
                        "points": q["points"]
                    })
                st.session_state.QUESTIONS = converted_questions
                st.session_state.questions_source = "database"
                st.success("✅ Questions loaded from database!")
            else:
                st.session_state.QUESTIONS = QUESTIONS  # Fallback to hardcoded
                st.session_state.questions_source = "fallback"
                st.warning("⚠️ Using fallback questions - backend connection issue")
        else:
            st.session_state.QUESTIONS = QUESTIONS  # Fallback to hardcoded
            st.session_state.questions_source = "fallback"
            st.warning("⚠️ Backend server not running - using fallback questions. To enable full functionality, please start the Django backend server.")
        st.session_state.questions_loaded = True


# ═══════════════════════════════════════════════════════════════════════════════
# LOGIN SYSTEM - PROFESSIONAL UI/UX
# ═══════════════════════════════════════════════════════════════════════════════
def render_login_page():
    """Render the professional-grade futuristic login page with enhanced UX"""
    
    # Enhanced Login Page Styling
    st.markdown('''
    <style>
        /* Professional Login Container */
        .login-hero {
            text-align: center;
            padding: 60px 20px 40px;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
            border-radius: 20px;
            margin-bottom: 40px;
            position: relative;
            overflow: hidden;
        }
        
        .login-hero::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(0, 255, 255, 0.05), transparent);
            animation: scanline 8s linear infinite;
        }
        
        @keyframes scanline {
            0% { transform: translateX(-100%) rotate(45deg); }
            100% { transform: translateX(100%) rotate(45deg); }
        }
        
        .login-icon {
            font-size: 7rem;
            display: inline-block;
            animation: iconPulse 3s ease-in-out infinite;
            filter: drop-shadow(0 0 30px rgba(0, 255, 255, 0.6));
        }
        
        @keyframes iconPulse {
            0%, 100% { 
                transform: scale(1) rotateY(0deg);
                filter: drop-shadow(0 0 30px rgba(0, 255, 255, 0.6));
            }
            50% { 
                transform: scale(1.1) rotateY(180deg);
                filter: drop-shadow(0 0 50px rgba(255, 0, 255, 0.8));
            }
        }
        
        /* Professional Form Styling */
        .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.08) !important;
            border: 2px solid rgba(0, 255, 255, 0.3) !important;
            border-radius: 12px !important;
            color: white !important;
            padding: 16px 20px !important;
            font-size: 1.05rem !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        
        .stTextInput > div > div > input:focus {
            border-color: var(--primary-glow) !important;
            box-shadow: 0 0 25px rgba(0, 255, 255, 0.4), 0 4px 20px rgba(0, 0, 0, 0.3) !important;
            background: rgba(255, 255, 255, 0.12) !important;
            transform: translateY(-2px);
        }
        
        .stTextInput > div > div > input::placeholder {
            color: rgba(255, 255, 255, 0.4) !important;
        }
        
        /* Enhanced Button Styling */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 16px 40px !important;
            font-weight: 700 !important;
            font-size: 1.15rem !important;
            text-transform: uppercase !important;
            letter-spacing: 1.5px !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
            position: relative !important;
            overflow: hidden !important;
        }
        
        .stButton > button::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }
        
        .stButton > button:hover::before {
            width: 300px;
            height: 300px;
        }
        
        .stButton > button:hover {
            transform: translateY(-4px) scale(1.02) !important;
            box-shadow: 0 12px 40px rgba(102, 126, 234, 0.6) !important;
        }
        
        .stButton > button:active {
            transform: translateY(-2px) scale(0.98) !important;
        }
        
        /* Professional Info Box */
        .pro-info-box {
            background: linear-gradient(135deg, rgba(0, 255, 255, 0.08), rgba(255, 0, 255, 0.08));
            border: 2px solid rgba(0, 255, 255, 0.2);
            border-radius: 15px;
            padding: 25px;
            margin-top: 30px;
            position: relative;
            overflow: hidden;
        }
        
        .pro-info-box::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transition: left 0.5s;
        }
        
        .pro-info-box:hover::before {
            left: 100%;
        }
        
        /* Feature List */
        .feature-item {
            display: flex;
            align-items: center;
            padding: 12px 0;
            color: rgba(255, 255, 255, 0.9);
            font-size: 1.05rem;
            transition: all 0.3s;
        }
        
        .feature-item:hover {
            padding-left: 10px;
            color: var(--primary-glow);
        }
        
        .feature-icon {
            margin-right: 15px;
            font-size: 1.3rem;
        }
        
        /* Validation Messages */
        .stAlert {
            border-radius: 12px !important;
            padding: 16px 20px !important;
            animation: slideIn 0.3s ease-out;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Tab Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 20px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 10px;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 10px;
            padding: 15px 30px;
            font-size: 1.1rem;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.3), rgba(118, 75, 162, 0.3));
        }
        
        /* Password Strength Indicator */
        .strength-meter {
            height: 4px;
            border-radius: 2px;
            margin-top: 8px;
            transition: all 0.3s;
        }
        
        /* Loading Animation */
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
    ''', unsafe_allow_html=True)
    
    # Professional Hero Section
    st.markdown('''
    <div class="login-hero">
        <div class="login-icon">🔐</div>
        <h1 style="font-family: 'Orbitron', monospace; font-size: 3.5rem; font-weight: 900; 
                   margin: 20px 0 10px; background: linear-gradient(135deg, #00ffff, #ff00ff, #00ffff);
                   background-size: 200% 200%; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   animation: gradientShift 3s ease infinite;">
            ACCESS TERMINAL
        </h1>
        <p style="font-size: 1.4rem; color: var(--primary-glow); font-weight: 500;
                  text-shadow: 0 0 20px var(--primary-glow); margin-top: 10px;">
            🚀 Enter the FOSS Universe
        </p>
        <div style="margin-top: 20px; font-size: 0.95rem; color: rgba(255,255,255,0.7);">
            <span style="margin: 0 15px;">✓ Secure</span>
            <span style="margin: 0 15px;">✓ Fast</span>
            <span style="margin: 0 15px;">✓ Progressive</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Professional Form Container
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        # Professional Tabs with Enhanced UX
        tab1, tab2 = st.tabs(["🔑 Sign In", "✨ Create Account"])
        
        # ═══════════════════════════════════════════════════════════
        # TAB 1: LOGIN - PROFESSIONAL VERSION
        # ═══════════════════════════════════════════════════════════
        with tab1:
            st.markdown('''
            <div style="padding: 30px 20px 20px; text-align: center;">
                <h2 style="color: var(--primary-glow); font-size: 2.2rem; font-weight: 700; margin-bottom: 10px;">
                    Welcome Back, Hunter! 🎯
                </h2>
                <p style="color: rgba(255,255,255,0.7); font-size: 1.05rem; margin-bottom: 30px;">
                    Sign in to continue your FOSS adventure
                </p>
            </div>
            ''', unsafe_allow_html=True)
            
            with st.form("login_form", clear_on_submit=False):
                # Username Input
                st.markdown('<p style="font-weight: 600; margin-bottom: 8px; color: var(--primary-glow);">👤 Username</p>', unsafe_allow_html=True)
                username = st.text_input(
                    "Username",
                    placeholder="Enter your username",
                    key="login_username",
                    label_visibility="collapsed"
                )
                
                st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
                
                # Password Input
                st.markdown('<p style="font-weight: 600; margin-bottom: 8px; color: var(--primary-glow);">🔒 Password</p>', unsafe_allow_html=True)
                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password",
                    key="login_password",
                    label_visibility="collapsed"
                )
                
                # Remember Me & Forgot Password (Visual Only)
                col_remember, col_forgot = st.columns([1, 1])
                with col_remember:
                    st.markdown('<p style="font-size: 0.9rem; color: rgba(255,255,255,0.6); margin-top: 10px;">✓ Remember me</p>', unsafe_allow_html=True)
                with col_forgot:
                    st.markdown('<p style="font-size: 0.9rem; color: var(--secondary-glow); margin-top: 10px; text-align: right;">🔗 Forgot password?</p>', unsafe_allow_html=True)
                
                st.markdown('<div style="height: 25px;"></div>', unsafe_allow_html=True)
                
                # Submit Button
                submit_button = st.form_submit_button(
                    "🚀 ENTER GAME",
                    use_container_width=True,
                    type="primary"
                )
            
            if submit_button:
                if username.strip() == "":
                    st.error("⚠️ Username cannot be empty!")
                elif not password:
                    st.error("⚠️ Password cannot be empty!")
                else:
                    # Try authentication
                    with st.spinner("🔄 Authenticating..."):
                        success, message, data = DjangoAPI.login_user(username.strip(), password)
                        
                        if success:
                            # Login successful
                            st.session_state.logged_in = True
                            st.session_state.username = username.strip()
                            st.session_state.auth_token = data.get('token') if data else None
                            st.session_state.user_id = data.get('user', {}).get('id') if data else None
                            st.session_state.start_time = datetime.now()
                            
                            # Load saved progress
                            saved_progress = DjangoAPI.load_progress(username.strip())
                            if saved_progress:
                                st.session_state.level = saved_progress.get('level', 0)
                                st.session_state.score = saved_progress.get('score', 0)
                                st.session_state.hints_used = saved_progress.get('hints_used', 0)
                                st.session_state.achievements = saved_progress.get('achievements', [])
                                st.session_state.streak = saved_progress.get('streak', 0)
                                st.session_state.max_streak = saved_progress.get('max_streak', 0)
                                st.session_state.combo_multiplier = saved_progress.get('combo_multiplier', 1.0)
                                st.session_state.perfect_levels = saved_progress.get('perfect_levels', 0)
                                st.session_state.wrong_attempts = saved_progress.get('wrong_attempts', 0)
                                st.info(f"📥 Progress loaded! Level {st.session_state.level + 1} | 🔥 {st.session_state.streak}x streak")
                            
                            # Check if game was completed permanently
                            if saved_progress and saved_progress.get('game_completed_permanently', False):
                                st.session_state.finished = True
                                st.session_state.game_completed_permanently = True
                                st.info("🏆 Game already completed! No replay allowed.")
                            
                            st.success(f"✅ {message}")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
            
            # Professional Info Box
            st.markdown('''
            <div class="pro-info-box">
                <h4 style="color: var(--primary-glow); margin-bottom: 15px; font-size: 1.1rem;">🎮 Quick Start Guide</h4>
                <div class="feature-item">
                    <span class="feature-icon">🔐</span>
                    <span><strong>Secure Auth:</strong> Django backend + JSON fallback</span>
                </div>
                <div class="feature-item">
                    <span class="feature-icon">💾</span>
                    <span><strong>Auto-Save:</strong> Progress saved after each level</span>
                </div>
                <div class="feature-item">
                    <span class="feature-icon">🏆</span>
                    <span><strong>Achievements:</strong> Unlock badges as you progress</span>
                </div>
                <div class="feature-item">
                    <span class="feature-icon">🔥</span>
                    <span><strong>Streaks:</strong> Build combos for bonus points</span>
                </div>
                <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid rgba(0,255,255,0.2); text-align: center;">
                    <p style="color: rgba(255,255,255,0.7); font-size: 0.95rem;">
                        🆕 Don't have an account? Switch to <strong style="color: var(--secondary-glow);">Create Account</strong> tab!
                    </p>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        # ═══════════════════════════════════════════════════════════
        # TAB 2: REGISTRATION - PROFESSIONAL VERSION
        # ═══════════════════════════════════════════════════════════
        with tab2:
            st.markdown('''
            <div style="padding: 30px 20px 20px; text-align: center;">
                <h2 style="color: var(--secondary-glow); font-size: 2.2rem; font-weight: 700; margin-bottom: 10px;">
                    Join the FOSS Universe! 🌟
                </h2>
                <p style="color: rgba(255,255,255,0.7); font-size: 1.05rem; margin-bottom: 30px;">
                    Create your account and start your treasure hunt
                </p>
            </div>
            ''', unsafe_allow_html=True)
            
            with st.form("register_form", clear_on_submit=False):
                # Username Input
                st.markdown('<p style="font-weight: 600; margin-bottom: 8px; color: var(--secondary-glow);">👤 Username</p>', unsafe_allow_html=True)
                reg_username = st.text_input(
                    "Choose Username",
                    placeholder="Pick a unique username (min 3 characters)",
                    key="reg_username",
                    label_visibility="collapsed"
                )
                
                st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
                
                # Email Input
                st.markdown('<p style="font-weight: 600; margin-bottom: 8px; color: var(--secondary-glow);">📧 Email <span style="color: rgba(255,255,255,0.5); font-size: 0.9rem;">(Optional)</span></p>', unsafe_allow_html=True)
                reg_email = st.text_input(
                    "Email",
                    placeholder="your.email@example.com",
                    key="reg_email",
                    label_visibility="collapsed"
                )
                
                st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
                
                # Password Input
                st.markdown('<p style="font-weight: 600; margin-bottom: 8px; color: var(--secondary-glow);">🔒 Password</p>', unsafe_allow_html=True)
                reg_password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Choose a secure password (min 6 characters)",
                    key="reg_password",
                    label_visibility="collapsed"
                )
                
                # Password Strength Indicator (Visual)
                if 'reg_password' in st.session_state and st.session_state.reg_password:
                    strength = len(st.session_state.reg_password)
                    if strength < 6:
                        st.markdown('<div class="strength-meter" style="background: #ff4444; width: 33%;"></div>', unsafe_allow_html=True)
                        st.caption("🔴 Weak password")
                    elif strength < 10:
                        st.markdown('<div class="strength-meter" style="background: #ffaa00; width: 66%;"></div>', unsafe_allow_html=True)
                        st.caption("🟡 Medium password")
                    else:
                        st.markdown('<div class="strength-meter" style="background: #00ff88; width: 100%;"></div>', unsafe_allow_html=True)
                        st.caption("🟢 Strong password")
                
                st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
                
                # Confirm Password Input
                st.markdown('<p style="font-weight: 600; margin-bottom: 8px; color: var(--secondary-glow);">🔒 Confirm Password</p>', unsafe_allow_html=True)
                reg_password_confirm = st.text_input(
                    "Confirm Password",
                    type="password",
                    placeholder="Re-enter your password",
                    key="reg_password_confirm",
                    label_visibility="collapsed"
                )
                
                st.markdown('<div style="height: 25px;"></div>', unsafe_allow_html=True)
                
                # Submit Button
                register_button = st.form_submit_button(
                    "🌟 CREATE ACCOUNT",
                    use_container_width=True,
                    type="primary"
                )
            
            if register_button:
                # Validation
                if not reg_username.strip():
                    st.error("⚠️ Username is required!")
                elif len(reg_username.strip()) < 3:
                    st.error("⚠️ Username must be at least 3 characters!")
                elif not reg_password:
                    st.error("⚠️ Password is required!")
                elif len(reg_password) < 6:
                    st.error("⚠️ Password must be at least 6 characters!")
                elif reg_password != reg_password_confirm:
                    st.error("⚠️ Passwords do not match!")
                else:
                    # Try registration
                    with st.spinner("🔄 Creating your account..."):
                        success, message, data = DjangoAPI.register_user(
                            reg_username.strip(),
                            reg_email.strip(),
                            reg_password
                        )
                        
                        if success:
                            # Registration successful - auto login
                            st.session_state.logged_in = True
                            st.session_state.username = reg_username.strip()
                            st.session_state.auth_token = data.get('token') if data else None
                            st.session_state.user_id = data.get('user', {}).get('id') if data else None
                            st.session_state.start_time = datetime.now()
                            
                            st.success(f"✅ {message} Welcome, {reg_username}!")
                            st.info("🎮 Starting your FOSS adventure...")
                            time.sleep(1)
                            st.rerun()
                        else:
                            # Registration failed
                            st.error(f"❌ {message}")
                            st.info("💡 Tip: Try a different username or check your password length")
            
            # Registration info
            st.markdown('''
            <div style="background: rgba(255, 0, 255, 0.05); border-left: 4px solid var(--secondary-glow); 
                        padding: 20px; margin-top: 30px; border-radius: 10px;">
                <h4 style="color: var(--secondary-glow); margin-bottom: 15px;">📋 Registration Info</h4>
                <p style="line-height: 1.8; color: rgba(255,255,255,0.8);">
                    ✅ <strong>Username:</strong> Minimum 3 characters<br>
                    ✅ <strong>Password:</strong> Minimum 6 characters<br>
                    ✅ <strong>Email:</strong> Optional (for future features)<br><br>
                    🎯 Create your account to:<br>
                    • Track your progress and scores<br>
                    • Compete on the leaderboard<br>
                    • Earn achievements and badges<br>
                    • Join the FOSS community!<br>
                </p>
            </div>
            ''', unsafe_allow_html=True)
    
    # Decorative elements
    st.markdown('''
    <div style="text-align: center; margin-top: 60px; color: rgba(255,255,255,0.5);">
        <p style="font-size: 1.2rem;">Made with ❤️ for Software Freedom Day</p>
        <p style="font-size: 1rem; margin-top: 10px;">🌐 Celebrating Open Source • Building Digital Freedom</p>
    </div>
    ''', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def auto_save_progress():
    """Auto-save current game state to backend/JSON"""
    if st.session_state.get('logged_in') and st.session_state.get('username'):
        DjangoAPI.save_progress(
            st.session_state.username,
            st.session_state.level,
            st.session_state.score,
            st.session_state.hints_used,
            st.session_state.achievements,
            st.session_state.streak,
            st.session_state.max_streak,
            st.session_state.combo_multiplier,
            st.session_state.perfect_levels,
            st.session_state.wrong_attempts
        )


def get_rank() -> Tuple[str, str]:
    """Calculate player rank and icon based on comprehensive performance"""
    score = st.session_state.score
    hints = st.session_state.hints_used
    streak = st.session_state.max_streak
    perfect = st.session_state.perfect_levels

    if score >= 95 and hints == 0 and perfect == len(st.session_state.QUESTIONS):
        return "🏆 FOSS GRANDMASTER", "Perfect Score! Flawless Victory!"
    elif score >= 85 and hints <= 1:
        return "⭐ LEGENDARY HACKER", "Exceptional Performance!"
    elif score >= 75 and hints <= 2:
        return "💎 ELITE DEVELOPER", "Outstanding Skills!"
    elif score >= 60 and streak >= 4:
        return "🚀 SENIOR ENGINEER", "Great Consistency!"
    elif score >= 45:
        return "🐧 LINUX ENTHUSIAST", "Strong Knowledge!"
    elif score >= 30:
        return "🌱 FOSS EXPLORER", "Good Progress!"
    else:
        return "🔰 BEGINNER CODER", "Keep Learning!"


def format_time(seconds: float) -> str:
    """Format seconds into human-readable time"""
    if seconds < 60:
        return f"{int(seconds)}s"
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}m {secs}s"


def calculate_bonus_points(is_riddle: bool = True) -> int:
    """Calculate bonus points based on performance"""
    bonus = 0

    # No wrong attempts bonus
    attempts = st.session_state.wrong_attempts if is_riddle else st.session_state.security_wrong_attempts
    if attempts == 0:
        bonus += 5

    # Streak bonus
    if st.session_state.streak >= 3:
        bonus += 3
    if st.session_state.streak >= 5:
        bonus += 5

    # Combo multiplier
    if st.session_state.combo_multiplier > 1.0:
        bonus = int(bonus * st.session_state.combo_multiplier)

    return bonus


def create_fireworks():
    """Create firework animation for level completion"""
    colors = ["#FF595E", "#FFCA3A", "#8AC926", "#1982C4", "#6A4C93",
              "#FF9F1C", "#FA0096", "#00FAE1", "#FFD700", "#00FA15"]
    
    fireworks_html = '<div id="fireworks-container" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; pointer-events: none; z-index: 9997;">'
    
    for _ in range(30):  # 30 fireworks for celebration
        startX = random.randint(20, 80)
        startY = random.randint(50, 80)
        color = random.choice(colors)
        delay = random.uniform(0, 1.5)
        duration = random.uniform(0.8, 1.5)
        
        # Create simple particle burst animation
        fireworks_html += f'<div style="position: absolute; left: {startX}vw; top: {startY}vh; width: 8px; height: 8px; border-radius: 50%; background: {color}; animation: fireworkBurst {duration}s ease-out {delay}s; opacity: 0;"></div>'
    
    fireworks_html += '</div>'
    
    # Include the animation CSS
    fireworks_html += '''
    <style>
        @keyframes fireworkBurst {
            0% {
                transform: translate(0, 0) scale(0);
                opacity: 1;
            }
            50% {
                transform: translate(0, -40vh) scale(2);
                opacity: 0.8;
            }
            100% {
                transform: translate(0, -60vh) scale(0.5);
                opacity: 0;
            }
        }
    </style>
    '''
    
    return fireworks_html


def create_question_win_animation():
    """Create celebration animation for correct riddle answer (Phase 1)"""
    return '''
    <div id="question-win-wrapper" style="text-align: center; margin: 20px 0;">
        <div style="font-size: 4rem; animation: bounce 0.6s ease-in-out 3;">
            🎉 ✨ 🎊
        </div>
        <div style="font-size: 2rem; color: #00ff88; font-weight: 900; text-shadow: 0 0 20px #00ff88; animation: pulse 0.5s ease-in-out infinite;">
            RIDDLE SOLVED!
        </div>
    </div>
    <style>
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-30px); }
        }
    </style>
    '''


def create_level_complete_animation():
    """Create epic animation for level completion (Phase 2)"""
    stars_html = ""
    for _ in range(20):
        left = random.randint(10, 90)  # Keep stars within viewport
        top = random.randint(10, 90)
        delay = random.uniform(0, 2)
        duration = random.uniform(1, 2)
        stars_html += f'<div style="position: fixed; left: {left}vw; top: {top}vh; font-size: 2rem; animation: starBurst {duration}s ease-out {delay}s; pointer-events: none; z-index: 9999;">⭐</div>'
    
    return f'''
    <div id="level-complete-wrapper" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; pointer-events: none; z-index: 9998;">
        <div style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 9999; pointer-events: none;">
            <div style="font-size: 5rem; animation: scaleUp 0.5s ease-out; text-align: center;">
                🏆
            </div>
            <div style="font-size: 2.5rem; color: #ffd700; font-weight: 900; text-shadow: 0 0 30px #ffd700; animation: glow 1s ease-in-out infinite; margin-top: 20px; white-space: nowrap; text-align: center;">
                LEVEL COMPLETE!
            </div>
        </div>
        {stars_html}
    </div>
    <style>
        @keyframes scaleUp {{
            0% {{ transform: scale(0) rotate(0deg); opacity: 0; }}
            50% {{ transform: scale(1.3) rotate(180deg); }}
            100% {{ transform: scale(1) rotate(360deg); opacity: 1; }}
        }}
        @keyframes glow {{
            0%, 100% {{ text-shadow: 0 0 20px #ffd700; }}
            50% {{ text-shadow: 0 0 40px #ffd700, 0 0 60px #ff8c00; }}
        }}
        @keyframes starBurst {{
            0% {{ transform: scale(0) rotate(0deg); opacity: 1; }}
            100% {{ transform: scale(3) rotate(720deg); opacity: 0; }}
        }}
    </style>
    '''


def create_confetti() -> str:
    """Generate colorful confetti animation"""
    colors = ["#FF595E", "#FFCA3A", "#8AC926", "#1982C4", "#6A4C93",
              "#FF9F1C", "#FA0096", "#00FAE1", "#FFD700", "#00FA15"]
    pieces = ""
    for i in range(50):
        left = random.randint(0, 100)
        delay = round(random.uniform(0, 4), 2)
        color = random.choice(colors)
        pieces += (
            f'<div class="confetti-piece" '
            f'style="left:{left}vw; top:{random.randint(-10, 0)}vh; '
            f'background:{color}; animation-delay:{delay}s;"></div>'
        )
    return pieces


def add_achievement(achievement: str):
    """Add achievement to player's collection"""
    if achievement not in st.session_state.achievements:
        st.session_state.achievements.append(achievement)


def reset_game():
    """Reset all game state for new game"""
    keys_to_keep = []
    for key in list(st.session_state.keys()):
        if key not in keys_to_keep:
            del st.session_state[key]
    init_session_state()


# ═══════════════════════════════════════════════════════════════════════════════
# RENDER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def render_progress_tracker():
    """Render enhanced progress tracking system"""
    progress_pct = (st.session_state.level / len(st.session_state.QUESTIONS)) * 100
    current = st.session_state.level

    nodes_html = '<div class="node-tracker">'
    for i in range(len(st.session_state.QUESTIONS)):
        if i < current:
            nodes_html += f'<div class="node completed">{i + 1}</div>'
        elif i == current:
            nodes_html += f'<div class="node active">{i + 1}</div>'
        else:
            nodes_html += f'<div class="node">{i + 1}</div>'

        if i < len(st.session_state.QUESTIONS) - 1:
            connector_class = "node-connector active" if i < current else "node-connector"
            nodes_html += f'<div class="{connector_class}"></div>'

    nodes_html += '</div>'

    st.markdown(f"""
    <div style="margin: 30px 0;">
        {nodes_html}
        <div style="text-align: center; margin-top: 20px;">
            <span style="font-size: 1.5rem; color: var(--primary-glow); font-weight: 700;">
                Progress: {progress_pct:.0f}% • Level {current + 1}/{len(st.session_state.QUESTIONS)}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_stats_dashboard():
    """Render holographic stats dashboard"""
    elapsed = (datetime.now() - st.session_state.start_time).total_seconds()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 2.5rem;">📍</div>
            <div class="stat-value">{st.session_state.level + 1}/{len(st.session_state.QUESTIONS)}</div>
            <div class="stat-label">Level</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 2.5rem;">🎯</div>
            <div class="stat-value">{st.session_state.score}</div>
            <div class="stat-label">Score</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 2.5rem;">🔥</div>
            <div class="stat-value">{st.session_state.streak}</div>
            <div class="stat-label">Streak</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 2.5rem;">⏱</div>
            <div class="stat-value">{format_time(elapsed)}</div>
            <div class="stat-label">Time</div>
        </div>
        """, unsafe_allow_html=True)


def render_sidebar():
    """Render enhanced sidebar with game info"""
    with st.sidebar:
        # User Info Section
        if st.session_state.get("logged_in", False) and st.session_state.get("username", ""):
            st.markdown(f'''
            <div style="background: linear-gradient(135deg, rgba(0, 255, 255, 0.2), rgba(255, 0, 255, 0.2));
                        border: 2px solid var(--primary-glow); border-radius: 15px; padding: 20px;
                        text-align: center; margin-bottom: 20px;">
                <div style="font-size: 3rem; margin-bottom: 10px;">👤</div>
                <div style="font-size: 1.3rem; font-weight: 700; color: var(--primary-glow);
                            text-shadow: 0 0 10px var(--primary-glow);">
                    {st.session_state.username}
                </div>
                <div style="font-size: 0.9rem; color: rgba(255,255,255,0.7); margin-top: 5px;">
                    FOSS Hunter
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        
        st.markdown('<h2 style="color: var(--primary-glow); text-align: center;">🎮 GAME CONTROL</h2>',
                    unsafe_allow_html=True)
        st.markdown("---")

        # Progress Ring
        progress_pct = (st.session_state.level / len(st.session_state.QUESTIONS)) * 100
        st.markdown(f"""
        <div class="progress-ring" style="--progress: {progress_pct}">
            <div class="progress-content">
                <div style="font-size: 2.5rem; font-weight: 900; color: var(--primary-glow);">
                    {progress_pct:.0f}%
                </div>
                <div style="font-size: 0.9rem; color: rgba(255,255,255,0.7);">
                    Complete
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Time Display
        elapsed = (datetime.now() - st.session_state.start_time).total_seconds()
        st.markdown(f"""
        <div style="background: rgba(255, 255, 255, 0.05); padding: 15px; 
                    border-radius: 10px; text-align: center; margin-bottom: 20px;">
            <div style="font-size: 1rem; color: rgba(255,255,255,0.7);">⏱ ELAPSED TIME</div>
            <div style="font-size: 2rem; font-weight: 900; color: var(--primary-glow); margin-top: 5px;">
                {format_time(elapsed)}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Game Rules
        st.markdown("### 📋 MISSION BRIEFING")
        st.markdown("""
        <div class="glass-container" style="padding: 15px; font-size: 0.9rem;">
        <b>🎯 Objective:</b> Complete all 6 levels<br><br>
        <b>⚡ Two-Phase System:</b><br>
        • Phase 1: Solve the riddle<br>
        • Phase 2: Crack security key<br><br>
        <b>🏆 Scoring:</b><br>
        • Easy: 10 pts<br>
        • Medium: 15 pts<br>
        • Hard: 20 pts<br>
        • Perfect run bonus: +5 pts<br>
        • Streak bonus: +3-8 pts<br><br>
        <b>⚠ Penalties:</b><br>
        • Hints reset streak<br>
        • Wrong answers delay progress
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Live Stats
        st.markdown("### 📊 LIVE STATS")

        if st.session_state.streak > 0:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #ff6b6b, #ff8e53); 
                        padding: 15px; border-radius: 10px; text-align: center;
                        box-shadow: 0 0 20px rgba(255, 107, 107, 0.5);">
                <div style="font-size: 2rem;">🔥</div>
                <div style="font-size: 1.5rem; font-weight: 900;">{st.session_state.streak}</div>
                <div style="font-size: 0.9rem;">CURRENT STREAK</div>
            </div>
            """, unsafe_allow_html=True)

        if st.session_state.max_streak > 0:
            st.info(f"🏅 Best Streak: {st.session_state.max_streak}")

        if st.session_state.combo_multiplier > 1.0:
            st.success(f"⚡ Combo: {st.session_state.combo_multiplier}x")

        st.metric("💡 Hints Used", st.session_state.hints_used)
        st.metric("⭐ Perfect Levels", st.session_state.perfect_levels)

        st.markdown("---")

        # Quick Actions
        if st.button("🔄 Restart Game", use_container_width=True):
            reset_game()
            st.rerun()
        
        # Progress Management
        if st.session_state.level > 0 and not st.session_state.finished:
            st.markdown("---")
            st.markdown("### 💾 PROGRESS CONTROL")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📥 Save", use_container_width=True, help="Progress auto-saves"):
                    success = DjangoAPI.save_progress(
                        st.session_state.username,
                        st.session_state.level,
                        st.session_state.score,
                        st.session_state.hints_used,
                        st.session_state.achievements,
                        st.session_state.streak,
                        st.session_state.max_streak,
                        st.session_state.combo_multiplier,
                        st.session_state.perfect_levels,
                        st.session_state.wrong_attempts
                    )
                    if success:
                        st.success("✅ Progress saved!")
                    else:
                        st.error("❌ Save failed!")
            
            with col2:
                if st.button("🗑️ Clear", use_container_width=True, help="Delete saved progress"):
                    if DjangoAPI.clear_progress(st.session_state.username):
                        st.warning("🛡️ Progress cleared!")
                        reset_game()
                        st.rerun()
            
            st.caption("💾 Progress auto-saves after each level")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════
init_session_state()

# Check if user is logged in
if not st.session_state.get("logged_in", False):
    # Show login page
    render_login_page()
else:
    # Show game (user is logged in)
    render_sidebar()

    # Animated Title
    st.markdown('<h1 class="hero-title">Treassure-Hunt Adventure</h1>', unsafe_allow_html=True)

    st.markdown('<h2 class="subtitle">Software Freedom Day Edition</h2>', unsafe_allow_html=True)

    # Info Banner - Updated from second code
    st.markdown("""
    <div class="info-box">
        <p style='font-size: 1.1rem; line-height: 1.6;'>
            🎉 <strong>Software Freedom Day (SFD)</strong> - A celebration of Free and Open Source Software!
            <br><br>
            <strong>🎮 How to Play:</strong><br>
            1️⃣ Solve the main riddle to earn points<br>
            2️⃣ Find the security key to unlock the next level<br>
            3️⃣ Complete all levels to become a FOSS Master!
        </p>
        <p style='margin-top: 15px;'>
            <a href='https://digitalfreedoms.org/en/sfd' target='_blank' 
               style='color: #00FFCC; text-decoration: none; font-weight: bold;'>
               Learn More at Digital Freedom Foundation →
            </a>
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ═══════════════════════════════════════════════════════════════════════════════
    # GAME LOGIC
    # ═══════════════════════════════════════════════════════════════════════════════
    # Check if game was completed permanently
    if st.session_state.get('game_completed_permanently', False):
        st.info("🏆 This treasure hunt can only be played once. Your achievement has been permanently saved!")
    else:
        if not st.session_state.finished:
            # Display animations if triggered
            if st.session_state.show_riddle_animation:
                points = st.session_state.QUESTIONS[st.session_state.level]['points']
                bonus = calculate_bonus_points(is_riddle=True)
            
                st.success(f"✅ **CORRECT!** +{points} points" + (f" (+{bonus} bonus 🎉)" if bonus > 0 else ""))
                st.info("🔐 **PHASE 2 UNLOCKED:** Crack the security key to proceed!")
            
                # Display animations separately to ensure proper rendering
                st.markdown(create_question_win_animation(), unsafe_allow_html=True)
                st.markdown(create_fireworks(), unsafe_allow_html=True)
            
                # Clear animation flag and reload
                st.session_state.show_riddle_animation = False
                time.sleep(2)
                st.rerun()
    
        if st.session_state.show_level_animation:
            if st.session_state.finished:
                # Final victory animation
                st.success(f"🏆 **ALL LEVELS COMPLETE!** You are a FOSS Master!")
                st.markdown(create_level_complete_animation(), unsafe_allow_html=True)
                st.markdown(create_confetti(), unsafe_allow_html=True)
                st.markdown(create_fireworks(), unsafe_allow_html=True)
            else:
                # Level completion animation
                st.success(f"🔓 **ACCESS GRANTED!** Level {st.session_state.level} unlocked! 🎉")
                st.markdown(create_level_complete_animation(), unsafe_allow_html=True)
                st.markdown(create_fireworks(), unsafe_allow_html=True)
        
            # Clear animation flag and reload
            st.session_state.show_level_animation = False
            time.sleep(2)
            st.rerun()
    
    render_progress_tracker()
    render_stats_dashboard()

    st.markdown("---")

    # Show motivational GIF at start
    if st.session_state.level == 0 and not st.session_state.riddle_solved:
        st.markdown(
            """
            <div style="display:flex; justify-content:center; margin: 30px 0;">
                <img src="https://media.tenor.com/DQRSMm8uuq4AAAAi/tamil-hindu.gif" width="350" style="border-radius: 20px; box-shadow: 0 0 30px rgba(0,255,255,0.5);">
            </div>
            """,
            unsafe_allow_html=True
        )

    # Show completed levels
    if st.session_state.level > 0:
        with st.expander(f"✅ Completed Missions ({st.session_state.level}/{len(st.session_state.QUESTIONS)})", expanded=False):
            for i in range(st.session_state.level):
                q = st.session_state.QUESTIONS[i]
                st.markdown(
                    f'<div class="completed-level">Level {i + 1}: {q["category"]} - '
                    f'{q["difficulty"].upper()} ✓ | 🔐 Unlocked</div>',
                    unsafe_allow_html=True
                )

    # Only show current question if game is not finished
    if not st.session_state.finished:
        # Current Question
        current_q = st.session_state.QUESTIONS[st.session_state.level]

        # Phase Banner
        if not st.session_state.riddle_solved:
            phase_icon = "🧩"
            phase_text = "PHASE 1: DECODE THE RIDDLE"
            phase_color = "var(--primary-glow)"
        else:
            phase_icon = "🔐"
            phase_text = "PHASE 2: CRACK THE SECURITY KEY"
            phase_color = "var(--danger-glow)"

        st.markdown(f"""
        <div class="phase-banner">
            <div class="phase-text" style="color: {phase_color};">
                {phase_icon} {phase_text}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Question Header
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            badge_class = f"badge-{current_q['difficulty']}"
            st.markdown(f'<div class="badge {badge_class}">{current_q["difficulty"].upper()}</div>',
                        unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.05); padding: 10px 20px; 
                        border-radius: 20px; display: inline-block;">
                <span style="color: var(--gold-glow); font-weight: 700;">
                    💰 {current_q['points']} POINTS
                </span>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.05); padding: 10px 20px; 
                        border-radius: 20px; text-align: center;">
                <span style="color: var(--primary-glow); font-size: 0.9rem;">
                    📚 {current_q['category']}
                </span>
            </div>
            """, unsafe_allow_html=True)

        # ═══════════════════════════════════════════════════════════════════════════
        # PHASE 1: MAIN RIDDLE
        # ═══════════════════════════════════════════════════════════════════════════
        if not st.session_state.riddle_solved:
            st.markdown(f"""
            <div class="riddle-container">
                <pre class="riddle-text">{current_q['question']}</pre>
            </div>
            """, unsafe_allow_html=True)

            answer = st.text_input(
                "🔑 Enter Your Answer:",
                key=f"ans_{st.session_state.level}_main",
                placeholder="Type your solution here...",
                help="Solve the riddle to unlock Phase 2"
            )

            col1, col2, col3 = st.columns([2, 2, 1])

            with col1:
                submit_btn = st.button("⚡ SUBMIT ANSWER", use_container_width=True, type="primary")

            with col2:
                hint_btn = st.button("💡 REQUEST HINT", use_container_width=True)

            with col3:
                if st.session_state.wrong_attempts > 0:
                    st.markdown(f"""
                    <div style="text-align: center; color: var(--danger-glow); font-weight: 700;">
                        ❌ {st.session_state.wrong_attempts}
                    </div>
                    """, unsafe_allow_html=True)

            if submit_btn and answer.strip():
                user_answer = answer.strip().lower()
                correct_answer = current_q['answer'].lower()

                if user_answer == correct_answer:
                    # Correct Answer
                    points = current_q['points']
                    bonus = calculate_bonus_points(is_riddle=True)

                    st.session_state.score += points + bonus
                    st.session_state.riddle_solved = True
                    st.session_state.show_hint = False

                    if st.session_state.wrong_attempts == 0:
                        st.session_state.perfect_levels += 1
                        add_achievement("Perfect Solver")

                    st.session_state.wrong_attempts = 0
                    st.session_state.combo_multiplier = min(3.0, st.session_state.combo_multiplier + 0.2)
                    
                    # AUTO-SAVE after solving riddle
                    auto_save_progress()
                    
                    st.session_state.show_riddle_animation = True
                    st.rerun()
                else:
                    # Wrong Answer
                    st.session_state.wrong_attempts += 1
                    st.session_state.combo_multiplier = 1.0
                    st.error(f"❌ Incorrect! Attempt {st.session_state.wrong_attempts}/∞")

                    # Show disappointed GIF on wrong answer
                    st.markdown(
                        """
                        <div style="display:flex; justify-content:center; margin: 10px 0;">
                            <img src="https://media.tenor.com/ve3YH1XBAyIAAAAi/uarrr-disappointed.gif" width="200">
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if st.session_state.wrong_attempts >= 3:
                        st.warning("💡 Struggling? Consider using a hint!")

            if st.session_state.show_hint:
                st.markdown(f"""
                <div class="hint-container">
                    <div style="font-size: 1.5rem; margin-bottom: 10px;">💡 HINT</div>
                    <div style="font-size: 1.1rem;">{current_q['hint']}</div>
                </div>
                """, unsafe_allow_html=True)

        # ═══════════════════════════════════════════════════════════════════════════
        # PHASE 2: SECURITY KEY
        # ═══════════════════════════════════════════════════════════════════════════
        else:
            st.success("✅ **RIDDLE SOLVED!** Phase 2 initiated...")

            st.markdown(f"""
            <div class="security-zone">
                <h3 class="security-title">🔐 SECURITY CHALLENGE</h3>
                <p style="font-size: 1.3rem; line-height: 1.8; color: white;">
                    {current_q['security_riddle']}
                </p>
            </div>
            """, unsafe_allow_html=True)

            security_answer = st.text_input(
                "🔐 Enter Security Key:",
                key=f"sec_{st.session_state.level}",
                placeholder="Enter the key to unlock next level...",
                help="Find the security key to advance"
            )

            col1, col2, col3 = st.columns([2, 2, 1])

            with col1:
                security_submit = st.button("🔓 UNLOCK LEVEL", use_container_width=True, type="primary")

            with col2:
                security_hint_btn = st.button("💡 SECURITY HINT", use_container_width=True)

            with col3:
                if st.session_state.security_wrong_attempts > 0:
                    st.markdown(f"""
                    <div style="text-align: center; color: var(--danger-glow); font-weight: 700;">
                        ❌ {st.session_state.security_wrong_attempts}
                    </div>
                    """, unsafe_allow_html=True)

            if security_hint_btn:
                if not st.session_state.show_security_hint:
                    st.session_state.hints_used += 1
                    st.session_state.streak = 0
                    st.session_state.combo_multiplier = 1.0
                    st.info("⚠ Streak and combo reset!")
                    
                    # AUTO-SAVE after using security hint
                    auto_save_progress()
                    
                st.session_state.show_security_hint = True

            if st.session_state.show_security_hint:
                st.markdown(f"""
                <div class="hint-container">
                    <div style="font-size: 1.5rem; margin-bottom: 10px;">🔐 SECURITY HINT</div>
                    <div style="font-size: 1.1rem;">{current_q['security_hint']}</div>
                </div>
                """, unsafe_allow_html=True)

            if security_submit and security_answer.strip():
                user_security = security_answer.strip().lower()
                correct_security = current_q['security_key'].lower()

                if user_security == correct_security:
                    # Correct Security Key
                    st.session_state.level += 1
                    st.session_state.riddle_solved = False
                    st.session_state.show_security_hint = False
                    st.session_state.streak += 1
                    st.session_state.max_streak = max(st.session_state.max_streak, st.session_state.streak)
                    st.session_state.security_wrong_attempts = 0
                    st.session_state.level_start_time = datetime.now()

                    # Check if game is finished (all 6 levels completed)
                    if st.session_state.level >= len(st.session_state.QUESTIONS):
                        st.session_state.finished = True
                        # Mark game as completed permanently to prevent replay
        # Preview Upcoming Levels
        st.markdown("---")
        st.markdown("### 🔮 UPCOMING MISSIONS")

        remaining = min(3, len(st.session_state.QUESTIONS) - st.session_state.level - 1)
        if remaining > 0:
            cols = st.columns(remaining)
            for i in range(remaining):
                level_num = st.session_state.level + i + 1
                next_q = st.session_state.QUESTIONS[level_num]
                with cols[i]:
                    st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.03); padding: 20px; border-radius: 15px;
                                border: 2px dashed rgba(255,255,255,0.2); text-align: center;">
                        <div style="font-size: 2rem; margin-bottom: 10px;">🔒</div>
                        <div style="font-weight: 700; font-size: 1.2rem;">LEVEL {level_num + 1}</div>
                        <div class="badge badge-{next_q['difficulty']}" style="margin: 10px 0;">
                            {next_q['difficulty'].upper()}
                        </div>
                        <div style="color: rgba(255,255,255,0.6);">{next_q['category']}</div>
                        <div style="color: var(--gold-glow); margin-top: 10px;">💰 {next_q['points']} pts</div>
                    </div>
                    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# VICTORY SCREEN
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.finished:
    elapsed = (datetime.now() - st.session_state.start_time).total_seconds()
    rank, subtitle = get_rank()

    # Epic Victory Celebration
    st.markdown("""
    <div style="text-align:center; margin: 30px 0;">
        <h1 style="color: #FFD700; font-size: 5rem; text-shadow: 0 0 30px #FFD700; animation: victoryPulse 1s ease-in-out infinite;">
            🏆 LEGENDARY VICTORY! 🏆
        </h1>
        <div style="font-size: 3rem; margin-top: 20px; animation: celebrateBounce 0.8s ease-in-out infinite;">
            🎉 ✨ 🎊 ⭐ 🌟 💫 ✨ 🎉
        </div>
    </div>
    <style>
        @keyframes victoryPulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        @keyframes celebrateBounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }
    </style>
    """, unsafe_allow_html=True)

    # Multiple celebration animations
    st.markdown(create_confetti(), unsafe_allow_html=True)
    st.markdown(create_fireworks(), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def auto_save_progress():
    """Auto-save current game state to backend/JSON"""
    if st.session_state.get('logged_in') and st.session_state.get('username'):
        success = DjangoAPI.save_progress(
            st.session_state.username,
            st.session_state.level,
            st.session_state.score,
            st.session_state.hints_used,
            st.session_state.achievements,
            st.session_state.streak,
            st.session_state.max_streak,
            st.session_state.combo_multiplier,
            st.session_state.perfect_levels,
            st.session_state.wrong_attempts
        )
        if success:
            st.sidebar.success("✅ Progress auto-saved!")
        else:
            st.sidebar.error("❌ Auto-save failed!")

        # Preview Upcoming Levels
        st.markdown("---")
        st.markdown("### 🔮 UPCOMING MISSIONS")

        remaining = min(3, len(st.session_state.QUESTIONS) - st.session_state.level - 1)
        if remaining > 0:
            cols = st.columns(remaining)
            for i in range(remaining):
                level_num = st.session_state.level + i + 1
                next_q = st.session_state.QUESTIONS[level_num]
                with cols[i]:
                    st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.03); padding: 20px; border-radius: 15px;
                                border: 2px dashed rgba(255,255,255,0.2); text-align: center;">
                        <div style="font-size: 2rem; margin-bottom: 10px;">🔒</div>
                        <div style="font-weight: 700; font-size: 1.2rem;">LEVEL {level_num + 1}</div>
                        <div class="badge badge-{next_q['difficulty']}" style="margin: 10px 0;">
                            {next_q['difficulty'].upper()}
                        </div>
                        <div style="color: rgba(255,255,255,0.6);">{next_q['category']}</div>
                        <div style="color: var(--gold-glow); margin-top: 10px;">💰 {next_q['points']} pts</div>
                    </div>
                    """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════════
    # VICTORY SCREEN
    # ═══════════════════════════════════════════════════════════════════════════════
    if st.session_state.finished:
        elapsed = (datetime.now() - st.session_state.start_time).total_seconds()
        rank, subtitle = get_rank()

        # Epic Victory Celebration
        st.markdown("""
        <div style="text-align:center; margin: 30px 0;">
            <h1 style="color: #FFD700; font-size: 5rem; text-shadow: 0 0 30px #FFD700; animation: victoryPulse 1s ease-in-out infinite;">
                🏆 LEGENDARY VICTORY! 🏆
            </h1>
            <div style="font-size: 3rem; margin-top: 20px; animation: celebrateBounce 0.8s ease-in-out infinite;">
                🎉 ✨ 🎊 ⭐ 🌟 💫 ✨ 🎉
            </div>
        </div>
        <style>
            @keyframes victoryPulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.1); }
            }
            @keyframes celebrateBounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-20px); }
            }
        </style>
        """, unsafe_allow_html=True)
    
        # Multiple celebration animations
        st.markdown(create_confetti(), unsafe_allow_html=True)
        st.markdown(create_fireworks(), unsafe_allow_html=True)
    
        # PROGRAMMER-THEMED FLOATING CODE SNIPPETS
        st.markdown("""
        <div style="position: fixed; top: 15%; left: 8%; font-size: 2rem; animation: floatCode1 4s ease-in-out infinite; 
                    z-index: 100; pointer-events: none; background: rgba(0,0,0,0.7); padding: 10px; 
                    border: 1px solid #00ff00; border-radius: 8px; color: #00ff00; font-family: monospace;">
            console.log('🎉');
        </div>
        <div style="position: fixed; top: 25%; right: 8%; font-size: 2rem; animation: floatCode2 5s ease-in-out infinite; 
                    z-index: 100; pointer-events: none; background: rgba(0,0,0,0.7); padding: 10px; 
                    border: 1px solid #00ffff; border-radius: 8px; color: #00ffff; font-family: monospace;">
            return 'WIN';
        </div>
        <div style="position: fixed; top: 50%; left: 5%; font-size: 2rem; animation: floatCode3 4.5s ease-in-out infinite; 
                    z-index: 100; pointer-events: none; background: rgba(0,0,0,0.7); padding: 10px; 
                    border: 1px solid #ff00ff; border-radius: 8px; color: #ff00ff; font-family: monospace;">
            git push 🚀
        </div>
        <div style="position: fixed; top: 60%; right: 5%; font-size: 2rem; animation: floatCode4 5.5s ease-in-out infinite; 
                    z-index: 100; pointer-events: none; background: rgba(0,0,0,0.7); padding: 10px; 
                    border: 1px solid #ffff00; border-radius: 8px; color: #ffff00; font-family: monospace;">
            def legend():
        </div>
        <div style="position: fixed; top: 70%; left: 12%; font-size: 2.5rem; animation: floatLeft 3s ease-in-out infinite; 
                    z-index: 100; pointer-events: none;">
            💻
        </div>
        <div style="position: fixed; top: 35%; right: 12%; font-size: 2.5rem; animation: floatRight 3.5s ease-in-out infinite; 
                    z-index: 100; pointer-events: none;">
            ⚡
        </div>
        <div style="position: fixed; top: 80%; left: 50%; font-size: 2.5rem; animation: orbit 6s linear infinite; 
                    z-index: 100; pointer-events: none;">
            🔥
        </div>
        <style>
            @keyframes floatCode1 {
                0%, 100% { transform: translate(0, 0) rotate(0deg); opacity: 0.8; }
                25% { transform: translate(-30px, -30px) rotate(-5deg); opacity: 1; }
                50% { transform: translate(0, -60px) rotate(0deg); opacity: 0.9; }
                75% { transform: translate(30px, -30px) rotate(5deg); opacity: 1; }
            }
            @keyframes floatCode2 {
                0%, 100% { transform: translate(0, 0) rotate(0deg); opacity: 0.8; }
                25% { transform: translate(30px, -25px) rotate(5deg); opacity: 1; }
                50% { transform: translate(0, -50px) rotate(0deg); opacity: 0.9; }
                75% { transform: translate(-30px, -25px) rotate(-5deg); opacity: 1; }
            }
            @keyframes floatCode3 {
                0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.8; }
                50% { transform: translate(-20px, -40px) scale(1.1); opacity: 1; }
            }
            @keyframes floatCode4 {
                0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.8; }
                50% { transform: translate(20px, -40px) scale(1.1); opacity: 1; }
            }
            @keyframes floatLeft {
                0%, 100% { transform: translate(0, 0) rotate(0deg); }
                25% { transform: translate(-25px, -25px) rotate(-15deg); }
                50% { transform: translate(0, -50px) rotate(0deg); }
                75% { transform: translate(25px, -25px) rotate(15deg); }
            }
            @keyframes floatRight {
                0%, 100% { transform: translate(0, 0) rotate(0deg); }
                25% { transform: translate(25px, -25px) rotate(15deg); }
                50% { transform: translate(0, -50px) rotate(0deg); }
                75% { transform: translate(-25px, -25px) rotate(-15deg); }
            }
            @keyframes orbit {
                0% { transform: translate(-50%, 0) rotate(0deg) translateX(100px) rotate(0deg); }
                100% { transform: translate(-50%, 0) rotate(360deg) translateX(100px) rotate(-360deg); }
            }
        </style>
        """, unsafe_allow_html=True)
    
        # EPIC CODE COMPILATION SUCCESS ANIMATION
        st.markdown("""
        <div style="text-align: center; margin: 40px 0;">
            <div style="background: linear-gradient(135deg, rgba(0,255,0,0.2), rgba(0,255,255,0.2)); 
                        border: 2px solid #00ff00; border-radius: 15px; padding: 30px; 
                        display: inline-block; box-shadow: 0 0 40px rgba(0,255,0,0.6);">
                <div style="font-size: 5rem; animation: compileSuccess 2s ease-in-out;">
                    ✓
                </div>
                <div style="color: #00ff00; font-size: 2rem; font-weight: 900; font-family: monospace; 
                            text-shadow: 0 0 20px #00ff00; margin-top: 15px;">
                    BUILD SUCCESSFUL
                </div>
                <div style="color: #00ffff; font-size: 1.2rem; margin-top: 10px; font-family: monospace;">
                    0 errors, 0 warnings, 100% legendary
                </div>
            </div>
        </div>
        <style>
            @keyframes compileSuccess {
                0% { transform: scale(0) rotate(-180deg); opacity: 0; color: #ff0000; }
                50% { transform: scale(1.3) rotate(0deg); opacity: 1; color: #ffff00; }
                100% { transform: scale(1) rotate(0deg); opacity: 1; color: #00ff00; }
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Floating celebration elements
        st.markdown("""
        <div style="position: fixed; top: 20%; left: 10%; font-size: 3rem; animation: floatLeft 3s ease-in-out infinite; z-index: 1000; pointer-events: none;">
            🎈
        </div>
        <div style="position: fixed; top: 25%; right: 10%; font-size: 3rem; animation: floatRight 3s ease-in-out infinite; z-index: 1000; pointer-events: none;">
            🎈
        </div>
        <div style="position: fixed; top: 40%; left: 5%; font-size: 2.5rem; animation: floatLeft 4s ease-in-out infinite 0.5s; z-index: 1000; pointer-events: none;">
            ⭐
        </div>
        <div style="position: fixed; top: 45%; right: 5%; font-size: 2.5rem; animation: floatRight 4s ease-in-out infinite 0.5s; z-index: 1000; pointer-events: none;">
            ⭐
        </div>
        <style>
            @keyframes floatLeft {
                0%, 100% { transform: translate(0, 0) rotate(0deg); }
                25% { transform: translate(-20px, -20px) rotate(-10deg); }
                50% { transform: translate(0, -40px) rotate(0deg); }
                75% { transform: translate(20px, -20px) rotate(10deg); }
            }
            @keyframes floatRight {
                0%, 100% { transform: translate(0, 0) rotate(0deg); }
                25% { transform: translate(20px, -20px) rotate(10deg); }
                50% { transform: translate(0, -40px) rotate(0deg); }
                75% { transform: translate(-20px, -20px) rotate(-10deg); }
            }
        </style>
        """, unsafe_allow_html=True)
    
        # Victory sound effect simulation with visual pulse
        st.markdown("""
        <div style="text-align: center; margin: 40px 0;">
            <div style="display: inline-block; font-size: 6rem; animation: victoryBurst 1.5s ease-out;">
                🎆
            </div>
        </div>
        <style>
            @keyframes victoryBurst {
                0% { transform: scale(0) rotate(0deg); opacity: 0; }
                50% { transform: scale(1.5) rotate(180deg); opacity: 1; }
                100% { transform: scale(1) rotate(360deg); opacity: 1; }
            }
        </style>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="victory-container">
        <h1 class="victory-title">🏆 VICTORY 🏆</h1>
        <div style="font-size: 4rem; margin: 30px 0; animation: trophyFloat 2s ease-in-out infinite;">
            🏆 🥇 ⭐ 🥇 🏆
        </div>
        <h2 style="font-size: 3rem; color: var(--gold-glow); margin: 20px 0; animation: rankAppear 1s ease-out;">
            {rank}
        </h2>
        <p style="font-size: 1.5rem; color: var(--primary-glow); margin: 20px 0; animation: subtitleGlow 2s ease-in-out infinite;">
            {subtitle}
        </p>
        <div style="margin: 30px 0; font-size: 2.5rem; animation: celebrateSpin 3s linear infinite;">
            🎊 🎈 🎁 🎇 🎆
        </div>
        <p style="font-size: 1.2rem; line-height: 2; margin-top: 30px;">
            All {len(st.session_state.QUESTIONS)} levels completed!<br>
            All security keys cracked!<br>
            🌐 Thank you for celebrating Software Freedom!
        </p>
        </div>
        <style>
        @keyframes trophyFloat {{
            0%, 100% {{ transform: translateY(0) rotate(0deg); }}
            25% {{ transform: translateY(-10px) rotate(5deg); }}
            75% {{ transform: translateY(-10px) rotate(-5deg); }}
        }}
        @keyframes rankAppear {{
            0% {{ transform: scale(0); opacity: 0; }}
            50% {{ transform: scale(1.2); }}
            100% {{ transform: scale(1); opacity: 1; }}
        }}
        @keyframes subtitleGlow {{
            0%, 100% {{ text-shadow: 0 0 10px var(--primary-glow); }}
            50% {{ text-shadow: 0 0 30px var(--primary-glow), 0 0 50px var(--secondary-glow); }}
        }}
        @keyframes celebrateSpin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        </style>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Congratulatory message with animation
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(255, 215, 0, 0.2), rgba(255, 140, 0, 0.2)); 
                    border: 3px solid var(--gold-glow); border-radius: 25px; padding: 40px; 
                    text-align: center; margin: 30px 0; animation: messageGlow 2s ease-in-out infinite;">
            <div style="font-size: 3rem; margin-bottom: 20px;">🎆 🎇 🎉 🎇 🎆</div>
            <h2 style="color: var(--gold-glow); font-size: 2.5rem; margin-bottom: 15px; font-family: 'Orbitron', monospace;">
                CONGRATULATIONS, CHAMPION!
            </h2>
            <p style="font-size: 1.3rem; color: white; line-height: 1.8;">
                You've conquered all challenges and proven yourself as a true <strong>FOSS Master</strong>!<br>
                Your dedication to Software Freedom is legendary! 🌟
            </p>
            <div style="font-size: 2.5rem; margin-top: 20px;">🏆 🥇 🥈 🥉 🏆</div>
        </div>
        <style>
            @keyframes messageGlow {
                0%, 100% { box-shadow: 0 0 30px rgba(255, 215, 0, 0.5); }
                50% { box-shadow: 0 0 60px rgba(255, 215, 0, 0.8), 0 0 90px rgba(255, 140, 0, 0.6); }
            }
        </style>
        """, unsafe_allow_html=True)

        # PROGRAMMING LANGUAGES BADGES SHOWCASE
        st.markdown("""
        <div style="text-align: center; margin: 40px 0;">
            <div style="background: rgba(0,0,0,0.8); border: 2px solid var(--primary-glow); 
                        border-radius: 15px; padding: 30px; display: inline-block;">
                <h3 style="color: var(--gold-glow); font-size: 1.8rem; margin-bottom: 20px;">
                    💎 LEGENDARY TECH STACK MASTERED 💎
                </h3>
                <div style="display: flex; gap: 15px; flex-wrap: wrap; justify-content: center;">
                    <div class="tech-badge" style="animation-delay: 0s;">🐍 Python</div>
                    <div class="tech-badge" style="animation-delay: 0.1s;">☕ Java</div>
                    <div class="tech-badge" style="animation-delay: 0.2s;">⚛️ React</div>
                    <div class="tech-badge" style="animation-delay: 0.3s;">🔥 C++</div>
                    <div class="tech-badge" style="animation-delay: 0.4s;">🦀 Rust</div>
                    <div class="tech-badge" style="animation-delay: 0.5s;">🎯 TypeScript</div>
                    <div class="tech-badge" style="animation-delay: 0.6s;">🐧 Linux</div>
                    <div class="tech-badge" style="animation-delay: 0.7s;">🐳 Docker</div>
                </div>
            </div>
        </div>
        <style>
            .tech-badge {
                background: linear-gradient(135deg, rgba(0,255,255,0.2), rgba(255,0,255,0.2));
                border: 2px solid var(--primary-glow);
                border-radius: 20px;
                padding: 12px 20px;
                font-size: 1.1rem;
                font-weight: 700;
                color: white;
                animation: badgeAppear 0.6s ease-out backwards, badgeFloat 3s ease-in-out infinite;
                box-shadow: 0 0 20px rgba(0,255,255,0.5);
            }
            @keyframes badgeAppear {
                0% { transform: scale(0) rotate(-180deg); opacity: 0; }
                100% { transform: scale(1) rotate(0deg); opacity: 1; }
            }
            @keyframes badgeFloat {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-10px); }
            }
        </style>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="victory-container">
            <div style="background: linear-gradient(135deg, rgba(0,0,0,0.9), rgba(20,20,20,0.9)); 
                        border: 3px solid var(--gold-glow); border-radius: 25px; padding: 40px;
                        box-shadow: 0 0 50px rgba(255,215,0,0.6);">
                <h1 class="victory-title" style="font-family: 'Courier New', monospace; font-size: 3.5rem;">
                    🏆 LEGENDARY ACHIEVEMENT 🏆
                </h1>
                <div style="background: rgba(0,0,0,0.7); border: 1px solid #00ff00; border-radius: 10px; 
                            padding: 20px; margin: 20px 0; font-family: monospace; text-align: left;">
                    <div style="color: #00ff00; font-size: 1rem; margin-bottom: 10px;">$ cat achievement.txt</div>
                    <div style="color: #00ffff; font-size: 1.1rem;">
                        &gt; Rank: <span style="color: #FFD700; font-weight: 900; font-size: 2rem;">{rank}</span><br>
                        &gt; Status: <span style="color: #00ff00;">{subtitle}</span><br>
                        &gt; Levels Conquered: <span style="color: #ff00ff;">{len(st.session_state.QUESTIONS)}/{len(st.session_state.QUESTIONS)}</span><br>
                        &gt; Security Keys Cracked: <span style="color: #ffff00;">{len(st.session_state.QUESTIONS)}/{len(st.session_state.QUESTIONS)}</span>
                    </div>
                </div>
                <div style="margin: 30px 0; font-size: 3rem; animation: techSpin 4s linear infinite;">
                    🚀 ⚡ 💻 🔥 ⭐ 💎 🎯 ✨
                </div>
                <div style="background: linear-gradient(90deg, #00ff00, #00ffff, #ff00ff, #ffff00); 
                            -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                            font-size: 1.8rem; font-weight: 900; margin: 20px 0; animation: rainbow 3s linear infinite;">
                    💯 PERFECT EXECUTION • ZERO BUGS • 100% LEGENDARY 💯
                </div>
                <p style="font-size: 1.3rem; line-height: 2; margin-top: 30px; color: var(--primary-glow);">
                    🌐 All {len(st.session_state.QUESTIONS)} FOSS challenges conquered!<br>
                    🔐 Every security protocol bypassed with finesse!<br>
                    🏅 You are now officially a <span style="color: var(--gold-glow); font-weight: 900;">LEGENDARY PROGRAMMER</span>!<br>
                    💪 Thank you for celebrating Software Freedom!
                </p>
            </div>
        </div>
        <style>
            @keyframes techSpin {{
                0% {{ transform: rotateY(0deg); }}
                100% {{ transform: rotateY(360deg); }}
            }}
            @keyframes rainbow {{
                0% {{ filter: hue-rotate(0deg); }}
                100% {{ filter: hue-rotate(360deg); }}
            }}
            @keyframes trophyFloat {{
                0%, 100% {{ transform: translateY(0) rotate(0deg); }}
                25% {{ transform: translateY(-10px) rotate(5deg); }}
                75% {{ transform: translateY(-10px) rotate(-5deg); }}
            }}
            @keyframes rankAppear {{
                0% {{ transform: scale(0); opacity: 0; }}
                50% {{ transform: scale(1.2); }}
                100% {{ transform: scale(1); opacity: 1; }}
            }}
            @keyframes subtitleGlow {{
                0%, 100% {{ text-shadow: 0 0 10px var(--primary-glow); }}
                50% {{ text-shadow: 0 0 30px var(--primary-glow), 0 0 50px var(--secondary-glow); }}
            }}
        </style>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # GITHUB COMMIT CELEBRATION
        st.markdown("""
        <div style="background: rgba(0,0,0,0.9); border: 2px solid #00ff00; border-radius: 15px; 
                    padding: 30px; margin: 30px 0; font-family: 'Courier New', monospace;">
            <div style="color: #00ff00; font-size: 1.2rem; margin-bottom: 15px;">
                <span style="animation: blink 1s infinite;">▶</span> git log --oneline --decorate
            </div>
            <div style="background: rgba(0,255,0,0.1); padding: 15px; border-radius: 8px; margin: 10px 0;">
                <div style="color: #ffff00; font-size: 1rem;">
                    <span style="color: #ff00ff;">commit a1b2c3d</span> 
                    <span style="color: #00ffff;">(HEAD -> main, origin/main)</span><br>
                    <span style="color: #00ff00;">Author: {st.session_state.username} &lt;legend@foss.dev&gt;</span><br>
                    <span style="color: #ffffff;">Date: {datetime.now().strftime('%a %b %d %H:%M:%S %Y')}</span><br><br>
                    <span style="color: #FFD700; font-weight: 900; font-size: 1.3rem;">
                        🎉 feat: LEGENDARY VICTORY ACHIEVED 🎉
                    </span><br><br>
                    <span style="color: #00ff00;">    ✓ Completed all {len(st.session_state.QUESTIONS)} FOSS challenges</span><br>
                    <span style="color: #00ff00;">    ✓ Cracked every security protocol</span><br>
                    <span style="color: #00ff00;">    ✓ Achieved rank: {rank}</span><br>
                    <span style="color: #00ff00;">    ✓ Total score: {st.session_state.score} points</span><br>
                    <span style="color: #00ff00;">    ✓ Zero bugs found</span><br><br>
                    <span style="color: #00ffff;">    +999 legendary points</span><br>
                    <span style="color: #00ffff;">    +∞ respect from the community</span>
                </div>
            </div>
            <div style="color: #00ff00; font-size: 1rem; margin-top: 15px; animation: blink 1.5s infinite;">
                $ git push origin legendary<br>
                <span style="color: #00ffff;">Counting objects: 100% legendary...<br>
                Writing objects: 100% (∞/∞), done.<br>
                Total legendary achievement deployed successfully! 🚀</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # STACK OVERFLOW REPUTATION SURGE
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(244,128,36,0.2), rgba(244,128,36,0.1)); 
                    border: 3px solid #f48024; border-radius: 20px; padding: 35px; 
                    text-align: center; margin: 30px 0; animation: soGlow 2s ease-in-out infinite;">
            <div style="font-size: 3.5rem; margin-bottom: 15px; animation: bounce 2s ease-in-out infinite;">⭐ 📚 💡</div>
            <div style="background: rgba(244,128,36,0.3); border-radius: 10px; padding: 20px; display: inline-block;">
                <h2 style="color: #f48024; font-size: 2.5rem; margin-bottom: 10px; font-weight: 900;">
                    STACK OVERFLOW ACHIEVEMENT
                </h2>
                <div style="color: #FFD700; font-size: 2.5rem; font-weight: 900; margin: 15px 0;">
                    +9,999 REPUTATION
                </div>
                <div style="color: white; font-size: 1.2rem;">
                    🏅 <span style="color: #ffcc00;">Gold Badge:</span> FOSS Master<br>
                    🥈 <span style="color: #b4b8bb;">Silver Badge:</span> Security Expert<br>
                    🥉 <span style="color: #d1a684;">Bronze Badge:</span> Quick Learner
                </div>
            </div>
            <p style="font-size: 1.4rem; color: white; margin-top: 20px; line-height: 1.8;">
                You've conquered all challenges and proven yourself as a true <strong style="color: #FFD700;">FOSS LEGEND</strong>!<br>
                Your dedication to Software Freedom is <span style="color: #00ff00; font-weight: 900;">LEGENDARY</span>! 🌟
            </p>
            <div style="font-size: 2.8rem; margin-top: 20px; animation: spin 3s linear infinite;">🏆 👑 💎 🎯 🚀</div>
        </div>
        <style>
            @keyframes soGlow {
                0%, 100% { box-shadow: 0 0 30px rgba(244,128,36,0.5); }
                50% { box-shadow: 0 0 60px rgba(244,128,36,0.8), 0 0 90px rgba(255,215,0,0.6); }
            }
            @keyframes spin {
                0% { transform: rotateY(0deg); }
                100% { transform: rotateY(360deg); }
            }
            @keyframes bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-15px); }
            }
        </style>
        """, unsafe_allow_html=True)
    
        # Victory GIF
        st.markdown(
        """
        <div style="display:flex; justify-content:center; margin: 30px 0;">
            <img src="https://media.tenor.com/2OesmlazcyoAAAAi/celebration-celebrate.gif" width="300" style="border-radius: 20px; box-shadow: 0 0 40px rgba(255, 215, 0, 0.6);">
        </div>
        """,
        unsafe_allow_html=True
        )

        # PROFESSIONAL METRICS DASHBOARD
        st.markdown(f"""
        <div class="metrics-dashboard">
            <div class="dashboard-header">
                <h2 class="dashboard-title">📊 Performance Analytics</h2>
                <div class="dashboard-subtitle">Real-time Achievement Metrics</div>
            </div>
            <div class="metrics-grid">
                <div class="metric-card" style="--delay: 0s;">
                    <div class="metric-icon">⏱️</div>
                    <div class="metric-value">{format_time(elapsed)}</div>
                    <div class="metric-label">Completion Time</div>
                    <div class="metric-code">time.delta()</div>
                </div>
                <div class="metric-card" style="--delay: 0.1s;">
                    <div class="metric-icon">🎯</div>
                    <div class="metric-value">{st.session_state.score}</div>
                    <div class="metric-label">Total Score</div>
                    <div class="metric-code">score.total</div>
                </div>
                <div class="metric-card" style="--delay: 0.2s;">
                    <div class="metric-icon">🔥</div>
                    <div class="metric-value">{st.session_state.max_streak}x</div>
                    <div class="metric-label">Max Streak</div>
                    <div class="metric-code">streak.max</div>
                </div>
                <div class="metric-card" style="--delay: 0.3s;">
                    <div class="metric-icon">⭐</div>
                    <div class="metric-value">{st.session_state.perfect_levels}/{len(st.session_state.QUESTIONS)}</div>
                    <div class="metric-label">Perfect Levels</div>
                    <div class="metric-code">perfect.count</div>
                </div>
                <div class="metric-card" style="--delay: 0.4s;">
                    <div class="metric-icon">💡</div>
                    <div class="metric-value">{st.session_state.hints_used}</div>
                    <div class="metric-label">Hints Used</div>
                    <div class="metric-code">hints.total</div>
                </div>
            </div>
        </div>
        <style>
            .metrics-dashboard {{
                max-width: 1200px;
                margin: 50px auto;
                padding: 30px;
                background: linear-gradient(135deg, rgba(0, 0, 0, 0.8), rgba(20, 20, 40, 0.8));
                border: 1px solid rgba(0, 255, 255, 0.3);
                border-radius: 16px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
            }}
            .dashboard-header {{
                text-align: center;
                margin-bottom: 40px;
            }}
            .dashboard-title {{
                font-size: 2.2rem;
                font-weight: 900;
                color: #00ffff;
                margin-bottom: 10px;
                text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
            }}
            .dashboard-subtitle {{
                font-size: 1rem;
                color: rgba(255, 255, 255, 0.6);
                font-family: 'Courier New', monospace;
            }}
            .metrics-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
            }}
            .metric-card {{
                background: linear-gradient(135deg, rgba(0, 255, 255, 0.05), rgba(255, 0, 255, 0.05));
                border: 2px solid rgba(0, 255, 255, 0.3);
                border-radius: 12px;
                padding: 24px;
                text-align: center;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                animation: slideUp 0.6s ease-out var(--delay) backwards;
            }}
            .metric-card:hover {{
                transform: translateY(-8px);
                border-color: #00ffff;
                box-shadow: 0 10px 30px rgba(0, 255, 255, 0.3);
            }}
            .metric-icon {{
                font-size: 2.5rem;
                margin-bottom: 12px;
                filter: drop-shadow(0 0 10px rgba(255, 255, 255, 0.5));
            }}
            .metric-value {{
                font-size: 2.5rem;
                font-weight: 900;
                color: #ffd700;
                margin: 12px 0;
                font-family: 'Courier New', monospace;
                text-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
            }}
            .metric-label {{
                font-size: 0.95rem;
                color: rgba(255, 255, 255, 0.8);
                font-weight: 600;
                margin-bottom: 10px;
            }}
            .metric-code {{
                font-family: 'Courier New', monospace;
                font-size: 0.8rem;
                color: #00ff41;
                opacity: 0.7;
                margin-top: 8px;
            }}
            @keyframes slideUp {{
                from {{
                    opacity: 0;
                    transform: translateY(40px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}
        </style>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # PROFESSIONAL ACHIEVEMENT SYSTEM
        st.markdown("""
        <div class="achievements-section">
            <div class="section-header">
                <div class="header-icon">🏅</div>
                <div class="header-content">
                    <h2 class="section-title">Achievement System</h2>
                    <p class="section-description">Milestone Badges Unlocked</p>
                </div>
            </div>
        </div>
        <style>
            .achievements-section {
                max-width: 1200px;
                margin: 60px auto 40px;
            }
            .section-header {
                display: flex;
                align-items: center;
                gap: 20px;
                padding: 30px;
                background: linear-gradient(135deg, rgba(255, 215, 0, 0.1), rgba(255, 140, 0, 0.1));
                border: 2px solid rgba(255, 215, 0, 0.3);
                border-radius: 16px;
                margin-bottom: 30px;
            }
            .header-icon {
                font-size: 4rem;
                filter: drop-shadow(0 0 20px rgba(255, 215, 0, 0.6));
                animation: iconPulse 2s ease-in-out infinite;
            }
            .header-content {
                flex: 1;
            }
            .section-title {
                font-size: 2.5rem;
                font-weight: 900;
                color: #ffd700;
                margin: 0 0 8px 0;
                text-shadow: 0 2px 15px rgba(255, 215, 0, 0.5);
            }
            .section-description {
                font-size: 1.1rem;
                color: rgba(255, 255, 255, 0.7);
                margin: 0;
                font-family: 'Courier New', monospace;
            }
            @keyframes iconPulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.1); }
            }
        </style>
        """, unsafe_allow_html=True)

        base_achievements = [
        "🎓 FOSS Graduate",
        "🔐 Security Expert",
        f"⚡ Speed Runner" if elapsed < 600 else "🐢 Methodical Thinker"
        ]

        all_achievements = base_achievements + st.session_state.achievements

        # PROFESSIONAL BADGE CARDS
        achievement_cols = st.columns(min(4, len(all_achievements)))
        for i, achievement in enumerate(all_achievements):
            with achievement_cols[i % 4]:
                # Professional color scheme
                badge_colors = {
                    0: {'primary': '#00ff41', 'secondary': 'rgba(0, 255, 65, 0.1)', 'name': 'Success'},
                    1: {'primary': '#00d4ff', 'secondary': 'rgba(0, 212, 255, 0.1)', 'name': 'Info'},
                    2: {'primary': '#ffd700', 'secondary': 'rgba(255, 215, 0, 0.1)', 'name': 'Gold'},
                    3: {'primary': '#ff6b6b', 'secondary': 'rgba(255, 107, 107, 0.1)', 'name': 'Accent'}
                }
                color_scheme = badge_colors[i % 4]
                
                st.markdown(f"""
                <div class="badge-card" style="--badge-color: {color_scheme['primary']}; --badge-bg: {color_scheme['secondary']}; animation-delay: {i * 0.1}s;">
                    <div class="badge-header">
                        <div class="badge-icon">🏆</div>
                        <div class="badge-status">
                            <span class="status-dot"></span>
                            <span class="status-text">UNLOCKED</span>
                        </div>
                    </div>
                    <div class="badge-content">
                        <h3 class="badge-title">{achievement}</h3>
                        <div class="badge-meta">
                            <span class="meta-item">
                                <span class="meta-icon">✓</span>
                                <span class="meta-text">Verified</span>
                            </span>
                            <span class="meta-item">
                                <span class="meta-icon">📊</span>
                                <span class="meta-text">Elite</span>
                            </span>
                        </div>
                    </div>
                    <div class="badge-footer">
                        <code class="badge-code">achievement_{i + 1}.unlock()</code>
                    </div>
                </div>
                <style>
                    .badge-card {{
                        background: linear-gradient(135deg, var(--badge-bg), rgba(0, 0, 0, 0.6));
                        border: 2px solid var(--badge-color);
                        border-radius: 12px;
                        padding: 20px;
                        margin-bottom: 20px;
                        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                        animation: badgeFadeIn 0.6s ease-out backwards;
                        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
                    }}
                    .badge-card:hover {{
                        transform: translateY(-8px) scale(1.02);
                        box-shadow: 0 12px 30px var(--badge-color);
                        border-color: var(--badge-color);
                    }}
                    .badge-header {{
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        margin-bottom: 16px;
                    }}
                    .badge-icon {{
                        font-size: 2.5rem;
                        filter: drop-shadow(0 0 10px var(--badge-color));
                    }}
                    .badge-status {{
                        display: flex;
                        align-items: center;
                        gap: 6px;
                        background: rgba(0, 0, 0, 0.5);
                        padding: 6px 12px;
                        border-radius: 20px;
                        border: 1px solid var(--badge-color);
                    }}
                    .status-dot {{
                        width: 8px;
                        height: 8px;
                        background: var(--badge-color);
                        border-radius: 50%;
                        animation: pulse 2s ease-in-out infinite;
                    }}
                    .status-text {{
                        font-size: 0.75rem;
                        color: var(--badge-color);
                        font-weight: 700;
                        font-family: 'Courier New', monospace;
                    }}
                    .badge-content {{
                        margin: 16px 0;
                    }}
                    .badge-title {{
                        font-size: 1.15rem;
                        font-weight: 900;
                        color: white;
                        margin: 0 0 12px 0;
                        line-height: 1.3;
                    }}
                    .badge-meta {{
                        display: flex;
                        gap: 12px;
                    }}
                    .meta-item {{
                        display: flex;
                        align-items: center;
                        gap: 4px;
                        font-size: 0.85rem;
                        color: rgba(255, 255, 255, 0.7);
                    }}
                    .meta-icon {{
                        color: var(--badge-color);
                    }}
                    .badge-footer {{
                        margin-top: 16px;
                        padding-top: 16px;
                        border-top: 1px solid rgba(255, 255, 255, 0.1);
                    }}
                    .badge-code {{
                        font-family: 'Courier New', monospace;
                        font-size: 0.8rem;
                        color: var(--badge-color);
                        background: rgba(0, 0, 0, 0.5);
                        padding: 6px 10px;
                        border-radius: 6px;
                        display: block;
                    }}
                    @keyframes badgeFadeIn {{
                        from {{
                            opacity: 0;
                            transform: scale(0.8) rotate(-10deg);
                        }}
                        to {{
                            opacity: 1;
                            transform: scale(1) rotate(0deg);
                        }}
                    }}
                    @keyframes pulse {{
                        0%, 100% {{ opacity: 1; }}
                        50% {{ opacity: 0.5; }}
                    }}
                </style>
                """, unsafe_allow_html=True)

        st.markdown("---")

        # Level Breakdown
        with st.expander("📋 COMPLETE MISSION BREAKDOWN", expanded=False):
            st.markdown("### Your Journey Through FOSS:")
            for i, q in enumerate(QUESTIONS, 1):
                st.markdown(f"""
            <div class="glass-container" style="padding: 15px; margin: 10px 0;">
                <strong>Level {i}:</strong> {q['category']} 
                <span class="badge badge-{q['difficulty']}">{q['difficulty'].upper()}</span><br>
                🧩 <strong>Answer:</strong> <code>{q['answer']}</code><br>
                🔐 <strong>Security Key:</strong> <code>{q['security_key']}</code><br>
                💰 <strong>Points:</strong> {q['points']}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Performance Analysis
        st.markdown("### 📈 PERFORMANCE ANALYSIS")

        accuracy = ((len(st.session_state.QUESTIONS) * 2) / (len(st.session_state.QUESTIONS) * 2 + st.session_state.hints_used)) * 100
        speed_score = max(0, 100 - (elapsed / 10))

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
        <div class="glass-container">
            <h4 style="color: var(--primary-glow);">Accuracy Rating</h4>
            <div style="font-size: 3rem; font-weight: 900; color: var(--success-glow);">
                {accuracy:.0f}%
            </div>
            <p>Based on hints used vs questions solved</p>
        </div>
        """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
        <div class="glass-container">
            <h4 style="color: var(--secondary-glow);">Speed Rating</h4>
            <div style="font-size: 3rem; font-weight: 900; color: var(--gold-glow);">
                {speed_score:.0f}%
            </div>
            <p>Time efficiency score</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Share Section
        st.markdown("### 🌐 SHARE YOUR VICTORY!")

        share_text = f"🏆 I just completed the Elite FOSS Treasure Hunt!\n\n📊 Score: {st.session_state.score} pts\n🏅 Rank: {rank}\n⏱ Time: {format_time(elapsed)}\n🔥 Best Streak: {st.session_state.max_streak}x\n\nCelebrating Software Freedom Day! #FOSS #SoftwareFreedom"

        st.markdown(f"""
        <div class="glass-container" style="text-align: center;">
        <p style="font-size: 1.1rem; line-height: 1.8;">
            <strong>Your Stats:</strong><br>
            🎯 Score: {st.session_state.score} points<br>
            🏆 Rank: {rank}<br>
            ⏱ Time: {format_time(elapsed)}<br>
            🔥 Streak: {st.session_state.max_streak}x<br>
            ⭐ Perfect Levels: {st.session_state.perfect_levels}/{len(st.session_state.QUESTIONS)}
        </p>
        <p style="margin-top: 20px; font-size: 1.1rem;">
            📚 <strong>Learn More About FOSS:</strong><br>
            <a href='https://digitalfreedoms.org/en/sfd' target='_blank' 
               style='color: var(--primary-glow); margin: 0 10px;'>Software Freedom Day</a> •
            <a href='https://www.fsf.org/' target='_blank' 
               style='color: var(--primary-glow); margin: 0 10px;'>FSF</a> •
            <a href='https://www.linuxfoundation.org/' target='_blank' 
               style='color: var(--primary-glow); margin: 0 10px;'>Linux Foundation</a>
        </p>
        </div>
        """)

        # PROFESSIONAL CALL-TO-ACTION
        st.markdown("""
        <div class="cta-section">
            <div class="cta-card">
                <div class="cta-header">
                    <div class="cta-icon">🔄</div>
                    <h3 class="cta-title">Challenge Yourself Again</h3>
                </div>
                <p class="cta-description">
                    Think you can beat your performance? Test your FOSS knowledge once more and aim for perfection.
                </p>
                <div class="cta-meta">
                    <span class="meta-badge">🎯 Current Score: {st.session_state.score}</span>
                    <span class="meta-badge">⏱️ Time: {format_time(elapsed)}</span>
                </div>
            </div>
        </div>
        <style>
            .cta-section {{
                max-width: 800px;
                margin: 60px auto;
            }}
            .cta-card {{
                background: linear-gradient(135deg, rgba(0, 255, 255, 0.1), rgba(255, 0, 255, 0.1));
                border: 2px solid rgba(0, 255, 255, 0.4);
                border-radius: 16px;
                padding: 40px;
                text-align: center;
                transition: all 0.3s ease;
            }}
            .cta-card:hover {{
                transform: translateY(-4px);
                box-shadow: 0 15px 40px rgba(0, 255, 255, 0.3);
            }}
            .cta-header {{
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 16px;
                margin-bottom: 20px;
            }}
            .cta-icon {{
                font-size: 3rem;
                filter: drop-shadow(0 0 15px rgba(0, 255, 255, 0.8));
            }}
            .cta-title {{
                font-size: 2rem;
                font-weight: 900;
                color: #00ffff;
                margin: 0;
            }}
            .cta-description {{
                font-size: 1.1rem;
                color: rgba(255, 255, 255, 0.8);
                line-height: 1.6;
                margin: 20px 0;
            }}
            .cta-meta {{
                display: flex;
                gap: 16px;
                justify-content: center;
                flex-wrap: wrap;
                margin-top: 24px;
            }}
            .meta-badge {{
                background: rgba(0, 0, 0, 0.5);
                border: 1px solid rgba(255, 255, 255, 0.2);
                padding: 8px 16px;
                border-radius: 20px;
                font-family: 'Courier New', monospace;
                font-size: 0.9rem;
                color: #ffd700;
            }}
        </style>
        """, unsafe_allow_html=True)
        
        # Show completion message - NO REPLAY ALLOWED
        st.markdown("""
        <div style="text-align: center; padding: 40px; background: rgba(255, 215, 0, 0.1); 
                    border: 2px solid rgba(255, 215, 0, 0.4); border-radius: 16px; margin: 30px 0;">
            <h2 style="color: #ffd700; font-size: 2rem; margin-bottom: 15px;">🎯 GAME COMPLETED</h2>
            <p style="font-size: 1.2rem; color: rgba(255,255,255,0.9); line-height: 1.6;">
                This treasure hunt can only be played <strong>once</strong>.<br>
                Your achievement has been permanently saved!<br><br>
                <span style="color: #00ffff;">✨ Thank you for celebrating Software Freedom Day! ✨</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # PROFESSIONAL DEVELOPER CREDITS & STATS SUMMARY
        st.markdown(f"""
        <div class="dev-credits">
            <div class="credits-card">
                <div class="credits-header">
                    <div class="header-badge">
                        <span class="badge-icon">👑</span>
                        <span class="badge-text">ELITE STATUS</span>
                    </div>
                </div>
                <div class="credits-content">
                    <h2 class="achievement-rank">{rank}</h2>
                    <p class="achievement-desc">{subtitle}</p>
                    <div class="stats-summary">
                        <div class="stat-item">
                            <span class="stat-label">Total Score</span>
                            <span class="stat-value">{st.session_state.score} pts</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Completion Time</span>
                            <span class="stat-value">{format_time(elapsed)}</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Max Streak</span>
                            <span class="stat-value">{st.session_state.max_streak}x</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Perfect Levels</span>
                            <span class="stat-value">{st.session_state.perfect_levels}/{len(st.session_state.QUESTIONS)}</span>
                        </div>
                    </div>
                </div>
                <div class="credits-footer">
                    <div class="footer-message">
                        <p class="message-text">
                            <strong>🌟 Congratulations!</strong> You've mastered all FOSS challenges and earned your place among the elite.
                        </p>
                        <p class="message-subtext">
                            Your commitment to open source excellence is truly exceptional.
                        </p>
                    </div>
                    <div class="footer-code">
                        <code>// Achievement verified and logged ✓</code>
                    </div>
                </div>
            </div>
        </div>
        <style>
            .dev-credits {{
                max-width: 900px;
                margin: 60px auto;
            }}
            .credits-card {{
                background: linear-gradient(135deg, rgba(0, 0, 0, 0.9), rgba(30, 30, 60, 0.9));
                border: 2px solid rgba(255, 215, 0, 0.4);
                border-radius: 20px;
                overflow: hidden;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.6);
            }}
            .credits-header {{
                background: linear-gradient(135deg, rgba(255, 215, 0, 0.2), rgba(255, 140, 0, 0.2));
                padding: 24px;
                text-align: center;
                border-bottom: 2px solid rgba(255, 215, 0, 0.3);
            }}
            .header-badge {{
                display: inline-flex;
                align-items: center;
                gap: 10px;
                background: rgba(255, 215, 0, 0.2);
                border: 2px solid #ffd700;
                padding: 12px 24px;
                border-radius: 30px;
            }}
            .badge-icon {{
                font-size: 1.8rem;
            }}
            .badge-text {{
                font-size: 1.1rem;
                font-weight: 900;
                color: #ffd700;
                font-family: 'Courier New', monospace;
                letter-spacing: 2px;
            }}
            .credits-content {{
                padding: 40px;
                text-align: center;
            }}
            .achievement-rank {{
                font-size: 3rem;
                font-weight: 900;
                color: #ffd700;
                margin: 0 0 16px 0;
                text-shadow: 0 0 30px rgba(255, 215, 0, 0.6);
            }}
            .achievement-desc {{
                font-size: 1.3rem;
                color: #00ffff;
                margin: 0 0 40px 0;
                font-weight: 600;
            }}
            .stats-summary {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 24px;
                margin-top: 30px;
            }}
            .stat-item {{
                background: rgba(0, 255, 255, 0.05);
                border: 1px solid rgba(0, 255, 255, 0.3);
                border-radius: 12px;
                padding: 20px;
                display: flex;
                flex-direction: column;
                gap: 8px;
            }}
            .stat-label {{
                font-size: 0.85rem;
                color: rgba(255, 255, 255, 0.6);
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            .stat-value {{
                font-size: 1.8rem;
                font-weight: 900;
                color: #00ffff;
                font-family: 'Courier New', monospace;
            }}
            .credits-footer {{
                background: rgba(0, 0, 0, 0.5);
                padding: 30px;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
            }}
            .footer-message {{
                text-align: center;
                margin-bottom: 20px;
            }}
            .message-text {{
                font-size: 1.1rem;
                color: white;
                line-height: 1.6;
                margin: 0 0 12px 0;
            }}
            .message-subtext {{
                font-size: 0.95rem;
                color: rgba(255, 255, 255, 0.7);
                margin: 0;
            }}
            .footer-code {{
                text-align: center;
                margin-top: 20px;
            }}
            .footer-code code {{
                background: rgba(0, 255, 0, 0.1);
                border: 1px solid rgba(0, 255, 0, 0.3);
                padding: 8px 16px;
                border-radius: 6px;
                font-family: 'Courier New', monospace;
                font-size: 0.9rem;
                color: #00ff41;
            }}
        </style>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 30px; color: rgba(255,255,255,0.5);">
    <p style="font-size: 1.2rem; margin-bottom: 10px;">Made with ❤ for Software Freedom Day</p>
    <p style="font-size: 1rem;">Celebrating Open Source • Building Digital Freedom</p>
    <p style="font-size: 0.9rem; margin-top: 15px;">🔐 Elite Two-Phase Challenge System</p>
</div>
""", unsafe_allow_html=True)