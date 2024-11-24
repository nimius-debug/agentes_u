from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from typing import Any, Dict, List
from datetime import datetime
import streamlit as st
import os
from werkzeug.security import generate_password_hash

# Initialize MongoDB Client
@st.cache_resource
def get_mongo_client():
    mongo_uri = os.getenv('MONGODB_URI')  # Your MongoDB connection string
    print(mongo_uri)
    # Create a new client and connect to the server
    client = MongoClient(mongo_uri, server_api=ServerApi('1'))
    return client


#################################USER AUTHENTICATION####################################
# Fetch user data from MongoDB based on username
@st.cache_data
def get_user_from_db(username):
    """Fetch user data from MongoDB based on username."""
    client = get_mongo_client()
    db = client['users']  # Replace with your database name
    users_collection = db['users_info']  # Replace with your users collection name
    user = users_collection.find_one({"username": username})
    return user

# Register a new user by storing their username and hashed password in MongoDB
@st.cache_data
def register_user(username, password):
    """Register a new user by storing their username and hashed password in MongoDB."""
    client = get_mongo_client()
    db = client['users']  # Replace with your database name
    users_collection = db['users_info']  # Replace with your users collection name
    
    # Check if user already exists
    if get_user_from_db(username):
        st.warning("Username already exists. Please choose another one.")
        return False

    # Hash the password
    password_hash = generate_password_hash(password)
    
    # Insert new user into the database
    users_collection.insert_one({
        "username": username,
        "password_hash": password_hash
    })
    
    st.success("User registered successfully!")
    return True
########################################################################################

####################################collection and data#################################
# Save the run data to MongoDB
def save_run_to_collection(user_id, collection_name: str, query: str, data: List[Dict[str, Any]]):
    client = get_mongo_client()
    db = client['google_data']  # Use your database name
    collection = db['user_google_data']  # Single collection for all user data

    # Check if the run already exists
    existing_run = collection.find_one({
        'user_id': user_id,
        'collection_name': collection_name,
        'query': query
    })

    if existing_run:
        st.warning("Data with the same query already saved. No need to save again.")
        return

    # If not, save the new run
    run = {
        'user_id': user_id,  # Associate the run with the user ID
        'collection_name': collection_name,  # Optionally store the collection name
        'query': query,
        'date': datetime.utcnow(),
        'data': data
    }

    # Save the run to the 'user_google_data' collection
    collection.insert_one(run)
    
    st.success(f"Data saved successfully! Go to the dashboard to view the data.")

@st.cache_data
def fetch_user_data(user_id):
    client = get_mongo_client()
    db = client['google_data']  # Use your database name
    collection = db['user_google_data']  # Single collection for all user data
    
    # Retrieve all documents that match the user's ID
    user_data = list(collection.find({"user_id": user_id}))
    return user_data

@st.cache_data
def fetch_existing_runs(user_id, queries_list):
    """Check if any of the queries have already been run for the user in MongoDB."""
    client = get_mongo_client()
    db = client['google_data']  # Replace with your database name
    collection = db['user_google_data']  # Replace with your user data collection name
    
    existing_runs = []
    for query in queries_list:
        run = collection.find_one({
            'user_id': user_id,
            'query': query
        })
        if run:
            existing_runs.append(run)
    
    return existing_runs
# Retrieve all collections from MongoDB
# def get_collections_from_mongo():
#     client = get_mongo_client()
#     db = client['googlebuzdata']  # Replace with your database name
#     existing_collections = db.list_collection_names()
#     # Retrieve all categories and their runs
#     return existing_collections

########################################################################################
# Send a ping to confirm a successful connection
# try:
#     client = get_mongo_client()
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)