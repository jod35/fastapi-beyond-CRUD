from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field
from typing import Annotated

app = FastAPI()


@app.get("/")
async def main() -> dict:
    return {"message": "Hello World"}


# path params


@app.get("/greet/{name}")
async def greet_name(name: str = Path(max_length=12, min_length=2)) -> dict:
    return {"message": f"Hello {name}"}


@app.get("/products/{product_id}")
async def product_detail(product_id: int = Path(ge=1, le=1_000_000)) -> dict:
    return {"product_id": product_id}


# query params

# www.google.com/search?q=web

names = ["Phil", "JOnathan", "Joel", "Jackie"]


@app.get("/names")
async def list_names(name: str = Query(default="", max_length=12)) -> dict:
    res = {"names": [n for n in names if n == name]} if name else {"names": names}

    return res


# product filters query param group


class ProductFilters(BaseModel):
    name: str = Field(default="", max_length=12)
    max_price: int = Field(default=1_000_000, le=1_000_000)
    min_price: int = Field(default=1, ge=1)
    category: str = Field(default="")


@app.get("/products")
async def product_list(product_filters: Annotated[ProductFilters, Query()]) -> dict:
    return {
        "filters": {
            "name": product_filters.name,
            "max_price": product_filters.max_price,
            "min_price": product_filters.min_price,
            "category": product_filters.category,
        }
    }
