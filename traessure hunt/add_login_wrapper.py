#!/usr/bin/env python3
"""Add login wrapper to final2_backup.py and create final2_with_login.py"""

# Read original file
with open('final2_backup.py', 'r', encoding='utf-8') as f:
    original_content = f.read()

# Find where to insert login code (after imports, before set_page_config)
lines = original_content.split('\n')

# Find the line with st.set_page_config
config_line_idx = -1
for i, line in enumerate(lines):
    if 'st.set_page_config' in line:
        config_line_idx = i
        break

# Find the line with "# MAIN APPLICATION" 
main_app_idx = -1
for i, line in enumerate(lines):
    if '# MAIN APPLICATION' in line and '═' in lines[i-1]:
        main_app_idx = i
        break

print(f"Found config at line {config_line_idx}")
print(f"Found main app at line {main_app_idx}")

# Insert login function after render_sidebar function and before MAIN APPLICATION
# Find where render_sidebar ends
render_sidebar_end = -1
for i in range(len(lines)-1, -1, -1):
    if 'def render_sidebar' in lines[i]:
        # Find the end of this function
        for j in range(i+1, len(lines)):
            if lines[j].strip() and not lines[j].startswith(' ') and not lines[j].startswith('\t') and lines[j].strip() != '':
                if '# ═══' in lines[j] or 'def ' in lines[j]:
                    render_sidebar_end = j
                    break
        break

print(f"render_sidebar ends at line {render_sidebar_end}")

# Create login function
login_function = """

# ═══════════════════════════════════════════════════════════════════════════════
# LOGIN SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════
def render_login_page():
    \"\"\"Render the futuristic login page\"\"\"
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

"""

# Now build the new file
new_lines = lines[:render_sidebar_end] + [login_function] + lines[render_sidebar_end:]

# Now find init_session_state and add logged_in and username to defaults
for i, line in enumerate(new_lines):
    if 'def init_session_state():' in line:
        # Find the defaults dict
        for j in range(i, min(i+30, len(new_lines))):
            if 'defaults = {' in new_lines[j]:
                # Add logged_in and username after the opening brace
                new_lines[j] = new_lines[j].replace('defaults = {', 'defaults = {\n        "logged_in": False,\n        "username": "",')
                break
        break

# Now wrap the main game in if/else for login
# Find "init_session_state()" call and add login check
for i, line in enumerate(new_lines):
    if line.strip() == 'init_session_state()' and i > main_app_idx:
        # Insert login check after init
        new_lines[i] = '''init_session_state()

# Check login status
if not st.session_state.get("logged_in", False):
    render_login_page()
else:
    # User is logged in, show the game'''
        break

# Add indentation to all game code (from "# Animated Title" to "# Footer")
# Find these markers
title_idx = -1
footer_idx = -1

for i, line in enumerate(new_lines):
    if '# Animated Title' in line and title_idx == -1 and i > main_app_idx:
        title_idx = i
    if '# Footer' in line and footer_idx == -1 and i > title_idx:
        footer_idx = i
        break

print(f"Found title at {title_idx}, footer at {footer_idx}")

# Add 4 spaces to all lines between title_idx and footer_idx (inclusive of footer)
final_lines = []
for i, line in enumerate(new_lines):
    if i >= title_idx and i <= footer_idx:
        if line.strip():  # Not empty
            final_lines.append('    ' + line)
        else:
            final_lines.append(line)
    else:
        final_lines.append(line)

# Write new file
with open('final2_with_login.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(final_lines))

print("Created final2_with_login.py successfully!")
