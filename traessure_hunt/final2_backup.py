import streamlit as st
import random
from datetime import datetime
from typing import Dict, List, Tuple
import time

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
QUESTIONS: List[Dict] = [
    {
        "question": "🔍 The Hidden Core\n\nI am invisible but control it all,\nCPU, memory, devices—I stand tall.\nWithout me, Linux would never run,\nFind my name, and Level 2 is begun.",
        "answer": "kernel",
        "security_riddle": "What 3-letter command shows you where you are in the Linux filesystem?",
        "security_key": "pwd",
        "hint": "💡 Think of the 'heart' of the operating system that manages hardware.",
        "security_hint": "💡 Stands for 'Print Working Directory'.",
        "category": "OS Architecture",
        "difficulty": "easy",
        "points": 10
    },
    {
        "question": "🔍 The Command Interpreter\n\nI'm not food, but I'm called a shell,\nWithout me, using the kernel is hell.\nI take your commands, one by one,\nBash, Zsh, Fish—I'm the one!",
        "answer": "shell",
        "security_riddle": "What license ensures software remains free and open source? (3 letters, created by FSF)",
        "security_key": "gpl",
        "hint": "💡 The interface between users and the kernel. Famous types include Bash and Zsh.",
        "security_hint": "💡 GNU _____ License. Richard Stallman's creation.",
        "category": "System Components",
        "difficulty": "medium",
        "points": 15
    },
    {
        "question": "🔍 The Ancient Ancestor\n\nBorn at Bell Labs in the 1970s,\nI shaped today's systems and realities.\nLinux is my child, that's true,\nFour letters, can you name me too?",
        "answer": "unix",
        "security_riddle": "Decode: 01101100 01101001 01101110 01110101 01111000",
        "security_key": "linux",
        "hint": "💡 The operating system that inspired Linux. Starts with 'U'.",
        "security_hint": "💡 Convert binary to ASCII. Each group is 8 bits = 1 character.",
        "category": "OS History",
        "difficulty": "hard",
        "points": 20
    },
    {
        "question": "🔍 The Software Manager\n\nI fetch, install, and update with ease,\napt, yum, pacman—examples of me.\nWithout me, your software is stranded,\nWhat's my name, two words demanded?",
        "answer": "package manager",
        "security_riddle": "What command changes your current directory in Linux? (2 letters)",
        "security_key": "cd",
        "hint": "💡 Two words. First word is 'Package'. Manages software installation.",
        "security_hint": "💡 'Change Directory' - one of the most basic Linux commands.",
        "category": "System Tools",
        "difficulty": "medium",
        "points": 15
    },
    {
        "question": "🔍 The Permission Master\n\nI control who can read, write, execute,\nThree groups of three—that's my tribute.\nOwner, group, others—I set the law,\nWhat am I called? Answer with awe.",
        "answer": "chmod",
        "security_riddle": "What famous OS did Linus Torvalds create? (5 letters)",
        "security_key": "linux",
        "hint": "💡 A Linux command to change file permissions. Starts with 'ch'.",
        "security_hint": "💡 The creator's first name is Linus. OS released in 1991.",
        "category": "File System",
        "difficulty": "medium",
        "points": 15
    },
    {
        "question": "🔍 The Final Treasure\n\nI wrote the kernel back in '91,\nFor fun at first, but now it runs everyone.\nA Finnish programmer, still maintaining today,\nWho am I—can you say?",
        "answer": "linus torvalds",
        "security_riddle": "What 3-letter open source version control system did Linus also create?",
        "security_key": "git",
        "hint": "💡 His first name is Linus. Created Linux as a student project.",
        "security_hint": "💡 Rhymes with 'sit'. Used for tracking code changes.",
        "category": "Linux History",
        "difficulty": "hard",
        "points": 20
    }
]


# ═══════════════════════════════════════════════════════════════════════════════
# SESSION STATE MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════
def init_session_state():
    """Initialize all session state variables with proper defaults"""
    defaults = {
        "logged_in": False,
        "username": "",
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
        "show_level_animation": False
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ═══════════════════════════════════════════════════════════════════════════════
# LOGIN SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════
def render_login_page():
    """Render the futuristic login page"""
    # Login Page Header
    st.markdown('''
    <div style="text-align: center; margin: 50px 0;">
        <div style="font-size: 6rem; animation: loginFloat 3s ease-in-out infinite;">🔐</div>
        <h1 class="hero-title" style="margin-top: 20px;">ACCESS TERMINAL</h1>
        <p style="font-size: 1.5rem; color: var(--primary-glow); text-shadow: 0 0 20px var(--primary-glow);">
            Enter your credentials to begin the adventure
        </p>
    </div>
    <style>
        @keyframes loginFloat {
            0%, 100% { transform: translateY(0) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(10deg); }
        }
    </style>
    ''', unsafe_allow_html=True)
    
    # Login Form Container
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('''
        <div class="glass-container" style="padding: 50px; margin: 30px 0;">
            <h2 style="text-align: center; color: var(--primary-glow); margin-bottom: 30px; font-size: 2rem;">
                🔑 SECURITY CHECKPOINT
            </h2>
        </div>
        ''', unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input(
                "👤 Username",
                placeholder="Enter your username",
                help="Choose any username to identify yourself"
            )
            
            password = st.text_input(
                "🔒 Password",
                type="password",
                placeholder="Enter password",
                help="Default password: foss2024"
            )
            
            st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
            
            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_b:
                submit_button = st.form_submit_button(
                    "🚀 ENTER GAME",
                    use_container_width=True,
                    type="primary"
                )
        
        if submit_button:
            if username.strip() == "":
                st.error("⚠️ Username cannot be empty!")
            elif password != "foss2024":
                st.error("❌ Access Denied! Incorrect password.")
                st.markdown('''
                <div style="display:flex; justify-content:center; margin: 20px 0;">
                    <img src="https://media.tenor.com/DQRSMm8uuq4AAAAi/tamil-hindu.gif" width="200">
                </div>
                ''', unsafe_allow_html=True)
            else:
                # Successful login
                st.session_state.logged_in = True
                st.session_state.username = username.strip()
                st.session_state.start_time = datetime.now()
                st.success(f"✅ Welcome, {username}! Initializing treasure hunt...")
                st.markdown('''
                <div style="display:flex; justify-content:center; margin: 20px 0;">
                    <img src="https://media.tenor.com/2OesmlazcyoAAAAi/celebration-celebrate.gif" width="200">
                </div>
                ''', unsafe_allow_html=True)
                time.sleep(1.5)
                st.rerun()
        
        # Login hints
        st.markdown('''
        <div style="background: rgba(0, 255, 255, 0.05); border-left: 4px solid var(--primary-glow); 
                    padding: 20px; margin-top: 30px; border-radius: 10px;">
            <h4 style="color: var(--primary-glow); margin-bottom: 15px;">💡 Login Information</h4>
            <p style="line-height: 1.8; color: rgba(255,255,255,0.8);">
                <strong>Default Password:</strong> <code style="background: rgba(255,255,255,0.1); 
                padding: 5px 10px; border-radius: 5px; color: var(--success-glow);">foss2024</code><br>
                <strong>Username:</strong> Enter any name you like!<br><br>
                🎮 Prepare yourself for the ultimate FOSS challenge!<br>
                🏆 Complete all levels to become a FOSS Grandmaster!
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
def get_rank() -> Tuple[str, str]:
    """Calculate player rank and icon based on comprehensive performance"""
    score = st.session_state.score
    hints = st.session_state.hints_used
    streak = st.session_state.max_streak
    perfect = st.session_state.perfect_levels

    if score >= 95 and hints == 0 and perfect == len(QUESTIONS):
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
    progress_pct = (st.session_state.level / len(QUESTIONS)) * 100
    current = st.session_state.level

    nodes_html = '<div class="node-tracker">'
    for i in range(len(QUESTIONS)):
        if i < current:
            nodes_html += f'<div class="node completed">{i + 1}</div>'
        elif i == current:
            nodes_html += f'<div class="node active">{i + 1}</div>'
        else:
            nodes_html += f'<div class="node">{i + 1}</div>'

        if i < len(QUESTIONS) - 1:
            connector_class = "node-connector active" if i < current else "node-connector"
            nodes_html += f'<div class="{connector_class}"></div>'

    nodes_html += '</div>'

    st.markdown(f"""
    <div style="margin: 30px 0;">
        {nodes_html}
        <div style="text-align: center; margin-top: 20px;">
            <span style="font-size: 1.5rem; color: var(--primary-glow); font-weight: 700;">
                Progress: {progress_pct:.0f}% • Level {current + 1}/{len(QUESTIONS)}
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
            <div class="stat-value">{st.session_state.level + 1}/{len(QUESTIONS)}</div>
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
        progress_pct = (st.session_state.level / len(QUESTIONS)) * 100
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
    if not st.session_state.finished:
        # Display animations if triggered
        if st.session_state.show_riddle_animation:
        points = QUESTIONS[st.session_state.level]['points']
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
        with st.expander(f"✅ Completed Missions ({st.session_state.level}/{len(QUESTIONS)})", expanded=False):
            for i in range(st.session_state.level):
                q = QUESTIONS[i]
                st.markdown(
                    f'<div class="completed-level">Level {i + 1}: {q["category"]} - '
                    f'{q["difficulty"].upper()} ✓ | 🔐 Unlocked</div>',
                    unsafe_allow_html=True
                )

    # Current Question
    current_q = QUESTIONS[st.session_state.level]

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

        if hint_btn:
            if not st.session_state.show_hint:
                st.session_state.hints_used += 1
                st.session_state.streak = 0
                st.session_state.combo_multiplier = 1.0
                st.info("⚠ Streak and combo reset!")
            st.session_state.show_hint = True

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

                # Check for achievements
                if st.session_state.streak >= 5:
                    add_achievement("Streak Master")
                if st.session_state.streak >= 6:
                    add_achievement("Unstoppable")

                if st.session_state.level >= len(QUESTIONS):
                    st.session_state.finished = True

                st.session_state.show_level_animation = True
                st.rerun()
            else:
                # Wrong Security Key
                st.session_state.security_wrong_attempts += 1
                st.session_state.streak = 0
                st.session_state.combo_multiplier = 1.0
                st.error(f"🔒 **ACCESS DENIED!** Attempt {st.session_state.security_wrong_attempts}/∞")

                if st.session_state.security_wrong_attempts >= 3:
                    st.warning("💡 Need assistance? Try the security hint!")

        if security_hint_btn:
            if not st.session_state.show_security_hint:
                st.session_state.hints_used += 1
                st.session_state.streak = 0
                st.session_state.combo_multiplier = 1.0
                st.info("⚠ Streak and combo reset!")
            st.session_state.show_security_hint = True

        if st.session_state.show_security_hint:
            st.markdown(f"""
            <div class="hint-container">
                <div style="font-size: 1.5rem; margin-bottom: 10px;">🔐 SECURITY HINT</div>
                <div style="font-size: 1.1rem;">{current_q['security_hint']}</div>
            </div>
            """, unsafe_allow_html=True)

    # Preview Upcoming Levels
    st.markdown("---")
    st.markdown("### 🔮 UPCOMING MISSIONS")

    remaining = min(3, len(QUESTIONS) - st.session_state.level - 1)
    if remaining > 0:
        cols = st.columns(remaining)
        for i in range(remaining):
            level_num = st.session_state.level + i + 1
            next_q = QUESTIONS[level_num]
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
else:
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
            All {len(QUESTIONS)} levels completed!<br>
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
    
    # Victory GIF
    st.markdown(
        """
        <div style="display:flex; justify-content:center; margin: 30px 0;">
            <img src="https://media.tenor.com/2OesmlazcyoAAAAi/celebration-celebrate.gif" width="300" style="border-radius: 20px; box-shadow: 0 0 40px rgba(255, 215, 0, 0.6);">
        </div>
        """,
        unsafe_allow_html=True
    )

    # Final Stats with celebration
    st.markdown("""
        <div style="text-align: center; margin: 30px 0;">
            <h3 style="font-size: 2rem; color: var(--primary-glow); animation: statsPulse 1.5s ease-in-out infinite;">
                📊 FINAL STATISTICS 📊
            </h3>
        </div>
        <style>
            @keyframes statsPulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)

    stats = [
        (col1, "⏱", format_time(elapsed), "Total Time"),
        (col2, "🎯", st.session_state.score, "Final Score"),
        (col3, "💡", st.session_state.hints_used, "Hints Used"),
        (col4, "🔥", st.session_state.max_streak, "Best Streak"),
        (col5, "⭐", st.session_state.perfect_levels, "Perfect Levels")
    ]

    for idx, (col, icon, value, label) in enumerate(stats):
        with col:
            delay = idx * 0.15
            st.markdown(f"""
            <div class="stat-card" style="animation: statCardAppear {0.6 + delay}s ease-out;">
                <div style="font-size: 2.5rem; animation: iconBounce 2s ease-in-out infinite;">{icon}</div>
                <div class="stat-value" style="animation: valueCount 1s ease-out {delay}s;">{value}</div>
                <div class="stat-label">{label}</div>
            </div>
            <style>
                @keyframes statCardAppear {{
                    0% {{ transform: translateY(50px); opacity: 0; }}
                    100% {{ transform: translateY(0); opacity: 1; }}
                }}
                @keyframes iconBounce {{
                    0%, 100% {{ transform: translateY(0); }}
                    50% {{ transform: translateY(-10px); }}
                }}
                @keyframes valueCount {{
                    0% {{ transform: scale(0); }}
                    50% {{ transform: scale(1.2); }}
                    100% {{ transform: scale(1); }}
                }}
            </style>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Achievements
    st.markdown("""
        <div style="text-align: center; margin: 40px 0;">
            <h3 style="font-size: 2.5rem; color: var(--gold-glow); animation: achievementGlow 2s ease-in-out infinite;">
                🏅 ACHIEVEMENTS UNLOCKED 🏅
            </h3>
            <div style="font-size: 2rem; margin-top: 15px;">
                ✨ 🌟 ⭐ 💎 ⭐ 🌟 ✨
            </div>
        </div>
        <style>
            @keyframes achievementGlow {
                0%, 100% { text-shadow: 0 0 20px var(--gold-glow); }
                50% { text-shadow: 0 0 40px var(--gold-glow), 0 0 60px var(--secondary-glow); }
            }
        </style>
    """, unsafe_allow_html=True)

    base_achievements = [
        "🎓 FOSS Graduate",
        "🔐 Security Expert",
        f"⚡ Speed Runner" if elapsed < 600 else "🐢 Methodical Thinker"
    ]

    all_achievements = base_achievements + st.session_state.achievements

    cols = st.columns(min(4, len(all_achievements)))
    for i, achievement in enumerate(all_achievements):
        with cols[i % 4]:
            delay = i * 0.1
            st.markdown(f"""
            <div class="glass-container" style="text-align: center; padding: 20px; animation: achievementPop {0.5 + delay}s ease-out;">
                <div style="font-size: 3rem; margin-bottom: 10px; animation: badgeSpin 2s ease-in-out infinite;">🏆</div>
                <div style="font-weight: 700; font-size: 1.1rem;">{achievement}</div>
            </div>
            <style>
                @keyframes achievementPop {{
                    0% {{ transform: scale(0) rotate(-180deg); opacity: 0; }}
                    50% {{ transform: scale(1.1) rotate(10deg); }}
                    100% {{ transform: scale(1) rotate(0deg); opacity: 1; }}
                }}
                @keyframes badgeSpin {{
                    0%, 100% {{ transform: rotate(0deg); }}
                    50% {{ transform: rotate(15deg); }}
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

    accuracy = ((len(QUESTIONS) * 2) / (len(QUESTIONS) * 2 + st.session_state.hints_used)) * 100
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
            ⭐ Perfect Levels: {st.session_state.perfect_levels}/{len(QUESTIONS)}
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

    # Play Again
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 PLAY AGAIN", use_container_width=True, type="primary"):
            reset_game()
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 30px; color: rgba(255,255,255,0.5);">
    <p style="font-size: 1.2rem; margin-bottom: 10px;">Made with ❤ for Software Freedom Day</p>
    <p style="font-size: 1rem;">Celebrating Open Source • Building Digital Freedom</p>
    <p style="font-size: 0.9rem; margin-top: 15px;">🔐 Elite Two-Phase Challenge System</p>
</div>
""", unsafe_allow_html=True)