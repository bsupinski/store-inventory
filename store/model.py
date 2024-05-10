from sqlalchemy import (create_engine, Column, 
                        Integer, String, Date)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///inventory.db")
Session = sessionmaker(bind = engine)
session = Session()
Base = declarative_base()



class Product(Base):
    __tablename__ = "inventory"
    
    product_id = Column(Integer, primary_key=True)
    product_name = Column("Product Name", String)
    product_price = Column("Price", Integer)
    product_quantity = Column("Quanity", Integer)
    date_updated  = Column("Last Updated", Date)
    
    
    def __repr__(self):
        return f"Name: {self.product_name} Price: {self.product_price} Quanity: {self.product_quantity} Last Updated: {self.date_updated}"

if __name__ == "__main__":
    Base.metadata.create_all(engine)