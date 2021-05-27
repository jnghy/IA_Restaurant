import tkinter as tk
import ingredients
import restock
import products
import product_details
import orders
import order_details
import customers
import delivery
import database
import report_menu as rm

class menu(tk.Frame):
    def __init__(self):
        super().__init__()
        self.pack()
        self.menu()
        self.deficit_ingredient()

    def menu(self):
        self.title_text = tk.Label(self, text="Main Menu", pady=30, font=("Lucida Grande", 20, 'bold'))
        self.title_text.grid(columnspan=2)

        self.ingredients_button = tk.Button(self, text="Ingredients", width = 15, pady=10, command=lambda: (self.forget(), ingredients.display()))
        self.ingredients_button.grid(row=1, column=0, padx=10)

        self.restock_button = tk.Button(self, text="Restock", width = 15, pady=10, command=lambda: (self.forget(), restock.display()))
        self.restock_button.grid(row=1, column=1, padx=10)

        self.product_button = tk.Button(self, text="Product", width = 15, pady=10, command=lambda: (self.forget(), products.display()))
        self.product_button.grid(row=2, column=0)

        self.product_details_button = tk.Button(self, text="Product Details",  width = 15, pady=10, command=lambda: (self.forget(), product_details.display()))
        self.product_details_button.grid(row=2, column=1)

        self.order_button = tk.Button(self, text="Orders", pady=10,  width = 15, command=lambda: (self.forget(), orders.display()))
        self.order_button.grid(row=3, column=0)

        self.order_details_button = tk.Button(self, text="Order Details",  width = 15, pady=10, command=lambda: (self.forget(), order_details.display()))
        self.order_details_button.grid(row=3, column=1)

        self.deliveries_button = tk.Button(self, text="Deliveries", pady=10,  width = 15,  command=lambda: (self.forget(), delivery.display()))
        self.deliveries_button.grid(row=4, column=0)
        
        self.customers_button = tk.Button(self, text="Customers", pady=10,  width = 15, command=lambda: (self.forget(), customers.display()))
        self.customers_button.grid(row=4, column=1)

        self.report_button = tk.Button(self, text="Reports", pady=10,  width = 15, command=lambda: (self.forget(),rm.menu()))
        self.report_button.grid()

    #displays the ingredients, which stock level is too low
    def deficit_ingredient(self):

        self.ingredient_label = tk.Label(self, text="Deficient Ingredients: ", font=("Lucida Grande", 20, 'bold'))
        self.ingredient_label.grid(row=6, columnspan=2,  pady=(30,0))

        #gets all ingredients and adds them to list
        list = ""
        for row in database.select('''SELECT GROUP_CONCAT(name, ", ")
                                FROM ingredients
                                WHERE stock <= deficit_amount''', None):
            if row[0] == None:
                list = "None"
            else:
                list += row[0]

        self.ingredient_list = tk.Label(self, text=list, font=("Lucida Grande", 15))
        self.ingredient_list.grid(row=7, columnspan=2)
