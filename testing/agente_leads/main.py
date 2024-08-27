from botasaurus.browser import browser, Driver, AsyncQueueResult
from botasaurus.request import request, Request
import json


def extract_title(html):
    try:
        title = json.loads(
            html.split(";window.APP_INITIALIZATION_STATE=")[1].split(";window.APP_FLAGS")[0]
        )[5][3][2][1]
        return title
    except Exception as e:
        print(f"Error extracting title: {e}")
        return None

def extract_phone(html):
    try:
        phone = json.loads(
            html.split(";window.APP_INITIALIZATION_STATE=")[1].split(";window.APP_FLAGS")[0]
        )[5][3][2][12][0][3][0]
        return phone
    except Exception as e:
        print(f"Error extracting phone: {e}")
        return None

def extract_website(html):
    try:
        website = json.loads(
            html.split(";window.APP_INITIALIZATION_STATE=")[1].split(";window.APP_FLAGS")[0]
        )[5][3][2][100][0][5][2]
        return website
    except Exception as e:
        print(f"Error extracting website: {e}")
        return None

def extract_reviews(html):
    try:
        reviews = json.loads(
            html.split(";window.APP_INITIALIZATION_STATE=")[1].split(";window.APP_FLAGS")[0]
        )[5][3][2][14][4]
        return reviews
    except Exception as e:
        print(f"Error extracting reviews: {e}")
        return None

def extract_rating(html):
    try:
        rating = json.loads(
            html.split(";window.APP_INITIALIZATION_STATE=")[1].split(";window.APP_FLAGS")[0]
        )[5][3][2][4][7]
        return rating
    except Exception as e:
        print(f"Error extracting rating: {e}")
        return None
      
@request(
    parallel=5,
    async_queue=True,
    max_retry=5,

)

def scrape_place_info(request, link, metadata):
    
    cookies = metadata["cookies"]
    html = request.get(link, cookies=cookies, timeout=12).text
    
    title = extract_title(html)
    phone = extract_phone(html)
    website = extract_website(html)
    reviews = extract_reviews(html)
    rating = extract_rating(html)
    
    place_data = {
        "title": title,
        "phone": phone,
        "website": website,
        "reviews": reviews,
        "rating": rating,
        "link": link
    }
    
    print("Place Data:", place_data)
    return place_data
  
# def scrape_place_title(request: Request, link, metadata):
#     cookies = metadata["cookies"]
#     html = request.get(link, cookies=cookies, timeout=12).text
#     title = extract_title(html)
#     print("Title:", title)
#     return title

def has_reached_end(driver):
    return driver.select('p.fontBodyMedium > span > span') is not None

def extract_links(driver):
    return driver.get_all_links('[role="feed"] > div > div > a')

@browser(headless=True)
def scrape_google_maps(driver: Driver, link):
    driver.google_get(link, accept_google_cookies=True)  # accepts google cookies popup

    scrape_place_obj: AsyncQueueResult = scrape_place_info()  # initialize the async queue for scraping places
    cookies = driver.get_cookies_dict()  # get the cookies from the driver

    while True:
        links = extract_links(driver)  # get the links to places
        print("Links:", len(links))
        scrape_place_obj.put(links, metadata={"cookies": cookies})  # add the links to the async queue for scraping

        print("scrolling")
        driver.scroll_to_bottom('[role="feed"]')  # scroll to the bottom of the feed

        if has_reached_end(driver):  # we have reached the end, let's break buddy
            print
            break

    results = scrape_place_obj.get()  # get the scraped results from the async queue
    return results

scrape_google_maps("https://www.google.com/maps/search/restaurants+in+New+York")