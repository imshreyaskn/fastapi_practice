

from app.dependencies.pagination_params import pagination_params
from fastapi import APIRouter, HTTPException, Depends
from ..schemas import ProductCreate,ProductResponse,ProductUpdate

router = APIRouter(prefix="/api/v1/products",tags=["products"])

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



@router.get("/{product_id}")
def get_product_by_id(product_id : int) -> ProductResponse:
    if product_id not in products_db:
        raise HTTPException(status_code=404,detail="Product not found")
    return products_db[product_id]

@router.get("/")
def get_all_products(pagination_parmas : dict = Depends(pagination_params), search : str | None = None) -> list[ProductResponse]:
    
    all_products = list(products_db.values())

    limit = pagination_parmas["limit"]
    offset = pagination_parmas["offset"]

    if search:
        all_products = [
            item for item in all_products
            if search.lower() in item["name"].lower()
        ]
        return all_products[offset:offset+limit]

    return all_products[offset:offset+limit]


@router.post("/",status_code=201)
def create_product(RequestBody : ProductCreate) -> ProductResponse:

    id = max(products_db.keys(),default= 0) +1 
    products_db[id] = {"id":id,**RequestBody.model_dump()}
    return products_db[id]


@router.put("/{product_id}")
def replace_product_id(product_id : int , RequestBody : ProductCreate) -> ProductCreate:
    
    if product_id not in products_db:
        raise HTTPException(status_code=404,detail="Product not found")
    products_db[product_id] = {"id":product_id,**RequestBody.model_dump()}
    return products_db[product_id]

@router.patch("/{product_id}")
def update_product_id(product_id : int , RequestBody : ProductUpdate):
    updated_content = RequestBody.model_dump(exclude_unset=True)
    if product_id not in products_db:
        raise HTTPException(status_code=404,detail="Product not found")
    
    for item in updated_content:
        products_db[product_id][item] = updated_content[item]

    return products_db[product_id]

@router.delete("/{product_id}",status_code=204)
def delete_product_id(product_id:int):
    if product_id not in products_db:
        raise HTTPException(status_code=404,detail="Product not found")
    del products_db[product_id]
    return None
