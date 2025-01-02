import requests
import os
from dotenv import load_dotenv
from db.tursodb_utils import clean_data
import json
from typing import List, Dict, Any
import streamlit as st
from rich import print as rprint
# Load environment variables from .env file
load_dotenv()

# @st.cache_data(show_spinner=False)
def fetch_business_data(payload: Dict) -> Dict[str, Any]:
    """
    Fetch business data from Google Maps or a similar service based on provided search queries.

    Parameters:
    - queries: List of search queries (e.g., ['plumbers in texas', 'hotels near san francisco']).
    - region: The region where the search will take place (e.g., 'us' for the United States).
    - language: The language for the search (e.g., 'en' for English).
    - limit: The maximum number of results to fetch. Default is 1000.
    - zoom: The zoom level for the search. Default is 13.
    - dedup: Whether to deduplicate the results. Default is True.

    Returns:
    - A dictionary containing the fetched business data.
    """

    url = "https://local-business-data.p.rapidapi.com/search"
    headers = {
        "x-rapidapi-key": os.environ.get("RAPID_API_KEY"),
        "x-rapidapi-host": "local-business-data.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



