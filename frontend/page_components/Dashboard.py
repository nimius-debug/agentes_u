import streamlit as st
from db.db_utils import fetch_user_data
import pandas as pd
from collections import defaultdict

def dashboard():
    st.header("_:violet[Dash]board_", divider="gray", anchor=False)
    # Fetch all collections from MongoDB for the logged-in user
    if 'user_id' in st.session_state:
        user_data = fetch_user_data(st.session_state['user_id'])

        if user_data:
            # Group runs by collection name
            collections = defaultdict(list)
            for run in user_data:
                collections[run['collection_name']].append(run)

            # Display each collection with its runs under a single expander
            for collection_name, runs in collections.items():
                with st.expander(f"Collection: {collection_name}", expanded=False):
                    for run in runs:
                        display_run(run)
        else:
            st.info("No collections found.")
    else:
        st.error("Please log in to view your collections.")

def display_run(run):
    """Display details for a single run."""
    run_id = str(run['_id'])
    st.write(f"**Query:** {run['query']}")
    st.write(f"**Date:** {run['date']}")
    if st.button(f"View Details for Query: {run['query']}", key=run_id):
        # Set the selected run in session state and display details
        st.session_state['selected_run'] = run
        show_run_details(run)

@st.dialog("Run Details", width="large")
def show_run_details(run):
    st.write(f"**Query:** {run['query']}")
    st.write(f"**Date:** {run['date']}")
    st.write("### Data")

    # Convert the 'data' field into a DataFrame and display it
    if 'data' in run and isinstance(run['data'], list):
        data_df = pd.DataFrame(run['data'])
        st.dataframe(data_df)
    else:
        st.write("No data available for this run.")