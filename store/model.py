from sqlalchemy import (create_engine, Column, 
                        Integer, String, Date)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///inventory.db", echo=True)
Session = sessionmaker(bind = engine)
session = Session()
Base = declarative_base()



class Product(Base):
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True)
    name = Column("Product Name", String)
    price = Column("Price", Integer)
    quanity = Column("Quanity", Integer)
    date = Column("Last Updated", Date)
    
    
    def __repr__(self):
        return f"Name: {self.name} Price: {self.price} Quanity: {self.quanity} Last Updated: {self.date}"

if __name__ == "__main__":
    Base.metadata.create_all(engine)