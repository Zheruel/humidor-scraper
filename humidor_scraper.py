import math
import json
import requests
from bs4 import BeautifulSoup, ResultSet


def get_number_of_pages(soup: BeautifulSoup) -> int:
    p = soup.find("p", class_="woocommerce-result-count")
    total_results = int(p.text.split(' ')[-2])
    results_per_page = 36
    return math.ceil(total_results / results_per_page)


def extract_info_from_products(products: ResultSet) -> list:
    product_list = []
    for product in products:
        inventory = product.find("p", class_="inventar").find("span").text.strip()
        if inventory.lower() == "unavailable":
            continue
            
        title = product.find("h2", class_="woocommerce-loop-product__title").text.strip()
        price = product.find("span", class_="woocommerce-Price-amount").text.strip()
        product_url = product.find("a")["href"] if product.find("a") else None
        
        product_data = {
            "title": title,
            "price": price,
            "url": product_url
        }
        product_list.append(product_data)
    
    return product_list


base_url = "https://humidor.hr/en/product-category/cigars/page/"
all_products = []

response = requests.get(base_url + "1/")
soup = BeautifulSoup(response.text, "html.parser")

num_pages = get_number_of_pages(soup)

for page in range(1, num_pages + 1):
    print(f"Scraping page {page} of {num_pages}")
    response = requests.get(base_url + str(page) + "/")
    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.find_all("li", class_="product")
    all_products.extend(extract_info_from_products(products))

with open("products.json", "w", encoding="utf-8") as f:
    json.dump({"products": all_products}, f, indent=2, ensure_ascii=False)