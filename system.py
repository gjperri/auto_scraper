"""
Python web scraper for classic car listings. Uses
BeautifulSoup4, Requests, and Pandas package for data
gathering.

ML models uses to predict car prices given previous data.
"""

# Imports =================================================
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import pandas as pd

# Scraping Logic ==========================================

url = "https://www.classic.com/"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url)

# Load content from site
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "body"))
    )
    print("Page loaded successfully!")
except Exception as e:
    print(f"Error loading page: {e}")
    driver.quit()

# Use BS to parse
html_content = driver.page_source
soup = bs(html_content, "html.parser")

# Extract listings
data = []
seen_titles = set()

listings = soup.find_all("div")
filtered_listings = [
    listing for listing in listings
    if "debug:bg-red-100" in listing.get("class", "")
]

# Go through and find car attributes
for listing in filtered_listings:

    # Locate the <h3> tag
    h3_tag = listing.find("h3")
    if h3_tag:
        # Locate the <a> tag inside the <h3> tag
        a_tag = h3_tag.find("a")
        title = a_tag.text.strip() if a_tag else "N/A"
    else:
        title = "N/A"
    
    print(f"Extracted title: {title}")  # Debug

    # Append data only if the title is unique
    if title != "N/A" and title not in seen_titles:
        seen_titles.add(title)
        data.append({"Title": title})

# Close the driver
driver.quit()

# Save data to a CSV file
df = pd.DataFrame(data)
df.to_csv("classic_cars.csv", index=False)
print("Data saved to classic_cars.csv")