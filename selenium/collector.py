"""
Selenium collector for job links from Greenhouse careers pages.
Usage: python selenium/collector.py
Outputs to ../data/raw/job_links.csv (appends)
Requires ChromeDriver in PATH or same dir.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import csv
import time
import os

SOURCES = [
    "https://boards.greenhouse.io/uber",
    "https://boards.greenhouse.io/shopify",
    "https://boards.greenhouse.io/doordash"
]

SEARCH_TERM = "software"
FILTER_LOCATION = "Remote"  # or "United States"

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Remove for debug
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    return driver

def collect_links(driver, base_url):
    print(f"Collecting from {base_url}")
    driver.get(base_url)
    wait = WebDriverWait(driver, 20)

    # Search
    search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-qa='search']")))
    search_box.clear()
    search_box.send_keys(SEARCH_TERM)
    search_button = driver.find_element(By.CSS_SELECTOR, "[data-qa='search-button']")
    search_button.click()
    time.sleep(3)

    # Filter location if possible
    try:
        filter_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-qa='location-search']")))
        filter_input.clear()
        filter_input.send_keys(FILTER_LOCATION)
        time.sleep(2)
        first_filter = driver.find_element(By.CSS_SELECTOR, ".css-1odm-1f6o44l")
        first_filter.click()
        time.sleep(3)
    except:
        print("Location filter not found, skipping")

    # Scroll to load all
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Extract URLs
    links = []
    postings = driver.find_elements(By.CSS_SELECTOR, "a[data-qa*='posting']")
    for post in postings:
        url = post.get_attribute('href')
        if url and 'greenhouse.io' in url:
            links.append(url)
    print(f"Found {len(links)} links")
    return links

def save_links(links, filename="../data/raw/job_links.csv"):
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if os.stat(filename).st_size == 0:
            writer.writerow(["job_url"])
        for link in links:
            if link not in open(filename).read():
                writer.writerow([link])

if __name__ == "__main__":
    driver = setup_driver()
    all_links = []
    try:
        for source in SOURCES:
            links = collect_links(driver, source)
            all_links.extend(links)
        save_links(all_links)
        print(f"Saved {len(all_links)} total links")
    finally:
        driver.quit()
