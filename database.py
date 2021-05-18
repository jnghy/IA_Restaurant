import sqlite3

conn = sqlite3.connect('restaurant.db')
conn.execute("PRAGMA foreign_keys = 1")
c = conn.cursor()

def create(details):
    c.execute('''CREATE TABLE IF NOT EXISTS ''' + details)
    conn.commit()

def execute(statement, data):
    if data == None:
        c.execute(statement)
    else:
        c.execute(statement, data)
    conn.commit()

def insert(table, values, data):
    try:
        if data == None:
            c.execute("INSERT INTO " + table + " values " + values)
        else:
            c.execute("INSERT INTO " + table + " values " + values, data)
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error")

def update(table, values, condition, data):
    if data == None:
        c.execute("UPDATE " + table + "SET " + values + "WHERE " + condition)
    else:
        c.execute("UPDATE " + table + "SET " + values + "WHERE " + condition, data)
    conn.commit()

def delete(table, conditions, data):
    if data == None:
        c.execute("DELETE FROM " + table + " WHERE " + conditions)
    else:
        c.execute("DELETE FROM " + table + " WHERE " + conditions, data)
    conn.commit()

def selectall(table):
    c.execute("SELECT * FROM " + table)
    conn.commit()
    rows = c.fetchall()
    return rows

def select(statement, data):
    if data == None:
        c.execute(statement)
    else:
        c.execute(statement, data)
    conn.commit()
    rows = c.fetchall()
    return rows

def selectone(statement, data):
    if data == None:
        c.execute(statement)
    else:
        c.execute(statement, data)
    conn.commit()
    row = c.fetchone()
    return row

def log():
    return
    #get table name, time changed, old data, and new data

create('''ingredients 
            (ingredient_id integer PRIMARY KEY, 
            name text not null, 
            stock real not null,
            deficit_amount real,
            units text not null
            )''')

create('''products
            (product_id integer PRIMARY KEY, 
            name text not null, 
            price integer not null,
            description text
            )''')

create(''' restocks 
            (restock_id integer PRIMARY KEY, 
            ingredient_id number not null,
            quantity integer not null, 
            total_cost integer,
            supplier text,
            date text not null,
            FOREIGN KEY (ingredient_id) REFERENCES ingredients (ingredient_id) 
            )''')

create(''' product_details
            (
            product_details_id integer PRIMARY KEY,
            ingredient_id integer, 
            product_id integer, 
            quantity real not null,
	        FOREIGN KEY (ingredient_id) REFERENCES ingredients (ingredient_id),
        	FOREIGN KEY (product_id) REFERENCES products (product_id) 
            )''')

create(''' customers 
            (customer_id integer PRIMARY KEY,
            last_name text,
            first_name text,
            phone_number text,
            city text,
            address text
            )''')

create('''orders 
            (order_id integer PRIMARY KEY, 
            cost real not null, 
            payment_method text,
            date text,
            customer_id number,
            discount real default 0,
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
            )''')

create('''order_details
            (order_detail_id integer PRIMARY KEY, 
            order_id integer,
            product_id number, 
            quantity integer,
            FOREIGN KEY (product_id) REFERENCES products (product_Id)
            FOREIGN KEY (order_id) REFERENCES orders (order_id)
            )''')

create('''delivery
            (delivery_id integer PRIMARY KEY,
            order_id integer, 
            delivery_fee real default 0,
	        FOREIGN KEY (order_id) REFERENCES orders (order_id)
            )''')

def dummy():
    #insert dummy data ingredients
    insert("ingredients","(Null, 'flour', 9000, 500, 'grams')", None)
    insert("ingredients","(Null, 'baking soda', 400, 30, 'grams')", None)
    insert("ingredients","(Null, 'salt', 350, 50, 'grams')", None)
    insert("ingredients","(Null, 'butter', 2270, 908, 'grams')", None)
    insert("ingredients","(Null, 'granulated sugar', 3000, 1500, 'grams')", None)
    insert("ingredients","(Null, 'brown sugar', 3000, 1500, 'grams')", None)
    insert("ingredients","(Null, 'eggs', 24, 6, 'pieces')", None)
    insert("ingredients","(Null, 'vanila extract', 50, 4.2, 'grams')", None)
    insert("ingredients","(Null, 'peanut butter', 1000, 480, 'grams')", None)
    insert("ingredients","(Null, 'baking powder', 50, 20, 'grams')", None)

    #insert dummy data products
    insert("products","(Null, 'plain cookies', 300,  '(pack of 6)')", None)
    insert("products","(Null, 'peanut butter cookies', 325, '(pack of 6)')", None)

    #insert dummy data restocks
    insert("restocks","(Null, 1, 1000, 500, Null, 2021-03-04)", None)
    insert("restocks","(Null, 5, 500, 430, Null, 2021-03-07)", None)
    insert("restocks","(Null, 4, 908, 300, Null, 2021-03-15)", None)
    insert("restocks","(Null, 2, 50, 80, Null, 2021-04-01)", None)
    insert("restocks","(Null, 9, 400, 650, Null, 2021-04-24)", None)
    insert("restocks","(Null, 7, 24, 500, Null, 2021-04-27)", None)

    #insert dummy data product_details
    insert("product_details","(Null, 1, 1, 170)", None)
    insert("product_details","(Null, 2, 1, 4.80)", None)
    insert("product_details","(Null, 3, 1, 2.5)", None)
    insert("product_details","(Null, 4, 1, 227)", None)
    insert("product_details","(Null, 5, 1, 150)", None)
    insert("product_details","(Null, 6, 1, 165)", None)
    insert("product_details","(Null, 7, 1, 1)", None)
    insert("product_details","(Null, 8, 1, 4.2)", None)
    insert("product_details","(Null, 5, 2, 100)", None)
    insert("product_details","(Null, 6, 2, 110)", None)
    insert("product_details","(Null, 9, 2, 120)", None)
    insert("product_details","(Null, 4, 2, 113)", None)
    insert("product_details","(Null, 7, 2, 1)", None)
    insert("product_details","(Null, 1, 1, 170)", None)
    insert("product_details","(Null, 2, 1, 3.6)", None)
    insert("product_details","(Null, 10, 2, 2)", None)
    insert("product_details","(Null, 3, 1, .75)", None)

    #insert dummy data customers
    insert("customers","(Null, 'Cruz', 'Andi', Null, Null, Null)", None)
    insert("customers","(Null, 'Elgar', 'Akemi', Null, Null, Null)", None)
    insert("customers","(Null, 'Cadiz', 'Julia', Null, Null, Null)", None)
    insert("customers","(Null, 'Sison', 'Gia', Null, Null, Null)", None)
    insert("customers","(Null, 'Viduya', 'Bianca', Null, Null, Null)", None)
    insert("customers","(Null, 'Palencia', 'Bianca', Null, Null, Null)", None)
    insert("customers","(Null, 'Se', 'Toni', Null, Null, Null)", None)
    insert("customers","(Null, 'Villanueva', 'Caitlin', Null, Null, Null)", None)
    insert("customers","(Null, 'Madayag', 'Alize', Null, Null, Null)", None)
    insert("customers","(Null, 'Young', 'Keika', Null, Null, Null)", None)

    #insert dummy data orders
    insert("orders","(Null, 600, 'cash', 2021-04-16, 1, Null)", None)
    insert("orders","(Null, 925, 'credit card', 2-21-04-17, 7, Null)", None)
    insert("orders","(Null, 300, 'cash', 2-21-04-17, 4, Null)", None)
    insert("orders","(Null, 325, 'cash', 2-21-04-18, 2, Null)", None)
    insert("orders","(Null, 900, 'cash', 2-21-04-19, 3, Null)", None)
    insert("orders","(Null, 950, 'cash', 2-21-04-27, 8, Null)", None)



    #insert dummy data order details
    insert("order_details","(Null, 1, 1, 2)", None)
    insert("order_details","(Null, 2, 1, 2)", None)
    insert("order_details","(Null, 2, 2, 1)", None)
    insert("order_details","(Null, 3, 1, 1)", None)
    insert("order_details","(Null, 4, 2, 1)", None)
    insert("order_details","(Null, 5, 1, 1)", None)
    insert("order_details","(Null, 5, 2, 2)", None)

    #insert dummy data deliveries
    insert("delivery","(Null, 1, Null)", None)
    insert("delivery","(Null, 5, 25)", None)
    insert("delivery","(Null, 3, 50)", None)

'''

templates

insert("ingredients","(Null, Name, Stock, Defict_Amount, Units)", None)
insert("products","(Null, Name, Price)", None)
insert("restocks","(Null, ingredient_id, quantity, total_cost, supplier, date)", None)
insert("product_details","(Null, ingredient_id, product_id, quantity)", None)
insert("customers","(Null, last_name, first_name, city, phone_number, address)", None)
insert("orders","(Null, cost, payment_method, data, customer_id, discount)", None)
insert("order_details","(Null, order_id, product_id, quantity)", None)
insert("delivery","(Null, order_id, customer_id, delivery_fee)", None)


'''
