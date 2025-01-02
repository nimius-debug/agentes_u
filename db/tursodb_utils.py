import json
from typing import Any, Dict , Optional , List

################################ Data Validation ################################
def validate_business_data(data: Dict[str, Any]) -> bool:
    required_fields = ["business_id", "google_id", "place_id"]
    return all(data.get(field) for field in required_fields)


################################ Data Preparation ################################
def prepare_composite_text(data: Dict[str, Any]) -> str:
    # Extract and clean the `about` section
    about_text = ""
    about = data.get("about", {})
    if isinstance(about, dict):
        summary = about.get("summary", "")
        details = about.get("details", {})

        # Extract details dynamically
        details_parts = []
        for category, subitems in details.items():
            subitem_text = ", ".join([subkey for subkey, value in subitems.items() if value])
            if subitem_text:
                details_parts.append(f"{category}: {subitem_text}")
        details_text = "; ".join(details_parts)

        # Combine summary and structured details
        about_text = f"Summary: {summary}. Details: {details_text}".strip()

    # Handle subtypes correctly as a list
    subtypes = data.get("subtypes", [])
    subtypes_text = ", ".join(subtypes) if isinstance(subtypes, list) else ""

    # Organize fields for embedding-friendly structure
    composite_parts = [
        f"Business Name: {data.get('name', '')}",
        f"Type: {data.get('type', '')}",
        f"Subtypes: {subtypes_text}",
        f"Address: {data.get('address', '')}, {data.get('city', '')}, {data.get('state', '')}, {data.get('country', '')}, {data.get('zipcode', '')}",
        about_text,
        f"Review Count: {data.get('review_count', 0)}",
        f"Rating: {data.get('rating', 0.0)}",
        f"Opening Status: {data.get('opening_status', '')}",
        f"Verified: {data.get('verified', False)}",
        f"Website: {data.get('website', '')}",
    ]

    # Remove empty components and join with a delimiter
    composite_text = " | ".join(filter(None, composite_parts))
    return composite_text



################################ Embedding ################################
from openai import OpenAI
from dotenv import load_dotenv
import os
import numpy as np
load_dotenv()

def get_embedding(text: str, model="text-embedding-3-small") -> List[float]:
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding


def embedding_to_bytes(embedding: List[float]) -> bytes:
    array = np.array(embedding, dtype=np.float32)
    return array.tobytes()

# Set your OpenAI API key
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
def generate_embedding(text: str) -> Optional[bytes]:
    if text.strip():
        embedding = get_embedding(text)
        return embedding_to_bytes(embedding)
    return None

################################# Clean Data ################################
def clean_data(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    cleaned_data = []
    if response.get("status") == "OK" and "data" in response:
        for business in response["data"]:
            if validate_business_data(business):
                embeding_str = prepare_composite_text(business)
                embeding_bytes = generate_embedding(embeding_str)
                cleaned_data.append({
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
                    # Serialize dict to JSON string
                    "working_hours": json.dumps(business.get("working_hours")) if business.get("working_hours") else None,
                    "about": json.dumps(business.get("about")) if business.get("about") else None,
                    # Exclude unused fields like photos_sample
                    "composite_embedding": embeding_bytes,  # Placeholder for embedding to be generated later
                })
    return cleaned_data