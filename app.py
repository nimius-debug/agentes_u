from login import check_password
import streamlit as st
# from st_discord_nav import st_discord_nav
from page_components.GmapExtractor import g_map_extractor
from page_components.Dashboard import dashboard
from page_components.Logout import logout

st.set_page_config(page_title="Leads", page_icon="🔍", layout="wide", initial_sidebar_state="collapsed")

def main():
   
    g_map_extractor()      

if __name__ == "__main__":
    #Check password before running the app
    if not check_password():
        st.stop()
    main()
