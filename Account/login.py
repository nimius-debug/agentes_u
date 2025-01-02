# login.py
import streamlit as st
from dotenv import load_dotenv
from db.mangodb_utils import get_user_from_db
from werkzeug.security import check_password_hash

load_dotenv()

def check_password():
    """Return True if the user provided valid credentials, else show a form."""
    # If already logged in, skip the form
    if st.session_state.get("logged_in", False):
        return True

    # Build columns
    colms = st.columns([1, 2, 1])

    def login_form():
        with colms[1]:
            with st.form("Credentials"):
                st.text_input("Username", key="username")
                st.text_input("Password", type="password", key="password")
                st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        username = st.session_state["username"]
        password = st.session_state["password"]

        # Fetch user data from MongoDB
        user = get_user_from_db(username)

        # Validate the provided credentials
        if user and check_password_hash(user['password_hash'], password):
            st.session_state["logged_in"] = True
            st.session_state["user_id"] = str(user['_id'])
            st.toast("##### Welcome to Leads Extractor", icon="🔍")
        else:
            st.session_state["logged_in"] = False
            # Show error right here or handle it after the form

        # Clean up sensitive data
        del st.session_state["username"]
        del st.session_state["password"]

    # Show the login form if not logged in
    login_form()

    # After the form submission, check if we're now logged in
    if st.session_state.get("logged_in", False):
        return True
    else:
        # Optionally show an error if not logged in
        with colms[1]:
            if "username" not in st.session_state:  # means user just submitted form
                st.error("😕 User not known or password incorrect")

        return False
