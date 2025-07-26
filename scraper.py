# scraper.py

from playwright.sync_api import sync_playwright
import time

def scrape_flipkart(search_url):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(search_url)
        time.sleep(3)

        while True:
            page.wait_for_selector("._1AtVbE")

            items = page.query_selector_all("._1AtVbE")
            for item in items:
                title = item.query_selector("._4rR01T") or item.query_selector(".IRpwTa")
                price = item.query_selector("._30jeq3")
                link = item.query_selector("a")
                image = item.query_selector("img")

                if title and price and link and image:
                    results.append({
                        "title": title.inner_text().strip(),
                        "price": price.inner_text().strip(),
                        "link": "https://www.flipkart.com" + link.get_attribute("href"),
                        "image": image.get_attribute("src")
                    })

            # Pagination
            next_btn = page.query_selector("a._1LKTO3 span:has-text('Next')")
            if next_btn:
                try:
                    page.click("a._1LKTO3 span:has-text('Next')")
                    time.sleep(2)
                except:
                    break
            else:
                break

        browser.close()

    return results
