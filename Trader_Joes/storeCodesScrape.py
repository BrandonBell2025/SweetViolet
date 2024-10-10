from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import csv

# Mapping of state names to their abbreviations
state_mapping = {
    "Alabama": "al",
    "Arkansas": "ar",
    "Arizona": "az",
    "California": "ca",
    "Colorado": "co",
    "Connecticut": "ct",
    "District Of Columbia": "dc",
    "Delaware": "de",
    "Florida": "fl",
    "Georgia": "ga",
    "Iowa": "ia",
    "Idaho": "id",
    "Illinois": "il",
    "Indiana": "in",
    "Kansas": "ks",
    "Kentucky": "ky",
    "Louisiana": "la",
    "Massachusetts": "ma",
    "Maryland": "md",
    "Maine": "me",
    "Michigan": "mi",
    "Minnesota": "mn",
    "Missouri": "mo",
    "North Carolina": "nc",
    "Nebraska": "ne",
    "New Hampshire": "nh",
    "New Jersey": "nj",
    "New Mexico": "nm",
    "Nevada": "nv",
    "New York": "ny",
    "Ohio": "oh",
    "Oklahoma": "ok",
    "Oregon": "or",
    "Pennsylvania": "pa",
    "Rhode Island": "ri",
    "South Carolina": "sc",
    "Tennessee": "tn",
    "Texas": "tx",
    "Utah": "ut",
    "Virginia": "va",
    "Vermont": "vt",
    "Washington": "wa",
    "Wisconsin": "wi"
}

# Setup WebDriver
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Start maximized
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    return driver

# Main function
def main():
    driver = setup_driver()
    
    store_numbers_set = set()  # Use a set to store unique store numbers

    try:
        for state_name, state_abbreviation in state_mapping.items():
            url = f'https://locations.traderjoes.com/{state_abbreviation}/'
            print(f'Navigating to: {url}')
            driver.get(url)

            # Wait for the page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'itemListWrapper'))
            )

            # Locate the div containing the links
            item_list_wrapper = driver.find_element(By.CLASS_NAME, 'itemListWrapper')
            links = item_list_wrapper.find_elements(By.CSS_SELECTOR, 'a.ga_w2gi_lp.listitem')

            store_urls = [link.get_attribute('href') for link in links]
            print(f'Found {len(store_urls)} store links.')

            for store_url in store_urls:
                print(f'Navigating to store: {store_url}')
                driver.get(store_url)

                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'ga_w2gi_lp'))
                )

                spans = driver.find_elements(By.CLASS_NAME, 'ga_w2gi_lp')
                for span in spans:
                    print(f'Extracting text: "{span.text}"')  # Debug print for extracted text
                    match = re.search(r'\((\d+)\)', span.text)  # Updated pattern to look for number in parentheses
                    if match:
                        store_number = match.group(1)
                        store_numbers_set.add(store_number)  # Add store number to the set
                        print(f'Extracted store number: {store_number}')  # Debug print for extracted store number

                driver.back()
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'itemListWrapper'))
                )

    except Exception as e:
        print(f'An error occurred: {e}')
    
    finally:
        # Write all unique store numbers to a CSV file
        with open('store_numbers.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Store Number'])  # Write header
            for number in store_numbers_set:  # Write each unique store number
                writer.writerow([number])  
        
        print(f'Extracted {len(store_numbers_set)} unique store numbers. Data saved to store_numbers.csv.')

        # Cleanup
        driver.quit()

# Entry point
if __name__ == '__main__':
    main()
