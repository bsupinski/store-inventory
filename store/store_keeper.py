from model import (Base, session, Product, engine)
import datetime
import csv
import time

class Store_Keeper():
    
    def clean_price(self, price_str):
        float_price = price_str.replace("$", "")
        float_price = float(float_price)
        return int(float_price * 100)
    
    
    def clean_date(self, date_str):
        split_date = date_str.split("/")
        year = int(split_date[2])
        month = int(split_date[0])
        day = int(split_date[1])
        return_Date = datetime.date(year, month, day)
        
        return return_Date
    
    
    def view_product(self):
        available_products = []
        for product in session.query(Product):
            available_products.append(product.product_id)
        error_warning = True
        while error_warning:
            try:
                
                print(f'''\nAvailable product IDs\r{available_products}''')
                user_choice = input("Select what product ID you would like to view.  ")
                user_choice = int(user_choice)
                view_product = session.query(Product).filter(Product.product_id==int(user_choice)).first()
                print(f'''
                    \nName: {view_product.product_name}
                    \rQuanity: {view_product.product_quantity}
                    \rPrice: ${view_product.product_price / 100}
                    \rLast Updated: {datetime.date.strftime(view_product.date_updated, "%b %d, %Y")}
                    ''')
                error_warning = False
                
            except ValueError:
                input(f'''You entered an incorrect value. Press "Enter" to try again. ''')
            except AttributeError:
                 input(f'''You entered an incorrect value. Press "Enter" to try again. ''')
        print("Outside the While block")


def edit_product(self):
    available_inputs =["1", "2", "3"]
    user_input = input('''\rWhat would you like to do?
                       \n   1. Edit Product
                       \n   2. Check Profuct Profit''')


    def add_csv(self):
        with open("../inventory.csv") as csvfile:
            data = csv.reader(csvfile)
            next(data)
            for row in data:
                product_in_db = session.query(Product).filter(Product.product_name==row[0]).one_or_none()
                if product_in_db == None:
                    name = row[0]
                    price = self.clean_price(row[1])
                    quanity = row[2]
                    date = self.clean_date(row[3])
                    new_product = Product(product_name=name, product_price=price, product_quantity=quanity, date_updated=date)
                    session.add(new_product)
            session.commit()
            



if __name__ == "__main__":
    Base.metadata.create_all(engine)
    newstore = Store_Keeper()
    newstore.add_csv()
    newstore.view_product()
