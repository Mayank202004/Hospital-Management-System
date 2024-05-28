import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import *
from tkinter import ttk
from tkinter import Frame
from datetime import datetime
import ttkbootstrap as bs
from ttkbootstrap import Style
from ttkbootstrap.constants import *
import popupWindows.findDoctor as fd
import popupWindows.findPatient as fp
import popupWindows.findMedicine as fm

class EditPrescription(tk.Tk):
    def __init__(self,db=None):
        super().__init__()
        self.db=db
        self.set_widgets()
        self.setTable()
        

    def set_widgets(self):
        self.title("Add New Prescription")
        self.geometry("1270x800")
        #self.configure(bg="cornflowerblue")
        topframe=Frame(self)
        topframe.place(x=0,y=0,width=1300,height=210)
        tk.Label(topframe, text="Add New Prescriptions", font=("Helvetica", 25, "bold")).place(x=450, y=10)
        #bs.Button(topframe, text="Add New Prescription",command=self.addDoctor).place(x=460,y=80)

        #searchby logic
        tk.Label(topframe, text="Patient ID:", font=("Helvetica", 10, "bold")).place(x=5,y=80)
        self.ID_input_text = tk.Text(topframe, height=1, width=7)
        self.ID_input_text.place(x=95,y=80)
        tk.Button(topframe, text="Fetch",command=self.fetchPatient).place(x=160,y=83)
        self.Name_display_text = tk.Text(topframe, height=1, width=20)
        self.Name_display_text.place(x=200,y=80)
        tk.Button(topframe, text="Find Patient",command=self.findPatient).place(x=350,y=83)
        # fetch doctor 
        tk.Label(topframe, text="Doctor ID:", font=("Helvetica", 10, "bold")).place(x=480,y=80)
        self.DocID_input_text = tk.Text(topframe, height=1, width=7)
        self.DocID_input_text.place(x=555,y=80)
        tk.Button(topframe, text="Fetch",command=self.fetchDoctor).place(x=620,y=83)
        self.DocName_display_text = tk.Text(topframe, height=1, width=20)
        self.DocName_display_text.place(x=670,y=80)
        tk.Button(topframe, text="Find Doctor",command=self.findDoctor).place(x=820,y=83)

        #Medicine fetch section
        tk.Label(topframe, text="Medicine ID:", font=("Helvetica", 10, "bold")).place(x=5,y=130)
        self.MedID_input_text = tk.Text(topframe, height=1, width=7)
        self.MedID_input_text.place(x=95,y=130)
        tk.Button(topframe, text="Fetch",command=self.fetchMedicine).place(x=160,y=133)
        self.MedName_display_text = tk.Text(topframe, height=1, width=20)
        self.MedName_display_text.place(x=200,y=130)
        tk.Button(topframe, text="Find Medicine",command=self.findMedicine).place(x=350,y=133)

        tk.Label(topframe, text="Price:", font=("Helvetica", 10, "bold")).place(x=470,y=130)
        self.MedPrice_input_text = tk.Text(topframe, height=1, width=15)
        self.MedPrice_input_text.place(x=530,y=130)

        #instruction row
        tk.Label(topframe, text="Instruction:", font=("Helvetica", 10, "bold")).place(x=5,y=175)
        self.Instruction_input_text = tk.Text(topframe, height=1, width=80)
        self.Instruction_input_text.place(x=100,y=175)
        tk.Button(topframe, text="Add Medicine",command=self.add_medicine).place(x=600,y=178)
        tk.Button(topframe, text="Remove Medicine",command=self.remove_selected_row).place(x=700,y=178)

        #bottom end buttons
        tk.Button(self,text="SAVE",height=2,width=7,font=("Helvetica", 12, "bold"),command=self.save_prescription).place(x=10,y=740)
        tk.Button(self,text="RESET",height=2,width=7,font=("Helvetica", 12, "bold"),command=self.resetWindow).place(x=100,y=740)
        

    def setTable(self):
        table_frame=Frame(self,bd=5,relief=RIDGE)
        table_frame.place(x=10,y=220,width=1250,height=510)

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

        #style = Style()
        #style.configure("Treeview.Heading", background="#5B62F4", foreground="white", font=("Arial", 10, "bold"))

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
        #self.table.bind("<Double-Button-1>", self.on_select)

    def findPatient(self):
        fp.findPatients(self.db,self)
    
    def setPatient(self,id,name):
        self.ID_input_text.delete("1.0", tk.END)
        self.ID_input_text.insert("1.0", str(id))
        self.Name_display_text.delete("1.0", tk.END)
        self.Name_display_text.insert("1.0", str(name))

    def findDoctor(self):
        fd.findDoctors(self.db,self)
    
    def setDoctor(self,id,name):
        self.DocID_input_text.delete("1.0", tk.END)
        self.DocID_input_text.insert("1.0", str(id))
        self.DocName_display_text.delete("1.0", tk.END)
        self.DocName_display_text.insert("1.0", str(name))

    def fetchPatient(self):
        patient_id = self.ID_input_text.get("1.0", "end-1c")
        patient_name = self.db.get_patient_name(patient_id)
        if patient_name:
            self.Name_display_text.delete("1.0", "end")
            self.Name_display_text.insert("1.0", patient_name)
        else:
            messagebox.showinfo("No Patient Found", f"No patient found with ID: {patient_id}")
            self.focus_force()
    
    def fetchDoctor(self):
        doctor_id = self.DocID_input_text.get("1.0", "end-1c")
        doctor_name = self.db.get_doctor_name(doctor_id)
        if doctor_name:
            self.DocName_display_text.delete("1.0", "end")
            self.DocName_display_text.insert("1.0", doctor_name)
        else:
            messagebox.showinfo("No Doctor Found", f"No doctor found with ID: {doctor_id}")
            self.focus_force()

    def findMedicine(self):
        fm.findMedicines(self.db,self)

    def setMedicine(self,id,name,price):
        self.MedID_input_text.delete("1.0", tk.END)
        self.MedID_input_text.insert("1.0", str(id))
        self.MedName_display_text.delete("1.0", tk.END)
        self.MedName_display_text.insert("1.0", str(name))
        self.MedPrice_input_text.delete("1.0", tk.END)
        self.MedPrice_input_text.insert("1.0", str(price))

    def fetchMedicine(self):
        medicine_id = self.MedID_input_text.get("1.0", "end-1c")
        medicine = self.db.get_medicine_name(medicine_id)
        if medicine:
            self.MedName_display_text.delete("1.0", "end")
            self.MedName_display_text.insert("1.0", medicine[0])
            self.MedPrice_input_text.delete("1.0", "end")
            self.MedPrice_input_text.insert("1.0", medicine[1])
        else:
            messagebox.showinfo("No Medicine Found", f"No medicine found with ID: {medicine_id}")
            self.focus_force()

    #Used to Add medicine to prescription table
    def add_medicine(self):
        # Retrieve data from text fields
        med_id = self.MedID_input_text.get("1.0", tk.END).strip()
        med_name = self.MedName_display_text.get("1.0", tk.END).strip()
        med_price = self.MedPrice_input_text.get("1.0", tk.END).strip()
        instruction = self.Instruction_input_text.get("1.0", tk.END).strip()
        # Validate data
        if not med_id or not med_name or not med_price:
            messagebox.showerror("Input Error", "Medicine ID, Name, and Price fields must be filled")
            self.focus_force()
            return
        # Insert data into table
        self.table.insert("", tk.END, values=(med_id, med_name, med_price, instruction))
        # Clear text fields after insertion
        self.MedID_input_text.delete("1.0", tk.END)
        self.MedName_display_text.delete("1.0", tk.END)
        self.MedPrice_input_text.delete("1.0", tk.END)
        self.Instruction_input_text.delete("1.0", tk.END)

    #Used to remove a row of medicine from prescription table
    def remove_selected_row(self):
        selected_item = self.table.selection()  # Get selected item
        if selected_item:
            self.table.delete(selected_item)  # Remove the selected item
        else:
            messagebox.showerror("Selection Error", "No item selected")
            self.focus_force()

     #This is used to save prescription to sqlite table when button clicked
    def save_prescription(self):
        doctor_id = self.DocID_input_text.get("1.0", "end-1c").strip()
        patient_id = self.ID_input_text.get("1.0", "end-1c").strip()
        if doctor_id=="" or patient_id=="":
            messagebox.showerror("Missing Information", "Doctor ID and Patient ID are required.")
            self.focus_force()
            return

        # Calculate the current date dynamically
        prescription_date = datetime.now().strftime("%Y-%m-%d")

         # Collect all rows into a list of tuples
        prescription_data = []
        try:
            prescriptionID=self.db.getprescriptionID()
        except:
            prescriptionID=1
            #print("Failed")       #debugging
        for row in self.table.get_children():
            values = self.table.item(row, 'values')
            medicine_id = values[0]
            instruction = values[3]
            prescription_data.append((prescriptionID,doctor_id, patient_id, prescription_date, instruction, medicine_id))
        
        try:
            self.db.insertPrescription(prescription_data)
            self.destroy() # reset window after inserting to insert new one
            self.__init__(self.db)
            messagebox.showinfo("Success", "Prescription saved successfully.")
            self.focus_force()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the prescription: {str(e)}")
            self.focus_force()


    #This is to reset the window (destroy and make new window)
    def resetWindow(self):
        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to reset the window?")
        if confirmation:
            self.destroy()
            self.__init__(self.db)






if __name__ == "__main__":
    #style = bs.Style("morph")
    app = EditPrescription()
    app.mainloop()
