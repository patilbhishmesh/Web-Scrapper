import requests
from bs4 import BeautifulSoup
import csv

# List of target government URLs (add more as needed)
TARGET_URLS = [
    "https://www.india.gov.in/", # Main portal
    "https://www.mygov.in/schemes/", # Schemes page
    # Add more government scheme URLs here
]

OUTPUT_CSV = "government_schemes.csv"

def fetch_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return None

def parse_schemes(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    schemes = []
    # Look for typical scheme sections by anchor or headline
    # (For demo purposes, scrape all anchor tags containing 'scheme' in text)
    for a in soup.find_all('a'):
        if a.text and "scheme" in a.text.lower():
            schemes.append({
                "title": a.text.strip(),
                "link": a.get('href') if a.get('href') else "",
                "source": base_url
            })
    # Can be expanded for custom logic per site
    return schemes

def main():
    all_schemes = []
    for url in TARGET_URLS:
        print(f"Fetching: {url}")
        html = fetch_page(url)
        if html:
            schemes = parse_schemes(html, url)
            print(f"Found {len(schemes)} scheme(s) on {url}")
            all_schemes.extend(schemes)

    # Save results to CSV
    keys = ["title", "link", "source"]
    with open(OUTPUT_CSV, "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        for row in all_schemes:
            writer.writerow(row)
    print(f"Scraping complete. Results saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()