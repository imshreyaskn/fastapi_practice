# pyrefly: ignore [missing-import]
from traitlets import default
from asyncio import proactor_events
from fastapi import FastAPI, HTTPException
from .schemas import ProductCreate

app = FastAPI()



products_db = {
    1 : {
        "id":1,
        "name":"Keyboard",
        "price":99.99,
        "stock":10
    },
    2 : {
        "id":2,
        "name":"Mouse",
        "price":9.99,
        "stock":20
    },
    3 : {
        "id":3,
        "name":"CPU",
        "price":999.99,
        "stock":1
    }
}


@app.get("/api/v1/health")
def health_check():
    return {
        "status":"ok"
    }


@app.get("/api/v1/products/{product_id}")
def get_product_by_id(product_id : int):
    if product_id not in products_db:
        raise HTTPException(status_code=404,detail="Product not found")
    return products_db[product_id]

@app.get("/api/v1/products")
def get_all_products(limit : int = 10, search : str | None = None):
    all_products = list(products_db.values())
    if search:
        
        all_products = [
            item for item in all_products
            if search.lower() in item["name"].lower()
        ]

        return all_products[:limit]

    return list(products_db.values())[:limit]


@app.post("/api/v1/products",status_code=201)
def create_product(RequestBody : ProductCreate):

    id = max(products_db.keys(),default= 0) +1 
    products_db[id] = RequestBody.model_dump()
    return products_db[id]