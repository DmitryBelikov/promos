from sqlalchemy.orm import Session

from . import models, schemas


def get_all_products(db: Session):
    return db.query(models.Product).all()


def get_product(db: Session, product_id: int):
    return \
        db.query(models.Product).\
        filter(models.Product.id == product_id).\
        first()


def delete_product(db: Session, product_id: int):
    product = get_product(db, product_id)
    if product is not None:
        db.delete(product)
        db.commit()
        return True
    return False


def create_product(db: Session, create_product_query: schemas.ProductCreate):
    product = models.Product(**create_product_query.dict())
    db.add(product)
    db.commit()
    return product


def update_product(db: Session, product: schemas.Product):
    deleted = delete_product(db, product.id)
    if deleted:
        create_request = schemas.ProductCreate.from_orm(product)
        return create_product(db, create_request)
    return None


def create_category(db: Session, category: schemas.Category):
    db.add(models.Category(**category.dict()))
    db.commit()
