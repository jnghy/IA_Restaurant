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

        self.title_text = tk.Label(self.title_frame, text="Restock Display", pady=30, font=("Lucida Grande", 20, 'bold'))
        self.title_text.grid(columnspan=2)

        self.navigation_frame()
        self.display_frame()
        self.table_frame()
        self.menu_frame()

    def navigation_frame(self):

        self.fields_frame = tk.Frame(self)
        self.fields_frame.grid(row=1, column=0, sticky=tk.NW)

        self.columns = ["Restock_Id", "i.Name","Quantity","Total_Cost", "Supplier","Date"]

        self.field_selected = tk.StringVar()
        self.fields_menu = tk.OptionMenu(self.fields_frame, self.field_selected , *self.columns)
        self.fields_menu.config(width=20)
        self.fields_menu.grid(row=0, column = 1)

        self.field_selected.set("restock_id")

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

        self.label_restock_id = tk.Label(self.left_frame,text="Restock ID: ", anchor=tk.W,justify='left')
        self.label_restock_id.grid(row=0, column=0, sticky=tk.NW, padx=5)
        self.entry_restock_id = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_restock_id.grid(row=0, column=1)

        self.name_fields = []
        for row in database.select("SELECT DISTINCT name FROM ingredients", None):
            self.name_fields += row

        self.ingredient_selected = tk.StringVar()

        self.label_ingredient_name = tk.Label(self.left_frame, text="Ingredient Name: ", anchor=tk.W,justify='left')
        self.label_ingredient_name.grid(row=1, column=0, sticky=tk.NW, padx=5)

        self.ingredient_menu = tk.OptionMenu(self.left_frame, self.ingredient_selected , *self.name_fields)
        self.ingredient_menu.config(width=35)
        self.ingredient_menu.grid(row=1, column = 1)

        self.label_restock_quantity = tk.Label(self.left_frame, text="Restock Quantity: ", anchor=tk.W,justify='left')
        self.label_restock_quantity.grid(row=2, column=0, sticky=tk.NW, padx=5)
        self.entry_restock_quantity = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_restock_quantity.grid(row=2, column=1)

        self.label_cost = tk.Label(self.left_frame,text="Cost: ", anchor=tk.W,justify='left')
        self.label_cost.grid(row=3, column=0, sticky=tk.NW, padx=5)
        self.entry_cost = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_cost.grid(row=3, column=1)

        self.label_supplier = tk.Label(self.left_frame,text="Supplier: ", anchor=tk.W,justify='left')
        self.label_supplier.grid(row=4, column=0, sticky=tk.NW, padx=5)
        self.entry_supplier = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_supplier.grid(row=4, column=1)

        self.label_date = tk.Label(self.left_frame,text="Date: ", anchor=tk.W,justify='left')
        self.label_date.grid(row=5, column=0, sticky=tk.NW, padx=5)
        self.entry_date = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_date.grid(row=5, column=1)

    def table_frame(self):
        self.fields = ["Id", "Ingredient Name","Quantity","Cost", "Supplier","Date"]

        self.right_frame = tk.Frame(self, bd=5, width=600, height=200, padx=2, pady=5)
        self.right_frame.grid(row=2, column=1)

        scroll_x = tk.Scrollbar(self.right_frame, orient='horizontal')
        scroll_y = tk.Scrollbar(self.right_frame, orient='vertical')

        self.restock_table = ttk.Treeview(self.right_frame, height=12, column=self.fields, xscrollcommand = scroll_x.set, yscrollcommand = scroll_y.set)

        scroll_x.pack(side='bottom', fill='x')
        scroll_y.pack(side='bottom', fill='y')

        self.restock_table.column(self.fields[0], width=75)
        self.restock_table.column(self.fields[1], width=150)
        self.restock_table.column(self.fields[2], width=100)
        self.restock_table.column(self.fields[3], width=100)
        self.restock_table.column(self.fields[4], width=100)
        self.restock_table.column(self.fields[5], width=100)

        for field in self.fields:
            self.restock_table.heading(field, text=field)

        self.restock_table['show'] = 'headings'
        self.restock_table.pack(fill ='both', expand=1)

        self.restock_table.bind("<Button-1>",self.focus_data)
        self.load_data()

    def menu_frame(self):
        self.menu_frame = tk.Frame(self)
        self.menu_frame.grid(row=3, columnspan=2)

        self.add_button = tk.Button(self.menu_frame, text="Add", command=lambda: (self.forget(), add_restock()))
        self.add_button.grid(row = 0, column=0)

        self.edit_button = tk.Button(self.menu_frame, text="Edit", command=lambda: (self.edit()))
        self.edit_button.grid(row = 0, column=1)

        self.delete_button = tk.Button(self.menu_frame, text="Delete", command=lambda: self.delete())
        self.delete_button.grid(row=0, column=2)

        self.export_button = tk.Button(self.menu_frame, text="Export", command=lambda: self.export())
        self.export_button.grid(row=0, column=3)

        self.menu_button = tk.Button(self.menu_frame, text="Back", command=lambda: (self.forget(), m.menu()))
        self.menu_button.grid(row=0, column=4)

    def focus_data(self, event):
        global restock_data
        self.reset()
        self.view_info = self.restock_table.focus()
        self.restock_selected = self.restock_table.item(self.view_info)
        restock_data = self.restock_selected['values']
        self.entry_restock_id.insert('end', restock_data[0])
        self.ingredient_selected.set(restock_data[1])
        self.entry_restock_quantity.insert('end', restock_data[2])
        self.entry_cost.insert('end', restock_data[3])
        self.entry_supplier.insert('end', restock_data[4])
        self.entry_date.insert('end', restock_data[5])

    def load_data(self):
        data = database.select('''SELECT r.restock_id, i.name as 'Ingredient Name',  r.quantity, r.total_cost, r.supplier, r.date
                               FROM  ingredients I, Restocks R
                               WHERE I.ingredient_id = r.ingredient_id
                               ORDER BY ''' + self.field_selected.get() + " " + self.order_selected.get(), None)
        if (len(data) != 0):
            self.restock_table.delete(*self.restock_table.get_children())
            for row in data:
                self.restock_table.insert('','end',values=row)

    def reset(self):
        self.entry_restock_id.delete(0, 'end')
        self.ingredient_menu.selection_clear()
        self.entry_restock_quantity.delete(0, 'end')
        self.entry_cost.delete(0, 'end')
        self.entry_supplier.delete(0, 'end')
        self.entry_date.delete(0, 'end')

    def edit(self):
        if (self.entry_restock_id.get() == ""):
            tk.messagebox.showerror('Error','Select an entry')
        else:
            self.forget()
            edit_restock()

    def delete(self):
        try:
            if (self.entry_restock_id.get() == ""):
                tk.messagebox.showerror('Error','Select an entry')
            else:
                confirmation = tk.messagebox.askquestion('Delete Data','Are you sure you want to delete this entry')
                if confirmation == 'yes':
                    data = (self.entry_restock_id.get())
                    database.delete("Restocks", "restock_id = ?", (data,))
                    self.load_data()
                    self.reset()
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
            for row_id in self.restock_table.get_children():
                row = self.restock_table.item(row_id)['values']
                csvwriter.writerow(row)
            tk.messagebox.showinfo("Save to CSV file","File was saved")

class add_restock(tk.Frame):
    def __init__(self):
        super().__init__()
        self.pack()
        self.title_frame = tk.Frame(self)
        self.title_frame.grid(row=0,columnspan=2, column=0)

        self.title_text = tk.Label(self.title_frame, text="Add Restock", pady=30, font=("Lucida Grande", 20, 'bold'))
        self.title_text.grid(columnspan=2)

        self.display_frame()
        self.menu_frame()

    def display_frame(self):
        self.left_frame = tk.Frame(self, width=310, height=150, padx=2, pady=10)
        self.left_frame.grid(row=1, column=0, sticky=tk.NW)

        self.label_restock_quantity = tk.Label(self.left_frame, text="Restock Quantity: ", anchor=tk.W,justify='left')
        self.label_restock_quantity.grid(row=0, column=0, sticky=tk.NW, padx=5)
        self.entry_restock_quantity = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_restock_quantity.grid(row=0, column=1)

        self.label_cost = tk.Label(self.left_frame,text="Cost: ", anchor=tk.W,justify='left')
        self.label_cost.grid(row=1, column=0, sticky=tk.NW, padx=5)
        self.entry_cost = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_cost.grid(row=1, column=1)

        self.label_supplier = tk.Label(self.left_frame,text="Supplier: ", anchor=tk.W,justify='left')
        self.label_supplier.grid(row=2, column=0, sticky=tk.NW, padx=5)
        self.entry_supplier = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_supplier.grid(row=2, column=1)

        self.label_date = tk.Label(self.left_frame,text="Date: ", anchor=tk.W,justify='left')
        self.label_date.grid(row=3, column=0, sticky=tk.NW, padx=5)
        self.entry_date = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_date.grid(row=3, column=1)

        self.status_ingredient = tk.IntVar()
        self.status_ingredient.set(1)
        self.check = tk.Checkbutton(self.left_frame, text='Existing Ingredient',variable=self.status_ingredient, onvalue=1, offvalue=0, command=self.checkbox)
        self.check.grid(row=4, column = 0)

        self.add_ingredient_frame = tk.Frame(self.left_frame)
        self.checkbox()

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
            data = (self.ingredient_id[0], self.entry_restock_quantity.get(), self.entry_cost.get(), self.entry_supplier.get(), self.entry_date.get())
            database.insert("Restocks ", "(Null,?,?,?,?,?)", data)
            self.ingredient_quantity = database.selectone("SELECT stock FROM INGREDIENTS where ingredient_id = " + (str(self.ingredient_id[0])),None)
            self.added_stock = int(self.entry_restock_quantity.get()) + int(self.ingredient_quantity[0])
            self.stock_data = (self.added_stock, self.ingredient_id[0])
            database.update("Ingredients ", "stock = ?", "Ingredient_id = ?", self.stock_data)

    def checkbox(self):
        if (self.status_ingredient.get() == 1):
            self.add_ingredient_frame.destroy()
            self.selection_frame = tk.Frame(self.left_frame)
            self.selection_frame = tk.Frame(self.left_frame)
            self.selection_frame.grid(row=5, column=0, columnspan=2, sticky=tk.NW, padx=5)

            self.name_fields = []
            for row in database.select("SELECT DISTINCT name FROM ingredients", None):
                self.name_fields += row

            self.ingredient_selected = tk.StringVar()

            self.label_ingredient_name = tk.Label(self.selection_frame, text="Ingredient Name: ", anchor=tk.W,justify='left')
            self.label_ingredient_name.grid(row=0, column=0, sticky=tk.NW, padx=5)

            self.ingredient_menu = tk.OptionMenu(self.selection_frame, self.ingredient_selected , *self.name_fields)
            self.ingredient_menu.config(width=35)
            self.ingredient_menu.grid(row=0, column=1, sticky=tk.NW, padx=5)
        else:
            self.selection_frame.destroy()
            self.add_ingredient_frame = tk.Frame(self.left_frame)
            self.add_ingredient_frame.grid(row=5, column=0, columnspan=2, sticky=tk.NW, padx=5)

            self.label_ingredient_name = tk.Label(self.add_ingredient_frame, text="Ingredient Name: ", anchor=tk.W,justify='left')
            self.label_ingredient_name.grid(row=1, column=0, sticky=tk.NW, padx=5)
            self.entry_ingredient_name = tk.Entry(self.add_ingredient_frame,  width=35,justify='left')
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

class edit_restock(tk.Frame):
    def __init__(self):
        super().__init__()
        self.pack()
        self.title_frame = tk.Frame(self)
        self.title_frame.grid(row=0,columnspan=2, column=0)

        self.title_text = tk.Label(self.title_frame, text="Edit Restock", pady=30, font=("Lucida Grande", 20, 'bold'))
        self.title_text.grid(columnspan=2)

        self.display_frame()
        self.menu_frame()

    def display_frame(self):
        self.left_frame = tk.Frame(self, width=310, height=150, padx=2, pady=10)
        self.left_frame.grid(row=1, column=0, sticky=tk.NW)

        self.label_restock_quantity = tk.Label(self.left_frame, text="Restock Quantity: ", anchor=tk.W,justify='left')
        self.label_restock_quantity.grid(row=0, column=0, sticky=tk.NW, padx=5)
        self.entry_restock_quantity = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_restock_quantity.grid(row=0, column=1)

        self.label_cost = tk.Label(self.left_frame,text="Cost: ", anchor=tk.W,justify='left')
        self.label_cost.grid(row=1, column=0, sticky=tk.NW, padx=5)
        self.entry_cost = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_cost.grid(row=1, column=1)

        self.label_supplier = tk.Label(self.left_frame,text="Supplier: ", anchor=tk.W,justify='left')
        self.label_supplier.grid(row=2, column=0, sticky=tk.NW, padx=5)
        self.entry_supplier = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_supplier.grid(row=2, column=1)

        self.label_date = tk.Label(self.left_frame,text="Date: ", anchor=tk.W,justify='left')
        self.label_date.grid(row=3, column=0, sticky=tk.NW, padx=5)
        self.entry_date = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_date.grid(row=3, column=1)

        self.status_ingredient = tk.IntVar()
        self.status_ingredient.set(1)
        self.check = tk.Checkbutton(self.left_frame, text='Existing Ingredient',variable=self.status_ingredient, onvalue=1, offvalue=0, command=self.checkbox)
        self.check.grid(row=4, column = 0)

        self.add_ingredient_frame = tk.Frame(self.left_frame)
        self.checkbox()

        self.ingredient_selected.set(restock_data[1])
        self.entry_restock_quantity.insert('end', restock_data[2])
        self.entry_cost.insert('end', restock_data[3])
        self.entry_supplier.insert('end', restock_data[4])
        self.entry_date.insert('end', restock_data[5])

    def menu_frame(self):
        self.menu_frame = tk.Frame(self)
        self.menu_frame.grid(row=2, columnspan=2)

        self.edit_button = tk.Button(self.menu_frame, text="Edit", command=lambda: self.edit())
        self.edit_button.grid(row = 0, column=1)

        self.menu_button = tk.Button(self.menu_frame, text="Back", command=lambda: (self.forget(), display()))
        self.menu_button.grid(row=0, column=2)

    def edit(self):
        confirmation = tk.messagebox.askquestion('Edit Data','Are you sure you want to edit this data')
        if confirmation == 'yes':
            if (self.status_ingredient.get() == 1):
                self.ingredient_id = database.selectone("SELECT ingredient_id FROM INGREDIENTS where ingredients.name = ?", (self.ingredient_selected.get(),))
            else:
                database.insert("Ingredients", "(Null,?,?,?,?)",(self.entry_ingredient_name.get(),self.entry_ingredient_stock.get(), self.entry_ingredient_minimun_stock.get(), self.entry_ingredient_unit.get()))
                self.ingredient_id = database.selectone("SELECT ingredient_id FROM INGREDIENTS where ingredients.name = ?", (self.entry_ingredient_name.get(),))

            data = (self.ingredient_id[0], self.entry_restock_quantity.get(), self.entry_cost.get(), self.entry_supplier.get(), self.entry_date.get(), restock_data[0])
            database.update("Restocks ", "Ingredient_id = ?, quantity = ?, total_cost = ?, supplier = ?, date = ?", "restock_id like ?", data)

            self.ingredient_quantity = database.selectone("SELECT stock FROM INGREDIENTS where ingredient_id = " + (str(self.ingredient_id[0])),None)
            self.added_stock = int(self.entry_restock_quantity.get()) - int(restock_data[2]) + int(self.ingredient_quantity[0])
            self.stock_data = (self.added_stock, self.ingredient_id[0])
            database.update("Ingredients ", "stock = ?", "Ingredient_id = ?", self.stock_data)

    def checkbox(self):
        if (self.status_ingredient.get() == 1):
            self.add_ingredient_frame.destroy()
            self.selection_frame = tk.Frame(self.left_frame)
            self.selection_frame = tk.Frame(self.left_frame)
            self.selection_frame.grid(row=5, column=0, columnspan=2, sticky=tk.NW, padx=5)

            self.name_fields = []
            for row in database.select("SELECT DISTINCT name FROM ingredients", None):
                self.name_fields += row

            self.ingredient_selected = tk.StringVar()

            self.label_ingredient_name = tk.Label(self.selection_frame, text="Ingredient Name: ", anchor=tk.W,justify='left')
            self.label_ingredient_name.grid(row=0, column=0, sticky=tk.NW, padx=5)

            self.ingredient_menu = tk.OptionMenu(self.selection_frame, self.ingredient_selected , *self.name_fields)
            self.ingredient_menu.config(width=35)
            self.ingredient_menu.grid(row=0, column=1, sticky=tk.NW, padx=5)
        else:
            self.selection_frame.destroy()
            self.add_ingredient_frame = tk.Frame(self.left_frame)
            self.add_ingredient_frame.grid(row=5, column=0, columnspan=2, sticky=tk.NW, padx=5)

            self.label_ingredient_name = tk.Label(self.add_ingredient_frame, text="Ingredient Name: ", anchor=tk.W,justify='left')
            self.label_ingredient_name.grid(row=1, column=0, sticky=tk.NW, padx=5)
            self.entry_ingredient_name = tk.Entry(self.add_ingredient_frame,  width=35,justify='left')
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







