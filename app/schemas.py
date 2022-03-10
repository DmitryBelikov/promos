from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str
    category_id: int


class ProductCreate(ProductBase):
    class Config:
        orm_mode = True


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True


class Category(BaseModel):
    id: int
    name: str
    products: list[Product] = []

    class Config:
        orm_mode = True
