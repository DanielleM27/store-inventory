import sqlite3

#define connection and cursor

conn = sqlite3.connect('ínventory.db')
c = conn.cursor()

#create product tables

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS stuffToPlot(product_name TEXT, product_quantity INTEGER, product_price INTEGER, product_date_updated DateTime)')



#add to products


def data_entry():
    c.execute("INSERT INTO stuffToPlot VALUES('Bagel - Whole White Sesame', 97, '$4.30', '11/1/2018')")
    c.execute("INSERT INTO stuffToPlot VALUES('Sauce - Caesar Dressing', 81, '$8.05', '12/28/2018')")
    c.execute("INSERT INTO stuffToPlot VALUES('Shiratamako - Rice Flour', 71, '$7.99', '3/7/2018')")
    c.execute("INSERT INTO stuffToPlot VALUES('Tart - Raisin And Pecan', 86, '$1.06', '1/18/2019')")
    c.execute("INSERT INTO stuffToPlot VALUES('Radish', 22, '$2.47', '11/6/2018')")
    c.execute("INSERT INTO stuffToPlot VALUES('Juice - V8 Splash', 67, '$1.25', '1/10/2018')")
    c.execute("INSERT INTO stuffToPlot VALUES('Red Currants', 49, '$6.77', '10/1/2018')")
    c.execute("INSERT INTO stuffToPlot VALUES('Soup - Base Broth Beef', 62, '$5.44', '3/9/2019')")
    c.execute("INSERT INTO stuffToPlot VALUES('Tomatoes Tear Drop Yellow', 73, '$0.64', '2/9/2019')")
    c.execute("INSERT INTO stuffToPlot VALUES('Mussels - Cultivated', 24, '$9.34', '7/31/2018')")
    c.execute("INSERT INTO stuffToPlot VALUES('Bread - Crumbs BULK', 88, '$4.49', '1/12/2019')")
    c.execute("INSERT INTO stuffToPlot VALUES('Beans - Long, Chinese', 47, '$4.73', '9/22/2018')")
    c.execute("INSERT INTO stuffToPlot VALUES('Beans - Navy, Dry', 44, '$4.60', '1/20/2018')")
    c.execute("INSERT INTO stuffToPlot VALUES('Juice - V8 Splash', 67, '$1.15', '1/13/2018')")
    c.execute("INSERT INTO stuffToPlot VALUES('Basil - Dry, Rubbed', 21, '$8.69', '2/4/2018')")
    c.execute("INSERT INTO stuffToPlot VALUES('Apple - Granny Smith', 72, '$5.06', '1/12/2018')")
    c.execute("INSERT INTO stuffToPlot VALUES('Lid - High Heat, Super Clear', 5, '$1.23', '2/9/2018')")
    c.execute("INSERT INTO stuffToPlot VALUES('Oranges - Navel', 46, '$4.78', '6/6/2018')")
    c.execute("INSERT INTO stuffToPlot VALUES('Berry Brulee', 50, '$7.59', '8/25/2018')")
    c.execute("INSERT INTO stuffToPlot VALUES('Lobster - Canned Premium', 57, '$7.61', '4/15/2018')")
    c.execute("INSERT INTO stuffToPlot VALUES('Veal - Ground', 5, '$7.67', '12/19/2018')")
    c.execute("INSERT INTO stuffToPlot VALUES('Oil - Cooking Spray', 6, '$4.20', '6/11/2018')")
    c.execute("INSERT INTO stuffToPlot VALUES('Extract - Vanilla,artificial', 20, '$2.91', '6/8/2018')")
    c.execute("INSERT INTO stuffToPlot VALUES('Mushroom - Porcini, Dry', 71, '$8.14', '7/26/2018')")
    c.execute("INSERT INTO stuffToPlot VALUES('Wine - Chateau Bonnet', 54, '$7.41', '3/10/2018')")
    c.execute("INSERT INTO stuffToPlot VALUES('Sauce - Caesar Dressing', 16, '$8.25', '4/10/2019')")
    c.execute("INSERT INTO stuffToPlot VALUES('Ham - Procutinni', 8, '$5.70', '1/9/2019')")
    conn.commit()
    c.close()
    conn.close()



create_table()
data_entry()



                             
