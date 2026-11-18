from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Product

app = FastAPI()


class ProductCreate(BaseModel):
    title: str
    price: float
    category: str


class ProductOut(BaseModel):
    id: int
    title: str
    price: float
    category: str

    model_config = {"from_attributes": True}


class ProductUpdate(BaseModel):
    title: str | None = None
    price: float | None = None
    category: str | None = None


products = [
    {"id": 1, "title": "Essence Mascara", "price": 9.99, "category": "beauty"},
    {"id": 2, "title": "Red Lipstick", "price": 12.99, "category": "beauty"},
    {"id": 3, "title": "Wooden Chair", "price": 89.99, "category": "furniture"},
]


@app.get("/")
def read_root():
    return ("Hello,welcome to Shoplite!")


@app.get("/products", response_model=list[ProductOut])
def read_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@app.get("/products/{product_id}")
def read_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")


@app.post("/products", status_code=201, response_model=ProductOut)
def create_product(new_product: ProductCreate, db: Session = Depends(get_db)):
    product = Product(**new_product.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            products.remove(product)
            return
    raise HTTPException(status_code=404, detail="Product not found")


@app.put("/products/{product_id}")
def replace_product(product_id: int, updated: ProductCreate):
    for product in products:
        if product["id"] == product_id:
            product.update(updated.model_dump())
            return product
    raise HTTPException(status_code=404, detail="Product not found")


@app.patch("/products/{product_id}")
def update_product(product_id: int, changes: ProductUpdate):
    for product in products:
        if product["id"] == product_id:
            product.update(changes.model_dump(exclude_unset=True))
            return product
    raise HTTPException(status_code=404, detail="Product not found")
