import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import Frame
import ttkbootstrap as bs
from ttkbootstrap import Style
from ttkbootstrap.constants import *
import form_windows.docDetails

class DoctorsWindow(tk.Tk):
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
        tk.Label(topframe, text="Manage Doctors", font=("Helvetica", 25, "bold")).place(x=450, y=10)
        bs.Button(topframe, text="Add New Doctor",command=self.addDoctor).place(x=440,y=80)

        #searchby logic
        tk.Label(topframe, text="Searchby:", font=("Helvetica", 10, "bold")).place(x=5,y=80)
        self.searchbycbox=bs.Combobox(topframe,values=['Doctor Id','Name','Specialization','Department','Phone number'])
        self.searchbycbox.set('Name') # set default as Name 
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
        self.table = ttk.Treeview(table_frame, column=('doctor_id', 'first_name', 'last_name', 'specialization', 'contact_number', 'email', 'address', 'gender', 'date_of_birth', 'joining_date', 'qualification', 'experience', 'department'), xscrollcommand=s.set, yscrollcommand=s2.set)

        # Scroll bar setup
        s.pack(side=BOTTOM, fill=X)
        s2.pack(side=RIGHT, fill=Y)
        s.config(command=self.table.xview)
        s2.config(command=self.table.yview)

        style = Style()
        style.configure("Treeview.Heading", background="#5B62F4", foreground="white", font=("Arial", 10, "bold"))

        self.table.heading('doctor_id', text='Doctor ID')
        self.table.heading('first_name', text='First Name')
        self.table.heading('last_name', text='Last Name')
        self.table.heading('specialization', text='Specialization')
        self.table.heading('contact_number', text='Contact Number')
        self.table.heading('email', text='Email Address')
        self.table.heading('address', text='Address')
        self.table.heading('gender', text='Gender')
        self.table.heading('date_of_birth', text='Date of Birth')
        self.table.heading('joining_date', text='Joining Date')
        self.table.heading('qualification', text='Qualification')
        self.table.heading('experience', text='Experience')
        self.table.heading('department', text='Department')
        self.table['show'] = 'headings'
        self.table.column('doctor_id', width=80)
        self.table.column('first_name', width=100)
        self.table.column('last_name', width=100)
        self.table.column('specialization', width=120)
        self.table.column('contact_number', width=120)
        self.table.column('email', width=190)
        self.table.column('address', width=180)
        self.table.column('gender', width=80)
        self.table.column('date_of_birth', width=100)
        self.table.column('joining_date', width=100)
        self.table.column('qualification', width=100)
        self.table.column('experience', width=80)
        self.table.column('department', width=120)
        self.table.pack(fill=BOTH, expand=True)
        self.fetch_data()
        self.table.bind("<Double-Button-1>", self.on_select)

    def fetch_data(self):
        # Clear existing items in the table
        for item in self.table.get_children():
            self.table.delete(item)
        # Fetch data from the database
        data = self.db.fetch_doctors_data()
        # Insert data into the table
        for doctor in data:
            self.table.insert('', 'end', values=doctor)

     # Called when key release in searchby
    def fetch_details(self):
        self.table.delete(*self.table.get_children()) #clear existing data
        searchby=self.searchbycbox.get()
        #mapping to convert user friendly fields to 
        column_mapping = { 
        'Doctor Id': 'doctor_id',
        'Name': 'first_name',
        'Specialization': 'specialization',
        'Department': 'department',
        'Phone number': 'contact_number'
        }
        searchby = column_mapping.get(searchby)
        value = self.searchby_text.get("1.0", "end-1c")
        data = self.db.searchby_doctors(searchby,value)
        for patient in data:
            self.table.insert('', 'end', values=patient)

    #called when double clicked any tale row to edit 
    def on_select(self, event=None):
        selection = self.table.selection()
        if selection:
            selected_item = selection[0]
            # Get the values of the selected row
            values = self.table.item(selected_item, 'values')
            form_windows.docDetails.EditDoctors(self.db,self,values)
    
    def addDoctor(self):
        form_windows.docDetails.EditDoctors(self.db,self)

if __name__ == "__main__":
    style = bs.Style("morph")
    DoctorsWindow.main()