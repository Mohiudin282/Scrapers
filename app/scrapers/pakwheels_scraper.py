import requests
from bs4 import BeautifulSoup, Tag
import json
import httpx

async def scrape_pakwheels(make: str, model: str, city: str):
    url = f"https://www.pakwheels.com/used-cars/search/-/mk_{make}/md_{model}/ct_{city}/"
    headers = {"User-Agent": "Mozilla/5.0"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")

    results = []

    # Get all <ul> elements with the correct classes
    ul_tags = soup.find_all("ul", class_="list-unstyled search-results search-results-mid next-prev car-search-results")

    for ul in ul_tags:
        if not isinstance(ul, Tag):
            continue  # Skip if it's not an actual HTML tag

        li_tags = ul.find_all("li")

        for li in li_tags:
            if not isinstance(li, Tag):
                continue

            h3_tag = li.find("h3")
            title = h3_tag.get_text(strip=True) if h3_tag else None

            # Extract updated time from <div class="pull-left dated">
            updated_div = li.find("div", class_="pull-left dated")
            updated_time = updated_div.get_text(strip=True) if updated_div else None

            script_tag = li.find("script", type="application/ld+json")
            if script_tag:
                try:
                    data = json.loads(script_tag.get_text())

                    car_data = {
                        "name": data.get("name"),
                        "description": data.get("description"),
                        "brand": data.get("brand", {}).get("name"),
                        "manufacturer": data.get("manufacturer"),
                        "model_year": data.get("modelDate"),
                        "fuel_type": data.get("fuelType"),
                        "transmission": data.get("vehicleTransmission"),
                        "engine_displacement": data.get("vehicleEngine", {}).get("engineDisplacement"),
                        "mileage": data.get("mileageFromOdometer"),
                        "price": data.get("offers", {}).get("price"),
                        "price_currency": data.get("offers", {}).get("priceCurrency"),
                        "availability": data.get("offers", {}).get("availability"),
                        "url": data.get("offers", {}).get("url"),
                        "image": data.get("image"),
                        "title": title,
                        "updated_time": updated_time,
                    }
                    #essential_fields = ["price"]
                    if car_data.get("price"):
                        results.append(car_data)

                except json.JSONDecodeError:
                    continue

    return {"results": results if results else "No valid listings parsed"}
