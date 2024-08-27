import urllib.parse
from typing import List, Dict
from botasaurus.browser import browser, Driver, AsyncQueueResult
from botasaurus.request import request, Request

def extract_place_data(driver: Driver) -> Dict:
    # Extract title
    title_selector = 'h1'
    title = driver.get_text(title_selector)
    
    # Extract rating
    rating_selector = "span[aria-label*='stars']"
    rating = driver.get_text(rating_selector)
    
    # Extract reviews count
    reviews_selector = "button[jsaction='pane.rating.moreReviews']"
    reviews_text = driver.get_text(reviews_selector)
    reviews = int(''.join(filter(str.isdigit, reviews_text))) if reviews_text else None
    
    # Extract website link
    website_selector = "a[aria-label='Website']"
    website = driver.get_text(website_selector)
    
    # Extract phone number
    phone_selector = "button[jsaction='pane.phone.call']"
    phone = driver.get_text(phone_selector)

    return {
        "title": title,
        "phone": phone,
        "website": website,
        "reviews": reviews,
        "rating": rating,
        "link": driver.get_current_url(),
    }

@browser(
    block_images=True,
    reuse_driver=True,
)
def scrape_place(driver: Driver, link: str) -> Dict:
    driver.get(link)
    
    # Accept Cookies for European users
    if driver.is_in_page("https://consent.google.com/"):
        agree_button_selector = 'form:nth-child(2) > div > div > button'
        driver.click(agree_button_selector)
        driver.get(link)

    return extract_place_data(driver)

@browser(
    block_images=True,
)
def scrape_places_links(driver: Driver, query: str) -> List[str]:
    def visit_google_maps():
        url = f'https://www.google.com/maps/search/{urllib.parse.quote_plus(query)}'
        driver.get(url)
        if driver.is_in_page("https://consent.google.com/"):
            driver.click('form:nth-child(2) > div > div > button')
            driver.get(url)

    def scroll_to_end_of_places_list():
        while not driver.exists("p.fontBodyMedium > span > span"):
            driver.scroll('[role="feed"]')
            print('Scrolling...')
        print("Successfully scrolled to the end of the places list.")

    visit_google_maps()
    scroll_to_end_of_places_list()
    return driver.get_all_links('[role="feed"] > div > div > a')

def scrape_google_maps(query: str) -> List[Dict]:
    links = scrape_places_links(data=[query])
    results = []
    for link in links:
        results.append(scrape_place(data=[link]))
    return results

# Example usage
results = scrape_google_maps("restaurants in New York")
print("Results:", results)
