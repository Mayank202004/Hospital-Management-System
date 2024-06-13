import tkinter as tk
from tkinter import ttk
import ttkbootstrap as bs
from ttkbootstrap.constants import *
import tkinter.messagebox as messagebox
import popupWindows.findPatient as fp
import popupWindows.findWard as fw


class AddBeds(tk.Tk):
    def __init__(self,db,parent,values=None):
        super().__init__()
        self.db=db
        self.parent=parent #To update table in TestsWindow from here
        self.create_widgets()
        if values:
            self.fill_fields(values)

    def create_widgets(self):
        self.title("Add Bed Details")
        self.geometry("600x500")
        self.configure(bg="cornflowerblue")

        tk.Label(self, text="Beds Details", font=("Helvetica", 25, "bold"), bg="cornflowerblue").place(x=200, y=20)

        mainframe = tk.Frame(self)  
        mainframe.place(x=30, y=80,width=550,height=400)  
        idframe = tk.Frame(mainframe)  
        idframe.place(x=10, y=15,width=835,height=45)
        nameframe = tk.Frame(mainframe)  
        nameframe.place(x=10, y=55,width=835,height=90)
        frametop = tk.Frame(mainframe)  
        frametop.place(x=40, y=145,width=835,height=195)  
        frame = tk.Frame(mainframe,bg='black')  
        frame.place(x=45, y=330,width=435,height=60) 

        # Create labels and entry fields for doctor details inside the frame
        tk.Label(idframe, text="Bed ID:", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=16, pady=5)
        self.bed_id_text = tk.Text(idframe, height=1, width=15)
        self.bed_id_text.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(nameframe, text="Ward ID:", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        self.ward_id_text = tk.Text(nameframe, height=1, width=30)
        self.ward_id_text.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(nameframe, text="Fetch",command=self.fetchWard).grid(row=0,column=2)
        tk.Label(nameframe, text="Ward Name:", font=("Helvetica", 10, "bold")).grid(row=1, column=0, padx=5, pady=5)
        self.ward_name_text = tk.Text(nameframe, height=1, width=30)
        self.ward_name_text.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(nameframe, text="Find",command=self.findWard).grid(row=1,column=2)
        tk.Label(frametop, text="Bed Number:", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=16, pady=5)
        self.bed_number_text = tk.Text(frametop, height=1, width=20)
        self.bed_number_text.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frametop, text="Availability:", font=("Helvetica", 10, "bold")).grid(row=1, column=0, padx=16, pady=5)
        self.availabilitycbox=ttk.Combobox(frametop,values=['Available','Occupied'],height=2,width=20)
        self.availabilitycbox.set('Available') # set default as Name 
        self.availabilitycbox.configure(state="readonly") #To not allow typing in combobox
        self.availabilitycbox.grid(row=1,column=1)
        tk.Label(frametop, text="Patient ID:", font=("Helvetica", 10, "bold")).grid(row=2, column=0, padx=5, pady=5)
        self.patient_id_text = tk.Text(frametop, height=1, width=20)
        self.patient_id_text.grid(row=2, column=1, padx=15, pady=5)
        tk.Button(frametop, text="Fetch",command=self.fetchPatient).grid(row=2,column=2)
        tk.Label(frametop, text="Patient Name:", font=("Helvetica", 10, "bold")).grid(row=3, column=0, padx=5, pady=5)
        self.patient_name_text = tk.Text(frametop, height=1, width=20)
        self.patient_name_text.grid(row=3, column=1, padx=15, pady=5)
        tk.Button(frametop, text="Find",command=self.findPatient).grid(row=3,column=2)
        

        # Create a Save button to save changes
        tk.Button(frame, text="Save", width=10, height=2,command=self.save).place(x=50, y=15)
        tk.Button(frame, text="Update", width=10, height=2,command=self.update).place(x=150, y=15)
        tk.Button(frame, text="Delete", width=10, height=2,command=self.delete).place(x=250, y=15)
        tk.Button(frame, text="Clear", width=10, height=2,command=self.clear).place(x=350, y=15)

    def save(self):
        # Retrieve values from the text fields and create a tuple
        ward_id = self.ward_id_text.get("1.0", "end-1c").strip()
        bed_number = self.bed_number_text.get("1.0", "end-1c").strip()
        availability = self.availabilitycbox.get().strip()
        patient_id = self.patient_id_text.get("1.0", "end-1c").strip()

        # Check if any field is empty
        if not ward_id or not bed_number or not availability:
            messagebox.showerror("Error", "All fields are required!")
            self.focus_force()
            return
        values = (ward_id,bed_number,availability,patient_id)

        try:
            self.db.insertBed(values)
            messagebox.showinfo("Success", "Bed information added successfully!")
            self.parent.setTable()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add bed information: {str(e)}")
        self.destroy()

    def update(self):
        confirmation = messagebox.askyesno("Confirm Update", "Are you sure you want to update this bed's information?")
        if confirmation:
            # Retrieve values from the text fields and create a tuple
            ward_id = self.ward_id_text.get("1.0", "end-1c").strip()
            bed_number = self.bed_number_text.get("1.0", "end-1c").strip()
            availability = self.availabilitycbox.get().strip()
            patient_id = self.patient_id_text.get("1.0", "end-1c").strip()
            identifier = self.bed_id_text.get("1.0", "end-1c")

            # Check if any field is empty
            if not ward_id or not patient_id or not bed_number or not identifier:
                messagebox.showerror("Error", "All fields are required!")
                self.focus_force()
                return
            values = (
                ward_id,
                bed_number,
                availability,
                patient_id
            )
            try:
                self.db.updateBed(values, identifier)
                messagebox.showinfo("Success", "Bed information updated successfully!")
                self.parent.setTable()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update bed information: {str(e)}")
            self.destroy()

    def delete(self):
        confirmation = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this bed's information?")
        if confirmation:
            identifier = self.bed_id_text.get("1.0", "end-1c")
            # Check if any field is empty
            if not identifier:
                messagebox.showerror("Error", "All fields are required!")
                self.focus_force()
                return
            try:
                self.db.deleteBed(identifier)
                messagebox.showinfo("Success", "Bed information deleted successfully!")
                self.parent.setTable()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete bed information: {str(e)}")
            self.destroy()

    def clear(self):
        self.bed_id_text.delete("1.0", "end")
        self.ward_id_text.delete("1.0", "end")
        self.ward_name_text.delete("1.0", "end")
        self.patient_id_text.delete("1.0", "end")
        self.patient_name_text.delete("1.0", "end")
        self.bed_number_text.delete("1.0", "end")
        self.availabilitycbox.set("Available")


    def fill_fields(self, values):
        # Split the tuple into individual values
        bed_id, ward_id, ward_name, bed_number, availability, patient_id, patient_name = values
        # Set each text field with the corresponding value
        self.bed_id_text.delete("1.0", tk.END)
        self.bed_id_text.insert("1.0", str(bed_id))
        self.ward_id_text.delete("1.0", tk.END)
        self.ward_id_text.insert("1.0", str(ward_id))
        self.ward_name_text.delete("1.0", tk.END)
        self.ward_name_text.insert("1.0", str(ward_name))
        self.bed_number_text.delete("1.0", tk.END)
        self.bed_number_text.insert("1.0", str(bed_number))
        self.patient_id_text.delete("1.0", tk.END)
        self.availabilitycbox.set(availability)
        self.patient_id_text.delete("1.0", tk.END)
        self.patient_name_text.delete("1.0", tk.END)
        if availability=="Occupied":
            self.patient_id_text.insert("1.0", str(patient_id))
            self.patient_name_text.insert("1.0", str(patient_name))

    #Used to set department id and name from find department window
    def setward(self,id,name):
        self.ward_id_text.delete("1.0", tk.END)
        self.ward_id_text.insert("1.0", str(id))
        self.ward_name_text.delete("1.0", tk.END)
        self.ward_name_text.insert("1.0", str(name))

    def setPatient(self,id,name):
        self.patient_id_text.delete("1.0", tk.END)
        self.patient_id_text.insert("1.0", str(id))
        self.patient_name_text.delete("1.0", tk.END)
        self.patient_name_text.insert("1.0", str(name))

    #called when clicked fetch test button
    def fetchWard(self):
        ward_id = self.ward_id_text.get("1.0", "end-1c")
        try:
            ward = self.db.get_ward_name(ward_id)
        except:
            ward=None
        if ward:
            self.ward_name_text.delete("1.0", "end")
            self.ward_name_text.insert("1.0", ward[0])
        else:
            messagebox.showinfo("No ward Found", f"No ward found with ID: {ward_id}")
            self.focus_force()

    #called when clicked fetch patient button
    def fetchPatient(self):
        patient_id = self.patient_id_text.get("1.0", "end-1c")
        try:
            patient = self.db.get_patient_name(patient_id)
        except:
            patient=None
        if patient:
            self.patient_name_text.delete("1.0", "end")
            self.patient_name_text.insert("1.0", patient)
        else:
            messagebox.showinfo("No Patient Found", f"No Patient found with ID: {patient_id}")
            self.focus_force()

    #Called when clicked find button to open up find Patient window 
    def findPatient(self):
        fp.findPatients(self.db,self)

    #Called when clicked find button to open up find test window 
    def findWard(self):
        fw.findWard(self.db,self)


if __name__ == "__main__":
    app = AddBeds()
    app.mainloop()
