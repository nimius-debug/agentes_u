# main_app.py (or wherever you define your pages/navigation)
import streamlit as st
from Account.login import check_password

st.set_page_config(page_title="Leads", page_icon="🔍", layout="wide")

# Make sure your session state has a default
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    # Only proceed if user successfully logs in
    if not check_password():
        st.stop()

def logout():
    st.session_state.logged_in = False
    # If you want to clear user_id too
    st.session_state.pop("user_id", None)
    st.rerun()

# Construct pages
login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

dashboard = st.Page(
    "Collections/dashboard.py", title="Dashboard", icon=":material/dashboard:", default=True
)

search = st.Page("Tools/gmapExtractor.py", title="G Map", icon=":material/search:")
email = st.Page("Tools/sendEmails.py", title="Send Email", icon=":material/email:")

# Show navigation
if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Account": [logout_page],
            "Dashboard": [dashboard],
            "Tools": [search, email],
        }
    )
else:
    pg = st.navigation([login_page])

#debugging
#st.write(st.session_state)  # for debugging
pg.run()
