"""
Authentication module for Focus Companion beta access
This module provides shared authentication logic for all pages
"""

import streamlit as st
import json
import os
from pathlib import Path

# Load allowed emails from file
@st.cache_data
def load_whitelist():
    """Load the list of allowed email addresses"""
    try:
        with open("data/allowed_emails.txt", "r") as f:
            return [line.strip().lower() for line in f.readlines()]
    except FileNotFoundError:
        # If no whitelist file exists, return empty list (no access)
        return []

def save_user_session(email: str, remember_me: bool = False):
    """Save user session data"""
    session_data = {
        "email": email,
        "remember_me": remember_me,
        "timestamp": st.session_state.get("session_timestamp", None)
    }
    
    # Save to session state
    st.session_state.user_email = email
    st.session_state.remember_me = remember_me
    
    # If remember me is enabled, save to file
    if remember_me:
        try:
            with open("data/user_session.json", "w") as f:
                json.dump(session_data, f)
        except Exception:
            pass  # Silently fail if we can't save

def load_user_session():
    """Load user session data from file"""
    try:
        if os.path.exists("data/user_session.json"):
            with open("data/user_session.json", "r") as f:
                session_data = json.load(f)
                
            # Check if remember me was enabled
            if session_data.get("remember_me", False):
                return session_data.get("email")
    except Exception:
        pass  # Silently fail if we can't load
    
    return None

def check_beta_access():
    """
    Check if the current user has beta access.
    Returns True if authorized, False otherwise.
    """
    allowed_emails = load_whitelist()
    
    # Check if user is logged in via session state
    if "user_email" in st.session_state and st.session_state.user_email is not None:
        return st.session_state.user_email.lower() in allowed_emails
    
    # Check if user has saved session
    saved_email = load_user_session()
    if saved_email and saved_email.lower() in allowed_emails:
        st.session_state.user_email = saved_email
        return True
    
    return False

def require_beta_access():
    """
    Require beta access for the current page.
    If user is not authorized, show login form and stop execution.
    """
    if not check_beta_access():
        # Clear any existing content
        st.empty()
        
        # Show login form
        st.title("🔐 Beta Access Required")
        st.write("This page requires beta access. Please enter your email:")
        
        # Pre-fill with saved email if available
        saved_email = load_user_session()
        email_input = st.text_input("Email", value=saved_email or "", key="beta_email_input")
        
        # Remember me checkbox
        remember_me = st.checkbox("Remember my email", value=bool(saved_email), key="remember_me_checkbox")
        
        if st.button("Continue", key="beta_continue_btn"):
            allowed_emails = load_whitelist()
            if email_input.strip().lower() in allowed_emails:
                # Save user session
                save_user_session(email_input.strip().lower(), remember_me)
                st.success("✅ Access granted. Welcome!")
                st.rerun()
            else:
                st.error("❌ Sorry, this email is not on the beta access list.")
        
        # Show helpful message
        st.info("💡 If you believe you should have access, please contact the administrator.")
        
        # Stop execution
        st.stop()

def get_user_email():
    """Get the current user's email if authorized"""
    if check_beta_access():
        return st.session_state.user_email
    return None

def logout():
    """Log out the current user"""
    # Clear session state
    if "user_email" in st.session_state:
        del st.session_state.user_email
    if "remember_me" in st.session_state:
        del st.session_state.remember_me
    
    # Clear saved session file
    try:
        if os.path.exists("data/user_session.json"):
            os.remove("data/user_session.json")
    except Exception:
        pass  # Silently fail if we can't remove the file
    
    st.rerun() 