from typing import Dict, Any, List
from apis.fetchGMapData import fetch_business_data
from rich import print as rprint
from db.tursodb_utils import clean_data

payload = {
        "queries": ["restaurants in tampa", "hotels in tampa"],
        "region": "us",
        "language": "en",
        "limit": 1,
        "zoom": 13,
        "dedup": True
    }

# Fetch and clean data
business_data = fetch_business_data(payload)
rprint(business_data)
cleandata = clean_data(business_data)
rprint(cleandata)
