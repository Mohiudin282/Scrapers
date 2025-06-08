from fastapi import APIRouter, Query
from app.scrapers.pakwheels_scraper import scrape_pakwheels
from app.utils.slug_mapper import slugify_pakwheels

router = APIRouter()

@router.get("/search")
async def search_pakwheels(
    make: str = Query(...),
    model: str = Query(...),
    city: str = Query(...),
):
    slug_make, slug_model, slug_city = slugify_pakwheels(make, model, city)
    result = await scrape_pakwheels(slug_make, slug_model, slug_city)
    return result
