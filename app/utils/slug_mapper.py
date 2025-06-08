make_model_map = {
    "toyota": {
        "land cruiser": "land-cruiser",
        "corolla": "corolla",
        "yaris": "yaris",
        "fortuner": "fortuner"
    },
    "honda": {
        "civic": "civic",
        "city": "city",
        "accord": "accord"
    },
    "suzuki": {
        "alto": "alto",
        "cultus": "cultus",
        "wagon r": "wagon-r"
    },
    "hyundai": {
        "elantra": "elantra",
        "tucson": "tucson",
        "sonata": "sonata"
    }
}

olx_city_codes = {
    "lahore": "lahore_g4060673",
    "karachi": "karachi_g4060695",
    "islamabad": "islamabad_g4060615",
}

def slugify_pakwheels(make: str, model: str, city: str):
    make = make.strip().lower()
    model = model.strip().lower()
    city = city.strip().lower()

    slug_model = make_model_map.get(make, {}).get(model, model.replace(" ", "-"))
    slug_make = make
    slug_city = city.replace(" ", "-")

    return slug_make, slug_model, slug_city


def slugify_olx(make: str, model: str, city: str):
    make = make.strip().lower()
    model = model.strip().lower()
    city = city.strip().lower()

    slug_make = make
    slug_model = make_model_map.get(make, {}).get(model, model.replace(" ", "-"))
    slug_city = olx_city_codes.get(city)

    return slug_make, slug_model, slug_city
