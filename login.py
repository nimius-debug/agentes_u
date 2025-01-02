import hmac
import os
import streamlit as st
from dotenv import load_dotenv
from db.mangodb_utils import get_user_from_db, register_user
from werkzeug.security import check_password_hash
# Load environment variables from .env file
load_dotenv()

def check_password():
    """Returns `True` if the user had a correct password."""
    colms = st.columns([1,2,1])
    def login_form():
        """Form with widgets to collect user information"""
      
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
        
        if user and check_password_hash(user['password_hash'], password):
            st.session_state["password_correct"] = True
            # st.session_state["current_user"] = username
            st.session_state["user_id"] = str(user['_id'])  # Store the user's ID in session state
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
            st.toast("##### Welcome to Leads Extractor", icon="🔍")
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        
            if st.session_state["password_correct"]:
                return True
            else:
                with colms[1]:
                    st.error("😕 User not known or password incorrect")
        
    return False

# xz = register_user("user", "user")
# print(xz)