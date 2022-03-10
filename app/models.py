from sqlalchemy import Column, ForeignKey, Integer, String, Identity
from sqlalchemy.orm import relationship

from .database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, Identity(start=1), primary_key=True, index=True)
    name = Column(String, index=True)

    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, Identity(start=1), primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="products")
