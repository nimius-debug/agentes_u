
import streamlit as st

@st.dialog("Log out", width="small")
def logout():
    # Display the input data
    st.info("Are you sure you want to log out?")
    log_out = st.button("Log Out", key="log_out")
    if log_out:
      st.session_state["password_correct"] = False
      
     