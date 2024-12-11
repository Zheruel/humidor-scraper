import json
import asyncio
from playwright.async_api import async_playwright


async def scrape_products():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        base_url = "https://havana-cigar-shop.com/cigare"
        params = {
            "page_size": 99999,
            "sort": 2,
            "page_number": 1,
            "f": 1,
            "is_saleable": 1,
        }
        
        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        url = f"{base_url}?{query_string}"
        
        print("Loading page...")
        await page.goto(url)
        
        print("Waiting for products to load...")
        try:
            await page.wait_for_selector("a.product-display-grid", timeout=10000)
            print("Products found")
        except Exception as e:
            print(f"Error waiting for products: {str(e)}")
        
        await page.wait_for_timeout(5000)

        products = await page.evaluate("""
            () => {
                const products = [];
                document.querySelectorAll('a.product-display-grid').forEach(product => {
                    try {
                        const title = product.getAttribute('title');
                        const url = product.getAttribute('href');
                        const priceElem = product.querySelector('.price');
                        
                        if (title && url && priceElem) {
                            products.push({
                                title: title,
                                price: priceElem.textContent.trim(),
                                url: new URL(url, window.location.origin).href,
                                description: ''
                            });
                        }
                    } catch (e) {
                        console.error('Error processing product:', e);
                    }
                });
                return products;
            }
        """)
        
        print(f"Found {len(products)} products")
        
        await browser.close()
        return products


async def main():
    print("Starting scraper...")
    products = await scrape_products()
    
    print(f"Extracted {len(products)} products")
    
    with open("havana_products.json", "w", encoding="utf-8") as f:
        json.dump({"products": products}, f, indent=2, ensure_ascii=False)
    
    print("Data saved to havana_products.json")


asyncio.run(main()) 
