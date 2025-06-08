from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import asyncio

#open chrome headless means without opening window
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("window-size=3840,2160")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")

#driver = webdriver.Chrome(options=options)


def blocking_scrape_olx (make: str, model: str, city: str):
    driver = webdriver.Chrome(options=options)
    url = f"https://www.olx.com.pk/{city}/cars_c84/q-{make}-{model}"
    driver.get(url)
    for _ in range(3):
        driver.execute_script("window.scrollBy(0, 2000);")
        time.sleep(0.1)
    #content 
    soup = BeautifulSoup(driver.page_source, "lxml")
    driver.quit()

    results = []
    # html parsing
    ul_tags = soup.find_all("ul", class_="_1aad128c ec65250d")
    for ul in ul_tags:
        li_tags = ul.find_all("li")
        for li in li_tags:
            article = li.find("article", class_="_63a946ba")
            if article:
                #title
                title_tag = article.find("h2", class_="_562a2db2")
                title = title_tag.text.strip() if title_tag else "N/A"
                #year
                for span in article.find_all("span"):
                    if span.text.strip().isdigit() and len(span.text.strip()) == 4:
                        model_year = span.text.strip()
                        break
                #link
                a_tag = article.find("a")
                base_url = "https://www.olx.com.pk"
                ad_link = base_url + a_tag['href'] if a_tag else "N/A"
                #price
                price_tag = article.find("span", class_="ddc1b288")
                ad_price = price_tag.text.strip() if price_tag else "N/A"
                #location
                location = article.find("span", class_="f7d5e47e")
                ad_location = location.text.strip() if location else "N/A"
                #posted ago
                posted_span = article.find("span", class_="c72cec28 undefined")
                post_date = posted_span.text.strip() if posted_span else "N/A"
                #image
                img_tag = article.find("img", class_="_8e6d5d2b _914cbe21")
                img_url = img_tag['src'] if img_tag else "N/A"
                #milage
                milage_span = article.find("span" , attrs={"aria-label": "Mileage"})
                mileage=milage_span.text

                car_data = {
                    "model_year": model_year,
                    "title": title,
                    "url": ad_link,
                    "price": ad_price,
                    "location": ad_location,
                    "updated_time": post_date,
                    "image": img_url,
                    "mileage": mileage
                }

                results.append(car_data)

    return {"results": results if results else "No valid listings parsed"}


async def scrape_olx(make: str, model: str, city: str):
    return await asyncio.to_thread(blocking_scrape_olx, make, model, city)

               


                    