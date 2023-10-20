import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


def scrape_product_details(url):
    headers = {
        "User-Agent": "customer"  
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    product_name = soup.find("span", {"id": "productTitle"}).get_text(strip=True)
    product_price = soup.find("span", {"id": "priceblock_ourprice"}).get_text(strip=True)
    rating = soup.find("span", {"class": "a-icon-alt"}).get_text(strip=True)
    num_reviews = soup.find("span", {"id": "acrCustomerReviewText"}).get_text(strip=True)
    product_description = soup.find("div", {"id": "productDescription"}).get_text(strip=True)
    asin = soup.find("div", {"data-asin": True})["data-asin"]
    manufacturer = soup.find("a", {"id": "bylineInfo"}).get_text(strip=True)

    return {
        "Product URL": url,
        "Product Name": product_name,
        "Product Price": product_price,
        "Rating": rating,
        "Number of Reviews": num_reviews,
        "Description": product_description,
        "ASIN": asin,
        "Manufacturer": manufacturer
    }


def scrape_search_page(url, max_pages, max_products_per_page):
    all_products = []

    for page_num in range(1, max_pages + 1):
        page_url = f"{url}&page={page_num}"
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, "html.parser")

        product_links = soup.find_all("a", {"class": "s-no-outline"})
        product_links = product_links[:10] 

        for link in product_links:
            product_url = "https://www.amazon.in" + link.get("href")
            product_data = scrape_product_details(product_url)
            all_products.append(product_data)

   
        time.sleep(2)

    return all_products


search_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
max_pages = 20
max_products_per_page = 10


scraped_data = scrape_search_page(search_url, max_pages, max_products_per_page)


df = pd.DataFrame(scraped_data)
df.to_csv("amazon_products.csv", index=False)
