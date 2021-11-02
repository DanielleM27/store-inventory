import time
import datetime
import csv
import os


from Models import engine, session, Base, Product


def menu():
    while True:
        choice = input('''
            \nSTORE INVENTORY MENU
            \rv > View A Single Products Inventory
            \ra > Add A New Product To The Database
            \rb > Make A Backup Of The Entire Inventory
            \rq > Exit
            \rWhat would you like to do? ''')
        if choice.lower() in ('v', 'a', 'b', 'q'):
            return choice.lower()
        else:
            input('''
                  \nPlease choose one of the options above(v, a, b or q).
                  \rPress enter to try again.''')
            
            
def app():
    app_running = False
    while app_running:
        menu_choice = menu()
        if menu_choice == 'v':
            view_product()
        elif menu_choice == 'a':
            add_product()
        elif menu_choice == 'b':
            export_csv()
        else:
            print('-- Goodbye! --')
            app_running = False


def clean_price(price_str):
    price = price_str.split('$')[1] if '$' in price_str else price_str
    try:
        price = int(float(price) * 100)
    except ValueError:
        print('The value entered is not the correct format. Please enter a price in the format: $19.95')
    else:
        return price
    return None


def clean_date(date_str):
    try:
        return_date = datetime.datetime.strptime(date_str, '%m/%d/%Y')
    except ValueError:
        input('''
              \n Oh no there is a Date Error 
              \rDate should include a valid Month/Day/Year from the past: 27/10/1000
              \rPress enter to try again.
              \r''')
        return
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
              \n Oh no there is  ID Number Error 
              \rID should be a number.
              \rPress enter to try again.
              \r''')
        return
    else:
        if product_id in id_options:
            return product_id
        else:
            input(f'''
                  \n Oh no there is  ID Number Error
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
            \n--------------------------------------------
            \rName: {product_viewed.product_name}
            \rPRICE: {product_viewed.product_price / 100}
            \rQTY:{product_viewed.product_quantity}
            \rDate Updated: {product_viewed.date_updated}
            \r--------------------------------------------''')


def add_product():
    name = input('What is the name of the product? ')

    quantity_error = True
    while quantity_error == True:
        quantity = input('How many are there? ')
        try:
            int(quantity)
        except ValueError:
            quit_or_again = input('''
                    \nThe quantity must be an number.
                    \rPress enter to try again.''')
        else:
            quantity_error = False

    price_error = True
    while price_error == True:
        price = input('What is the price of the product?(ex. 3.99) ')
        price = clean_price(price)
        if type(price) == int:
            price_error = False

    date = datetime.datetime.now()

    session.query(Product).filter(name == Product.product_name).delete()

    new_product = Product(product_name=name, product_quantity=quantity,
                          product_price=price, date_updated=date)
    session.add(new_product)
    session.commit()
    print(f'-- {name} was added. --')
    time.sleep(1)


def export_csv():
    with open('backup.csv', 'w', newline='') as csvfile:
        fieldnames = Product.__table__.columns.keys()
        product_writer = csv.DictWriter(
            csvfile, fieldnames=fieldnames, lineterminator='\n')

        product_writer.writeheader()
        for product in session.query(Product):
            product_writer.writerow({'product_id': product.product_id,
                                     'product_name': product.product_name,
                                     'product_quantity': product.product_quantity,
                                     'product_price': product.product_price,
                                     'date_updated': product.date_updated})
    print('-- Export successful. --')
    time.sleep(1)


def add_csv():
    with open('inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        next(data, None)
        for row in data:
            product_in_db = session.query(Product).filter(
                Product.product_name == row[0]).one_or_none()
            name = row[0]
            price = clean_price(row[1])
            quantity = (row[2])
            date = clean_date(row[3])
            new_product = Product(
                product_name=name, product_quantity=quantity, product_price=price, date_updated=date)

            if product_in_db is not None:
                db_time = product_in_db.date_updated
                db_time = datetime.datetime(
                    db_time.year, db_time.month, db_time.day)
                if date > db_time:
                    session.query(Product).filter(
                        Product.product_name == row[0]).delete()
                    session.add(new_product)
            else:
                session.add(new_product)
            session.flush()
        session.commit()




if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()


