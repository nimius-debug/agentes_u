from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import urllib.parse
from ai_utils import get_response

def _gmap(search_query):
  driver = Driver()
  url = f'https://www.google.com/maps/search/{urllib.parse.quote_plus(search_query)}'
  # Navigate to Google
  driver.open(url)
  
  

if __name__ == "__main__":
  role = "You are an assistant that converts a user's search intent into a Google Maps search query."
  prompt = "I want to extract leads in Barcelona in the shoes store industry."
  search_query = get_response(role, prompt)
  _gmap(search_query)
  # scraper = GoogleScraper()
  # scraper.run_scraper("restaurants in Tampa, FL")