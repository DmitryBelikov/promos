from typing import Optional

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import schemas, models, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_app():
    db = next(get_db())
    categories = [
        'cars',
        'clothes',
        'health',
        'food'
    ]

    for idx, category_name in enumerate(categories):
        category = schemas.Category(id=idx + 1, name=category_name)
        crud.create_category(db, category)


app = FastAPI()
init_app()


@app.post("/products", response_model=schemas.Product)
def create_product(create_product_query: schemas.ProductCreate,
                   db: Session = Depends(get_db)):
    """
    Creates new product
    """
    product = crud.create_product(db, create_product_query)
    return product


@app.get("/products", response_model=list[schemas.Product])
def get_products(query: Optional[str] = None,
                 db: Session = Depends(get_db)):
    if query is None:
        return crud.get_all_products(db)


@app.get("/products/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if product is None:
        raise HTTPException(
            status_code=404,
            detail=f"Product with id {product_id} doesn't exist"
        )
    return product


@app.put("/products/{product_id}", response_model=schemas.Product)
def edit_product(product_id: int, product: schemas.Product,
                 db: Session = Depends(get_db)):
    pass


@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    result = crud.delete_product(db, product_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Product with id {product_id} doesn't exist"
        )
