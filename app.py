from login import check_password
import streamlit as st
from st_discord_nav import st_discord_nav
from page_components.GmapExtractor import g_map_extractor
from page_components.Dashboard import dashboard
from page_components.Logout import logout
st.set_page_config(page_title="Leads", page_icon="🔍", layout="centered", initial_sidebar_state="collapsed")

def main():
   
    # Main Streamlit app starts here
    st.markdown(f"""
    <style>
    [data-testid="stSidebar"] {{
        min-width: 120px !important;
        max-width: 120px !important;
    }}
    </style>
""", unsafe_allow_html=True)
# Define your pages and their icons
    pages = [
        {"name": "Look Up", "icon": "FaSearch"},  # FaSearch can represent a lookup or search functionality
        {"name": "Upload", "icon": "FaUpload"},  # FaUpload is perfect for an upload page
        {"name": "Dashboard", "icon": "FaTachometerAlt"},  # FaTachometerAlt is commonly used for dashboards
        {"name": "Agents", "icon": "FaUserSecret"},  # FaUserSecret can represent agents or user roles
        {"name": "Logout", "icon": "FaSignOutAlt"},  # FaSignOutAlt is a good match for logout functionality
    ]
    with st.sidebar:
        page = st_discord_nav(pages=pages,font_size=28,icon_size=48)
    
    if page == "Look Up":
        g_map_extractor()
    elif page == "Upload":
        st.title("Upload")
        st.write("coming soon...")
    elif page == "Dashboard":
        dashboard()
    elif page == "Agents":
        st.title("Agents")
        st.write("coming soon...")
    elif page == "Logout":
        logout()
        
       
if __name__ == "__main__":
    #Check password before running the app
    if not check_password():
        st.stop()
    main()
