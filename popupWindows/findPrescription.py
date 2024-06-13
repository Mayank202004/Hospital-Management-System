import tkinter as tk
from tkinter import *
from tkinter import ttk
from ttkbootstrap import Style
import ttkbootstrap as bs


class findPrescription(tk.Tk,):
    def __init__(self,db,edit_appointment_window):
        super().__init__()
        self.db = db
        self.create_widgets()
        self.edit_appointment_window = edit_appointment_window

    def create_widgets(self):
        self.title("Find Patients")
        self.geometry("800x510")
        self.configure(bg="cornflowerblue")

        tk.Label(self, text="Find Prescription", font=("Helvetica", 20, "bold")).place(x=300, y=10)

        #frames setup
        frametop = tk.Frame(self,bg='green')  
        frametop.place(x=20, y=65,width=770,height=50)
        tableframe = tk.Frame(self,bg='black')  
        tableframe.place(x=20, y=120,width=770,height=380)

        #searchby logic
        tk.Label(frametop, text="Searchby:", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        self.searchbycbox=bs.Combobox(frametop,values=['Patient ID','Patient Name','Doctor ID','Doctor Name'])
        self.searchbycbox.set('Patient Name') # set default as Patient Name 
        self.searchbycbox.configure(state="readonly") #To not allow typing in combobox
        self.searchbycbox.grid(row=0,column=1)
        self.searchby_text = tk.Text(frametop, height=1, width=25)
        self.searchby_text.grid(row=0, column=2, padx=20, pady=5)
        self.searchby_text.bind("<KeyRelease>", lambda event: self.fetch_details()) #keyrelease bind to call function 

        #table layout
        # Table creation
        s = ttk.Scrollbar(tableframe, orient=HORIZONTAL)
        s2 = ttk.Scrollbar(tableframe, orient=VERTICAL)
        self.table = ttk.Treeview(tableframe, column=('PrescriptionID','DoctorID','DoctorName','PatientID','PatientName','TotalPrice'), xscrollcommand=s.set, yscrollcommand=s2.set)

        # Scroll bar setup
        s.pack(side=BOTTOM, fill=X)
        s2.pack(side=RIGHT, fill=Y)
        s.config(command=self.table.xview)
        s2.config(command=self.table.yview)

        style = Style()
        style.configure("Treeview.Heading", background="#5B62F4", foreground="white", font=("Arial", 10, "bold"))

        self.table.heading('PrescriptionID', text='Prescription ID')
        self.table.heading('DoctorID', text='Doctor ID')
        self.table.heading('DoctorName', text='Doctor Name')
        self.table.heading('PatientID', text='Patient ID')
        self.table.heading('PatientName', text='Patient Name')
        self.table.heading('TotalPrice', text='Total Price')
        self.table['show'] = 'headings'
        self.table.column('PrescriptionID', width=90)
        self.table.column('DoctorID', width=70)
        self.table.column('DoctorName', width=150)
        self.table.column('PatientID', width=70)
        self.table.column('PatientName', width=200)
        self.table.column('TotalPrice', width=150)
        self.table.pack(fill=BOTH, expand=True)
        self.table.bind("<Double-Button-1>", self.on_select)

     # Called when key release in searchby
    def fetch_details(self):
        self.table.delete(*self.table.get_children()) #clear existing data
        searchby=self.searchbycbox.get()
        #mapping to convert user friendly fields to 
        column_mapping = { 
        'Doctor ID': 'DoctorID',
        'Doctor Name': 'first_name',
        'Patient ID': 'PatientID',
        'Patient Name': 'Name',
        }
        searchby = column_mapping.get(searchby)
        value = self.searchby_text.get("1.0", "end-1c")
        data = self.db.search_p(searchby,value)
        for prescription in data:
            self.table.insert('', 'end', values=prescription)

    #To return found patient to manageAppointment
    def on_select(self, event=None):
        selection = self.table.selection()
        if selection:
            id = self.table.item(selection[0], 'values')[0]
            self.edit_appointment_window.FetchPrescription_throughfind(id)
            self.after(100, self.destroy)
            

        

        

        


if __name__ == "__main__":
    #stye=bs.Style()
    app = findPrescription()
    app.mainloop()
