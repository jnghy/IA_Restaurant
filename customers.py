import tkinter as tk
import tkinter.ttk as ttk
import menu as m
import database
import sqlite3
import datetime
import csv

'''self.label_ = tk.Label(self.left_frame, text="First Name: ", anchor=tk.W,justify='left')
        self.label_.grid(row=1, column=0, sticky=tk.NW, padx=5)
        self.entry_ = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_.grid(row=1, column=1)'''


class display(tk.Frame):
    def __init__(self):
        super().__init__()
        self.pack()

        self.title_frame = tk.Frame(self)
        self.title_frame.grid(row=0,columnspan=2, column=0)

        self.title_text = tk.Label(self.title_frame, text="Customer Display", pady=30, font=("Lucida Grande", 20, 'bold'))
        self.title_text.grid(columnspan=2)

        self.navigation_frame()
        self.display_frame()
        self.table_frame()
        self.menu_frame()

    def navigation_frame(self):

        self.fields_frame = tk.Frame(self)
        self.fields_frame.grid(row=1, column=0, sticky=tk.NW)

        self.columns = ["Customer_Id", "Last_Name","First_Name","Phone_Number","City","Address"]

        self.field_selected = tk.StringVar()
        self.fields_menu = tk.OptionMenu(self.fields_frame, self.field_selected , *self.columns)
        self.fields_menu.config(width=20)
        self.fields_menu.grid(row=0, column = 1)

        self.field_selected.set("Customer_Id")

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

        self.label_customer_id = tk.Label(self.left_frame,text="Customer ID: ", anchor=tk.W,justify='left')
        self.label_customer_id.grid(row=0, column=0, sticky=tk.NW, padx=5)
        self.entry_customer_id = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_customer_id.grid(row=0, column=1)

        self.label_last_name = tk.Label(self.left_frame, text="Last Name: ", anchor=tk.W,justify='left')
        self.label_last_name.grid(row=1, column=0, sticky=tk.NW, padx=5)
        self.entry_last_name = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_last_name.grid(row=1, column=1)

        self.label_first_name = tk.Label(self.left_frame, text="First Name: ", anchor=tk.W,justify='left')
        self.label_first_name.grid(row=2, column=0, sticky=tk.NW, padx=5)
        self.entry_first_name = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_first_name.grid(row=2, column=1)

        self.label_phone_number = tk.Label(self.left_frame, text="Phone_Number: ", anchor=tk.W,justify='left')
        self.label_phone_number.grid(row=3, column=0, sticky=tk.NW, padx=5)
        self.entry_phone_number = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_phone_number.grid(row=3, column=1)

        self.label_city = tk.Label(self.left_frame, text="City: ", anchor=tk.W,justify='left')
        self.label_city.grid(row=4, column=0, sticky=tk.NW, padx=5)
        self.entry_city = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_city.grid(row=4, column=1)

        self.label_address = tk.Label(self.left_frame, text="Address: ", anchor=tk.W,justify='left')
        self.label_address.grid(row=5, column=0, sticky=tk.NW, padx=5)
        self.entry_address = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_address.grid(row=5, column=1)

    def table_frame(self):
        self.fields = ["Id", "Last Name","First Name","Phone Number","City", "Address"]

        self.right_frame = tk.Frame(self, bd=5, width=600, height=200, padx=2, pady=5)
        self.right_frame.grid(row=2, column=1)

        scroll_x = tk.Scrollbar(self.right_frame, orient='horizontal')
        scroll_y = tk.Scrollbar(self.right_frame, orient='vertical')

        self.customer_table = ttk.Treeview(self.right_frame, height=12, column=self.fields, xscrollcommand = scroll_x.set, yscrollcommand = scroll_y.set)

        scroll_x.pack(side='bottom', fill='x')
        scroll_y.pack(side='bottom', fill='y')

        self.customer_table.column(self.fields[0], width=20)
        self.customer_table.column(self.fields[1], width=150)
        self.customer_table.column(self.fields[2], width=150)
        self.customer_table.column(self.fields[3], width=100)
        self.customer_table.column(self.fields[4], width=75)
        self.customer_table.column(self.fields[5], width=100)


        for field in self.fields:
            self.customer_table.heading(field, text=field)

        self.customer_table['show'] = 'headings'
        self.customer_table.pack(fill ='both', expand=1)

        self.customer_table.bind("<Button-1>",self.focus_data)
        self.load_data()

    def menu_frame(self):
        self.menu_frame = tk.Frame(self)
        self.menu_frame.grid(row=3, columnspan=2)

        self.add_button = tk.Button(self.menu_frame, text="Add", command=lambda: (self.forget(), add_customer()))
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
        global customer_data
        self.reset()
        self.view_info = self.customer_table.focus()
        self.customer_selected = self.customer_table.item(self.view_info)
        customer_data = self.customer_selected['values']
        self.entry_customer_id.insert('end', customer_data[0])
        self.entry_last_name.insert('end', customer_data[1])
        self.entry_first_name.insert('end', customer_data[2])
        self.entry_phone_number.insert('end', customer_data[3])
        self.entry_city.insert('end', customer_data[4])
        self.entry_address.insert('end', customer_data[5])

    def load_data(self):
        data = database.select("SELECT * FROM Customers ORDER BY " + self.field_selected.get() + " " + self.order_selected.get(), None)
        if (len(data) != 0):
            self.customer_table.delete(*self.customer_table.get_children())
            for row in data:
                self.customer_table.insert('','end',values=row)

    def reset(self):
        self.entry_customer_id.delete(0, 'end')
        self.entry_last_name.delete(0, 'end')
        self.entry_first_name.delete(0, 'end')
        self.entry_phone_number.delete(0, 'end')
        self.entry_city.delete(0, 'end')
        self.entry_address.delete(0, 'end')

    def edit(self):
        if (self.entry_customer_id.get() == ""):
            tk.messagebox.showerror('Error','Select an entry')
        else:
            self.forget()
            edit_customer()

    def delete(self):
        try:
            if (self.entry_customer_id.get() == ""):
                tk.messagebox.showerror('Error','Select an entry')
            else:
                confirmation = tk.messagebox.askquestion('Delete Data','Are you sure you want to delete this entry')
                if confirmation == 'yes':
                    data = (self.entry_customer_id.get(), self.entry_last_name.get(), self.entry_first_name.get())
                    database.delete("Customers ", "customer_id = ? and last_name = ? and first_name = ?", data)
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
            for row_id in self.customer_table.get_children():
                row = self.customer_table.item(row_id)['values']
                csvwriter.writerow(row)
            tk.messagebox.showinfo("Save to CSV file","File was saved")

class add_customer(tk.Frame):
    def __init__(self):
        super().__init__()
        self.pack()
        self.title_frame = tk.Frame(self)
        self.title_frame.grid(row=0,columnspan=2, column=0)

        self.title_text = tk.Label(self.title_frame, text="Add Customer", pady=30, font=("Lucida Grande", 20, 'bold'))
        self.title_text.grid(columnspan=2)

        self.display_frame()
        self.menu_frame()

    def display_frame(self):
        self.left_frame = tk.Frame(self, width=310, height=150, padx=2, pady=10)
        self.left_frame.grid(row=1, column=0, sticky=tk.NW)

        self.label_last_name = tk.Label(self.left_frame, text="Last Name: ", anchor=tk.W,justify='left')
        self.label_last_name.grid(row=1, column=0, sticky=tk.NW, padx=5)
        self.entry_last_name = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_last_name.grid(row=1, column=1)

        self.label_first_name = tk.Label(self.left_frame, text="First Name: ", anchor=tk.W,justify='left')
        self.label_first_name.grid(row=2, column=0, sticky=tk.NW, padx=5)
        self.entry_first_name = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_first_name.grid(row=2, column=1)

        self.label_phone_number = tk.Label(self.left_frame, text="Phone_Number: ", anchor=tk.W,justify='left')
        self.label_phone_number.grid(row=3, column=0, sticky=tk.NW, padx=5)
        self.entry_phone_number = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_phone_number.grid(row=3, column=1)

        self.label_city = tk.Label(self.left_frame, text="City: ", anchor=tk.W,justify='left')
        self.label_city.grid(row=4, column=0, sticky=tk.NW, padx=5)
        self.entry_city = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_city.grid(row=4, column=1)

        self.label_address = tk.Label(self.left_frame, text="Address: ", anchor=tk.W,justify='left')
        self.label_address.grid(row=5, column=0, sticky=tk.NW, padx=5)
        self.entry_address = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_address.grid(row=5, column=1)

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
            database.insert("Customers", "(Null,?,?,?,?,?)",(self.entry_last_name.get(),self.entry_first_name.get(), self.entry_phone_number.get(), self.entry_city.get(),self.entry_address.get()))

class edit_customer(tk.Frame):
    def __init__(self):
        super().__init__()
        self.pack()
        self.title_frame = tk.Frame(self)
        self.title_frame.grid(row=0,columnspan=2, column=0)

        self.title_text = tk.Label(self.title_frame, text="Edit Customers", pady=30, font=("Lucida Grande", 20, 'bold'))
        self.title_text.grid(columnspan=2)

        self.display_frame()
        self.menu_frame()

    def display_frame(self):
        self.left_frame = tk.Frame(self, width=310, height=150, padx=2, pady=10)
        self.left_frame.grid(row=1, column=0, sticky=tk.NW)

        self.label_last_name = tk.Label(self.left_frame, text="Last Name: ", anchor=tk.W,justify='left')
        self.label_last_name.grid(row=1, column=0, sticky=tk.NW, padx=5)
        self.entry_last_name = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_last_name.grid(row=1, column=1)

        self.label_first_name = tk.Label(self.left_frame, text="First Name: ", anchor=tk.W,justify='left')
        self.label_first_name.grid(row=2, column=0, sticky=tk.NW, padx=5)
        self.entry_first_name = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_first_name.grid(row=2, column=1)

        self.label_phone_number = tk.Label(self.left_frame, text="Phone_Number: ", anchor=tk.W,justify='left')
        self.label_phone_number.grid(row=3, column=0, sticky=tk.NW, padx=5)
        self.entry_phone_number = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_phone_number.grid(row=3, column=1)

        self.label_city = tk.Label(self.left_frame, text="City: ", anchor=tk.W,justify='left')
        self.label_city.grid(row=4, column=0, sticky=tk.NW, padx=5)
        self.entry_city = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_city.grid(row=4, column=1)

        self.label_address = tk.Label(self.left_frame, text="Address: ", anchor=tk.W,justify='left')
        self.label_address.grid(row=5, column=0, sticky=tk.NW, padx=5)
        self.entry_address = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_address.grid(row=5, column=1)

        self.entry_last_name.insert('end', customer_data[1])
        self.entry_first_name.insert('end', customer_data[2])
        self.entry_phone_number.insert('end', customer_data[3])
        self.entry_city.insert('end', customer_data[4])
        self.entry_address.insert('end', customer_data[5])

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
            data = (self.entry_last_name.get(),self.entry_first_name.get(), self.entry_phone_number.get(), self.entry_city.get(),self.entry_address.get(), customer_data[0])
            database.update("Customers ", "Last_name = ?, First_name = ?, Phone_Number = ?, City = ?, Address = ?", "Customer_id like ?", data)
