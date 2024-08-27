import requests
from bs4 import BeautifulSoup
import re
import urllib.parse

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def clean_email(email):
    email = re.sub(r'[^a-zA-Z0-9._%+-@]+$', '', email)
    email = re.sub(r'^[^a-zA-Z0-9._%+-@]+', '', email)
    return email
  
def get_emails(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        valid_emails = set()
        for email in emails:
          cleaned_email = clean_email(email)
          if is_valid_email(cleaned_email):
            valid_emails.add(cleaned_email)
        return valid_emails
      
    except requests.RequestException as e:
        print(f"An error occurred while fetching {url}: {e}")
        return []

def check_contact_pages(base_url):
    contact_paths = ['contact', 'contacto', 'contact-us',]
    for path in contact_paths:
        url = urllib.parse.urljoin(base_url, path)
        print(f"Checking potential contact page: {url}")
        emails = get_emails(url)
        if emails:
            return emails
    return []

def get_internal_links(url, base_url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        internal_links = set()
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urllib.parse.urljoin(base_url, href)
            if full_url.startswith(base_url):
                internal_links.add(full_url)
        return internal_links
    except requests.RequestException as e:
        print(f"An error occurred while fetching links from {url}: {e}")
        return set()

def crawl_website(start_url, max_pages=10):
    visited = set()
    to_visit = [start_url]
    all_emails = set()
    page_count = 0

    while to_visit and page_count < max_pages:
        url = to_visit.pop(0)
        if url not in visited:
            print(f"Crawling: {url}")
            visited.add(url)
            page_count += 1

            emails = get_emails(url)
            if emails:
                all_emails.update(emails)
                break  # Stop crawling if we find emails

            internal_links = get_internal_links(url, start_url)
            for link in internal_links:
                if link not in visited:
                    to_visit.append(link)

    return all_emails

def main(url):
    print(f"Searching for email addresses on {url}")
    
    # First, check specific contact page URLs
    base_url = urllib.parse.urlparse(url).scheme + "://" + urllib.parse.urlparse(url).netloc
    emails = check_contact_pages(base_url)
    
    if emails:
        print("Found email address(es) on a contact page:")
        for email in set(emails):
            print(email)
    else:
        print("No emails found on specific contact pages. Crawling the website...")
        emails = crawl_website(url)
        
        if emails:
            print("\nFound email address(es) while crawling:")
            for email in set(emails):
                print(email)
        else:
            print("No email addresses found.")

if __name__ == "__main__":
    website_url = input("Enter the website URL: ")
    main(website_url)