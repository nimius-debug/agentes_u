from login import check_password
import streamlit as st
from utils.constants import REGIONS, LANGUAGES
from apis.fetchGMapData import fetch_business_data
from apis.dataToTable import data_frame_table
from apis.emailScrawler import process_businesses_email

@st.dialog("Form Submitted", width="small")
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

def main():
    # Main Streamlit app starts here
    colm = st.columns([4, 1], gap="large")
    with colm[0]:
        st.header("_:violet[Leads] Extractor_", divider="gray", anchor=False)
    with colm[1]:
        st.image("https://ik.imagekit.io/indesign/gmap/unnamed.png?updatedAt=1724268033278", width=100)
      
    with st.form(key='search_form'):
        # Queries input
        st.markdown("##### Search Parameters")
        queries = st.text_area("Queries (separate each query with a comma)", help="Enter the search queries, separated by commas.")
        queries_list = [q.strip() for q in queries.split(',')] if queries else []
        
        # Region select box
        region = st.selectbox("Region", options=list(REGIONS.keys()), help="Select the region.")
        selected_region_code = REGIONS[region] if region else None

        # Submit button
        submit_button = st.form_submit_button(label='Search')
    
    # Handling form submission
    if submit_button:
        if queries_list:
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
       
if __name__ == "__main__":
    # Check password before running the app
    if not check_password():
        st.stop()
    main()
