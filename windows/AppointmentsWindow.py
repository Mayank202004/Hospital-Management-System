import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import Frame
import form_windows.appointmentsDetails
import ttkbootstrap as bs
from ttkbootstrap import Style
from ttkbootstrap.constants import *

class AppointmentsWindow(tk.Tk):
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
        tk.Label(topframe, text="Manage Appointments", font=("Helvetica", 25, "bold")).place(x=400, y=10)
        bs.Button(topframe, text="Add New Appointment",command=self.addAppointment).place(x=440,y=80)

        #searchby logic
        tk.Label(topframe, text="Searchby:", font=("Helvetica", 10, "bold")).place(x=5,y=80)
        self.searchbycbox=bs.Combobox(topframe,values=['Appointment ID','Patient ID','Patient Name','Doctor ID','Doctor Name','Date'])
        self.searchbycbox.set('Appointment ID') # set default as Name 
        self.searchbycbox.configure(state="readonly") #To not allow typing in combobox
        self.searchbycbox.place(x=90,y=80)
        self.searchby_text = tk.Text(topframe, height=1, width=25)
        self.searchby_text.place(x=260,y=80)
        self.searchby_text.bind("<KeyRelease>", lambda event: self.fetch_details()) #keyrelease bind to call function 

    def setTable(self):
        table_frame = Frame(self.frame, bd=5, relief=RIDGE, bg='white')
        table_frame.place(x=10, y=125, width=1250, height=710)
    
        # Scroll bars
        s = bs.Scrollbar(table_frame, orient=HORIZONTAL)
        s2 = bs.Scrollbar(table_frame, orient=VERTICAL)
    
        # Table creation
        self.table = ttk.Treeview(table_frame, column=('AppointmentID', 'PatientID','patient_name', 'DoctorID','doctor_name', 'AppointmentDate', 'Reason', 'Status'), xscrollcommand=s.set, yscrollcommand=s2.set)
    
        # Scroll bar setup
        s.pack(side=BOTTOM, fill=X)
        s2.pack(side=RIGHT, fill=Y)
        s.config(command=self.table.xview)
        s2.config(command=self.table.yview)

        # Configure the style for the header cells
        style = Style()
        style.configure("Treeview.Heading", background="#5B62F4", foreground="white", font=("Arial", 10, "bold"))
    
        # Table headings
        self.table.heading('AppointmentID', text='Appointment ID', anchor='center')
        self.table.heading('PatientID', text='Patient ID', anchor='center')
        self.table.heading('patient_name', text='Patient Name', anchor='center')
        self.table.heading('DoctorID', text='Doctor ID', anchor='center')
        self.table.heading('doctor_name', text='Doctor Name', anchor='center')
        self.table.heading('AppointmentDate', text='Appointment Date', anchor='center')
        self.table.heading('Reason', text='Reason', anchor='center')
        self.table.heading('Status', text='Status', anchor='center')
        self.table['show'] = 'headings'
    
        # Column widths
        self.table.column('AppointmentID', width=100, anchor='center')
        self.table.column('PatientID', width=100, anchor='center')
        self.table.column('patient_name', width=100, anchor='center')
        self.table.column('DoctorID', width=100, anchor='center')
        self.table.column('doctor_name', width=100, anchor='center')
        self.table.column('AppointmentDate', width=200, anchor='center')
        self.table.column('Reason', width=200, anchor='center')
        self.table.column('Status', width=100, anchor='center')
    
        self.table.pack(fill=BOTH, expand=True)
        self.fetch_data()
        self.table.bind("<Double-Button-1>", self.on_select)

    def fetch_data(self):
        # Clear existing items in the table
        for item in self.table.get_children():
            self.table.delete(item)
        # Fetch data from the database
        data = self.db.fetch_appointments()
        # Insert data into the table
        for appointment in data:
            self.table.insert('', 'end', values=appointment)

     # Called when key release in searchby
    def fetch_details(self):
        self.table.delete(*self.table.get_children()) #clear existing data
        searchby=self.searchbycbox.get()
        #mapping to convert user friendly fields to 
        column_mapping = {
        'Appointment ID': 'AppointmentID',
        'Patient ID': 'PatientID',
        'Patient Name': 'Name', 
        'Doctor ID': 'DoctorID',
        'Doctor Name': 'first_name',
        'Date': 'AppointmentDate',
        }
        searchby = column_mapping.get(searchby)
        value = self.searchby_text.get("1.0", "end-1c")
        data = self.db.searchby_appointments(searchby,value)
        for appointment in data:
            self.table.insert('', 'end', values=appointment)

    
    def on_select(self, event=None):
        selection = self.table.selection()
        if selection:
            selected_item = selection[0]
            values = self.table.item(selected_item, 'values')
            form_windows.appointmentsDetails.EditAppointment(self,values,self.db)

    def addAppointment(self):
        form_windows.appointmentsDetails.EditAppointment(self,db=self.db)
            

if __name__ == "__main__":
    AppointmentsWindow.mainloop()  # This should be changed to `main()` if you are using `bs.Tk()` instead of `tk.Tk()`
