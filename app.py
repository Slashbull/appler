import streamlit as st
from core.security import initialize_session, login, check_session, logout

def main():
    # Initialize session
    initialize_session()

    # Handle authentication
    if not st.session_state.authenticated:
        login()
        return

    # Check session validity
    check_session()

    # Main Dashboard Content
    st.sidebar.title("Importer Dashboard")
    st.sidebar.button("Logout", on_click=logout)
    st.title("Welcome to the Importer Dashboard!")
    st.write("🔍 Explore your import data and gain insights.")

if __name__ == "__main__":
    main()
