import requests
from .email_utils import scrape_emails_from_html,jina_get_page_content,extract_emails_from_markdown,get_all_website_links
import streamlit as st

def get_emails(url, timeout=10):
    print(f"Fetching emails from {url}")
    try:
        # First attempt: Regular web scraping
        emails = scrape_emails_from_html(url, timeout)
        if emails:
            return emails

        # # Second attempt: Use Jina AI to get page content
        # print("No emails found. Attempting to use Jina AI.")
        # jina_content = jina_get_page_content(url)
        # if jina_content:
        #     return extract_emails_from_markdown(jina_content)

        print("No valid emails found")
        return set()

    except requests.RequestException as e:
        print(f"Error fetching {url}: {str(e)}")
        return set()
    

def filter_likely_email_pages(urls):
    priority_keywords = ['contact', 'about', 'team']
    
    # Filter URLs based on keywords
    filtered_urls = [url for url in urls if any(keyword in url.lower() for keyword in priority_keywords)]
    
    # Sort URLs by length (shorter URLs first)
    sorted_urls = sorted(filtered_urls, key=lambda url: len(url))
    # print(f"Filtered and sorted URLs: {sorted_urls}")  # Debugging statement
    print("***************************")  # Debugging statement
    # print(sorted_urls[:3])  # Debugging statement
    return sorted_urls[:3]

def process_businesses_email(businesses):
    # Initialize progress bar
    progress_bar = st.progress(0)
    
    total_businesses = len(businesses)
    
    for index, business in enumerate(businesses):
        website = business.get("website")
        if website:
            emails = get_emails(website)
            if emails:
                business["emails"] = list(emails)
            else:
                internal_url = get_all_website_links(website)
                filtered_links = filter_likely_email_pages(internal_url)
                for link in filtered_links:
                    emails = get_emails(link)
                    if emails:
                        # print(f"Found email address(es) for {business['name']}: {emails}")
                        business["emails"] = list(emails)
                        break
                
                if not business.get("emails"):
                    print(f"No email addresses found for {business['name']}.")
                    business["emails"] = []
        else:
            print(f"No website found for {business['name']}.")
            business["emails"] = []
        
        # Update progress bar
        progress = (index + 1) / total_businesses
        progress_bar.progress(progress)

    return businesses



# print(len(x))
# print("------------------------------------------------")
# # y = get_internal_links("https://avantiway.com/", "https://avantiway.com/")
# # print(len(y))
# # print(y)
# filtered_links = filter_likely_email_pages(x)
# print(filtered_links)

# z = get_emails("https://avantiway.com/")
# print(z)
# all = get_all_website_links("https://360realtytampa.com/team")
# x = filter_likely_email_pages(all)
# print(x)
# for link in x:
# print(get_emails("https://www.calzadoslobo.com/contactenos/"))
