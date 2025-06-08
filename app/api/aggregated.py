from fastapi import APIRouter, Query
from app.utils.slug_mapper import slugify_pakwheels, slugify_olx
from app.scrapers.pakwheels_scraper import scrape_pakwheels
from app.scrapers.olx_scraper import scrape_olx
import asyncio

router = APIRouter()

@router.get("/search")
async def search_all(
    make: str = Query(...),
    model: str = Query(...),
    city: str = Query(...),
):
    # Convert user-friendly names into slugs for each platform
    slug_pw = slugify_pakwheels(make, model, city)
    slug_olx = slugify_olx(make, model, city)

    # Run both scraping functions concurrently
    pw_task = asyncio.create_task(scrape_pakwheels(*slug_pw))
    olx_task = asyncio.create_task(scrape_olx(*slug_olx))

    # Wait for both tasks to complete
    pw_result, olx_result = await asyncio.gather(pw_task, olx_task)

    return {
        "pakwheels": pw_result,
        "olx": olx_result
    }
