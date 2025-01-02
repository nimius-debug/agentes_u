import streamlit as st
import pandas as pd
from typing import Dict, Any 

@st.cache_data
def data_frame_table(business_data: Dict[str, Any]) -> pd.DataFrame:
    """Convert a list of business info into a DataFrame with each business as a row."""
    
    # Prepare a list of dictionaries, each representing a row in the table
    table_data = []
    
    for business in business_data:
        # Safeguard to ensure 'working_hours' is a dictionary
        working_hours = business.get('working_hours', {})
        if isinstance(working_hours, dict):
            business_info = {
                'Name': business['name'],
                'Phone Number': business['phone_number'],
                'Email': ', '.join(business.get('emails', ['N/A'])),
                'Address': business['address'],
                'Rating': business['rating'],
                'Review Count': business['review_count'],
                'Website': business['website'],
                'Working Hours (Monday)': ', '.join(working_hours.get('Monday', ['N/A'])),
                'Working Hours (Tuesday)': ', '.join(working_hours.get('Tuesday', ['N/A'])),
                'Working Hours (Wednesday)': ', '.join(working_hours.get('Wednesday', ['N/A'])),
                'Working Hours (Thursday)': ', '.join(working_hours.get('Thursday', ['N/A'])),
                'Working Hours (Friday)': ', '.join(working_hours.get('Friday', ['N/A'])),
                'Working Hours (Saturday)': ', '.join(working_hours.get('Saturday', ['N/A'])),
                'Working Hours (Sunday)': ', '.join(working_hours.get('Sunday', ['N/A'])),
            }
        else:
            # If 'working_hours' is not a dictionary, handle accordingly
            business_info = {
                'Name': business['name'],
                'Phone Number': business['phone_number'],
                'Email': ', '.join(business.get('emails', ['N/A'])),  # Adding the Email field
                'Address': business['address'],
                'Rating': business['rating'],
                'Review Count': business['review_count'],
                'Website': business['website'],
                'Working Hours (Monday)': 'N/A',
                'Working Hours (Tuesday)': 'N/A',
                'Working Hours (Wednesday)': 'N/A',
                'Working Hours (Thursday)': 'N/A',
                'Working Hours (Friday)': 'N/A',
                'Working Hours (Saturday)': 'N/A',
                'Working Hours (Sunday)': 'N/A',
            }
        
        table_data.append(business_info)
    
    # Convert the list of dictionaries into a DataFrame
    combined_df = pd.DataFrame(table_data)
    
    return combined_df

# # Your data
# data = {
#     "name": "Metro City Realty",
#     "phone_number": "+14072373331",
#     "address": "Metro City Realty, 520 E Church St #101, Orlando, FL 32801",
#     "rating": 4.9,
#     "review_count": 193,
#     "website": "https://www.mymetrocity.com",
#     "working_hours": {
#         "Friday": ["9 AM–5 PM"],
#         "Saturday": ["Closed"],
#         "Sunday": ["Closed"],
#         "Monday": ["9 AM–5 PM"],
#         "Tuesday": ["9 AM–5 PM"],
#         "Wednesday": ["9 AM–5 PM"],
#         "Thursday": ["9 AM–5 PM"]
#     }
# }

# # Create and display the business information
# create_and_display_business_info(data)
