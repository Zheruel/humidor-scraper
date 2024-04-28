import math
import requests
from bs4 import BeautifulSoup, ResultSet


def get_number_of_pages(soup: BeautifulSoup) -> int:
    p = soup.find("p", class_="woocommerce-result-count")
    total_results = int(p.text.split(' ')[-2])
    results_per_page = 36
    return math.ceil(total_results / results_per_page)


def extract_info_from_products(products: ResultSet):
    with open("products.txt", "a") as file:
        for product in products:
            title = product.find("h2", class_="woocommerce-loop-product__title").text
            inventory = product.find("p", class_="inventar").find("span").text

            if inventory.lower() != "unavailable":
                file.write(f"{title}\n")


base_url = "https://humidor.hr/en/product-category/cigars/page/"

response = requests.get(base_url + "1/")
soup = BeautifulSoup(response.text, "html.parser")

num_pages = get_number_of_pages(soup)

for page in range(1, num_pages + 1):
    response = requests.get(base_url + str(page) + "/")
    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.find_all("li", class_="product")
    extract_info_from_products(products)