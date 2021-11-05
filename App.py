import time
import datetime
import csv
import os
from Models import engine, session, Base, Product


def menu():
    while True:
        print('''
            \n ****** STORE INVENTORY MENU ******
            \r(v) > View A Single Products Inventory
            \r(a) > Add A New Product To The Database
            \r(b) > Make A Backup Of The Entire Inventory
            \r(q) > Quit''')
        choice = input("What would you like to do on Store Inventory?\n").lower() 
        if choice.lower() in ('v', 'a', 'b', 'q'):
            return choice.lower()
        else:
            input('''
                  \n Please only choose one of the options above.
                  \rThe options are 'v', 'a', 'b', and 'q'.
                  \r Press enter to try again.''')
            


def clean_price(price_str):
    price = price_str.split('$')[1] if '$' in price_str else price_str
    try:
        price = int(float(price) * 100)
    except ValueError:
        print('''
              \n Oh no there is a Price Error 
              \r Value entered is not in the correct format. Please enter a price in the following format: $12.99
              \r Press enter to try again.
              \r''')
    else:
        return price
    return None


def clean_date(date_str):
    try:
        return_date = datetime.datetime.strptime(date_str, '%m/%d/%Y')
    except ValueError:
        input('''
              \n Oh no there is a Date Error 
              \r Date should include a valid Month/Day/Year from the past: 27/10/2000
              \r Press enter to try again.
              \r''')
    else:
        return return_date


def clean_id(id_str):
    id_options = []
    for product in session.query(Product):
        id_options.append(product.product_id)
    try:
        product_id = int(id_str)
    except ValueError:
        input('''
              \n Oh no there is a ID Number Error 
              \rID should be a number.
              \rPress enter to try again.
              \r''')
        return
    else:
        if product_id in id_options:
            return product_id
        else:
            input(f'''
                  \n Oh no there is  ID Error
                  \rOptions: {id_options}
                  \rPress enter to try again.
                  \r''')
            return


def view_product():
    id_error = True
    while id_error == True:
        product_id = input('What is the the product ID? ')
        product_id = clean_id(product_id)
        if type(product_id) == int:
            id_error = False
    product_viewed = session.query(Product).filter(
        Product.product_id == product_id).one_or_none()
    print(f'''
            \nProduct Name: {product_viewed.product_name}
            \rProduct Price: {product_viewed.product_price / 100}
            \rProduct Quantity:{product_viewed.product_quantity}
              \rDate Updated: {product_viewed.date_updated}
            \r ''')


def add_product():
    product_name = input('What is the products name? ')
    price_error = True
    while price_error:
        product_price = input('What is the price of the product?(Example: 27) ')
        product_price = clean_price(product_price)
        if type(product_price) == int:
            price_error = False
            quantity_error = True
    while quantity_error:
      product_quantity = input('How many are there in stock? ')
      try:
            int(product_quantity)
      except ValueError:
            input('''
                \nThe quantity must be a whole number.
                \rPress enter to try again
                \r''')
      else:
            quantity_error = False
            
    now = datetime.datetime.now()
    date_updated = clean_date(now.strftime("%m/%d/%Y"))
    new_product = Product(product_name=product_name,
        product_price=product_price,
        product_quantity=product_quantity,
        date_updated=date_updated)

    product_in_db = session.query(Product).filter(
        Product.product_name==new_product.product_name).one_or_none()
    if product_in_db != None:
            session.query(Product).filter(
                Product.product_name==new_product.product_name).update({
                Product.product_price: new_product.product_price,
                Product.product_quantity: new_product.product_quantity,
                Product.date_updated: new_product.date_updated
            })
    else:
        session.add(new_product)
    session.commit()
    print(f'-- {product_name} Added. --')
    time.sleep(1)



def backup_csv():
    backup_choice = input('''
        \nYou are about to make a backup of the database
        \rDo you wish to proceed? ('y' or n')\n''').lower()
    if backup_choice == 'y':
        now = datetime.datetime.now().date()
        file = open(f"backup_database_{now}.csv", "a")
        file.write('product_name,product_price,product_quantity,product_id,date_updated\n')
        for product in session.query(Product):
            file.write(f'{product}\n')
        file.close()
        print('***** BACKUP WAS CREATED *****')
    else:
      return


def add_csv():
    with open('inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        next(data)
        for row in data:
            product_in_db = session.query(Product).filter(Product.product_name == row[0]).one_or_none()
            product_name = row[0]
            product_price = clean_price(row[1])
            product_quantity = int(row[2])
            date_updated = clean_date(row[3])
            new_product = Product(product_name=product_name,product_price=product_price,product_quantity=product_quantity,date_updated=date_updated)
            if product_in_db is not None:
                db_time = product_in_db.date_updated
                db_time = datetime.datetime(db_time.year, db_time.month, db_time.day)
                if new_product.date_updated > db_time:
                    session.query(Product).filter(
                    Product.product_name == row[0]).delete()
                    session.add(new_product)
            else:
                session.add(new_product)
        session.commit()
        

        
def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == 'v':
            view_product()
        elif choice == 'a':
            add_product()
        elif choice == 'b':
            backup_csv()
        else:
            print('****** GOODBYEEEEEE!! ******')
            break
            app_running = False



if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()