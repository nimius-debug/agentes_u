import requests
import re
import urllib.parse
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import streamlit as st

def is_valid_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def clean_email(email: str) -> str:
    email = re.sub(r'[^a-zA-Z0-9._%+-@]+$', '', email)
    email = re.sub(r'^[^a-zA-Z0-9._%+-@]+', '', email)
    return email

def get_emails(content: str) -> set:
    if not content:
        return set()
    
    email_candidates = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)
    valid_emails = set()
    
    for email in email_candidates:
        cleaned_email = clean_email(email)
        if is_valid_email(cleaned_email):
            valid_emails.add(cleaned_email)
    
    return valid_emails

def normalize_url(url: str) -> str:
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    url = url.replace('http://', 'https://')
    return url

def get_internal_links(url: str, base_url: str) -> set:
    print(f"Fetching links from {url}")
    try:
        response = requests.get(url, timeout=10,verify=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        internal_links = set()
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urllib.parse.urljoin(base_url, href)
            if full_url.startswith(base_url):
                internal_links.add(normalize_url(full_url))
        print(internal_links)
        return internal_links
      
    except requests.RequestException as e:
        print(f"An error occurred while fetching links from {url}: {e}")
        return set()

def get_page_content(url: str) -> str:
    JINA_API_KEY = "jina_4a8bb933c005416eb0b18f732d1d94e5hKUlDRPY6UBo0ljoQB3H6A3W1JbH"
    jina_url = f"https://r.jina.ai/{url}"
    headers = {
        "Authorization": f"Bearer {JINA_API_KEY}"
    }
    try:
        response = requests.get(jina_url, headers=headers)
        print(response)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"An error occurred while fetching {url} using Jina AI: {e}")
        return None


def check_contact_pages(base_url):
    contact_paths = ['contact', 'contacto', 'contact-us',]
    for path in contact_paths:
        url = urllib.parse.urljoin(base_url, path)
        print(f"Checking potential contact page: {url}")
        emails = get_emails(url)
        if emails:
            return emails
    return []

def crawl_website(start_url: str, max_pages: int = 10) -> str:
    start_url = normalize_url(start_url)
    visited = set()
    to_visit = [start_url]
    page_count = 0

    while to_visit and page_count < max_pages:
        url = to_visit.pop(0)
        print(f"Crawling: {url}")
        if url not in visited:
            visited.add(url)
            page_count += 1

            content = get_page_content(url)
            if content:
                emails = get_emails(content)
                if emails:
                    return next(iter(emails))  # Return the first email found

            internal_links = get_internal_links(url, start_url)
            prioritized_links = prioritize_pages(internal_links)
            for link in prioritized_links:
                if link not in visited:
                    to_visit.insert(0, link)  # Add prioritized links to the beginning of the list

    return "No email found"

def add_email_to_businesses(businesses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    for business in businesses:
        website = business.get("website")
        if website:
            website = normalize_url(website)
            email = crawl_website(website)
            business["email"] = email
        else:
            business["email"] = "No email found"
    
    return businesses

# Example usage
if __name__ == "__main__":
    businesses = [
        {
            "name": "The Kendall Bonner Team, Best Tampa Real Estate Agents",
            "phone_number": "+18135827332",
            "address": "The Kendall Bonner Team, Best Tampa Real Estate Agents, 2124 W Kennedy Blvd suite a, Tampa, FL 33606",
            "rating": 5,
            "review_count": 630,
            "website": "https://www.leeautotampa.com",
            "working_hours": {
                "Friday": ["8 AM–6 PM"],
                "Saturday": ["Closed"],
                "Sunday": ["Closed"],
                "Monday": ["8 AM–6 PM"],
                "Tuesday": ["8 AM–6 PM"],
                "Wednesday": ["8 AM–6 PM"],
                "Thursday": ["8 AM–6 PM"]
            }
        },
        # Add more businesses as needed
    ]

    updated_businesses = add_email_to_businesses(businesses)
    
    # Print the updated businesses with emails
    for business in updated_businesses:
        print(business)