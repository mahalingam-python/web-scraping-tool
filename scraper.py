import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# Target Website
url = "https://quotes.toscrape.com"

try:
    print("Connecting to website...")
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    quotes = soup.find_all("div", class_="quote")

    data = []

    for quote in quotes:
        text = quote.find("span", class_="text").get_text(strip=True)
        author = quote.find("small", class_="author").get_text(strip=True)

        tags = []
        for tag in quote.find_all("a", class_="tag"):
            tags.append(tag.get_text(strip=True))

        data.append({
            "Quote": text,
            "Author": author,
            "Tags": ", ".join(tags)
        })

    filename = f"quotes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["Quote", "Author", "Tags"]
        )

        writer.writeheader()
        writer.writerows(data)

    print("=" * 50)
    print("Web Scraping Completed Successfully")
    print(f"Total Quotes Collected : {len(data)}")
    print(f"Output File            : {filename}")
    print("=" * 50)

except requests.exceptions.RequestException as e:
    print("Network Error:", e)

except Exception as e:
    print("Unexpected Error:", e)
