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

        self.title_text = tk.Label(self.title_frame, text="Order Display", pady=30, font=("Lucida Grande", 20, 'bold'))
        self.title_text.grid(columnspan=2)

        self.navigation_frame()
        self.display_frame()
        self.table_frame()
        self.menu_frame()

    def navigation_frame(self):

        self.fields_frame = tk.Frame(self)
        self.fields_frame.grid(row=1, column=0, sticky=tk.NW)

        self.columns = ["Order_id", "Customer Name", "Date", "Cost","Payment_Method", "Discount"]

        self.field_selected = tk.StringVar()
        self.fields_menu = tk.OptionMenu(self.fields_frame, self.field_selected , *self.columns)
        self.fields_menu.config(width=20)
        self.fields_menu.grid(row=0, column = 1)

        self.field_selected.set("Order_id")

        self.orders = ["Asc", 'Desc']

        self.order_selected = tk.StringVar()
        self.order_menu = tk.OptionMenu(self.fields_frame, self.order_selected, *self.orders)
        self.order_menu.config(width=8)
        self.order_menu.grid(row=0, column = 2)

        self.order_selected.set("Asc")

        self.load_button = tk.Button(self.fields_frame, text="Load", command=lambda: (self.load_data()))
        self.load_button.grid(row = 0, column=0)

    def display_frame(self):
        self.left_frame = tk.Frame(self, width=310, height=150, padx=2, pady=10)
        self.left_frame.grid(row=2, column=0, sticky=tk.NW)

        self.label_order_id = tk.Label(self.left_frame,text="Order ID: ", anchor=tk.W,justify='left')
        self.label_order_id.grid(row=0, column=0, sticky=tk.NW, padx=5)
        self.entry_order_id = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_order_id.grid(row=0, column=1)

        '''self.name_fields = []
        for row in database.select("SELECT last_name || ', ' || first_name FROM customers", None):
            self.name_fields += row

        self.customer_selected = tk.StringVar()

        self.label_customer_name = tk.Label(self.left_frame, text="Customer Name: ", anchor=tk.W,justify='left')
        self.label_customer_name.grid(row=1, column=0, sticky=tk.NW, padx=5)

        self.customer_list = tk.OptionMenu(self.left_frame, self.customer_selected , *self.name_fields)
        self.customer_list.config(width=35)
        self.customer_list.grid(row=1, column = 1)'''

        self.label_fcustomer = tk.Label(self.left_frame,text="Customer First Name: ", anchor=tk.W,justify='left')
        self.label_fcustomer.grid(row=1, column=0, sticky=tk.NW, padx=5)
        self.entry_fcustomer = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_fcustomer.grid(row=1, column=1)

        self.label_lcustomer = tk.Label(self.left_frame,text="Customer Last Name: ", anchor=tk.W,justify='left')
        self.label_lcustomer.grid(row=2, column=0, sticky=tk.NW, padx=5)
        self.entry_lcustomer = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_lcustomer.grid(row=2, column=1)

        self.label_date = tk.Label(self.left_frame,text="Date: ", anchor=tk.W,justify='left')
        self.label_date.grid(row=3, column=0, sticky=tk.NW, padx=5)
        self.entry_date = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_date.grid(row=3, column=1)

        self.label_cost = tk.Label(self.left_frame,text="Cost: ", anchor=tk.W,justify='left')
        self.label_cost.grid(row=4, column=0, sticky=tk.NW, padx=5)
        self.entry_cost = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_cost.grid(row=4, column=1)

        self.label_payment_method = tk.Label(self.left_frame,text="Payment Method: ", anchor=tk.W,justify='left')
        self.label_payment_method.grid(row=5, column=0, sticky=tk.NW, padx=5)
        self.entry_payment_method = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_payment_method.grid(row=5, column=1)

        self.label_discount = tk.Label(self.left_frame,text="Discount: ", anchor=tk.W,justify='left')
        self.label_discount.grid(row=6, column=0, sticky=tk.NW, padx=5)
        self.entry_discount = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_discount.grid(row=6, column=1)

    def table_frame(self):
        self.fields = ["Id", "First Name", "Last Name","Date","Cost", "Payment Method","Discount"]

        self.right_frame = tk.Frame(self, bd=5, width=600, height=200, padx=2, pady=5)
        self.right_frame.grid(row=2, column=1)

        scroll_x = tk.Scrollbar(self.right_frame, orient='horizontal')
        scroll_y = tk.Scrollbar(self.right_frame, orient='vertical')

        self.order_table = ttk.Treeview(self.right_frame, height=12, column=self.fields, xscrollcommand = scroll_x.set, yscrollcommand = scroll_y.set)

        scroll_x.pack(side='bottom', fill='x')
        scroll_y.pack(side='bottom', fill='y')

        self.order_table.column(self.fields[0], width=75)
        self.order_table.column(self.fields[1], width=100)
        self.order_table.column(self.fields[2], width=100)
        self.order_table.column(self.fields[3], width=100)
        self.order_table.column(self.fields[4], width=100)
        self.order_table.column(self.fields[5], width=100)
        self.order_table.column(self.fields[6], width=100)

        for field in self.fields:
            self.order_table.heading(field, text=field)

        self.order_table['show'] = 'headings'
        self.order_table.pack(fill ='both', expand=1)

        self.order_table.bind("<Button-1>",self.focus_data)
        self.load_data()

    def menu_frame(self):
        self.menu_frame = tk.Frame(self)
        self.menu_frame.grid(row=3, columnspan=2)

        self.add_button = tk.Button(self.menu_frame, text="Add", command=lambda: (self.forget(), add_order()))
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
        global order_data
        self.reset()
        self.view_info = self.order_table.focus()
        self.orders_selected = self.order_table.item(self.view_info)
        order_data = self.orders_selected['values']

        self.entry_order_id.insert('end', order_data[0])
        self.entry_fcustomer.insert('end',order_data[1])
        self.entry_lcustomer.insert('end',order_data[2])
        self.entry_date.insert('end', order_data[3])
        self.entry_cost.insert('end', order_data[4])
        self.entry_payment_method.insert('end', order_data[5])
        self.entry_discount.insert('end', order_data[6])

    def load_data(self):
        data = database.select('''SELECT order_id, first_name, last_name, date, cost, payment_method, discount
                                FROM orders o, customers c
                                WHERE c.customer_id = o.customer_id 
                                ORDER BY ''' + self.field_selected.get() + " " + self.order_selected.get(), None)
        if (len(data) != 0):
            self.order_table.delete(*self.order_table.get_children())
            for row in data:
                self.order_table.insert('','end',values=row)

    def reset(self):
        self.entry_order_id.delete(0, 'end')
        self.entry_fcustomer.delete(0, 'end')
        self.entry_lcustomer.delete(0, 'end')
        self.entry_date.delete(0, 'end')
        self.entry_cost.delete(0, 'end')
        self.entry_payment_method.delete(0, 'end')
        self.entry_discount.delete(0, 'end')

    def edit(self):
        if (self.entry_order_id.get() == ""):
            tk.messagebox.showerror('Error','Select an entry')
        else:
            self.forget()
            edit_order()

    def delete(self):
        try:
            if (self.entry_order_id.get() == ""):
                tk.messagebox.showerror('Error','Select an entry')
            else:
                confirmation = tk.messagebox.askquestion('Delete Data','Are you sure you want to delete this entry')
                if confirmation == 'yes':
                    data = (self.entry_order_id.get())
                    database.delete("Orders", "order_id = ?", (data,))
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
            for row_id in self.order_table.get_children():
                row = self.order_table.item(row_id)['values']
                csvwriter.writerow(row)
            tk.messagebox.showinfo("Save to CSV file","File was saved")

class add_order(tk.Frame):
    def __init__(self):
        super().__init__()
        self.pack()
        self.title_frame = tk.Frame(self)
        self.title_frame.grid(row=0,columnspan=2, column=0)

        self.title_text = tk.Label(self.title_frame, text="Add Order", pady=30, font=("Lucida Grande", 20, 'bold'))
        self.title_text.grid(columnspan=2)

        self.display_frame()
        self.menu_frame()

    def display_frame(self):
        self.left_frame = tk.Frame(self, width=310, height=150, padx=2, pady=10)
        self.left_frame.grid(row=2, column=0, sticky=tk.NW)

        self.label_date = tk.Label(self.left_frame,text="Date: ", anchor=tk.W,justify='left')
        self.label_date.grid(row=1, column=0, sticky=tk.NW, padx=5)
        self.entry_date = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_date.grid(row=1, column=1)

        self.label_cost = tk.Label(self.left_frame,text="Cost: ", anchor=tk.W,justify='left')
        self.label_cost.grid(row=2, column=0, sticky=tk.NW, padx=5)
        self.entry_cost = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_cost.grid(row=2, column=1)

        self.label_payment_method = tk.Label(self.left_frame,text="Payment Method: ", anchor=tk.W,justify='left')
        self.label_payment_method.grid(row=3, column=0, sticky=tk.NW, padx=5)
        self.entry_payment_method = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_payment_method.grid(row=3, column=1)

        self.label_discount = tk.Label(self.left_frame,text="Discount: ", anchor=tk.W,justify='left')
        self.label_discount.grid(row=4, column=0, sticky=tk.NW, padx=5)
        self.entry_discount = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_discount.grid(row=4, column=1)

        self.status_customer = tk.IntVar()
        self.status_customer.set(1)
        self.check = tk.Checkbutton(self.left_frame, text='Existing Customer',variable=self.status_customer, onvalue=1, offvalue=0, command=self.checkbox_customer)
        self.check.grid(row=5, column = 0)

        self.add_customer_frame = tk.Frame(self.left_frame)
        self.checkbox_customer()

    def menu_frame(self):
        self.menu_frame = tk.Frame(self)
        self.menu_frame.grid(row=7, columnspan=2)

        self.add_button = tk.Button(self.menu_frame, text="Add Orders", command=lambda: self.add())
        self.add_button.grid(row = 0, column=0)

        self.menu_button = tk.Button(self.menu_frame, text="Back", command=lambda: (self.forget(), display()))
        self.menu_button.grid(row=0, column=1)

    def add(self):
        confirmation = tk.messagebox.askquestion('Add Data','Are you sure you want to enter this data')
        if confirmation == 'yes':
            if (self.status_customer.get() == 1):
                self.customer_id = database.selectone("SELECT customer_id FROM (SELECT customer_id, last_name || ', ' || first_name as name FROM customers) where name = ?", (self.customer_selected.get(),))
            else:
                database.insert("Customers", "(Null,?,?,?,?,?)",(self.entry_last_name.get(),self.entry_first_name.get(), self.entry_phone_number.get(), self.entry_city.get(),self.entry_address.get()))
                self.customer_id = database.selectone("SELECT customer_id FROM (SELECT customer_id, last_name || ', ' || first_name as name FROM customers) where name = ?", (self.customer_selected.get(),))
            data = (self.entry_cost.get(), self.entry_payment_method.get(), self.entry_date.get(), self.customer_id[0] , self.entry_discount.get())
            database.insert("Orders ", "(Null,?,?,?,?,?)", data)

    def checkbox_customer(self):
        if (self.status_customer.get() == 1):

            self.add_customer_frame.destroy()

            self.selection_frame = tk.Frame(self.left_frame)
            self.selection_frame.grid(row=6, column=0, columnspan=2, sticky=tk.NW, padx=5)

            self.name_fields = []
            for row in database.select("SELECT last_name || ', ' || first_name FROM customers", None):
                self.name_fields += row

            self.customer_selected = tk.StringVar()

            self.label_customer_name = tk.Label(self.selection_frame, text="Customer Name: ", anchor=tk.W,justify='left')
            self.label_customer_name.grid(row=0, column=0, sticky=tk.NW, padx=5)

            self.customer_list = tk.OptionMenu(self.selection_frame, self.customer_selected , *self.name_fields)
            self.customer_list.config(width=35)
            self.customer_list.grid(row=0, column = 1)

        else:
            self.selection_frame.destroy()

            self.add_customer_frame = tk.Frame(self.left_frame)
            self.add_customer_frame.grid(row=6, column=0, columnspan=2, sticky=tk.NW, padx=5)

            self.label_last_name = tk.Label(self.add_customer_frame, text="Last Name: ", anchor=tk.W,justify='left')
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

class edit_order(tk.Frame):
    def __init__(self):
        super().__init__()
        self.pack()
        self.title_frame = tk.Frame(self)
        self.title_frame.grid(row=0,columnspan=2, column=0)

        self.title_text = tk.Label(self.title_frame, text="Edit Order", pady=30, font=("Lucida Grande", 20, 'bold'))
        self.title_text.grid(columnspan=2)

        self.display_frame()
        self.menu_frame()

    def display_frame(self):
        self.left_frame = tk.Frame(self, width=310, height=150, padx=2, pady=10)
        self.left_frame.grid(row=2, column=0, sticky=tk.NW)

        self.label_date = tk.Label(self.left_frame,text="Date: ", anchor=tk.W,justify='left')
        self.label_date.grid(row=1, column=0, sticky=tk.NW, padx=5)
        self.entry_date = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_date.grid(row=1, column=1)

        self.label_cost = tk.Label(self.left_frame,text="Cost: ", anchor=tk.W,justify='left')
        self.label_cost.grid(row=2, column=0, sticky=tk.NW, padx=5)
        self.entry_cost = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_cost.grid(row=2, column=1)

        self.label_payment_method = tk.Label(self.left_frame,text="Payment Method: ", anchor=tk.W,justify='left')
        self.label_payment_method.grid(row=3, column=0, sticky=tk.NW, padx=5)
        self.entry_payment_method = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_payment_method.grid(row=3, column=1)

        self.label_discount = tk.Label(self.left_frame,text="Discount: ", anchor=tk.W,justify='left')
        self.label_discount.grid(row=4, column=0, sticky=tk.NW, padx=5)
        self.entry_discount = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_discount.grid(row=4, column=1)

        self.status_customer = tk.IntVar()
        self.status_customer.set(1)
        self.check = tk.Checkbutton(self.left_frame, text='Existing Customer',variable=self.status_customer, onvalue=1, offvalue=0, command=self.checkbox_customer)
        self.check.grid(row=5, column = 0)

        self.add_customer_frame = tk.Frame(self.left_frame)
        self.checkbox_customer()

        self.entry_date.insert('end', order_data[3])
        self.entry_cost.insert('end', order_data[4])
        self.entry_payment_method.insert('end', order_data[5])
        self.entry_discount.insert('end', order_data[6])

        self.customer_full_name = database.selectone("SELECT last_name || ', ' || first_name FROM customers WHERE last_name = ? and first_name = ?", (order_data[2],order_data[1]))
        self.customer_selected.set(self.customer_full_name[0])

    def menu_frame(self):
        self.menu_frame = tk.Frame(self)
        self.menu_frame.grid(row=7, columnspan=2)

        self.edit_button = tk.Button(self.menu_frame, text="Edit", command=lambda: self.edit())
        self.edit_button.grid(row = 0, column=1)

        self.menu_button = tk.Button(self.menu_frame, text="Back", command=lambda: (self.forget(), display()))
        self.menu_button.grid(row=0, column=2)

    def edit(self):
        confirmation = tk.messagebox.askquestion('Edit Data','Are you sure you want to edit this data')
        if confirmation == 'yes':
            if (self.status_customer.get() == 1):
                self.customer_id = database.selectone("SELECT customer_id FROM (SELECT customer_id, last_name || ', ' || first_name as name FROM customers) where name = ?", (self.customer_selected.get(),))
            else:
                database.insert("Customers", "(Null,?,?,?,?,?)",(self.entry_last_name.get(),self.entry_first_name.get(), self.entry_phone_number.get(), self.entry_city.get(),self.entry_address.get()))
                self.customer_id = database.selectone("SELECT customer_id FROM customers where first_name = ? and last_name = ?", (self.entry_first_name.get(),self.entry_last_name.get()))

            data = (self.entry_cost.get(), self.entry_payment_method.get(), self.entry_date.get(), self.customer_id[0] , self.entry_discount.get(), order_data[0])
            database.update("Orders ", "cost = ?, payment_method = ?, date = ?, customer_id = ?, discount = ?", "order_id like ?", data)

    def checkbox_customer(self):
        if (self.status_customer.get() == 1):

            self.add_customer_frame.destroy()

            self.selection_frame = tk.Frame(self.left_frame)
            self.selection_frame.grid(row=6, column=0, columnspan=2, sticky=tk.NW, padx=5)

            self.name_fields = []
            for row in database.select("SELECT last_name || ', ' || first_name FROM customers", None):
                self.name_fields += row

            self.customer_selected = tk.StringVar()

            self.label_customer_name = tk.Label(self.selection_frame, text="Customer Name: ", anchor=tk.W,justify='left')
            self.label_customer_name.grid(row=0, column=0, sticky=tk.NW, padx=5)

            self.customer_list = tk.OptionMenu(self.selection_frame, self.customer_selected , *self.name_fields)
            self.customer_list.config(width=35)
            self.customer_list.grid(row=0, column = 1)

        else:
            self.selection_frame.destroy()

            self.add_customer_frame = tk.Frame(self.left_frame)
            self.add_customer_frame.grid(row=6, column=0, columnspan=2, sticky=tk.NW, padx=5)

            self.label_last_name = tk.Label(self.add_customer_frame, text="Last Name: ", anchor=tk.W,justify='left')
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










