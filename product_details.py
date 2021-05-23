import tkinter as tk
import tkinter.ttk as ttk
import menu as m
import database
import sqlite3
import datetime
import csv

class display(tk.Frame):
    def __init__(self):
        super().__init__()
        self.pack()

        self.title_frame = tk.Frame(self)
        self.title_frame.grid(row=0,columnspan=2, column=0)

        self.title_text = tk.Label(self.title_frame, text="Product Details Display", pady=30, font=("Lucida Grande", 20, 'bold'))
        self.title_text.grid(columnspan=2)

        self.navigation_frame()
        self.display_frame()
        self.table_frame()
        self.menu_frame()

    def navigation_frame(self):

        self.fields_frame = tk.Frame(self)
        self.fields_frame.grid(row=1, column=0, sticky=tk.NW)

        self.columns = ["product_details_id", "Product_Name","Ingredient_Name","Quantity"]

        self.field_selected = tk.StringVar()
        self.fields_menu = tk.OptionMenu(self.fields_frame, self.field_selected , *self.columns)
        self.fields_menu.config(width=20)
        self.fields_menu.grid(row=0, column = 1)

        self.field_selected.set("product_details_id")

        self.orders = ["Asc", 'Desc']

        self.order_selected = tk.StringVar()
        self.order_menu = tk.OptionMenu(self.fields_frame, self.order_selected , *self.orders)
        self.order_menu.config(width=8)
        self.order_menu.grid(row=0, column = 2)

        self.order_selected.set("Asc")

        self.load_button = tk.Button(self.fields_frame, text="Load", command=lambda: (self.load_data()))
        self.load_button.grid(row = 0, column=0)

    def display_frame(self):
        self.left_frame = tk.Frame(self, width=310, height=150, padx=2, pady=10)
        self.left_frame.grid(row=2, column=0, sticky=tk.NW)

        self.label_product_details_id = tk.Label(self.left_frame,text="Product Details ID: ", anchor=tk.W,justify='left')
        self.label_product_details_id.grid(row=0, column=0, sticky=tk.NW, padx=5)
        self.entry_product_details_id = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_product_details_id.grid(row=0, column=1)

        self.product_fields = []
        for row in database.select("SELECT DISTINCT name FROM products", None):
            self.product_fields += row

        self.product_selected = tk.StringVar()

        self.label_product_name = tk.Label(self.left_frame, text="Product Name: ", anchor=tk.W,justify='left')
        self.label_product_name.grid(row=1, column=0, sticky=tk.NW, padx=5)

        self.product_menu = tk.OptionMenu(self.left_frame, self.product_selected , *self.product_fields)
        self.product_menu.config(width=35)
        self.product_menu.grid(row=1, column = 1)


        self.ingredient_fields = []
        for row in database.select("SELECT DISTINCT name FROM ingredients", None):
            self.ingredient_fields += row

        self.ingredient_selected = tk.StringVar()

        self.label_ingredient_name = tk.Label(self.left_frame, text="Ingredient Name: ", anchor=tk.W,justify='left')
        self.label_ingredient_name.grid(row=2, column=0, sticky=tk.NW, padx=5)

        self.ingredient_menu = tk.OptionMenu(self.left_frame, self.ingredient_selected , *self.ingredient_fields)
        self.ingredient_menu.config(width=35)
        self.ingredient_menu.grid(row=2, column = 1)


        self.label_quantity = tk.Label(self.left_frame,text="Quantity: ", anchor=tk.W,justify='left')
        self.label_quantity.grid(row=3, column=0, sticky=tk.NW, padx=5)
        self.entry_quantity = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_quantity.grid(row=3, column=1)

    def table_frame(self):
        self.fields = ["Id", "Product_Name","Ingredient_Name","Quantity"]

        self.right_frame = tk.Frame(self, bd=5, width=600, height=200, padx=2, pady=5)
        self.right_frame.grid(row=2, column=1)

        scroll_x = tk.Scrollbar(self.right_frame, orient='horizontal')
        scroll_y = tk.Scrollbar(self.right_frame, orient='vertical')

        self.product_details_table = ttk.Treeview(self.right_frame, height=12, column=self.fields, xscrollcommand = scroll_x.set, yscrollcommand = scroll_y.set)

        scroll_x.pack(side='bottom', fill='x')
        scroll_y.pack(side='bottom', fill='y')

        self.product_details_table.column(self.fields[0], width=75)
        self.product_details_table.column(self.fields[1], width=280)
        self.product_details_table.column(self.fields[2], width=280)
        self.product_details_table.column(self.fields[3], width=100)

        for field in self.fields:
            self.product_details_table.heading(field, text=field)

        self.product_details_table['show'] = 'headings'
        self.product_details_table.pack(fill ='both', expand=1)

        self.product_details_table.bind("<Button-1>",self.focus_data)
        self.load_data()

    def menu_frame(self):
        self.menu_frame = tk.Frame(self)
        self.menu_frame.grid(row=3, columnspan=2)

        self.add_button = tk.Button(self.menu_frame, text="Add", command=lambda: (self.forget(), add_product_details()))
        self.add_button.grid(row = 0, column=0)

        self.edit_button = tk.Button(self.menu_frame, text="Edit", command=lambda: (self.edit()))
        self.edit_button.grid(row = 0, column=1)

        self.delete_button = tk.Button(self.menu_frame, text="Delete", command=lambda: self.delete())
        self.delete_button.grid(row=0, column=2)

        self.export_button = tk.Button(self.menu_frame, text="Export", command=lambda: self.export())
        self.export_button.grid(row=0, column=3)

        self.menu_button = tk.Button(self.menu_frame, text="Back", command=lambda: (self.forget(), m.menu()))
        self.menu_button.grid(row=0, column=5)

    def focus_data(self, event):
        global product_details_data
        self.reset()
        self.view_info = self.product_details_table.focus()
        self.product_details_selected = self.product_details_table.item(self.view_info)
        product_details_data = self.product_details_selected['values']

        self.entry_product_details_id.insert('end', product_details_data[0])
        self.product_selected.set(product_details_data[1])
        self.ingredient_selected.set(product_details_data[2])
        self.entry_quantity.insert('end', product_details_data[3])

    def load_data(self):
        data = database.select('''SELECT product_details_id, p.name as "product_name", i.name as "ingredient_name", quantity
                                FROM product_details pd, products p, ingredients i
                                WHERE pd.product_id = p.product_id
                                AND pd.ingredient_id = i.ingredient_id ORDER BY ''' + self.field_selected.get() + " " + self.order_selected.get(), None)
        if (len(data) != 0):
            self.product_details_table.delete(*self.product_details_table.get_children())
            for row in data:
                self.product_details_table.insert('','end',values=row)

    def reset(self):
        self.entry_product_details_id.delete(0, 'end')
        self.product_menu.selection_clear()
        self.ingredient_menu.selection_clear()
        self.entry_quantity.delete(0, 'end')

    def edit(self):
        if (self.entry_product_details_id.get() == ""):
            tk.messagebox.showerror('Error','Select an entry')
        else:
            self.forget()
            edit_product_details()

    def delete(self):
        try:
            if (self.entry_product_details_id.get() == ""):
                tk.messagebox.showerror('Error','Select an entry')
            else:
                confirmation = tk.messagebox.askquestion('Delete Data','Are you sure you want to delete this entry')
                if confirmation == 'yes':
                    data = (self.entry_product_details_id.get(), self.entry_quantity.get())
                    database.delete("Product_Details ", "Product_details_id = ? and quantity = ? ", data)
                    self.load_data()
        except sqlite3.IntegrityError:
            tk.messagebox.showerror('Error','Deletion Failed')

    def export(self):
        current_date_and_time = datetime.datetime.now()
        current_date_and_time_string = str(current_date_and_time)
        extension = ".csv"
        file_name =  current_date_and_time_string + extension
        with open(file_name, 'w') as fp:
            csvwriter = csv.writer(fp, delimiter=',')
            csvwriter.writerow(self.fields)
            for row_id in self.product_details_table.get_children():
                row = self.product_details_table.item(row_id)['values']
                csvwriter.writerow(row)
            tk.messagebox.showinfo("Save to CSV file","File was saved")

class add_product_details(tk.Frame):
    def __init__(self):
        super().__init__()
        self.pack()
        self.title_frame = tk.Frame(self)
        self.title_frame.grid(row=0,columnspan=2, column=0)

        self.title_text = tk.Label(self.title_frame, text="Add Product_Details", pady=30, font=("Lucida Grande", 20, 'bold'))
        self.title_text.grid(columnspan=2)

        self.display_frame()
        self.menu_frame()

    def display_frame(self):
        self.left_frame = tk.Frame(self, width=310, height=150, padx=2, pady=10)
        self.left_frame.grid(row=1, column=0, sticky=tk.NW)

        self.status_ingredient = tk.IntVar()
        self.status_ingredient.set(1)
        self.check = tk.Checkbutton(self.left_frame, text='Existing Ingredient',variable=self.status_ingredient, onvalue=1, offvalue=0, command=self.checkbox_1)
        self.check.grid(row=2, column = 0)

        self.status_product = tk.IntVar()
        self.status_product.set(1)
        self.check = tk.Checkbutton(self.left_frame, width=15, text='Existing Product',variable=self.status_product, onvalue=1, offvalue=0, command=self.checkbox_2)
        self.check.grid(row=0, column = 0)

        self.add_ingredient_frame = tk.Frame(self.left_frame)
        self.add_product_frame = tk.Frame(self.left_frame)
        self.checkbox_1()
        self.checkbox_2()

        self.label_quantity = tk.Label(self.left_frame, text="Quantity: ", anchor=tk.W,justify='left')
        self.label_quantity.grid(row=4, column=0, sticky=tk.NW, padx=5)
        self.entry_quantity = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_quantity.grid(row=4, column=1)

    def menu_frame(self):
        self.menu_frame = tk.Frame(self)
        self.menu_frame.grid(row=2, columnspan=2)

        self.add_button = tk.Button(self.menu_frame, text="Add", command=lambda: self.add())
        self.add_button.grid(row = 0, column=1)

        self.menu_button = tk.Button(self.menu_frame, text="Back", command=lambda: (self.forget(), display()))
        self.menu_button.grid(row=0, column=2)

    def add(self):
        confirmation = tk.messagebox.askquestion('Add Data','Are you sure you want to enter this data')
        if confirmation == 'yes':
            if (self.status_ingredient.get() == 1):
                self.ingredient_id = database.selectone("SELECT ingredient_id FROM INGREDIENTS where ingredients.name = ?", (self.ingredient_selected.get(),))
            else:
                database.insert("Ingredients", "(Null,?,?,?,?)",(self.entry_ingredient_name.get(),self.entry_ingredient_stock.get(), self.entry_ingredient_minimun_stock.get(), self.entry_ingredient_unit.get()))
                self.ingredient_id = database.selectone("SELECT ingredient_id FROM INGREDIENTS where ingredients.name = ?", (self.entry_ingredient_name.get(),))
            if (self.status_product.get() == 1):
               self.product_id = database.selectone("SELECT product_id FROM products where products.name = ?", (self.product_selected.get(),))
            else:
                database.insert("Product", "(Null,?,?,?)",(self.entry_product_name.get(),self.entry_price.get(), self.entry_description.get()))
                self.product_id = database.selectone("SELECT product_id FROM Products where products.name = ?", (self.entry_product_name.get(),))
            data = (self.ingredient_id[0], self.product_id[0], self.entry_quantity.get())
            database.insert("Product_details ", "(Null,?,?,?)", data)

    def checkbox_1(self):
        if (self.status_ingredient.get() == 1):
            self.add_ingredient_frame.grid_forget()
            self.ingredient_selection_frame = tk.Frame(self.left_frame)
            self.ingredient_selection_frame.grid(row=3, column=0, columnspan=2, sticky=tk.NW)

            self.name_fields = []
            for row in database.select("SELECT DISTINCT name FROM ingredients", None):
                self.name_fields += row

            self.ingredient_selected = tk.StringVar()

            self.label_ingredient_name = tk.Label(self.ingredient_selection_frame,width=16, text="Ingredient Name: ", anchor=tk.W,justify='left')
            self.label_ingredient_name.grid(row=0, column=0, sticky=tk.NW, padx=5)

            self.ingredient_menu = tk.OptionMenu(self.ingredient_selection_frame, self.ingredient_selected , *self.name_fields)
            self.ingredient_menu.config(width=35)
            self.ingredient_menu.grid(row=0, column=1, sticky=tk.NW, padx=5)

        elif (self.status_ingredient.get() != 1):
            self.ingredient_selection_frame.grid_forget()
            self.add_ingredient_frame = tk.Frame(self.left_frame)
            self.add_ingredient_frame.grid(row=3, column=0, columnspan=2, sticky=tk.NW)

            self.label_ingredient_name = tk.Label(self.add_ingredient_frame,width=16, text="Ingredient Name: ", anchor=tk.W,justify='left')
            self.label_ingredient_name.grid(row=1, column=0, sticky=tk.NW, padx=5)
            self.entry_ingredient_name = tk.Entry(self.add_ingredient_frame, width=35,justify='left')
            self.entry_ingredient_name.grid(row=1, column=1)

            self.label_ingredient_stock = tk.Label(self.add_ingredient_frame,text="Ingredient Stock: ", anchor=tk.W,justify='left')
            self.label_ingredient_stock.grid(row=2, column=0, sticky=tk.NW, padx=5)
            self.entry_ingredient_stock = tk.Entry(self.add_ingredient_frame, width=35,justify='left')
            self.entry_ingredient_stock.grid(row=2, column=1)

            self.label_ingredient_minimun_stock = tk.Label(self.add_ingredient_frame, text="Minimum Stock: ", anchor=tk.W,justify='left')
            self.label_ingredient_minimun_stock.grid(row=3, column=0, sticky=tk.NW, padx=5)
            self.entry_ingredient_minimun_stock = tk.Entry(self.add_ingredient_frame, width=35,justify='left')
            self.entry_ingredient_minimun_stock.grid(row=3, column=1)

            self.label_ingredient_unit = tk.Label(self.add_ingredient_frame,text="Unit Used: ", anchor=tk.W,justify='left')
            self.label_ingredient_unit.grid(row=4, column=0, sticky=tk.NW, padx=5)
            self.entry_ingredient_unit = tk.Entry(self.add_ingredient_frame, width=35,justify='left')
            self.entry_ingredient_unit.grid(row=4, column=1)

    def checkbox_2(self):
        if (self.status_product.get() == 1):
            self.add_product_frame.grid_forget()
            self.product_selection_frame = tk.Frame(self.left_frame)
            self.product_selection_frame.grid(row=1, column=0, columnspan=2, sticky=tk.NW)

            self.name_fields = []
            for row in database.select("SELECT name FROM products", None):
                self.name_fields += row

            self.product_selected = tk.StringVar()

            self.label_product_name = tk.Label(self.product_selection_frame,width=15, text="Product Name: ", anchor=tk.W,justify='left')
            self.label_product_name.grid(row=0, column=0, sticky=tk.NW, padx=5)

            self.product_menu = tk.OptionMenu(self.product_selection_frame, self.product_selected , *self.name_fields)
            self.product_menu.config(width=35)
            self.product_menu.grid(row=0, column=1, sticky=tk.NW, padx=5)

        elif (self.status_product.get() != 1):
            self.product_selection_frame.grid_forget()
            self.add_product_frame = tk.Frame(self.left_frame)
            self.add_product_frame.grid(row=1, column=0, columnspan=2, sticky=tk.NW)

            self.label_product_name = tk.Label(self.add_product_frame, width=16, text="Product Name: ", anchor=tk.W,justify='left')
            self.label_product_name.grid(row=1, column=0, sticky=tk.NW, padx=5)
            self.entry_product_name = tk.Entry(self.add_product_frame, width=35,justify='left')
            self.entry_product_name.grid(row=1, column=1)

            self.label_price = tk.Label(self.add_product_frame,text="Price: ", anchor=tk.W,justify='left')
            self.label_price.grid(row=3, column=0, sticky=tk.NW, padx=5)
            self.entry_price = tk.Entry(self.add_product_frame, width=35,justify='left')
            self.entry_price.grid(row=3, column=1)

            self.label_description = tk.Label(self.add_product_frame,text="Description: ", anchor=tk.W,justify='left')
            self.label_description.grid(row=4, column=0, sticky=tk.NW, padx=5)
            self.entry_description = tk.Entry(self.add_product_frame, width=35,justify='left')
            self.entry_description.grid(row=4, column=1)


class edit_product_details(tk.Frame):
    def __init__(self):
        super().__init__()
        self.pack()
        self.title_frame = tk.Frame(self)
        self.title_frame.grid(row=0,columnspan=2, column=0)

        self.title_text = tk.Label(self.title_frame, text="Edit Product Details", pady=30, font=("Lucida Grande", 20, 'bold'))
        self.title_text.grid(columnspan=2)

        self.display_frame()
        self.menu_frame()

    def display_frame(self):
        self.left_frame = tk.Frame(self, width=310, height=150, padx=2, pady=10)
        self.left_frame.grid(row=1, column=0, sticky=tk.NW)

        self.status_ingredient = tk.IntVar()
        self.status_ingredient.set(1)
        self.check = tk.Checkbutton(self.left_frame, text='Existing Ingredient',variable=self.status_ingredient, onvalue=1, offvalue=0, command=self.checkbox_1)
        self.check.grid(row=2, column = 0)

        self.status_product = tk.IntVar()
        self.status_product.set(1)
        self.check = tk.Checkbutton(self.left_frame, width=15, text='Existing Product',variable=self.status_product, onvalue=1, offvalue=0, command=self.checkbox_2)
        self.check.grid(row=0, column = 0)

        self.add_ingredient_frame = tk.Frame(self.left_frame)
        self.add_product_frame = tk.Frame(self.left_frame)
        self.checkbox_1()
        self.checkbox_2()

        self.label_quantity = tk.Label(self.left_frame, text="Quantity: ", anchor=tk.W,justify='left')
        self.label_quantity.grid(row=4, column=0, sticky=tk.NW, padx=5)
        self.entry_quantity = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_quantity.grid(row=4, column=1)

        self.product_selected.set(product_details_data[1])
        self.ingredient_selected.set(product_details_data[2])
        self.entry_quantity.insert('end', product_details_data[3])

    def menu_frame(self):
        self.menu_frame = tk.Frame(self)
        self.menu_frame.grid(row=2, columnspan=2)

        self.edit_button = tk.Button(self.menu_frame, text="Edit", command=lambda: self.edit())
        self.edit_button.grid(row = 0, column=1)

        self.menu_button = tk.Button(self.menu_frame, text="Back", command=lambda: (self.forget(), display()))
        self.menu_button.grid(row=0, column=2)

    def edit(self):
        confirmation = tk.messagebox.askquestion('Edit Data','Are you sure you want to edit this entry')
        if confirmation == 'yes':
            if (self.status_ingredient.get() == 1):
                self.ingredient_id = database.selectone("SELECT ingredient_id FROM INGREDIENTS where ingredients.name = ?", (self.ingredient_selected.get(),))
            else:
                database.insert("Ingredients", "(Null,?,?,?,?)",(self.entry_ingredient_name.get(),self.entry_ingredient_stock.get(), self.entry_ingredient_minimun_stock.get(), self.entry_ingredient_unit.get()))
                self.ingredient_id = database.selectone("SELECT ingredient_id FROM INGREDIENTS where ingredients.name = ?", (self.entry_ingredient_name.get(),))
            if (self.status_product.get() == 1):
               self.product_id = database.selectone("SELECT product_id FROM products where products.name = ?", (self.product_selected.get(),))
            else:
                database.insert("Product", "(Null,?,?,?)",(self.entry_product_name.get(),self.entry_price.get(), self.entry_description.get()))
                self.product_id = database.selectone("SELECT product_id FROM Products where products.name = ?", (self.entry_product_name.get(),))
            data = (self.ingredient_id[0], self.product_id[0], self.entry_quantity.get(), product_details_data[0])
            database.update("Product_details ", "ingredient_id = ?, product_id = ?, quantity = ?", "product_details_id like ?", data)

    def checkbox_1(self):
        if (self.status_ingredient.get() == 1):
            self.add_ingredient_frame.grid_forget()
            self.ingredient_selection_frame = tk.Frame(self.left_frame)
            self.ingredient_selection_frame.grid(row=3, column=0, columnspan=2, sticky=tk.NW)

            self.name_fields = []
            for row in database.select("SELECT DISTINCT name FROM ingredients", None):
                self.name_fields += row

            self.ingredient_selected = tk.StringVar()

            self.label_ingredient_name = tk.Label(self.ingredient_selection_frame,width=16, text="Ingredient Name: ", anchor=tk.W,justify='left')
            self.label_ingredient_name.grid(row=0, column=0, sticky=tk.NW, padx=5)

            self.ingredient_menu = tk.OptionMenu(self.ingredient_selection_frame, self.ingredient_selected , *self.name_fields)
            self.ingredient_menu.config(width=35)
            self.ingredient_menu.grid(row=0, column=1, sticky=tk.NW, padx=5)

        elif (self.status_ingredient.get() != 1):
            self.ingredient_selection_frame.grid_forget()
            self.add_ingredient_frame = tk.Frame(self.left_frame)
            self.add_ingredient_frame.grid(row=3, column=0, columnspan=2, sticky=tk.NW)

            self.label_ingredient_name = tk.Label(self.add_ingredient_frame,width=16, text="Ingredient Name: ", anchor=tk.W,justify='left')
            self.label_ingredient_name.grid(row=1, column=0, sticky=tk.NW, padx=5)
            self.entry_ingredient_name = tk.Entry(self.add_ingredient_frame, width=35,justify='left')
            self.entry_ingredient_name.grid(row=1, column=1)

            self.label_ingredient_stock = tk.Label(self.add_ingredient_frame,text="Ingredient Stock: ", anchor=tk.W,justify='left')
            self.label_ingredient_stock.grid(row=2, column=0, sticky=tk.NW, padx=5)
            self.entry_ingredient_stock = tk.Entry(self.add_ingredient_frame, width=35,justify='left')
            self.entry_ingredient_stock.grid(row=2, column=1)

            self.label_ingredient_minimun_stock = tk.Label(self.add_ingredient_frame, text="Minimum Stock: ", anchor=tk.W,justify='left')
            self.label_ingredient_minimun_stock.grid(row=3, column=0, sticky=tk.NW, padx=5)
            self.entry_ingredient_minimun_stock = tk.Entry(self.add_ingredient_frame, width=35,justify='left')
            self.entry_ingredient_minimun_stock.grid(row=3, column=1)

            self.label_ingredient_unit = tk.Label(self.add_ingredient_frame,text="Unit Used: ", anchor=tk.W,justify='left')
            self.label_ingredient_unit.grid(row=4, column=0, sticky=tk.NW, padx=5)
            self.entry_ingredient_unit = tk.Entry(self.add_ingredient_frame, width=35,justify='left')
            self.entry_ingredient_unit.grid(row=4, column=1)

    def checkbox_2(self):
        if (self.status_product.get() == 1):
            self.add_product_frame.grid_forget()
            self.product_selection_frame = tk.Frame(self.left_frame)
            self.product_selection_frame.grid(row=1, column=0, columnspan=2, sticky=tk.NW)

            self.name_fields = []
            for row in database.select("SELECT name FROM products", None):
                self.name_fields += row

            self.product_selected = tk.StringVar()

            self.label_product_name = tk.Label(self.product_selection_frame,width=15, text="Product Name: ", anchor=tk.W,justify='left')
            self.label_product_name.grid(row=0, column=0, sticky=tk.NW, padx=5)

            self.product_menu = tk.OptionMenu(self.product_selection_frame, self.product_selected , *self.name_fields)
            self.product_menu.config(width=35)
            self.product_menu.grid(row=0, column=1, sticky=tk.NW, padx=5)

        elif (self.status_product.get() != 1):
            self.product_selection_frame.grid_forget()
            self.add_product_frame = tk.Frame(self.left_frame)
            self.add_product_frame.grid(row=1, column=0, columnspan=2, sticky=tk.NW)

            self.label_product_name = tk.Label(self.add_product_frame, width=16, text="Product Name: ", anchor=tk.W,justify='left')
            self.label_product_name.grid(row=1, column=0, sticky=tk.NW, padx=5)
            self.entry_product_name = tk.Entry(self.add_product_frame, width=35,justify='left')
            self.entry_product_name.grid(row=1, column=1)

            self.label_price = tk.Label(self.add_product_frame,text="Price: ", anchor=tk.W,justify='left')
            self.label_price.grid(row=3, column=0, sticky=tk.NW, padx=5)
            self.entry_price = tk.Entry(self.add_product_frame, width=35,justify='left')
            self.entry_price.grid(row=3, column=1)

            self.label_description = tk.Label(self.add_product_frame,text="Description: ", anchor=tk.W,justify='left')
            self.label_description.grid(row=4, column=0, sticky=tk.NW, padx=5)
            self.entry_description = tk.Entry(self.add_product_frame, width=35,justify='left')
            self.entry_description.grid(row=4, column=1)
