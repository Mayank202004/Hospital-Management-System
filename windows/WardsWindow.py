import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import Frame
import ttkbootstrap as bs
from ttkbootstrap import Style
from ttkbootstrap.constants import *
import form_windows.wardDetails



class WardsWindow(tk.Tk):
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.frame = Frame(parent, bd=5, relief="flat", bg='black')
        self.frame.pack(fill="both", expand=True)  
        self.setTable()
        self.on_select()
        self.set_widgets()

    def set_widgets(self):
        topframe=Frame(self.frame)
        topframe.place(x=10,y=0,width=1250,height=120)
        tk.Label(topframe, text="Manage Wards", font=("Helvetica", 25, "bold")).place(x=500, y=10)
        bs.Button(topframe, text="Add New Ward",command=self.addWard).place(x=440,y=80)

        #searchby logic
        tk.Label(topframe, text="Searchby:", font=("Helvetica", 10, "bold")).place(x=5,y=80)
        self.searchbycbox=bs.Combobox(topframe,values=['Ward ID','Ward Name','Ward Type'])
        self.searchbycbox.set('Ward Name') # set default as Name 
        self.searchbycbox.configure(state="readonly") #To not allow typing in combobox
        self.searchbycbox.place(x=90,y=80)
        self.searchby_text = tk.Text(topframe, height=1, width=25)
        self.searchby_text.place(x=260,y=80)
        self.searchby_text.bind("<KeyRelease>", lambda event: self.fetch_details()) #keyrelease bind to call function 

    def setTable(self):
        table_frame = Frame(self.frame, bd=5, relief=RIDGE, bg='white')
        table_frame.place(x=10, y=125, width=1250, height=710)

        # Scroll bar making
        s = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        s2 = ttk.Scrollbar(table_frame, orient=VERTICAL)

        # Table creation
        self.table = ttk.Treeview(table_frame, column=('ward_id', 'ward_name', 'ward_type', 'capacity'),
                                  xscrollcommand=s.set, yscrollcommand=s2.set)

        # Scroll bar setup
        s.pack(side=BOTTOM, fill=X)
        s2.pack(side=RIGHT, fill=Y)
        s.config(command=self.table.xview)
        s2.config(command=self.table.yview)

        style = Style()
        style.configure("Treeview.Heading", background="#5B62F4", foreground="white", font=("Arial", 10, "bold"))

        self.table.heading('ward_id', text='Ward ID')
        self.table.heading('ward_name', text='Ward Name')
        self.table.heading('ward_type', text='Ward Type')
        self.table.heading('capacity', text='Capacity')
        self.table['show'] = 'headings'
        self.table.column('ward_id', width=80)
        self.table.column('ward_name', width=200)
        self.table.column('ward_type', width=200)
        self.table.column('capacity', width=100)
        self.table.pack(fill=BOTH, expand=True)
        self.fetch_data()
        self.table.bind("<Double-Button-1>", self.on_select)

    def fetch_data(self):
        # Clear existing items in the table
        for item in self.table.get_children():
            self.table.delete(item)
        # Fetch data from the database
        data = self.db.fetch_wards_data()
        # Insert data into the table
        for ward in data:
            self.table.insert('', 'end', values=ward)

    # Called when key release in searchby
    def fetch_details(self):
        self.table.delete(*self.table.get_children()) #clear existing data
        searchby=self.searchbycbox.get()
        #mapping to convert user friendly fields to 
        column_mapping = { 
        'Ward ID': 'WardID',
        'Ward Name': 'WardName',
        'Ward Type': 'WardType',
        }
        searchby = column_mapping.get(searchby)
        value = self.searchby_text.get("1.0", "end-1c")
        data = self.db.searchby_wards(searchby,value)
        for patient in data:
            self.table.insert('', 'end', values=patient)

    def on_select(self, event=None):
        selection = self.table.selection()
        if selection:
            selected_item = selection[0]
            # Get the values of the selected row
            values = self.table.item(selected_item, 'values')
            form_windows.wardDetails.AddWard(self.db,self,values)

    def addWard(self):
        form_windows.wardDetails.AddWard(self.db,self)

