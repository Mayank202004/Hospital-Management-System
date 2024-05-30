import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import Frame
import ttkbootstrap as bs
from ttkbootstrap import Style
from ttkbootstrap.constants import *
import form_windows.addTest


class LabTestsWindow(tk.Tk):
    def __init__(self, parent,db):
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
        tk.Label(topframe, text="Manage Lab Tests", font=("Helvetica", 25, "bold")).place(x=450, y=10)
        bs.Button(topframe, text="Add New Lab Test",command=self.addTest).place(x=440,y=80)

        #searchby logic
        tk.Label(topframe, text="Searchby:", font=("Helvetica", 10, "bold")).place(x=5,y=80)
        self.searchbycbox=bs.Combobox(topframe,values=['Test ID','Test Name','Department'])
        self.searchbycbox.set('Test ID') # set default as Name 
        self.searchbycbox.configure(state="readonly") #To not allow typing in combobox
        self.searchbycbox.place(x=90,y=80)
        self.searchby_text = tk.Text(topframe, height=1, width=25)
        self.searchby_text.place(x=260,y=80)
        self.searchby_text.bind("<KeyRelease>", lambda event: self.fetch_details()) #keyrelease bind to call function 
    def setTable(self):
        table_frame=Frame(self.frame,bd=5,relief=RIDGE,bg='white')
        table_frame.place(x=10,y=125,width=1250,height=710)

        #scroll bar making
        s=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        s2=ttk.Scrollbar(table_frame,orient=VERTICAL)

        # Table creation
        self.table = ttk.Treeview(table_frame, column=('test_id', 'test_name', 'test_cost','department_id', 'department_name'), xscrollcommand=s.set, yscrollcommand=s2.set)

        # Scroll bar setup
        s.pack(side=BOTTOM, fill=X)
        s2.pack(side=RIGHT, fill=Y)
        s.config(command=self.table.xview)
        s2.config(command=self.table.yview)

        style = Style()
        style.configure("Treeview.Heading", background="#5B62F4", foreground="white", font=("Arial", 10, "bold"))

        self.table.heading('test_id', text='Test ID')
        self.table.heading('test_name', text='Test Name')
        self.table.heading('test_cost', text='Test Cost (INR)')
        self.table.heading('department_id', text='Dept ID')
        self.table.heading('department_name', text='Department')
        self.table['show'] = 'headings'
        self.table.column('test_id', width=80)
        self.table.column('test_name', width=200)
        self.table.column('test_cost', width=120)
        self.table.column('department_id', width=80)
        self.table.column('department_name', width=150)
        self.table.pack(fill=BOTH, expand=True)
        self.fetch_data()
        self.table.bind("<Double-Button-1>", self.on_select)

    def fetch_data(self):
        # Clear existing items in the table
        for item in self.table.get_children():
            self.table.delete(item)
        # Fetch data from the database
        data = self.db.fetch_labtests_data()
        # Insert data into the table
        for test in data:
            self.table.insert('', 'end', values=test)

     # Called when key release in searchby
    def fetch_details(self):
        self.table.delete(*self.table.get_children()) #clear existing data
        searchby=self.searchbycbox.get()
        #mapping to convert user friendly fields to 
        column_mapping = { 
        'Test ID': 'TestID',
        'Test Name': 'TestName',
        'Department': 'DepartmentName',
        }
        searchby = column_mapping.get(searchby)
        value = self.searchby_text.get("1.0", "end-1c")
        data = self.db.searchby_labtests(searchby,value)
        for test in data:
            self.table.insert('', 'end', values=test)

    #called when double clicked any tale row to edit 
    def on_select(self, event=None):
        selection = self.table.selection()
        if selection:
            selected_item = selection[0]
            # Get the values of the selected row
            values = self.table.item(selected_item, 'values')
            #windows.docDetails.EditDoctors(self.db,self,values)
            form_windows.addTest.AddTest(self.db,self,values)
    def addTest(self):
        pass
        form_windows.addTest.AddTest(self.db,self)

if __name__ == "__main__":
    style = bs.Style("morph")
    LabTestsWindow.main()