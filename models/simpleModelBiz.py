from typing import Optional
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import Text, BLOB

class Business(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    business_id: Optional[str] = Field(default=None)
    google_id: Optional[str] = Field(default=None)
    place_id: Optional[str] = Field(default=None)
    phone_number: Optional[str] = None
    name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    full_address: Optional[str] = None
    review_count: Optional[int] = None
    rating: Optional[float] = None
    timezone: Optional[str] = None
    opening_status: Optional[str] = None
    website: Optional[str] = None
    verified: Optional[bool] = None
    place_link: Optional[str] = None
    cid: Optional[str] = None
    reviews_link: Optional[str] = None
    owner_id: Optional[str] = None
    owner_link: Optional[str] = None
    owner_name: Optional[str] = None
    booking_link: Optional[str] = None
    reservations_link: Optional[str] = None
    business_status: Optional[str] = None
    type: Optional[str] = None
    subtypes: Optional[str] = Field(default=None, sa_column=Column(Text))  # Stored as JSON string
    address: Optional[str] = None
    order_link: Optional[str] = None
    price_level: Optional[str] = None  
    district: Optional[str] = None
    street_address: Optional[str] = None
    city: Optional[str] = None
    zipcode: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    working_hours: Optional[str] = Field(default=None, sa_column=Column(Text))  # Stored as JSON string
    about: Optional[str] = Field(default=None, sa_column=Column(Text))  # Stored as JSON string
    composite_embedding: Optional[bytes] = Field(
        default=None, sa_column=Column(BLOB, nullable=True)
    )