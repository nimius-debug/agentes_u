import streamlit as st
import pandas as pd
from utils.constants import REGIONS, LANGUAGES
from apis.fetchGMapData import fetch_business_data
from apis.dataToTable import data_frame_table
from apis.emailScrawler import process_businesses_email
from db.mangodb_utils import save_run_to_collection, fetch_user_data, fetch_existing_runs
from dotenv import load_dotenv
load_dotenv()

@st.dialog("Extracting Google Business", width="small")
def dialog(payload):
    # Display the input data
    with st.spinner("Searching..."):
        response = fetch_business_data(payload)
        length = len(response)
        if length == 0:
            st.info("No businesses found. Please try again with different search queries.")
        else:
            st.success(f"Found {length} businesses")
            # Update session state
            st.session_state['business_data'] = response

    st.header("Do you want to extract emails from the businesses?")
    st.info("Email extraction can take a couple of minutes as it is crawling the web for data. If enabled, please be patient.")
    emailon = st.button("Extract Email", key="extract_email")
    if emailon:
        # Add emails to the businesses
        with st.spinner("Extracting emails..."):
            st.session_state['business_data'] = process_businesses_email(st.session_state['business_data'])
            st.write(st.session_state['business_data'])
            st.success("Email extraction completed.")
            # Trigger a rerun to update the table
            st.rerun()
            
def g_map_extractor():
    colm = st.columns([4, 1], gap="large")
    with colm[0]:
        st.header("_:blue[B2B] Leads Extractor_", divider="gray", anchor=False)
    with colm[1]:
        st.image("https://ik.imagekit.io/indesign/gmap/unnamed.png?updatedAt=1724268033278", width=100)
      
    with st.form(key='search_form'):
        # Queries input
        st.markdown("##### Search Parameters")
        queries = st.text_area("Queries (separate each query with a comma)", help="Enter the search queries, separated by commas.", placeholder="e.g., Restaurants in newyork , Hotels in Madrid, etc.")
        queries_list = [q.strip() for q in queries.split(',')] if queries else []
        
        # Region select box
        region = st.selectbox("Region", options=list(REGIONS.keys()), help="Select the region.")
        selected_region_code = REGIONS[region] if region else None

        # Submit button
        submit_button = st.form_submit_button(label='Search')

    # Handling form submission
    if submit_button:
        if queries_list:
            user_id = st.session_state.get('user_id')
            
            # Check if the query has already been run for this user
            existing_runs = fetch_existing_runs(user_id, queries_list)
            if existing_runs:
                st.warning("This queries have already been performed. See details in Dashboard.")
                for run in existing_runs:
                    st.write(f"**Query:** {run['query']}")
                    data_df = pd.DataFrame(run['data'])
                    st.dataframe(data_df)
            else:
                # Prepare payload for fetching business data
                payload = {
                    "queries": queries_list,
                    "limit": 1000,
                    "zoom": 13,
                    "dedup": True
                }
                # Conditionally include region if selected
                if selected_region_code:
                    payload["region"] = selected_region_code

                dialog(payload)  # Call the dialog function to handle form submission      
        else:
            st.error("The 'Queries' field cannot be empty. Please enter at least one query.")
            
    # Display the table if business data is available in session state
    if 'business_data' in st.session_state and st.session_state['business_data']:
        # Render the table outside the dialog function
        business_table = data_frame_table(st.session_state['business_data'])
        st.dataframe(business_table)
        
        # Add a button to save data to MongoDB under a specific category
        if st.button('Save Data to MongoDB'):
            show_save_dialog(queries_list, st.session_state['business_data'])
            
            
            
@st.dialog("Save Data to MongoDB", width="small")
def show_save_dialog(queries_list, business_data):
    print("show_save_dialog")
    # Fetch existing collections for the user
    existing_collections = fetch_user_data(st.session_state['user_id'])
    
    collection_option = st.radio(
        "Do you want to create a new collection or save to an existing one?",
        ('Create New Collection', 'Use Existing Collection')
    )

    if collection_option == 'Create New Collection':
        new_collection_name = st.text_input("Enter the name for the new collection:")
        if st.button('Save to New Collection'):
            if new_collection_name:
                if 'user_id' in st.session_state:
                    # Call the function to save the run and check for duplicates
                    save_run_to_collection(st.session_state['user_id'], new_collection_name, ", ".join(queries_list), business_data)
                else:
                    st.error("User not authenticated.")
            else:
                st.error("Please enter a name for the new collection.")
    else:
        selected_collection = st.selectbox("Select an existing collection:", options=[col['collection_name'] for col in existing_collections])
        if st.button('Save to Existing Collection'):
            if selected_collection:
                # Call the function to save the run and check for duplicates
                save_run_to_collection(st.session_state['user_id'], selected_collection, ", ".join(queries_list), business_data)
            else:
                st.error("Please select an existing collection.")

g_map_extractor()