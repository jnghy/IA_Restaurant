import tkinter as tk
import tkinter.ttk as ttk
import menu as m
import database
import sqlite3

class display(tk.Frame):

    def __init__(self):
        super().__init__()
        self.pack()

        self.title_frame = tk.Frame(self)
        self.title_frame.grid(row=0,columnspan=2, column=0)

        self.title_text = tk.Label(self.title_frame, text="Product Display", pady=30, font=("Lucida Grande", 20, 'bold'))
        self.title_text.grid(columnspan=2)

        self.navigation_frame()
        self.display_frame()
        self.table_frame()
        self.menu_frame()

    def navigation_frame(self):

        self.fields_frame = tk.Frame(self)
        self.fields_frame.grid(row=1, column=0, sticky=tk.NW)

        self.columns = ["Product_Id", "Name","Price", "Description"]

        self.field_selected = tk.StringVar()
        self.fields_menu = tk.OptionMenu(self.fields_frame, self.field_selected , *self.columns)
        self.fields_menu.config(width=20)
        self.fields_menu.grid(row=0, column = 1)

        self.field_selected.set("Product_Id")

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

        self.label_product_id = tk.Label(self.left_frame,text="Product ID: ", anchor=tk.W,justify='left')
        self.label_product_id.grid(row=0, column=0, sticky=tk.NW, padx=5)
        self.entry_product_id = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_product_id.grid(row=0, column=1)

        self.label_product_name = tk.Label(self.left_frame, text="Product Name: ", anchor=tk.W,justify='left')
        self.label_product_name.grid(row=1, column=0, sticky=tk.NW, padx=5)
        self.entry_product_name = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_product_name.grid(row=1, column=1)

        self.label_price = tk.Label(self.left_frame,text="Price: ", anchor=tk.W,justify='left')
        self.label_price.grid(row=3, column=0, sticky=tk.NW, padx=5)
        self.entry_price = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_price.grid(row=3, column=1)

        self.label_description = tk.Label(self.left_frame,text="Description: ", anchor=tk.W,justify='left')
        self.label_description.grid(row=4, column=0, sticky=tk.NW, padx=5)
        self.entry_description = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_description.grid(row=4, column=1)

    def table_frame(self):
        self.fields = ["Id", "Name","Price","Description"]

        self.right_frame = tk.Frame(self, bd=5, width=600, height=200, padx=2, pady=5)
        self.right_frame.grid(row=2, column=1)

        scroll_x = tk.Scrollbar(self.right_frame, orient='horizontal')
        scroll_y = tk.Scrollbar(self.right_frame, orient='vertical')

        self.product_table = ttk.Treeview(self.right_frame, height=12, column=self.fields, xscrollcommand = scroll_x.set, yscrollcommand = scroll_y.set)

        scroll_x.pack(side='bottom', fill='x')
        scroll_y.pack(side='bottom', fill='y')

        self.product_table.column(self.fields[0], width=75)
        self.product_table.column(self.fields[1], width=280)
        self.product_table.column(self.fields[2], width=100)
        self.product_table.column(self.fields[3], width=300)


        for field in self.fields:
            self.product_table.heading(field, text=field)

        self.product_table['show'] = 'headings'
        self.product_table.pack(fill ='both', expand=1)

        self.product_table.bind("<Button-1>",self.focus_data)
        self.load_data()

    def menu_frame(self):
        self.menu_frame = tk.Frame(self)
        self.menu_frame.grid(row=3, columnspan=2)

        self.add_button = tk.Button(self.menu_frame, text="Add", command=lambda: (self.forget(), add_products()))
        self.add_button.grid(row = 0, column=0)

        self.edit_button = tk.Button(self.menu_frame, text="Edit", command=lambda: (self.edit()))
        self.edit_button.grid(row = 0, column=1)

        self.delete_button = tk.Button(self.menu_frame, text="Delete", command=lambda: self.delete())
        self.delete_button.grid(row=0, column=2)

        '''self.related_button = tk.Button(self.menu_frame, text="See Related")
        self.related_button.grid(row=0, column=3)'''

        self.menu_button = tk.Button(self.menu_frame, text="Back", command=lambda: (self.forget(), m.menu()))
        self.menu_button.grid(row=0, column=4)

    def focus_data(self, event):
        global product_data
        self.reset()
        self.view_info = self.product_table.focus()
        self.product_selected = self.product_table.item(self.view_info)
        product_data = self.product_selected['values']
        self.entry_product_id.insert('end', product_data[0])
        self.entry_product_name.insert('end',product_data[1])
        self.entry_price.insert('end', product_data[2])
        self.entry_description.insert('end', product_data[3])

    def load_data(self):
        data = database.select("SELECT * FROM PRODUCTS ORDER BY " + self.field_selected.get() + " " + self.order_selected.get(), None)
        if (len(data) != 0):
            self.product_table.delete(*self.product_table.get_children())
            for row in data:
                self.product_table.insert('','end',values=row)

    def reset(self):
        self.entry_product_id.delete(0, 'end')
        self.entry_product_name.delete(0, 'end')
        self.entry_price.delete(0, 'end')
        self.entry_description.delete(0, 'end')

    def edit(self):
        if (self.entry_product_id.get() == ""):
            tk.messagebox.showerror('Error','Select an entry')
        else:
            confirmation = tk.messagebox.askquestion('Edit Data','Are you sure you want to edit this data')
            if confirmation == 'yes':
                data = (self.entry_product_name.get(),self.entry_price.get(), self.entry_description.get(), self.entry_product_id.get())
                database.update("Products ", "Name = ?, Price = ?, Description = ?", "product_id like ?", data)
                self.load_data()

    def delete(self):
        try:
            if (self.entry_product_id.get() == ""):
                tk.messagebox.showerror('Error','Select an entry')
            else:
                confirmation = tk.messagebox.askquestion('Delete Data','Are you sure you want to delete this entry')
                if confirmation == 'yes':
                    data = (self.entry_product_id.get())
                    database.delete("Products", "product_id = ?", (data,))
                    self.load_data()
                    self.reset()
        except sqlite3.IntegrityError:
            tk.messagebox.showerror('Error','Deletion Failed')

class add_products(tk.Frame):
    def __init__(self):
        super().__init__()
        self.pack()
        self.title_frame = tk.Frame(self)
        self.title_frame.grid(row=0,columnspan=2, column=0)

        self.title_text = tk.Label(self.title_frame, text="Add Products", pady=30, font=("Lucida Grande", 20, 'bold'))
        self.title_text.grid(columnspan=2)

        self.display_frame()
        self.menu_frame()

    def display_frame(self):
        self.left_frame = tk.Frame(self, width=310, height=150, padx=2, pady=10)
        self.left_frame.grid(row=1, column=0, sticky=tk.NW)

        self.label_product_name = tk.Label(self.left_frame, text="Product Name: ", anchor=tk.W,justify='left')
        self.label_product_name.grid(row=1, column=0, sticky=tk.NW, padx=5)
        self.entry_product_name = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_product_name.grid(row=1, column=1)

        self.label_price = tk.Label(self.left_frame,text="Price: ", anchor=tk.W,justify='left')
        self.label_price.grid(row=3, column=0, sticky=tk.NW, padx=5)
        self.entry_price = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_price.grid(row=3, column=1)

        self.label_description = tk.Label(self.left_frame,text="Description: ", anchor=tk.W,justify='left')
        self.label_description.grid(row=4, column=0, sticky=tk.NW, padx=5)
        self.entry_description = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_description.grid(row=4, column=1)

    def menu_frame(self):
        self.menu_frame = tk.Frame(self)
        self.menu_frame.grid(row=2, columnspan=2)

        self.add_button = tk.Button(self.menu_frame, text="Add", command=lambda: self.add())
        self.add_button.grid(row = 0, column=1)

        self.menu_button = tk.Button(self.menu_frame, text="Back", command=lambda: (self.forget(), display()))
        self.menu_button.grid(row=0, column=2)

    def add(self):
        confirmation = tk.messagebox.askquestion('Edit Data','Are you sure you want to edit this data')
        if confirmation == 'yes':
            data = (self.entry_product_name.get(),self.entry_price.get(), self.entry_description.get())
            database.insert("Products ", "(Null,?, ?, ?)", data)

'''

SELECT pd.product_details_id, p.product_id, p.name, p.description, i.ingredient_id, i.name, pd.quantity
FROM product_details pd, products p, ingredients i
WHERE p.product_id = pd.product_id
AND i.ingredient_id = pd.ingredient_id

'''
