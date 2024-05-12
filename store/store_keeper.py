from model import (Base, session, Product, engine)
import datetime
import csv
import time

class Store_Keeper():


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


    def main_menu(self):
        
        Base.metadata.create_all(engine)
        menu_options = ["V", "A", "B"]
        print("Welcome to Store Keeper\n\n")
        input_error = True
        while input_error:
            user_choice = input('''
                  \rPlease choose one of the following option
                  \n Press "V" to view a product
                  \n Press "A" to add a new product
                  \n Press "B" to make a back up of the store data
                  
                  ''')
            if user_choice[0].upper() in menu_options:
                input_error = False
                if user_choice.upper() == "V":
                    self.view_product()
                elif user_choice.upper() == "A":
                    self.add_product()
                elif user_choice.upper() == "B":
                    self.make_backup()
            else:
                print("You entered an incorect command, please try again.")


    def view_product(self):
        available_products = []
        for product in session.query(Product):
            available_products.append(product.product_id)
        error_warning = True
        while error_warning:
            try:
                print(f'''\nAvailable product IDs\n{available_products}''')
                user_choice = input("Select what product ID you would like to view.  ")
                user_choice = int(user_choice)
                view_product = session.query(Product).filter(Product.product_id==int(user_choice)).first()
                print(f'''
                    \nName: {view_product.product_name}
                    \nQuanity: {view_product.product_quantity}
                    \nPrice: ${view_product.product_price / 100}
                    \nLast Updated: {datetime.date.strftime(view_product.date_updated, "%b %d, %Y")}
                    ''')
                error_warning = False
                
            except ValueError:
                input(f'''You entered an incorrect value. Press "Enter" to try again. ''')
            except AttributeError:
                 input(f'''You entered an incorrect value. Press "Enter" to try again. ''')
        time.sleep(1)
        self.edit_product_menu(view_product)


    def check_total_price(self, product):
            print(f"Estimated profit with current price and quantity: ${product.product_quantity * product.product_price / 100}")
            return product.product_quantity * product.product_price


    def add_product(self):
            print("Enter new product information to add.")
            new_name = self.new_name()
            new_price = self.new_price()
            new_quanity = self.new_quantity()
            new_date = self.update_now()
            
            new_product = Product(product_name=new_name, product_price=new_price, product_quantity=new_quanity, date_updated=new_date)
            session.add(new_product)
            session.commit()


    def make_backup(self):
        with open("backup_db.csv", "w") as csvfile:
            field_names = ["Product ID", "Product Name", "Price", "Quantity", "Last Updated"]
            backup_writer = csv.DictWriter(csvfile, fieldnames=field_names)
            backup_writer.writeheader()
            for row in session.query(Product):
                backup_writer.writerow({
                    "Product ID": row.product_id,
                    "Product Name": row.product_name,
                    "Price": row.product_price,
                    "Quantity": row.product_quantity,
                    "Last Updated": row.date_updated,
                })
            


    def clean_price(self, price_str):
        try:
            float_price = price_str.replace("$", "")
            float_price = float(float_price)
        except ValueError:
            input('''\nThe format did not match what is expected
                  \nEX: 14.25
                  \nPress "Enter" to continue''')
        else:
            return int(float_price * 100)


    def clean_date(self, date_str):
        split_date = date_str.split("/")
        year = int(split_date[2])
        month = int(split_date[0])
        day = int(split_date[1])
        return_Date = datetime.date(year, month, day)
        
        return return_Date


    def new_name(self):
        return input("What is the product's name?  ")


    def new_price(self):
        error_check = True
        while error_check:
            price = input("What will the price be set at?  ")
            price = self.clean_price(price)
            if type(price) == int:
                error_check = False
                return price


    def new_quantity(self):
        error_check = True
        while error_check:
            try:
                new_quantity = int(input("What is the quantity of the product?  "))
            except ValueError:    
                print("Please enter a numbers in digit form only(Ex: 32)  ")
            else:    
                error_check = False
                return new_quantity


    def edit_name(self, product):
        print(f"The current product name is: {product.product_name}")
        new_name = input("What would you like to change the name to?  ")
        product.product_name = new_name
        product.date_updated = self.update_now()


    def edit_price(self, product):
        error_check = True
        while error_check:
            print(f"The current price is set at: ${product.product_price / 100}")
            new_price = input("What would you like the new price to be set at(ex: $4.23)"  )
            new_price = self.clean_price(new_price)
            print(type(new_price))
            if type(new_price) == int:
                product.product_price = new_price
                product.date_updated = self.update_now()
                error_check = False


    def edit_quanity(self, product):
        print(f"Current quantity is {product.product_quantity}")
        integer_error = True
        while integer_error:
            try:
                new_quanity = int(input("What is the new quantity?  "))
                
            except ValueError:
                print("Please enter a numbers in digit form only(Ex: 32)  ")
            else:
                product.product_quantity = new_quanity
                product.date_updated = self.update_now()
                integer_error = False


    def update_now(self):
        current_date = datetime.date.today()
        return current_date




if __name__ == "__main__":
    newstore = Store_Keeper()
    newstore.add_csv()
    newstore.main_menu()