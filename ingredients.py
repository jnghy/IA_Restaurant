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

        self.title_text = tk.Label(self.title_frame, text="Ingredients Display", pady=30, font=("Lucida Grande", 20, 'bold'))
        self.title_text.grid(columnspan=2)

        self.navigation_frame()
        self.display_frame()
        self.table_frame()
        self.menu_frame()

    def navigation_frame(self):

        self.fields_frame = tk.Frame(self)
        self.fields_frame.grid(row=1, column=0, sticky=tk.NW)

        self.columns = ["Ingredient_id", "Name","Stock","Deficit Amount","Units"]

        self.field_selected = tk.StringVar()
        self.fields_menu = tk.OptionMenu(self.fields_frame, self.field_selected , *self.columns)
        self.fields_menu.config(width=20)
        self.fields_menu.grid(row=0, column = 1)

        self.field_selected.set("ingredient_id")

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

        self.label_ingredient_id = tk.Label(self.left_frame,text="Ingredient ID: ", anchor=tk.W,justify='left')
        self.label_ingredient_id.grid(row=0, column=0, sticky=tk.NW, padx=5)
        self.entry_ingredient_id = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_ingredient_id.grid(row=0, column=1)

        self.label_ingredient_name = tk.Label(self.left_frame, text="Ingredient Name: ", anchor=tk.W,justify='left')
        self.label_ingredient_name.grid(row=1, column=0, sticky=tk.NW, padx=5)
        self.entry_ingredient_name = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_ingredient_name.grid(row=1, column=1)

        self.label_ingredient_stock = tk.Label(self.left_frame, text="Ingredient Stock: ", anchor=tk.W,justify='left')
        self.label_ingredient_stock.grid(row=2, column=0, sticky=tk.NW, padx=5)
        self.entry_ingredient_stock = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_ingredient_stock.grid(row=2, column=1)

        self.label_ingredient_minimun_stock = tk.Label(self.left_frame,text="Minimum Stock: ", anchor=tk.W,justify='left')
        self.label_ingredient_minimun_stock.grid(row=3, column=0, sticky=tk.NW, padx=5)
        self.entry_ingredient_minimun_stock = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_ingredient_minimun_stock.grid(row=3, column=1)

        self.label_ingredient_unit = tk.Label(self.left_frame,text="Unit Used: ", anchor=tk.W,justify='left')
        self.label_ingredient_unit.grid(row=4, column=0, sticky=tk.NW, padx=5)
        self.entry_ingredient_unit = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_ingredient_unit.grid(row=4, column=1)

    def table_frame(self):
        self.fields = ["Id", "Name","Stock Amount","Deficit Amount","Units Used"]

        self.right_frame = tk.Frame(self, bd=5, width=600, height=200, padx=2, pady=5)
        self.right_frame.grid(row=2, column=1)

        scroll_x = tk.Scrollbar(self.right_frame, orient='horizontal')
        scroll_y = tk.Scrollbar(self.right_frame, orient='vertical')

        self.ingredient_table = ttk.Treeview(self.right_frame, height=12, column=self.fields, xscrollcommand = scroll_x.set, yscrollcommand = scroll_y.set)

        scroll_x.pack(side='bottom', fill='x')
        scroll_y.pack(side='bottom', fill='y')

        self.ingredient_table.column(self.fields[0], width=75)
        self.ingredient_table.column(self.fields[1], width=280)
        self.ingredient_table.column(self.fields[2], width=100)
        self.ingredient_table.column(self.fields[3], width=100)
        self.ingredient_table.column(self.fields[4], width=100)

        for field in self.fields:
            self.ingredient_table.heading(field, text=field)

        self.ingredient_table['show'] = 'headings'
        self.ingredient_table.pack(fill ='both', expand=1)

        self.ingredient_table.bind("<Button-1>",self.focus_data)
        self.load_data()

    def menu_frame(self):
        self.menu_frame = tk.Frame(self)
        self.menu_frame.grid(row=3, columnspan=2)

        self.add_button = tk.Button(self.menu_frame, text="Add", command=lambda: (self.forget(), add_ingredients()))
        self.add_button.grid(row = 0, column=0)

        self.edit_button = tk.Button(self.menu_frame, text="Edit", command=lambda: (self.edit()))
        self.edit_button.grid(row = 0, column=1)

        self.delete_button = tk.Button(self.menu_frame, text="Delete", command=lambda: self.delete())
        self.delete_button.grid(row=0, column=2)

        self.export_button = tk.Button(self.menu_frame, text="Export", command=lambda: self.export())
        self.export_button.grid(row=0, column=3)

        ''' related buttons '''

        self.menu_button = tk.Button(self.menu_frame, text="Back", command=lambda: (self.forget(), m.menu()))
        self.menu_button.grid(row=0, column=5)

    def focus_data(self, event):
        global ingredient_data
        self.reset()
        self.view_info = self.ingredient_table.focus()
        self.ingredient_selected = self.ingredient_table.item(self.view_info)
        ingredient_data = self.ingredient_selected['values']
        self.entry_ingredient_id.insert('end', ingredient_data[0])
        self.entry_ingredient_name.insert('end', ingredient_data[1])
        self.entry_ingredient_stock.insert('end',ingredient_data[2])
        self.entry_ingredient_minimun_stock.insert('end', ingredient_data[3])
        self.entry_ingredient_unit.insert('end',ingredient_data[4])

    def load_data(self):
        data = database.select("SELECT * FROM INGREDIENTS ORDER BY " + self.field_selected.get() + " " + self.order_selected.get(), None)
        if (len(data) != 0):
            self.ingredient_table.delete(*self.ingredient_table.get_children())
            for row in data:
                self.ingredient_table.insert('','end',values=row)

    def reset(self):
        self.entry_ingredient_id.delete(0, 'end')
        self.entry_ingredient_name.delete(0, 'end')
        self.entry_ingredient_stock.delete(0, 'end')
        self.entry_ingredient_minimun_stock.delete(0, 'end')
        self.entry_ingredient_unit.delete(0, 'end')

    def edit(self):
        if (self.entry_ingredient_id.get() == ""):
            tk.messagebox.showerror('Error','Select an entry')
        else:
            self.forget()
            edit_ingredients()

    def delete(self):
        try:
            if (self.entry_ingredient_id.get() == ""):
                tk.messagebox.showerror('Error','Select an entry')
            else:
                confirmation = tk.messagebox.askquestion('Delete Data','Are you sure you want to delete this entry')
                if confirmation == 'yes':
                    data = (self.entry_ingredient_id.get(), self.entry_ingredient_name.get(), self.entry_ingredient_stock.get(), self.entry_ingredient_minimun_stock.get(), self.entry_ingredient_unit.get())
                    database.delete("Ingredients ", "ingredient_id = ? and name = ? and stock = ? and deficit_amount = ? and units = ?", data)
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
            for row_id in self.ingredient_table.get_children():
                row = self.ingredient_table.item(row_id)['values']
                csvwriter.writerow(row)
            tk.messagebox.showinfo("Save to CSV file","File was saved")

class add_ingredients(tk.Frame):
    def __init__(self):
        super().__init__()
        self.pack()
        self.title_frame = tk.Frame(self)
        self.title_frame.grid(row=0,columnspan=2, column=0)

        self.title_text = tk.Label(self.title_frame, text="Add Ingredients", pady=30, font=("Lucida Grande", 20, 'bold'))
        self.title_text.grid(columnspan=2)

        self.display_frame()
        self.menu_frame()

    def display_frame(self):
        self.left_frame = tk.Frame(self, width=310, height=150, padx=2, pady=10)
        self.left_frame.grid(row=1, column=0, sticky=tk.NW)

        self.label_ingredient_name = tk.Label(self.left_frame, text="Ingredient Name: ", anchor=tk.W,justify='left')
        self.label_ingredient_name.grid(row=1, column=0, sticky=tk.NW, padx=5)
        self.entry_ingredient_name = tk.Entry(self.left_frame,  width=35,justify='left')
        self.entry_ingredient_name.grid(row=1, column=1)

        self.label_ingredient_stock = tk.Label(self.left_frame,text="Ingredient Stock: ", anchor=tk.W,justify='left')
        self.label_ingredient_stock.grid(row=2, column=0, sticky=tk.NW, padx=5)
        self.entry_ingredient_stock = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_ingredient_stock.grid(row=2, column=1)

        self.label_ingredient_minimun_stock = tk.Label(self.left_frame, text="Minimum Stock: ", anchor=tk.W,justify='left')
        self.label_ingredient_minimun_stock.grid(row=3, column=0, sticky=tk.NW, padx=5)
        self.entry_ingredient_minimun_stock = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_ingredient_minimun_stock.grid(row=3, column=1)

        self.label_ingredient_unit = tk.Label(self.left_frame,text="Unit Used: ", anchor=tk.W,justify='left')
        self.label_ingredient_unit.grid(row=4, column=0, sticky=tk.NW, padx=5)
        self.entry_ingredient_unit = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_ingredient_unit.grid(row=4, column=1)

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
            database.insert("Ingredients", "(Null,?,?,?,?)",(self.entry_ingredient_name.get(),self.entry_ingredient_stock.get(), self.entry_ingredient_minimun_stock.get(), self.entry_ingredient_unit.get()))

class edit_ingredients(tk.Frame):
    def __init__(self):
        super().__init__()
        self.pack()
        self.title_frame = tk.Frame(self)
        self.title_frame.grid(row=0,columnspan=2, column=0)

        self.title_text = tk.Label(self.title_frame, text="Add Ingredients", pady=30, font=("Lucida Grande", 20, 'bold'))
        self.title_text.grid(columnspan=2)

        self.display_frame()
        self.menu_frame()

    def display_frame(self):
        self.left_frame = tk.Frame(self, width=310, height=150, padx=2, pady=10)
        self.left_frame.grid(row=1, column=0, sticky=tk.NW)

        self.label_ingredient_name = tk.Label(self.left_frame, text="Ingredient Name: ", anchor=tk.W,justify='left')
        self.label_ingredient_name.grid(row=1, column=0, sticky=tk.NW, padx=5)
        self.entry_ingredient_name = tk.Entry(self.left_frame,  width=35,justify='left')
        self.entry_ingredient_name.grid(row=1, column=1)

        self.label_ingredient_stock = tk.Label(self.left_frame,text="Ingredient Stock: ", anchor=tk.W,justify='left')
        self.label_ingredient_stock.grid(row=2, column=0, sticky=tk.NW, padx=5)
        self.entry_ingredient_stock = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_ingredient_stock.grid(row=2, column=1)

        self.label_ingredient_minimun_stock = tk.Label(self.left_frame, text="Minimum Stock: ", anchor=tk.W,justify='left')
        self.label_ingredient_minimun_stock.grid(row=3, column=0, sticky=tk.NW, padx=5)
        self.entry_ingredient_minimun_stock = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_ingredient_minimun_stock.grid(row=3, column=1)

        self.label_ingredient_unit = tk.Label(self.left_frame,text="Unit Used: ", anchor=tk.W,justify='left')
        self.label_ingredient_unit.grid(row=4, column=0, sticky=tk.NW, padx=5)
        self.entry_ingredient_unit = tk.Entry(self.left_frame, width=35,justify='left')
        self.entry_ingredient_unit.grid(row=4, column=1)

        self.entry_ingredient_name.insert('end', ingredient_data[1])
        self.entry_ingredient_stock.insert('end',ingredient_data[2])
        self.entry_ingredient_minimun_stock.insert('end', ingredient_data[3])
        self.entry_ingredient_unit.insert('end',ingredient_data[4])

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
            data = (self.entry_ingredient_name.get(),self.entry_ingredient_stock.get(), self.entry_ingredient_minimun_stock.get(), self.entry_ingredient_unit.get(),ingredient_data[0])
            database.update("Ingredients ", "name = ?, stock = ?, deficit_amount = ?, units = ?", "Ingredient_id like ?", data)
