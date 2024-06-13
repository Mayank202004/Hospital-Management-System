import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as messagebox
from tkinter import Frame
import ttkbootstrap as bs
from ttkbootstrap import Style
from ttkbootstrap.constants import *
import form_windows.docDetails
import form_windows.prescriptionsDetails
import popupWindows.findPrescription as fp

class PrescriptionsWindow(tk.Tk):
    def __init__(self, parent,db):
        self.parent = parent
        self.db = db
        self.frame = Frame(parent, bd=5, relief="flat", bg='black')
        self.frame.pack(fill="both", expand=True)  
        self.setTable()
        self.set_widgets()
        

    def set_widgets(self):
        topframe=Frame(self.frame)
        topframe.place(x=10,y=0,width=1250,height=120)
        tk.Label(topframe, text="Manage Prescriptions", font=("Helvetica", 25, "bold")).place(x=450, y=10)
        bs.Button(topframe, text="Add New Prescription",command=self.addPrescription).place(x=460,y=80)

        #searchby logic
        tk.Label(topframe, text="Prescription ID:", font=("Helvetica", 10, "bold")).place(x=5,y=80)
        self.ID_input_text = tk.Text(topframe, height=1, width=20)
        self.ID_input_text.place(x=110,y=80)
        bs.Button(topframe, text="Fetch",command=self.FetchPrescription).place(x=260,y=80)
        bs.Button(topframe, text="Find Prescription",command=self.FindPrescription).place(x=330,y=80)

        #Bottom table layout
        bottom_frame=Frame(self.frame,bd=5,relief='flat',bg='white')
        bottom_frame.place(x=10,y=740,width=1250,height=90)
        tk.Label(bottom_frame, text="Patient Name: ", font=("Helvetica", 15, "bold")).grid(row=0,column=0)
        self.patient_name=tk.Label(bottom_frame, text="", font=("Helvetica", 15, "bold"))
        self.patient_name.grid(row=0,column=1)
        tk.Label(bottom_frame, text="Doctor Name: ", font=("Helvetica", 15, "bold")).grid(row=1,column=0)
        self.doctor_name=tk.Label(bottom_frame, text="", font=("Helvetica", 15, "bold"))
        self.doctor_name.grid(row=1,column=1)
        totalamt_label=tk.Label(bottom_frame, text="Total Amount: ", font=("Helvetica", 15, "bold"))
        totalamt_label.place(x=350,y=0)
        self.total_amt=tk.Label(bottom_frame, text="", font=("Helvetica", 15, "bold"))
        self.total_amt.place(x=500,y=0)

    def setTable(self):
        table_frame=Frame(self.frame,bd=5,relief=RIDGE,bg='white')
        table_frame.place(x=10,y=125,width=1250,height=610)

        #scroll bar making
        s=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        s2=ttk.Scrollbar(table_frame,orient=VERTICAL)

        # Table creation
        self.table = ttk.Treeview(table_frame, column=('Medicine ID','Medicine Name','Price','Instruction'), xscrollcommand=s.set, yscrollcommand=s2.set)

        # Scroll bar setup
        s.pack(side=BOTTOM, fill=X)
        s2.pack(side=RIGHT, fill=Y)
        s.config(command=self.table.xview)
        s2.config(command=self.table.yview)

        style = Style()
        style.configure("Treeview.Heading", background="#5B62F4", foreground="white", font=("Arial", 10, "bold"))

        self.table.heading('Medicine ID', text='Medicine ID')
        self.table.heading('Medicine Name', text='Medicine Name')
        self.table.heading('Price', text='Price')
        self.table.heading('Instruction', text='Instruction')
        self.table['show'] = 'headings'
        self.table.column('Medicine ID', width=100)
        self.table.column('Medicine Name', width=200)  
        self.table.column('Price', width=80)
        self.table.column('Instruction', width=250)
        self.table.pack(fill=BOTH, expand=True)


    
    def addPrescription(self):
        form_windows.prescriptionsDetails.EditPrescription(self.db)

    def FetchPrescription(self):
        try:
            if(self.ID_input_text.get("1.0","end-1c").strip()!=""):
                id=self.ID_input_text.get("1.0", "end-1c")
                data = self.db.fetch_prescription_data(id)
                for prescription in data:
                    self.table.insert('', 'end', values=prescription)
                data=self.db.fetch_prescription_details(id)
                self.doctor_name.config(text=data[0][0])         # data is in format [('Dr. Ravi', 'Neha Reddy',Total_amount)] so used [0][0] to get doctor name
                self.patient_name.config(text=data[0][1])
                self.total_amt.config(text=data[0][2])
        except:
            messagebox.showerror("No Prescription Found", f"No Prescription found with ID: {id}")

    def FetchPrescription_throughfind(self,id):
        try:
            data = self.db.fetch_prescription_data(id)
            for prescription in data:
                self.table.insert('', 'end', values=prescription)
            data=self.db.fetch_prescription_details(id)
            self.doctor_name.config(text=data[0][0]) 
            self.patient_name.config(text=data[0][1])
            self.total_amt.config(text=data[0][2]) 
            return
        except Exception as e:
            messagebox.showerror("No Prescription Found", f"No Prescription found with ID: {id}")

    def FindPrescription(self):
        fp.findPrescription(self.db,self)



if __name__ == "__main__":
    style = bs.Style("morph")
    PrescriptionsWindow.main()