# 🔗 Django Backend Integration Guide

## Overview

This guide shows how to integrate your Streamlit frontend with the Django backend.

## 📦 Required Package

Add to your Streamlit requirements:
```bash
pip install requests
```

## 🔧 Integration Code

### 1. API Helper Class

Add this to your `final2.py`:

```python
import requests

API_BASE_URL = "http://localhost:8000/api/auth"

class DjangoAPI:
    @staticmethod
    def login(username, password):
        try:
            response = requests.post(
                f"{API_BASE_URL}/login/",
                json={"username": username, "password": password},
                timeout=5
            )
            if response.status_code == 200:
                return True, response.json()
            return False, None
        except:
            return False, None
    
    @staticmethod
    def start_game_session(token):
        response = requests.post(
            f"{API_BASE_URL}/game/start/",
            headers={"Authorization": f"Token {token}"},
        )
        return response.json() if response.status_code == 201 else None
    
    @staticmethod
    def update_session(token, session_id, data):
        response = requests.put(
            f"{API_BASE_URL}/game/session/{session_id}/",
            headers={"Authorization": f"Token {token}"},
            json=data
        )
        return response.status_code == 200
```

### 2. Modify Login Function

Replace your current login logic:

```python
# In render_login_page(), modify the submit button handler:
if submit_button:
    success, data = DjangoAPI.login(username, password)
    if success:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.auth_token = data['token']
        st.session_state.user_id = data['user']['id']
        
        # Start Django session
        session = DjangoAPI.start_game_session(data['token'])
        st.session_state.django_session_id = session['id']
        
        st.success("Login successful!")
        st.rerun()
```

### 3. Sync Game Progress

Add sync function after each level:

```python
def sync_to_backend():
    if st.session_state.get('auth_token'):
        data = {
            "current_level": st.session_state.level,
            "score": st.session_state.score,
            "hints_used": st.session_state.hints_used,
            "current_streak": st.session_state.streak,
        }
        DjangoAPI.update_session(
            st.session_state.auth_token,
            st.session_state.django_session_id,
            data
        )

# Call after level completion:
if correct_answer:
    st.session_state.level += 1
    st.session_state.score += points
    sync_to_backend()  # Add this line
```

## 🚀 Running Both Servers

### Terminal 1: Django Backend
```bash
cd backend
python manage.py runserver
```

### Terminal 2: Streamlit Frontend
```bash
streamlit run final2.py
```

## ✅ Integration Checklist

- [ ] Install `requests` package
- [ ] Add DjangoAPI class to final2.py
- [ ] Modify login to use Django API
- [ ] Add session sync after level completion
- [ ] Test with both servers running
- [ ] Verify data is saved in Django admin

## 🎯 Complete Integration Example

See `SETUP_INSTRUCTIONS.md` for full API documentation and PowerShell test examples.

---

**Status:** Backend ready, integration optional
**Current:** Standalone Streamlit works perfectly
**Future:** Full Django integration for multi-user persistence
