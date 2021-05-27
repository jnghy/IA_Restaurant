import tkinter as tk
import menu as m
import amount_used as au
import amount_ordered as ao
import cost_ingredients as ci
import amount_earned as ae

class menu(tk.Frame):
    def __init__(self):
        super().__init__()
        self.pack()

        self.title_text = tk.Label(self, text="Report Menu", pady=30, font=("Lucida Grande", 20, 'bold'))
        self.title_text.grid(columnspan=2)

        self.most_used_ingredients_button = tk.Button(self, text="Amount of Ingredients Used", width = 25, pady=10, command=lambda: (self.forget(), au.display()))
        self.most_used_ingredients_button.grid(row=1, column=0, padx=10)

        self.ingredient_costs = tk.Button(self, text="Cost of Ingredients", width = 25, pady=10, command=lambda: (self.forget(), ci.display()))
        self.ingredient_costs.grid(row=2, column=0, padx=10)

        self.top_earning_products = tk.Button(self, text="Amount Earned by Products", width = 25, pady=10, command=lambda: (self.forget(), ae.display()))
        self.top_earning_products.grid(row=3, column=0, padx=10)

        self.most_ordered_products = tk.Button(self, text="Amount of Products Ordered", width = 25, pady=10, command=lambda: (self.forget(), ao.display()))
        self.most_ordered_products.grid(row=4, column=0, padx=10)

        self.menu_button = tk.Button(self, text="Main Menu", width = 25, pady=10, command=lambda: (self.forget(), m.menu()))
        self.menu_button.grid(row=5, column=0)
