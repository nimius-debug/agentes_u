import re
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from urllib.parse import urlparse, urljoin

# Load environment variables from .env file
load_dotenv()

def hex_at(string, index, mode):
    if (mode == 0):
        r = string[index:2]
    else:
        r = string[index-2:index]
    return int(r, 16)

def decrypt(ciphertext):
    output = ""
    i = 2
    key = hex_at(ciphertext, 0, 0)
    while i < len(ciphertext):
        i += 2
        plaintext = hex_at(ciphertext, i, 1) ^ key
        output += chr(plaintext)
    return output;

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

# Define a function to check if an email is valid
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Define a function to clean an email address
def clean_email(email):
    email = re.sub(r'[^a-zA-Z0-9._%+-@]+$', '', email)
    email = re.sub(r'^[^a-zA-Z0-9._%+-@]+', '', email)
    return email

# Define a function to scrape emails from an HTML page
def scrape_emails_from_html(url, timeout):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers ,timeout=timeout)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    # First, try to find an email in mailto links
    for a in soup.find_all('a', href=True):
        href = a['href']
        print(href)
        if href.startswith('mailto:'):
            email = href.replace('mailto:', '').split('?')[0].strip().lower()
            if is_valid_email(email):
                print(f"Found valid email in mailto link: {email}")
                return {email}

    #  Handle Cloudflare-protected emails
    for span in soup.find_all('span', class_='__cf_email__'):
        encoded_email = span.get('data-cfemail')
        if encoded_email:
            decrypted_email = decrypt(encoded_email)
            if is_valid_email(decrypted_email):
                print(f"Found encrypted email: {decrypted_email}")
                return {decrypted_email}
                
    # If no email found in mailto links, search in text content
    text_content = soup.get_text()
    emails = re.findall(email_pattern, text_content, re.IGNORECASE)
    
    for email in emails:
        clean_email = email.strip().lower()
        if is_valid_email(clean_email):
            print(f"Found valid email in text content: {clean_email}")
            return {clean_email}
    
    return set()
  

def jina_get_page_content(url):
    jina_url = f"https://r.jina.ai/{url}"
    headers = {
        "Authorization": f"Bearer {os.environ.get('JINA_API_KEY')}",
        "X-Target-Selector": "a[href^=mailto]"
    }
    try:
        response = requests.get(jina_url, headers=headers)
        response.raise_for_status()
       
        return response.text
    except requests.RequestException as e:
        print(f"An error occurred while fetching {url} using Jina AI: {e}")
        return None

def extract_emails_from_markdown(markdown_content):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, markdown_content, re.IGNORECASE)
    
    valid_emails = set()
    for email in emails:
        clean_email = email.strip().lower()
        if is_valid_email(clean_email):
            print(f"Found valid email in Jina AI content: {clean_email}")
            valid_emails.add(clean_email)
    
    return valid_emails

def get_all_website_links(url):
    """
    Returns all internal URLs found on `url` that belong to the same website.
    """
    urls = set()
    domain_name = urlparse(url).netloc
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        
        for a_tag in soup.findAll("a"):
            href = a_tag.attrs.get("href")
            if href == "" or href is None:
                continue
            
            # Join the URL if it's relative (not absolute link)
            href = urljoin(url, href)
            
            parsed_href = urlparse(href)
            href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
            
            if not is_valid(href):
                continue
            if domain_name not in href:
                # External link, ignore
                continue
            if href in urls:
                # Already added, skip
                continue
            
            # Internal link
            urls.add(href)
            
    except requests.RequestException as e:
        print(f"An error occurred while fetching links from {url}: {e}")
    
    return urls


# print(scrape_emails_from_html("https://www.grandeszapatos.com/contactanos", 10))
# def get_internal_links(url, base_url):
#     try:
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.text, 'html.parser')
#         internal_links = set()
#         for link in soup.find_all('a', href=True):
#             href = link['href']
#             full_url = urllib.parse.urljoin(base_url, href)
#             if full_url.startswith(base_url):
#                 internal_links.add(full_url)
#         return internal_links
#     except requests.RequestException as e:
#         print(f"An error occurred while fetching links from {url}: {e}")
#         return set()