import pandas as pd
import requests
import os

# Folder Structure for raw data
os.makedirs('data/raw', exist_ok=True)

urls = {
    "gdp": "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)_per_capita",
    "life_expectancy": "https://en.wikipedia.org/wiki/List_of_countries_by_life_expectancy",
    "literacy": "https://en.wikipedia.org/wiki/List_of_countries_by_literacy_rate"
}

# Browser Headers to prevent 403 Forbidden Errors
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

def scrape_all_data():
    print("=" * 60)
    print("\n              Data scraping in progress...\n")
    print("=" * 60)

    for key, url in urls.items():
        try:
            print(f"Fetching {key} data...")
            
            # Requesting page content
            response = requests.get(url, headers=headers)
            response.raise_for_status() # Check if the request was successful
            
            # Parse HTML tables
            tables = pd.read_html(response.text)
            
            # Selecting the tables
            if key == "gdp":
                df = tables[1] # IMF/World Bank table
            elif key == "life_expectancy":
                df = tables[3] # World Bank table
            else: # literacy
                df = tables[2] # Adult literacy rates table
            
            # Saving the "Messy" file to the raw data folder
            filename = f"data/raw/data_raw_{key}.csv"
            df.to_csv(filename, index=False)
            print(f"Successfully saved: {key} to {filename}")
            
        except Exception as e:
            print(f"Error scraping {key}: {e}")

    print("=" * 60)
    print("\n                 Data scraping complete\n")
    print("=" * 60)

if __name__ == "__main__":
    scrape_all_data()