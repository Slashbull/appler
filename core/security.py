import streamlit as st
from hashlib import sha256
import time

# Single User Credentials (hashed for security)
CREDENTIALS = {
    "username": "admin",
    "password_hash": sha256("adminpass".encode()).hexdigest()  # Replace 'adminpass' with your desired password
}

# Session Timeout in Seconds
SESSION_TIMEOUT = 600  # 10 minutes

def authenticate_user(username, password):
    """
    Validate username and password.
    """
    password_hash = sha256(password.encode()).hexdigest()
    if username == CREDENTIALS["username"] and password_hash == CREDENTIALS["password_hash"]:
        return True
    return False

def initialize_session():
    """
    Initialize the session state.
    """
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.start_time = None

def login():
    """
    Display login form and handle authentication.
    """
    st.title("🔒 Login to Importer Dashboard")
    st.info("Enter your credentials to access the dashboard.")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if authenticate_user(username, password):
            st.session_state.authenticated = True
            st.session_state.start_time = time.time()
            st.success("Login successful!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password.")

def check_session():
    """
    Check if the user is logged in and session is active.
    """
    if st.session_state.authenticated:
        if time.time() - st.session_state.start_time > SESSION_TIMEOUT:
            st.warning("Session expired. Please log in again.")
            st.session_state.authenticated = False
            st.experimental_rerun()
    else:
        st.experimental_rerun()

def logout():
    """
    Log out the user and clear the session.
    """
    st.session_state.authenticated = False
    st.session_state.start_time = None
    st.success("You have been logged out.")
    st.experimental_rerun()
