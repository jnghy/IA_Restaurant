import sqlite3
conn = sqlite3.connect('restaurant.db')
conn.execute("PRAGMA foreign_keys = 1")
c = conn.cursor()

def execute(command):
    c.execute(command)
    conn.commit()

def create(details):
    execute('''CREATE TABLE IF NOT EXISTS ''' + details)

def insert(table, fields, values):
    execute("INSERT INTO " + table + fields + " values " + values)


create('''ingredients 
            (ingredient_id integer PRIMARY KEY, 
            name text, 
            stock integer,
            defict_amount integer,
            units text
            )''')

create('''product
            (product_id integer PRIMARY KEY, 
            name text, 
            price integer
            )''')

create(''' restock (restock_id integer PRIMARY KEY, 
            ingredient_id number,
            quantity integer, 
            total_cost integer,
            supplier text,
            date text not null,
            FOREIGN KEY (ingredient_id) REFERENCES ingredients (ingredient_id) 
            )''')

create(''' product_details(ingredient_id integer, 
            product_id integer, 
            quantity integer,
	        PRIMARY KEY (ingredient_id, product_id),
	        FOREIGN KEY (ingredient_id) REFERENCES ingredients (ingredient_id),
        	FOREIGN KEY (product_id) REFERENCES products (product_id) 
            )''')


create(''' customers 
            (customer_id integer PRIMARY KEY,
            last_name text,
            first_name text,
            phone_number text,
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

create('''delivery
            (order_id integer, 
            customer_id integer, 
            quantity integer,
	        PRIMARY KEY (order_id, customer_id),
	        FOREIGN KEY (order_id) REFERENCES orders (order_id),
        	FOREIGN KEY (customer_id) REFERENCES customers (customer_id) 
            )''')




