from typing import List, Optional, Dict
from sqlalchemy import Column, JSON ,BLOB
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class WorkingHours(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    business_id: Optional[int] = Field(default=None, foreign_key="business.id")
    day: str
    hours: List[str] = Field(default_factory=list, sa_column=Column(JSON))  # Stored as JSON

    business: Optional["Business"] = Relationship(back_populates="working_hours")

class PhotoSample(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    business_id: Optional[int] = Field(default=None, foreign_key="business.id")
    photo_id: str
    photo_url: str
    photo_url_large: str
    video_thumbnail_url: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    type: str
    photo_datetime_utc: Optional[datetime] = None
    photo_timestamp: Optional[int] = None

    business: Optional["Business"] = Relationship(back_populates="photos_sample")

class AboutDetails(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    about_id: Optional[int] = Field(default=None, foreign_key="about.id")
    category: str  # e.g., "Service options"
    attributes: Dict[str, bool] = Field(default_factory=dict, sa_column=Column(JSON))  # Stored as JSON

    about: Optional["About"] = Relationship(back_populates="details")

class About(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    business_id: Optional[int] = Field(default=None, foreign_key="business.id")
    summary: Optional[str] = None

    details: List[AboutDetails] = Relationship(back_populates="about")
    business: Optional["Business"] = Relationship(back_populates="about")

class Business(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    business_id: str
    google_id: str
    place_id: str
    google_mid: Optional[str] = None
    phone_number: Optional[str] = None
    name: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    full_address: str
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
    subtypes: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    reviews_per_rating: Dict[str, int] = Field(default_factory=dict, sa_column=Column(JSON))
    photo_count: Optional[int] = None
    address: Optional[str] = None
    order_link: Optional[str] = None
    price_level: Optional[str] = None
    district: Optional[str] = None
    street_address: Optional[str] = None
    city: Optional[str] = None
    zipcode: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    hotel_location_rating: Optional[float] = None
    hotel_amenities: Dict[str, bool] = Field(default_factory=dict, sa_column=Column(JSON))
    hotel_stars: Optional[int] = None
    hotel_review_summary: Optional[str] = None

    working_hours: List[WorkingHours] = Relationship(back_populates="business")
    photos_sample: List[PhotoSample] = Relationship(back_populates="business")
    about: Optional[About] = Relationship(back_populates="business")

    # Embedding fields
    # Embedding fields
    composite_embedding: Optional[bytes] = Field(
        sa_column=Column(BLOB, nullable=True)
    )

    
    
    
    



