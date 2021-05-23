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

        self.title_text = tk.Label(self.title_frame, text="Order Details Display", pady=30, font=("Lucida Grande", 20, 'bold'))
        self.title_text.grid(columnspan=2)

        self.navigation_frame()
        self.display_frame()
        self.table_frame()
        self.menu_frame()

    def navigation_frame(self):

        self.fields_frame = tk.Frame(self)
        self.fields_frame.grid(row=1, column=0, sticky=tk.NW)

        self.columns = ["order_detail_id", "customer_name","o.date","p.name","quantity"]

        self.field_selected = tk.StringVar()
        self.fields_menu = tk.OptionMenu(self.fields_frame, self.field_selected , *self.columns)
        self.fields_menu.config(width=20)
        self.fields_menu.grid(row=0, column = 1)

        self.field_selected.set("order_detail_id")

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

        self.label_order_details_id = tk.Label(self.left_frame,text="Order Details ID: ", anchor=tk.W,justify='left')
        self.label_order_details_id.grid(row=0, column=0, sticky=tk.NW, padx=5)
        self.entry_order_details_id = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_order_details_id.grid(row=0, column=1)

        self.name_fields = []
        for row in database.select('''SELECT DISTINCT last_name || ', ' || first_name
                                    FROM order_details od, orders o, customers c, products p
                                    WHERE od.order_id = o.order_id
                                    AND c.customer_id = o.customer_id
                                    AND p.product_id = od.product_id''', None):
            self.name_fields += row

        self.customer_selected = tk.StringVar()

        self.label_customer_name = tk.Label(self.left_frame, text="Customer Name: ", anchor=tk.W,justify='left')
        self.label_customer_name.grid(row=1, column=0, sticky=tk.NW, padx=5)

        self.customer_list = tk.OptionMenu(self.left_frame, self.customer_selected , *self.name_fields)
        self.customer_list.config(width=35)
        self.customer_list.grid(row=1, column = 1)

        self.label_order_date = tk.Label(self.left_frame,text="Order Date: ", anchor=tk.W,justify='left')
        self.label_order_date.grid(row=2, column=0, sticky=tk.NW, padx=5)
        self.entry_order_date = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_order_date.grid(row=2, column=1)

        self.product_fields = []
        for row in database.select("SELECT name FROM products", None):
            self.product_fields += row

        self.product_selected = tk.StringVar()

        self.label_product_name = tk.Label(self.left_frame, text="Product Name: ", anchor=tk.W,justify='left')
        self.label_product_name.grid(row=3, column=0, sticky=tk.NW, padx=5)

        self.product_list = tk.OptionMenu(self.left_frame, self.product_selected , *self.product_fields)
        self.product_list.config(width=35)
        self.product_list.grid(row=3, column = 1)

        self.label_quantity = tk.Label(self.left_frame,text="Quantity: ", anchor=tk.W,justify='left')
        self.label_quantity.grid(row=4, column=0, sticky=tk.NW, padx=5)
        self.entry_quantity = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_quantity.grid(row=4, column=1)

    def table_frame(self):
        self.fields = ["Id", "Customer Name", "Order Date","Product Name","Quantity"]

        self.right_frame = tk.Frame(self, bd=5, width=600, height=200, padx=2, pady=5)
        self.right_frame.grid(row=2, column=1)

        scroll_x = tk.Scrollbar(self.right_frame, orient='horizontal')
        scroll_y = tk.Scrollbar(self.right_frame, orient='vertical')

        self.order_table = ttk.Treeview(self.right_frame, height=12, column=self.fields, xscrollcommand = scroll_x.set, yscrollcommand = scroll_y.set)

        scroll_x.pack(side='bottom', fill='x')
        scroll_y.pack(side='bottom', fill='y')

        self.order_table.column(self.fields[0], width=50)
        self.order_table.column(self.fields[1], width=200)
        self.order_table.column(self.fields[2], width=100)
        self.order_table.column(self.fields[3], width=200)
        self.order_table.column(self.fields[4], width=100)

        for field in self.fields:
            self.order_table.heading(field, text=field)

        self.order_table['show'] = 'headings'
        self.order_table.pack(fill ='both', expand=1)

        self.order_table.bind("<Button-1>",self.focus_data)
        self.load_data()

    def menu_frame(self):
        self.menu_frame = tk.Frame(self)
        self.menu_frame.grid(row=3, columnspan=2)

        self.add_button = tk.Button(self.menu_frame, text="Add", command=lambda: (self.forget(), add_order_details()))
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
        global order_details_data
        self.reset()
        self.view_info = self.order_table.focus()
        self.order_detail_selected = self.order_table.item(self.view_info)
        order_details_data = self.order_detail_selected['values']
        self.entry_order_details_id.insert('end', order_details_data[0])
        self.customer_selected.set(order_details_data[1])
        self.entry_order_date.insert('end',order_details_data[2])
        self.product_selected.set(order_details_data[3])
        self.entry_quantity.insert('end',order_details_data[4])

    def load_data(self):
        data = database.select('''SELECT order_detail_id, last_name || ', ' || first_name as "customer_name", o.date,  p.name, quantity
                                FROM order_details od, orders o, customers c, products p
                                WHERE od.order_id = o.order_id
                                AND c.customer_id = o.customer_id
                                AND p.product_id = od.product_id
                                order by ''' + self.field_selected.get() + " " + self.order_selected.get(), None)
        if (len(data) != 0):
            self.order_table.delete(*self.order_table.get_children())
            for row in data:
                self.order_table.insert('','end',values=row)

    def reset(self):
        self.entry_order_details_id.delete(0, 'end')
        self.entry_order_date.delete(0, 'end')
        self.entry_quantity.delete(0, 'end')
        self.customer_list.selection_clear()
        self.product_list.selection_clear()

    def edit(self):
        if (self.entry_order_details_id.get() == ""):
            tk.messagebox.showerror('Error','Select an entry')
        else:
            self.forget()
            edit_order_details()

    def delete(self):
        try:
            if (self.entry_order_details_id.get() == ""):
                tk.messagebox.showerror('Error','Select an entry')
            else:
                confirmation = tk.messagebox.askquestion('Delete Data','Are you sure you want to delete this entry')
                if confirmation == 'yes':
                    data = (self.entry_order_details_id.get(), self.entry_quantity.get())
                    database.delete("order_details ", "Order_detail_id = ? and quantity = ?", data)
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
            for row_id in self.order_table.get_children():
                row = self.order_table.item(row_id)['values']
                csvwriter.writerow(row)
            tk.messagebox.showinfo("Save to CSV file","File was saved")

class add_order_details(tk.Frame):
    def __init__(self):
        super().__init__()
        self.pack()
        self.title_frame = tk.Frame(self)
        self.title_frame.grid(row=0,columnspan=2, column=0)

        self.title_text = tk.Label(self.title_frame, text="Add Order Details", pady=30, font=("Lucida Grande", 20, 'bold'))
        self.title_text.grid(columnspan=2)

        self.display_frame()
        self.menu_frame()

    def display_frame(self):
        self.left_frame = tk.Frame(self, width=310, height=150, padx=2, pady=10)
        self.left_frame.grid(row=2, column=0, sticky=tk.NW)

        self.status_order = tk.IntVar()
        self.status_order.set(1)
        self.check = tk.Checkbutton(self.left_frame, text='Existing Order',variable=self.status_order, onvalue=1, offvalue=0, command=self.checkbox_1)
        self.check.grid(row=0, column = 0, sticky=tk.NW)

        self.add_order_frame = tk.Frame(self.left_frame)

        self.status_product = tk.IntVar()
        self.status_product.set(1)
        self.check = tk.Checkbutton(self.left_frame, text='Existing Product',variable=self.status_product, onvalue=1, offvalue=0, command=self.checkbox_2)
        self.check.grid(row=2, column = 0, sticky=tk.NW, )

        self.add_product_frame = tk.Frame(self.left_frame)

        self.checkbox_1()
        self.checkbox_2()

        self.label_quantity = tk.Label(self.left_frame,text="Quantity: ", width=15, anchor=tk.W,justify='left')
        self.label_quantity.grid(row=4, column=0, sticky=tk.NW, padx=5)
        self.entry_quantity = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_quantity.grid(row=4, column=1)

    def checkbox_1(self):
        if (self.status_order.get() == 1):
            self.add_order_frame.grid_forget()
            self.order_selection_frame = tk.Frame(self.left_frame)
            self.order_selection_frame.grid(row=1, column=0, columnspan=2, sticky=tk.NW)

            self.order_fields = []
            for row in database.select('''SELECT DISTINCT last_name || ', ' || first_name || ' - '  || o.date FROM order_details od, orders o, customers c
                                        WHERE od.order_id = o.order_id
                                        AND c.customer_id = o.customer_id''', None):
                self.order_fields += row

            self.order_selected = tk.StringVar()

            self.label_order = tk.Label(self.order_selection_frame,width=15, text="Order: ", anchor=tk.W,justify='left')
            self.label_order.grid(row=0, column=0, sticky=tk.NW, padx=5)

            self.order_menu = tk.OptionMenu(self.order_selection_frame, self.order_selected , *self.order_fields)
            self.order_menu.config(width=35)
            self.order_menu.grid(row=0, column=1, sticky=tk.NW, padx=5)

        elif (self.status_order.get() != 1):
            self.order_selection_frame.grid_forget()
            self.add_order_frame = tk.Frame(self.left_frame)
            self.add_order_frame.grid(row=1, column=0, columnspan=2, sticky=tk.NW)

            self.label_date =tk.Label(self.add_order_frame,text="Date: ", anchor=tk.W,justify='left')
            self.label_date.grid(row=1, column=0, sticky=tk.NW, padx=5)
            self.entry_date = tk.Entry(self.add_order_frame, width=35,justify='left')
            self.entry_date.grid(row=1, column=1)

            self.label_cost = tk.Label(self.add_order_frame,text="Cost: ", anchor=tk.W,justify='left')
            self.label_cost.grid(row=2, column=0, sticky=tk.NW, padx=5)
            self.entry_cost = tk.Entry(self.add_order_frame, width=35,justify='left')
            self.entry_cost.grid(row=2, column=1)

            self.label_payment_method = tk.Label(self.add_order_frame,text="Payment Method: ", anchor=tk.W,justify='left')
            self.label_payment_method.grid(row=3, column=0, sticky=tk.NW, padx=5)
            self.entry_payment_method = tk.Entry(self.add_order_frame, width=35,justify='left')
            self.entry_payment_method.grid(row=3, column=1)

            self.label_discount = tk.Label(self.add_order_frame,text="Discount: ", anchor=tk.W,justify='left')
            self.label_discount.grid(row=4, column=0, sticky=tk.NW, padx=5)
            self.entry_discount = tk.Entry(self.add_order_frame, width=35,justify='left')
            self.entry_discount.grid(row=4, column=1)

            self.status_customer = tk.IntVar()
            self.status_customer.set(1)
            self.check = tk.Checkbutton(self.add_order_frame, text='Existing Customer',variable=self.status_customer, onvalue=1, offvalue=0, command=self.checkbox_1_1)
            self.check.grid(row=5, column = 0, sticky=tk.NW)

            self.add_customer_frame = tk.Frame(self.add_order_frame)
            self.checkbox_1_1()

    def checkbox_1_1(self):
        if (self.status_customer.get() == 1):
            self.add_customer_frame.destroy()
            self.selection_frame = tk.Frame(self.add_order_frame)
            self.selection_frame.grid(row=6, column=0, columnspan=2, sticky=tk.NW)

            self.name_fields = []
            for row in database.select("SELECT last_name || ', ' || first_name FROM customers", None):
                self.name_fields += row

            self.customer_selected = tk.StringVar()

            self.label_customer_name = tk.Label(self.selection_frame,width=15, text="Customer Name: ", anchor=tk.W,justify='left')
            self.label_customer_name.grid(row=0, column=0, sticky=tk.NW, padx=5)

            self.customer_list = tk.OptionMenu(self.selection_frame, self.customer_selected , *self.name_fields)
            self.customer_list.config(width=35)
            self.customer_list.grid(row=0, column = 1, padx=5)

        else:
            self.selection_frame.destroy()

            self.add_customer_frame = tk.Frame(self.add_order_frame)
            self.add_customer_frame.grid(row=6, column=0, columnspan=2, sticky=tk.NW)

            self.label_last_name = tk.Label(self.add_customer_frame, width=16, text="Last Name: ", anchor=tk.W,justify='left')
            self.label_last_name.grid(row=1, column=0, sticky=tk.NW, padx=5)
            self.entry_last_name = tk.Entry(self.add_customer_frame, width=35,justify='left')
            self.entry_last_name.grid(row=1, column=1)

            self.label_first_name = tk.Label(self.add_customer_frame, text="First Name: ", anchor=tk.W,justify='left')
            self.label_first_name.grid(row=2, column=0, sticky=tk.NW, padx=5)
            self.entry_first_name = tk.Entry(self.add_customer_frame, width=35,justify='left')
            self.entry_first_name.grid(row=2, column=1)

            self.label_phone_number = tk.Label(self.add_customer_frame, text="Phone_Number: ", anchor=tk.W,justify='left')
            self.label_phone_number.grid(row=3, column=0, sticky=tk.NW, padx=5)
            self.entry_phone_number = tk.Entry(self.add_customer_frame, width=35,justify='left')
            self.entry_phone_number.grid(row=3, column=1)

            self.label_city = tk.Label(self.add_customer_frame, text="City: ", anchor=tk.W,justify='left')
            self.label_city.grid(row=4, column=0, sticky=tk.NW, padx=5)
            self.entry_city = tk.Entry(self.add_customer_frame, width=35,justify='left')
            self.entry_city.grid(row=4, column=1)

            self.label_address = tk.Label(self.add_customer_frame, text="Address: ", anchor=tk.W,justify='left')
            self.label_address.grid(row=5, column=0, sticky=tk.NW, padx=5)
            self.entry_address = tk.Entry(self.add_customer_frame, width=35,justify='left')
            self.entry_address.grid(row=5, column=1)

    def checkbox_2(self):
        if (self.status_product.get() == 1):
            self.add_product_frame.grid_forget()
            self.product_selection_frame = tk.Frame(self.left_frame)
            self.product_selection_frame.grid(row=3, column=0, columnspan=2, sticky=tk.NW)

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
            self.add_product_frame.grid(row=3, column=0, columnspan=2, sticky=tk.NW)

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

    def menu_frame(self):
        self.menu_frame = tk.Frame(self)
        self.menu_frame.grid(row=10, columnspan=2)

        self.add_button = tk.Button(self.menu_frame, text="Add", command=lambda: self.add())
        self.add_button.grid(row = 0, column=1)

        self.menu_button = tk.Button(self.menu_frame, text="Back", command=lambda: (self.forget(), display()))
        self.menu_button.grid(row=0, column=2)

    def add(self):
        confirmation = tk.messagebox.askquestion('Add Data','Are you sure you want to enter this data')
        if confirmation == 'yes':
            if (self.status_order.get() == 1):
                self.order_id = database.selectone('''SELECT order_id
                                                    FROM(SELECT o.order_id, last_name || ', ' || first_name || ' - '  || o.date  as info
                                                        FROM order_details od, orders o, customers c
                                                        WHERE od.order_id = o.order_id
                                                        AND c.customer_id = o.customer_id)
                                                    WHERE info = ?''', (self.order_selected.get(),))
            else:
                if (self.status_customer.get() == 1):
                    self.customer_id = database.selectone("SELECT customer_id FROM (SELECT customer_id, last_name || ', ' || first_name as name FROM customers) where name = ?", (self.customer_selected.get(),))
                else:
                    database.insert("Customers", "(Null,?,?,?,?,?)",(self.entry_last_name.get(),self.entry_first_name.get(), self.entry_phone_number.get(), self.entry_city.get(),self.entry_address.get()))
                    self.customer_id = database.selectone("SELECT customer_id FROM CUSTOMERS where first_name = ? and last_name = ?", (self.entry_first_name.get(),self.entry_last_name.get() ))

                database.insert("Orders ", "(Null,?,?,?,?,?)", (self.entry_cost.get(), self.entry_payment_method.get(), self.entry_date.get(), self.customer_id[0] , self.entry_discount.get()))
                self.data_order = (self.entry_date.get(), self.customer_id[0])
                self.order_id = database.selectone("SELECT order_id FROM ORDERS where date = ? and customer_id = ?", self.data_order)

            if (self.status_product.get() == 1):
               self.product_id = database.selectone("SELECT product_id FROM products where products.name = ?", (self.product_selected.get(),))
            else:
                database.insert("Products", "(Null,?,?,?)",(self.entry_product_name.get(),self.entry_price.get(), self.entry_description.get()))
                self.product_id = database.selectone("SELECT product_id FROM Products where products.name = ?", (self.entry_product_name.get(),))
            data = (self.order_id[0],self.product_id[0], self.entry_quantity.get())
            database.insert("Order_details", "(Null,?,?,?)",data)

            self.order_detail_id = database.selectone("SELECT order_detail_id FROM Order_details where order_id = ? and product_id = ? and quantity = ? ",data)
            print(self.order_detail_id)
            for row in (database.select('''SELECT i.stock -  od.quantity * pd.quantity, i.ingredient_id
                        FROM order_details od, products p, product_details pd, ingredients i
                        WHERE p.product_id = od.product_id
                        AND pd.ingredient_id = i.ingredient_id
                        AND order_detail_id = ?''', (self.order_detail_id[0],))):
                database.update("Ingredients ", "stock = ? ", "ingredient_id like ?", (row[0],row[1]))

class edit_order_details(tk.Frame):
    def __init__(self):
        super().__init__()
        self.pack()
        self.title_frame = tk.Frame(self)
        self.title_frame.grid(row=0,columnspan=2, column=0)

        self.title_text = tk.Label(self.title_frame, text="Edit Order Details", pady=30, font=("Lucida Grande", 20, 'bold'))
        self.title_text.grid(columnspan=2)

        self.display_frame()
        self.menu_frame()

    def display_frame(self):
        self.left_frame = tk.Frame(self, width=310, height=150, padx=2, pady=10)
        self.left_frame.grid(row=2, column=0, sticky=tk.NW)

        self.status_order = tk.IntVar()
        self.status_order.set(1)
        self.check = tk.Checkbutton(self.left_frame, text='Existing Order',variable=self.status_order, onvalue=1, offvalue=0, command=self.checkbox_1)
        self.check.grid(row=0, column = 0, sticky=tk.NW)

        self.add_order_frame = tk.Frame(self.left_frame)

        self.status_product = tk.IntVar()
        self.status_product.set(1)
        self.check = tk.Checkbutton(self.left_frame, text='Existing Product',variable=self.status_product, onvalue=1, offvalue=0, command=self.checkbox_2)
        self.check.grid(row=2, column = 0, sticky=tk.NW, )

        self.add_product_frame = tk.Frame(self.left_frame)

        self.checkbox_1()
        self.checkbox_2()

        self.label_quantity = tk.Label(self.left_frame,text="Quantity: ", width=15, anchor=tk.W,justify='left')
        self.label_quantity.grid(row=4, column=0, sticky=tk.NW, padx=5)
        self.entry_quantity = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_quantity.grid(row=4, column=1)

        self.entry_quantity.insert('end',order_details_data[4])

        self.order_selected.set(database.selectone('''SELECT last_name || ', ' || first_name || ' - ' || date
                                                    FROM (SELECT last_name, first_name, last_name || ', ' || first_name as name, o.date
                                                    FROM order_details od, orders o, customers c
                                                    WHERE od.order_id = o.order_id
                                                    AND c.customer_id = o.customer_id)
                                                    WHERE name = ?
                                                    AND date = ?''', (order_details_data[1],order_details_data[2]))[0])

        self.product_selected.set(order_details_data[3])

    def checkbox_1(self):
        if (self.status_order.get() == 1):
            self.add_order_frame.grid_forget()
            self.order_selection_frame = tk.Frame(self.left_frame)
            self.order_selection_frame.grid(row=1, column=0, columnspan=2, sticky=tk.NW)

            self.order_fields = []
            for row in database.select('''SELECT last_name || ', ' || first_name || ' - '  || o.date FROM order_details od, orders o, customers c
                                        WHERE od.order_id = o.order_id
                                        AND c.customer_id = o.customer_id''', None):
                self.order_fields += row

            self.order_selected = tk.StringVar()

            self.label_order = tk.Label(self.order_selection_frame,width=15, text="Order: ", anchor=tk.W,justify='left')
            self.label_order.grid(row=0, column=0, sticky=tk.NW, padx=5)

            self.order_menu = tk.OptionMenu(self.order_selection_frame, self.order_selected , *self.order_fields)
            self.order_menu.config(width=35)
            self.order_menu.grid(row=0, column=1, sticky=tk.NW, padx=5)

        elif (self.status_order.get() != 1):
            self.order_selection_frame.grid_forget()
            self.add_order_frame = tk.Frame(self.left_frame)
            self.add_order_frame.grid(row=1, column=0, columnspan=2, sticky=tk.NW)

            self.label_date =tk.Label(self.add_order_frame,text="Date: ", anchor=tk.W,justify='left')
            self.label_date.grid(row=1, column=0, sticky=tk.NW, padx=5)
            self.entry_date = tk.Entry(self.add_order_frame, width=35,justify='left')
            self.entry_date.grid(row=1, column=1)

            self.label_cost = tk.Label(self.add_order_frame,text="Cost: ", anchor=tk.W,justify='left')
            self.label_cost.grid(row=2, column=0, sticky=tk.NW, padx=5)
            self.entry_cost = tk.Entry(self.add_order_frame, width=35,justify='left')
            self.entry_cost.grid(row=2, column=1)

            self.label_payment_method = tk.Label(self.add_order_frame,text="Payment Method: ", anchor=tk.W,justify='left')
            self.label_payment_method.grid(row=3, column=0, sticky=tk.NW, padx=5)
            self.entry_payment_method = tk.Entry(self.add_order_frame, width=35,justify='left')
            self.entry_payment_method.grid(row=3, column=1)

            self.label_discount = tk.Label(self.add_order_frame,text="Discount: ", anchor=tk.W,justify='left')
            self.label_discount.grid(row=4, column=0, sticky=tk.NW, padx=5)
            self.entry_discount = tk.Entry(self.add_order_frame, width=35,justify='left')
            self.entry_discount.grid(row=4, column=1)

            self.status_customer = tk.IntVar()
            self.status_customer.set(1)
            self.check = tk.Checkbutton(self.add_order_frame, text='Existing Customer',variable=self.status_customer, onvalue=1, offvalue=0, command=self.checkbox_1_1)
            self.check.grid(row=5, column = 0, sticky=tk.NW)

            self.add_customer_frame = tk.Frame(self.add_order_frame)
            self.checkbox_1_1()

    def checkbox_1_1(self):
        if (self.status_customer.get() == 1):
            self.add_customer_frame.destroy()
            self.selection_frame = tk.Frame(self.add_order_frame)
            self.selection_frame.grid(row=6, column=0, columnspan=2, sticky=tk.NW)

            self.name_fields = []
            for row in database.select("SELECT last_name || ', ' || first_name FROM customers", None):
                self.name_fields += row

            self.customer_selected = tk.StringVar()

            self.label_customer_name = tk.Label(self.selection_frame,width=15, text="Customer Name: ", anchor=tk.W,justify='left')
            self.label_customer_name.grid(row=0, column=0, sticky=tk.NW, padx=5)

            self.customer_list = tk.OptionMenu(self.selection_frame, self.customer_selected , *self.name_fields)
            self.customer_list.config(width=35)
            self.customer_list.grid(row=0, column = 1, padx=5)

        else:
            self.selection_frame.destroy()

            self.add_customer_frame = tk.Frame(self.add_order_frame)
            self.add_customer_frame.grid(row=6, column=0, columnspan=2, sticky=tk.NW)

            self.label_last_name = tk.Label(self.add_customer_frame, width=16, text="Last Name: ", anchor=tk.W,justify='left')
            self.label_last_name.grid(row=1, column=0, sticky=tk.NW, padx=5)
            self.entry_last_name = tk.Entry(self.add_customer_frame, width=35,justify='left')
            self.entry_last_name.grid(row=1, column=1)

            self.label_first_name = tk.Label(self.add_customer_frame, text="First Name: ", anchor=tk.W,justify='left')
            self.label_first_name.grid(row=2, column=0, sticky=tk.NW, padx=5)
            self.entry_first_name = tk.Entry(self.add_customer_frame, width=35,justify='left')
            self.entry_first_name.grid(row=2, column=1)

            self.label_phone_number = tk.Label(self.add_customer_frame, text="Phone_Number: ", anchor=tk.W,justify='left')
            self.label_phone_number.grid(row=3, column=0, sticky=tk.NW, padx=5)
            self.entry_phone_number = tk.Entry(self.add_customer_frame, width=35,justify='left')
            self.entry_phone_number.grid(row=3, column=1)

            self.label_city = tk.Label(self.add_customer_frame, text="City: ", anchor=tk.W,justify='left')
            self.label_city.grid(row=4, column=0, sticky=tk.NW, padx=5)
            self.entry_city = tk.Entry(self.add_customer_frame, width=35,justify='left')
            self.entry_city.grid(row=4, column=1)

            self.label_address = tk.Label(self.add_customer_frame, text="Address: ", anchor=tk.W,justify='left')
            self.label_address.grid(row=5, column=0, sticky=tk.NW, padx=5)
            self.entry_address = tk.Entry(self.add_customer_frame, width=35,justify='left')
            self.entry_address.grid(row=5, column=1)

    def checkbox_2(self):
        if (self.status_product.get() == 1):
            self.add_product_frame.grid_forget()
            self.product_selection_frame = tk.Frame(self.left_frame)
            self.product_selection_frame.grid(row=3, column=0, columnspan=2, sticky=tk.NW)

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
            self.add_product_frame.grid(row=3, column=0, columnspan=2, sticky=tk.NW)

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

    def menu_frame(self):
        self.menu_frame = tk.Frame(self)
        self.menu_frame.grid(row=10, columnspan=2)

        self.edit_button = tk.Button(self.menu_frame, text="Edit", command=lambda: self.edit())
        self.edit_button.grid(row = 0, column=1)

        self.menu_button = tk.Button(self.menu_frame, text="Back", command=lambda: (self.forget(), display()))
        self.menu_button.grid(row=0, column=2)

    def edit(self):
        confirmation = tk.messagebox.askquestion('Add Data','Are you sure you want to enter this data')
        if confirmation == 'yes':
            if (self.status_order.get() == 1):
                self.order_id = database.selectone('''SELECT order_id
                                                    FROM(SELECT o.order_id, last_name || ', ' || first_name || ' - '  || o.date  as info
                                                        FROM order_details od, orders o, customers c
                                                        WHERE od.order_id = o.order_id
                                                        AND c.customer_id = o.customer_id)
                                                    WHERE info = ?''', (self.order_selected.get(),))
            else:
                if (self.status_customer.get() == 1):
                    self.customer_id = database.selectone("SELECT customer_id FROM (SELECT customer_id, last_name || ', ' || first_name as name FROM customers) where name = ?", (self.customer_selected.get(),))
                else:
                    database.insert("Customers", "(Null,?,?,?,?,?)",(self.entry_last_name.get(),self.entry_first_name.get(), self.entry_phone_number.get(), self.entry_city.get(),self.entry_address.get()))
                    self.customer_id = database.selectone("SELECT customer_id FROM CUSTOMERS where first_name = ? and last_name = ?", (self.entry_first_name.get(),self.entry_last_name.get() ))

                database.insert("Orders ", "(Null,?,?,?,?,?)", (self.entry_cost.get(), self.entry_payment_method.get(), self.entry_date.get(), self.customer_id[0] , self.entry_discount.get()))
                self.data_order = (self.entry_date.get(), self.customer_id[0])
                self.order_id = database.selectone("SELECT order_id FROM ORDERS where date = ? and customer_id = ?", self.data_order)

            if (self.status_product.get() == 1):
               self.product_id = database.selectone("SELECT product_id FROM products where products.name = ?", (self.product_selected.get(),))
            else:
                database.insert("Products", "(Null,?,?,?)",(self.entry_product_name.get(),self.entry_price.get(), self.entry_description.get()))
                self.product_id = database.selectone("SELECT product_id FROM Products where products.name = ?", (self.entry_product_name.get(),))


            data = (self.order_id[0],self.product_id[0], self.entry_quantity.get(),order_details_data[0])
            database.update("Order_details ","Order_id = ?, Product_Id = ?, Quantity = ?", "order_detail_id like ?", data)

            for row in (database.select('''SELECT i.stock, od.quantity, pd.quantity, i.ingredient_id
                        FROM order_details od, products p, product_details pd, ingredients i
                        WHERE p.product_id = od.product_id
                        AND pd.ingredient_id = i.ingredient_id
                        AND order_detail_id = ?''', (order_details_data[0],))):

                if (order_details_data[4] > row[1]):
                    self.stock = row[0] + ((order_details_data[4] - row[1]) * row[2])

                elif (row[1] > order_details_data[4]):
                    self.stock = row[0] - ((row[1] - order_details_data[4]) * row[2])

                database.update("Ingredients ", "stock = ?", "ingredient_id like ?", (self.stock,row[3]))
