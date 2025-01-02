import json
from typing import Any, Dict, List
################################# Clean Data ################################
def clean_data(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Cleans and normalizes business data from a response dict.

    Expects:
    - response['status'] == 'OK'
    - response['data'] as a list of business objects
    """
    if response.get("status") != "OK" or "data" not in response:
        return []

    cleaned_data = []

    for business in response["data"]:
        # Skip if the business does not have required fields

        cleaned_record = {
            "business_id": business.get("business_id"),
            "google_id": business.get("google_id"),
            "place_id": business.get("place_id"),
            "google_mid": business.get("google_mid"),
            "phone_number": business.get("phone_number"),
            "name": business.get("name"),
            "latitude": business.get("latitude"),
            "longitude": business.get("longitude"),
            "full_address": business.get("full_address") or business.get("address"),
            "review_count": business.get("review_count"),
            "rating": business.get("rating"),
            "timezone": business.get("timezone"),
            "opening_status": business.get("opening_status"),
            "website": business.get("website"),
            "verified": business.get("verified"),
            "place_link": business.get("place_link"),
            "cid": business.get("cid"),
            "reviews_link": business.get("reviews_link"),
            "owner_id": business.get("owner_id"),
            "owner_link": business.get("owner_link"),
            "owner_name": business.get("owner_name"),
            "booking_link": business.get("booking_link"),
            "reservations_link": business.get("reservations_link"),
            "business_status": business.get("business_status"),
            "type": business.get("type"),
            # Convert list to a comma-separated string
            "subtypes": ",".join(business.get("subtypes", [])) if business.get("subtypes") else None,
            "address": business.get("address"),
            "order_link": business.get("order_link"),
            "price_level": business.get("price_level"),
            "district": business.get("district"),
            "street_address": business.get("street_address"),
            "city": business.get("city"),
            "zipcode": business.get("zipcode"),
            "state": business.get("state"),
            "country": business.get("country"),
            # Serialize nested fields to JSON
            "working_hours": business.get("working_hours") if business.get("working_hours") else None,
            "about": business.get("about") if business.get("about") else None
            # Store the composite text for later usage
    
        }

        cleaned_data.append(cleaned_record)

    return cleaned_data