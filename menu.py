import tkinter as tk
import ingredients
import database as db
import sqlite3

conn = sqlite3.connect('restaurant.db')
conn.execute("PRAGMA foreign_keys = 1")
c = conn.cursor()

class menu(tk.Frame):
    def __init__(self):
        super().__init__()
        self.pack()

        self.title_text = tk.Label(self, text="Main Menu", pady=30, font=("Lucida Grande", 20, 'bold'))
        self.title_text.grid(columnspan=2)

        self.ingredients_button = tk.Button(self, text="Ingredients", pady=10, command=lambda: (self.forget(), ingredients.display()))
        self.ingredients_button.grid(row=1, column=0)


        '''     self.restock_button = tk.Button(self, text="Restock", pady=10, command=lambda: (self.forget(), restock_menu()))
                self.restock_button.grid()
        
                self.order_button = tk.Button(self, text="Orders", pady=10, command=lambda: (self.forget(), orders_menu()))
                self.order_button.grid()
        
                self.deliveries_button = tk.Button(self, text="Deliveries", pady=10, command=lambda: (self.forget(), deliveries_menu()))
                self.deliveries_button.grid()
        
                self.product_button = tk.Button(self, text="Product", pady=10, command=lambda: (self.forget(), products_menu()))
                self.product_button.grid()
        
                self.customers_button = tk.Button(self, text="Customers", pady=10, command=lambda: (self.forget(), customers_menu()))
                self.customers_button.grid()
        
                self.product_details_button = tk.Button(self, text="Product Details", pady=10, command=lambda: (self.forget(), product_details_menu()))
                self.product_details_button.grid()
        
                self.order_details_button = tk.Button(self, text="Order Details", pady=10, command=lambda: (self.forget(), order_details_menu()))
                self.order_details_button.grid()
        
                self.log_button = tk.Button(self, text="Database Logs", pady=10, command=lambda: (self.forget(), logs_menu()))
                self.log_button.grid()
        
                self.report_button = tk.Button(self, text="Reports", pady=10, command=lambda: (self.forget(),report_menu()))
                self.report_button.grid()'''
