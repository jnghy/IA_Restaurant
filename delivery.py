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

        self.title_text = tk.Label(self.title_frame, text="Delivery Display", pady=30, font=("Lucida Grande", 20, 'bold'))
        self.title_text.grid(columnspan=2)

        self.navigation_frame()
        self.display_frame()
        self.table_frame()
        self.menu_frame()

    def navigation_frame(self):

        self.fields_frame = tk.Frame(self)
        self.fields_frame.grid(row=1, column=0, sticky=tk.NW)

        self.columns = ["delivery_id", "customer_name","o.date","delivery_fee"]

        self.field_selected = tk.StringVar()
        self.fields_menu = tk.OptionMenu(self.fields_frame, self.field_selected , *self.columns)
        self.fields_menu.config(width=20)
        self.fields_menu.grid(row=0, column = 1)

        self.field_selected.set("delivery_id")

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

        self.label_delivery_id = tk.Label(self.left_frame,text="Delivery ID: ", anchor=tk.W,justify='left')
        self.label_delivery_id.grid(row=0, column=0, sticky=tk.NW, padx=5)
        self.entry_delivery_id = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_delivery_id.grid(row=0, column=1)

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

        self.label_city = tk.Label(self.left_frame,text="City: ", anchor=tk.W,justify='left')
        self.label_city.grid(row=2, column=0, sticky=tk.NW, padx=5)
        self.entry_city = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_city.grid(row=2, column=1)

        self.label_address = tk.Label(self.left_frame,text="Address: ", anchor=tk.W,justify='left')
        self.label_address.grid(row=3, column=0, sticky=tk.NW, padx=5)
        self.entry_address = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_address.grid(row=3, column=1)

        self.label_order_date = tk.Label(self.left_frame,text="Order Date: ", anchor=tk.W,justify='left')
        self.label_order_date.grid(row=4, column=0, sticky=tk.NW, padx=5)
        self.entry_order_date = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_order_date.grid(row=4, column=1)

        self.label_fee = tk.Label(self.left_frame,text="Fee: ", anchor=tk.W,justify='left')
        self.label_fee.grid(row=5, column=0, sticky=tk.NW, padx=5)
        self.entry_fee = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_fee.grid(row=5, column=1)

    def table_frame(self):
        self.fields = ["Id", "Customer Name", "City","Address","Order Date","Fee"]

        self.right_frame = tk.Frame(self, bd=5, width=600, height=200, padx=2, pady=5)
        self.right_frame.grid(row=2, column=1)

        scroll_x = tk.Scrollbar(self.right_frame, orient='horizontal')
        scroll_y = tk.Scrollbar(self.right_frame, orient='vertical')

        self.delivery_table = ttk.Treeview(self.right_frame, height=12, column=self.fields, xscrollcommand = scroll_x.set, yscrollcommand = scroll_y.set)

        scroll_x.pack(side='bottom', fill='x')
        scroll_y.pack(side='bottom', fill='y')

        self.delivery_table.column(self.fields[0], width=50)
        self.delivery_table.column(self.fields[1], width=100)
        self.delivery_table.column(self.fields[2], width=100)
        self.delivery_table.column(self.fields[3], width=200)
        self.delivery_table.column(self.fields[4], width=100)
        self.delivery_table.column(self.fields[5], width=50)

        for field in self.fields:
            self.delivery_table.heading(field, text=field)

        self.delivery_table['show'] = 'headings'
        self.delivery_table.pack(fill ='both', expand=1)

        self.delivery_table.bind("<Button-1>",self.focus_data)
        self.load_data()

    def menu_frame(self):
        self.menu_frame = tk.Frame(self)
        self.menu_frame.grid(row=3, columnspan=2)

        self.add_button = tk.Button(self.menu_frame, text="Add", command=lambda: (self.forget(), add_delivery()))
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
        global delivery_data
        self.reset()
        self.view_info = self.delivery_table.focus()
        self.order_detail_selected = self.delivery_table.item(self.view_info)
        delivery_data = self.order_detail_selected['values']
        self.entry_delivery_id.insert('end', delivery_data[0])
        self.customer_selected.set(delivery_data[1])
        self.entry_city.insert('end',delivery_data[2])
        self.entry_address.insert('end',delivery_data[3])
        self.entry_order_date.insert('end',delivery_data[4])
        self.entry_fee.insert('end',delivery_data[5])

    def load_data(self):
        data = database.select('''SELECT delivery_id, last_name || ', ' || first_name, city, address, o.date, delivery_fee
                                FROM delivery d, orders o, customers c
                                WHERE d.order_id = o.order_id
                                AND c.customer_id = o.customer_id
                                order by ''' + self.field_selected.get() + " " + self.order_selected.get(), None)
        if (len(data) != 0):
            self.delivery_table.delete(*self.delivery_table.get_children())
            for row in data:
                self.delivery_table.insert('','end',values=row)

    def reset(self):
        self.entry_delivery_id.delete(0, 'end')
        self.customer_list.selection_clear()
        self.entry_city.delete(0, 'end')
        self.entry_address.delete(0, 'end')
        self.entry_order_date.delete(0, 'end')
        self.entry_fee.delete(0, 'end')

    def edit(self):
        if (self.entry_delivery_id.get() == ""):
            tk.messagebox.showerror('Error','Select an entry')
        else:
            self.forget()
            edit_delivery()

    def delete(self):
        try:
            if (self.entry_delivery_id.get() == ""):
                tk.messagebox.showerror('Error','Select an entry')
            else:
                confirmation = tk.messagebox.askquestion('Delete Data','Are you sure you want to delete this entry')
                if confirmation == 'yes':
                    data = (self.entry_delivery_id.get(), self.entry_fee.get())
                    database.delete("delivery ", "delivery_id = ? and delivery_fee = ?", data)
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
            for row_id in self.delivery_table.get_children():
                row = self.delivery_table.item(row_id)['values']
                csvwriter.writerow(row)
            tk.messagebox.showinfo("Save to CSV file","File was saved")

class add_delivery(tk.Frame):
    def __init__(self):
        super().__init__()
        self.pack()
        self.title_frame = tk.Frame(self)
        self.title_frame.grid(row=0,columnspan=2, column=0)

        self.title_text = tk.Label(self.title_frame, text="Add Delivery", pady=30, font=("Lucida Grande", 20, 'bold'))
        self.title_text.grid(columnspan=2)

        self.display_frame()
        self.menu_frame()

    def display_frame(self):
        self.left_frame = tk.Frame(self, width=310, height=150, padx=2, pady=10)
        self.left_frame.grid(row=2, column=0, sticky=tk.NW)

        self.add_order_frame = tk.Frame(self.left_frame)

        self.status_order = tk.IntVar()
        self.status_order.set(1)
        self.check = tk.Checkbutton(self.left_frame, text='Existing Order',variable=self.status_order, onvalue=1, offvalue=0, command=self.checkbox_order())
        self.check.grid(row=0, column = 0, sticky=tk.NW)

        self.checkbox_order()

        self.label_fee = tk.Label(self.left_frame,text="Delivery Fee: ", width=15, anchor=tk.W,justify='left')
        self.label_fee.grid(row=4, column=0, sticky=tk.NW, padx=5)
        self.entry_fee = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_fee.grid(row=4, column=1)

    def checkbox_order(self):
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
            self.check = tk.Checkbutton(self.add_order_frame, text='Existing Customer',variable=self.status_customer, onvalue=1, offvalue=0, command=self.checkbox_customer())
            self.check.grid(row=5, column = 0, sticky=tk.NW)

            self.add_customer_frame = tk.Frame(self.add_order_frame)
            self.checkbox_customer()

    def checkbox_customer(self):
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

            data = (self.order_id[0], self.entry_fee.get())
            database.insert("Delivery", "(Null,?,?)",data)

class edit_delivery(tk.Frame):
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
        self.check = tk.Checkbutton(self.left_frame, text='Existing Order',variable=self.status_order, onvalue=1, offvalue=0, command=self.checkbox_order())
        self.check.grid(row=0, column = 0, sticky=tk.NW)

        self.add_order_frame = tk.Frame(self.left_frame)

        self.checkbox_customer()

        self.label_fee = tk.Label(self.left_frame,text="Delivery Fee: ", width=15, anchor=tk.W,justify='left')
        self.label_fee.grid(row=4, column=0, sticky=tk.NW, padx=5)
        self.entry_fee = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_fee.grid(row=4, column=1)

        self.entry_fee.insert('end',delivery_data[5])

        self.order_selected.set(database.selectone('''SELECT last_name || ', ' || first_name || ' - ' || date
                                                    FROM (SELECT last_name, first_name, last_name || ', ' || first_name as name, o.date
                                                    FROM order_details od, orders o, customers c
                                                    WHERE od.order_id = o.order_id
                                                    AND c.customer_id = o.customer_id)
                                                    WHERE name = ?
                                                    AND date = ?''', (delivery_data[1],delivery_data[4]))[0])

    def checkbox_order(self):
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
            self.check = tk.Checkbutton(self.add_order_frame, text='Existing Customer',variable=self.status_customer, onvalue=1, offvalue=0, command=self.checkbox_customer())
            self.check.grid(row=5, column = 0, sticky=tk.NW)

            self.add_customer_frame = tk.Frame(self.add_order_frame)
            self.checkbox_customer()

    def checkbox_customer(self):
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

            data = (self.order_id[0], self.entry_fee.get(), delivery_data[0])
            database.update("Delivery ", "order_id = ?, delivery_fee = ?", "delivery_id = ?", data)



