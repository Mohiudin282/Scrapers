from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import pakwheels
from app.api import olx
from app.api import aggregated
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pakwheels.router, prefix="/scrape/pakwheels", tags=["PakWheels"])
app.include_router(olx.router, prefix="/scrape/olx", tags=["Olx"])
app.include_router(aggregated.router, prefix="/scrape/all", tags=["All Sites"])

@app.get("/")
async def root():
    return {"message": "How you Doin"}