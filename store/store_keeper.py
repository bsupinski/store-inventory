from model import (Base, session, Product, engine)
import datetime
import csv
import time

class Store_Keeper():
    
    def clean_price(self, price_str):
        float_price = price_str.replace("$", "")
        float_price = float(float_price)
        return float_price
    
    
    def clean_date(self, date_str):
        split_date = date_str.split("/")
        year = int(split_date[2])
        month = int(split_date[0])
        day = int(split_date[1])
        return_Date = datetime.date(year, month, day)
        
        return return_Date
        

    def add_csv(self):
        with open("../inventory.csv") as csvfile:
            data = csv.reader(csvfile)
            next(data)
            for row in data:
                name = row[0]
                price = self.clean_price(row[1])
                quanity = row[2]
                date = self.clean_date(row[3])
                new_product = Product(name=name, price=price, quanity=quanity, date=date)
                print(new_product)
                session.add(new_product)
            session.commit()
            



if __name__ == "__main__":
    Base.metadata.create_all(engine)
    newstore = Store_Keeper()
    newstore.add_csv()