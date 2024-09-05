from sqlalchemy import String, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Model
from typing import List

ProductCountry = Table(
    'products_country',
    Model.metadata,
    Column('product_id', ForeignKey('products.id'), primary_key=True, nullable=False),
    Column('country_id', ForeignKey('countries.id'), primary_key=True, nullable=False)
)

class Product(Model):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    manufacturer_id: Mapped[int] = mapped_column(ForeignKey("manufacturers.id"), index=True)
    year: Mapped[int] = mapped_column(index=True)
    cpu: Mapped[str] = mapped_column(String(32))
    manufacturer: Mapped['Manufacturer'] = relationship(back_populates='products')
    countries: Mapped[List['Country']] = relationship(secondary=ProductCountry, back_populates='products')

    def __repr__(self):
        return f"Product({self.id}, {self.name})"
    
class Manufacturer(Model):
    __tablename__ = 'manufacturers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    products: Mapped[List['Product']] = relationship(back_populates='manufacturer')

    def __repr__(self):
        return f"Manufacturer({self.id}, {self.name})"
    
class Country(Model):
    __tablename__ = 'countries'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), index=True, unique=True)
    products: Mapped[List['Product']] = relationship(secondary=ProductCountry, back_populates='countries')

    def __repr__(self):
        return f'Country({self.id}, {self.name})'