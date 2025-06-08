from app.utils.slug_mapper import slugify_olx
from fastapi import APIRouter, Query
from app.scrapers.olx_scraper import scrape_olx

router = APIRouter()

@router.get("/search")
async def olx(
    make: str = Query(...),
    model: str = Query(...),
    city: str = Query(...),
):
    slug_make, slug_model, slug_city = slugify_olx(make, model, city)
    result = await scrape_olx(slug_make, slug_model, slug_city)
    return result

