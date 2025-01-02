# # Main Streamlit app starts here
#     st.html(f"""
#         <style>
#         [data-testid="stSidebar"] {{
#             min-width: 120px !important;
#             max-width: 120px !important;
#         }}
#         </style>
#     """)



# # Define your pages and their icons
#     pages = [
#         # {"name": "Look Up", "icon": "FaSearch"},  # FaSearch can represent a lookup or search functionality
#         # {"name": "Upload", "icon": "FaUpload"},  # FaUpload is perfect for an upload page
#         {"name": "Dashboard", "icon": "FaTachometerAlt"},  # FaTachometerAlt is commonly used for dashboards
#         {"name": "Agents", "icon": "FaUserSecret"},  # FaUserSecret can represent agents or user roles
#         {"name": "Logout", "icon": "FaSignOutAlt"},  # FaSignOutAlt is a good match for logout functionality
#     ]
#     with st.sidebar:
#         page = st_discord_nav(pages=pages,font_size=28,icon_size=48)
    
#     if page == "Dashboard":
#         dashboard()
#     elif page == "Agents":
#         st.title("Agents")
#         st.write("coming soon...")
#     elif page == "Logout":
#         logout()