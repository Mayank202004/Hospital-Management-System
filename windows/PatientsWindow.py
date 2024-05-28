import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import Frame
import ttkbootstrap as bs
from ttkbootstrap import Style
from ttkbootstrap.constants import *
import form_windows.patientDetails

class PatientsWindow(tk.Tk):
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.frame = Frame(parent, bd=5, relief="flat", bg='black')
        self.frame.pack(fill="both", expand=True)  
        self.setTable()
        self.set_widgets()

    def set_widgets(self):
        topframe=Frame(self.frame)
        topframe.place(x=10,y=0,width=1250,height=120)
        tk.Label(topframe, text="Manage Patients", font=("Helvetica", 25, "bold")).place(x=450, y=10)
        bs.Button(topframe, text="Add New Patient",command=self.addPatient).place(x=440,y=80)

        #searchby logic
        tk.Label(topframe, text="Searchby:", font=("Helvetica", 10, "bold")).place(x=5,y=80)
        self.searchbycbox=bs.Combobox(topframe,values=['Patient Id','Name','Phone Number','Blood Group','Insurance Provider'])
        self.searchbycbox.set('Name') # set default as Name 
        self.searchbycbox.configure(state="readonly") #To not allow typing in combobox
        self.searchbycbox.place(x=90,y=80)
        self.searchby_text = tk.Text(topframe, height=1, width=25)
        self.searchby_text.place(x=260,y=80)
        self.searchby_text.bind("<KeyRelease>", lambda event: self.fetch_details()) #keyrelease bind to call function 
        

    def setTable(self):
        table_frame = Frame(self.frame, bd=5, relief=RIDGE, bg='white')
        table_frame.place(x=10, y=125, width=1250, height=710)

        #scroll bar making
        s = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        s2 = ttk.Scrollbar(table_frame, orient=VERTICAL)

        # Table creation
        self.table = ttk.Treeview(table_frame, column=('PatientID', 'Name', 'DateOfBirth', 'Gender', 'ContactNumber', 'Email', 'BloodType', 'InsuranceProvider', 'EmergencyContactName', 'EmergencyContactNumber', 'Allergies', 'MedicalHistory'), xscrollcommand=s.set, yscrollcommand=s2.set)

        # Scroll bar setup
        s.pack(side=BOTTOM, fill=X)
        s2.pack(side=RIGHT, fill=Y)
        s.config(command=self.table.xview)
        s2.config(command=self.table.yview)

        style = Style()
        style.configure("Treeview.Heading", background="#5B62F4", foreground="white", font=("Arial", 10, "bold"))

        # Set headings
        self.table.heading('PatientID', text='Patient ID')
        self.table.heading('Name', text='Name')
        self.table.heading('DateOfBirth', text='Date of Birth')
        self.table.heading('Gender', text='Gender')
        self.table.heading('ContactNumber', text='Contact Number')
        self.table.heading('Email', text='Email Address')
        self.table.heading('BloodType', text='Blood Type')
        self.table.heading('InsuranceProvider', text='Insurance Provider')
        self.table.heading('EmergencyContactName', text='Emergency Contact Name')
        self.table.heading('EmergencyContactNumber', text='Emergency Contact Number')
        self.table.heading('Allergies', text='Allergies')
        self.table.heading('MedicalHistory', text='Medical History')

        # Set column widths
        self.table.column('PatientID', width=80)
        self.table.column('Name', width=150)
        self.table.column('DateOfBirth', width=100)
        self.table.column('Gender', width=80)
        self.table.column('ContactNumber', width=120)
        self.table.column('Email', width=180)
        self.table.column('BloodType', width=80)
        self.table.column('InsuranceProvider', width=150)
        self.table.column('EmergencyContactName', width=150)
        self.table.column('EmergencyContactNumber', width=120)
        self.table.column('Allergies', width=150)
        self.table.column('MedicalHistory', width=150)

        self.table['show'] = 'headings'
        self.table.pack(fill=BOTH, expand=True)
        self.fetch_data()
        self.table.bind("<Double-Button-1>", self.on_select)

    # To fetch initial tabe data
    def fetch_data(self):
        # Clear existing items in the table
        for item in self.table.get_children():
            self.table.delete(item)
        # Fetch data from the database
        data = self.db.fetch_patients_data()
        # Insert data into the table
        for patient in data:
            self.table.insert('', 'end', values=patient)

    # Called when key release in searchby
    def fetch_details(self):
        self.table.delete(*self.table.get_children()) #clear existing data
        searchby=self.searchbycbox.get()
        column_mapping = { 
        'Patient Id': 'PatientID',
        'Name': 'Name',
        'Blood Group': 'BloodType',
        'Insurance Provider':'InsuranceProvider',
        'Phone Number':'ContactNumber'
        }
        searchby = column_mapping.get(searchby)
        value = self.searchby_text.get("1.0", "end-1c")
        data = self.db.searchby_patients(searchby,value)
        for patient in data:
            self.table.insert('', 'end', values=patient)

    #Called when doube click any table row to edit it 
    def on_select(self, event=None):
        selection = self.table.selection()
        if selection:
            selected_item = selection[0]
            # Get the values of the selected row
            values = self.table.item(selected_item, 'values')
            form_windows.patientDetails.EditPatients(self.db,self,values)

    def addPatient(self):
        form_windows.patientDetails.EditPatients(self.db,self)
