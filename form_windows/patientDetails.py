import tkinter as tk
import tkinter.messagebox as messagebox

class EditPatients(tk.Tk):
    def __init__(self,db,PatientWindow, values=None):
        super().__init__()
        self.db=db
        self.PatientWindow=PatientWindow #To update table in PatientWindow from here
        self.create_widgets()
        if values:
            self.fill_fields(values)
        

    def create_widgets(self):
        self.title("Edit Patient Details")
        self.geometry("1000x500")
        self.configure(bg="cornflowerblue")

        tk.Label(self, text="Patient Detail", font=("Helvetica", 25, "bold"), bg="cornflowerblue").place(x=400, y=20)

        mainframe = tk.Frame(self)  
        mainframe.place(x=80, y=100,width=850,height=380)  
        frametop = tk.Frame(mainframe)  
        frametop.place(x=10, y=15,width=835,height=90)  
        frame = tk.Frame(mainframe)  
        frame.place(x=10, y=97,width=835,height=270) 


        # Create labels and entry fields for patient details inside the frame
        tk.Label(frametop, text="Patient ID:", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        self.patient_id_text = tk.Text(frametop, height=1, width=15)
        self.patient_id_text.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frametop, text="Name:", font=("Helvetica", 10, "bold")).grid(row=0, column=2, padx=5, pady=5)
        self.name_text = tk.Text(frametop, height=1, width=30)
        self.name_text.grid(row=0, column=3, padx=5, pady=5)
        tk.Label(frametop, text="Date of Birth:", font=("Helvetica", 10, "bold")).grid(row=0, column=4, padx=5, pady=5)
        self.date_of_birth_text = tk.Text(frametop, height=1, width=30)
        self.date_of_birth_text.grid(row=0, column=5, padx=5, pady=5)
        tk.Label(frametop, text="Gender:", font=("Helvetica", 10, "bold")).grid(row=1, column=0, padx=5, pady=5)
        self.gender_text = tk.Text(frametop, height=1, width=15)
        self.gender_text.grid(row=1, column=1, padx=1, pady=5)
        tk.Label(frametop, text="Contact:", font=("Helvetica", 10, "bold")).grid(row=1, column=2, padx=5, pady=5)
        self.contact_text = tk.Text(frametop, height=1, width=30)
        self.contact_text.grid(row=1, column=3, padx=5, pady=5)
        tk.Label(frametop, text="Email:", font=("Helvetica", 10, "bold")).grid(row=1, column=4, padx=5, pady=5)
        self.email_text = tk.Text(frametop, height=1, width=30)
        self.email_text.grid(row=1, column=5, padx=5, pady=5)
        tk.Label(frame, text="Blood Type:", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        self.blood_type_text = tk.Text(frame, height=1, width=30)
        self.blood_type_text.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frame, text="Insurance Provider:", font=("Helvetica", 10, "bold")).grid(row=0, column=2, padx=5, pady=5)
        self.insurance_provider_text = tk.Text(frame, height=1, width=30)
        self.insurance_provider_text.grid(row=0, column=3, padx=5, pady=5)
        tk.Label(frame, text="Emergency Contact Name:", font=("Helvetica", 10, "bold")).grid(row=1, column=0, padx=5, pady=5)
        self.emergency_contact_name_text = tk.Text(frame, height=1, width=30)
        self.emergency_contact_name_text.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(frame, text="Emergency Contact Number:", font=("Helvetica", 10, "bold")).grid(row=1, column=2, padx=5, pady=5)
        self.emergency_contact_number_text = tk.Text(frame, height=1, width=30)
        self.emergency_contact_number_text.grid(row=1, column=3, padx=5, pady=5)
        tk.Label(frame, text="Allergies:", font=("Helvetica", 10, "bold")).grid(row=2, column=0, padx=5, pady=5)
        self.allergies_text = tk.Text(frame, height=1, width=30)
        self.allergies_text.grid(row=2, column=1, padx=5, pady=5)
        tk.Label(frame, text="Medical History:", font=("Helvetica", 10, "bold")).grid(row=3, column=0, padx=5, pady=5)
        self.medical_history_text = tk.Text(frame, height=1, width=30)
        self.medical_history_text.grid(row=3, column=1, padx=5, pady=5)

        
        # Create a Save button to save changes
        tk.Button(frame, text="Save", width=10, height=2,command=self.save).place(x=50, y=210)
        tk.Button(frame, text="Update", width=10, height=2,command=self.update).place(x=150, y=210)
        tk.Button(frame, text="Delete", width=10, height=2,command=self.delete).place(x=250, y=210)
        tk.Button(frame, text="Clear", width=10, height=2,command=self.clear).place(x=350, y=210)

    def save(self):
        # Retrieve values from the text fields and create a tuple
        values = (
        self.name_text.get("1.0", "end-1c"),
        self.date_of_birth_text.get("1.0", "end-1c"),
        self.gender_text.get("1.0", "end-1c"),
        self.contact_text.get("1.0", "end-1c"),
        self.email_text.get("1.0", "end-1c"),
        self.blood_type_text.get("1.0", "end-1c"),
        self.insurance_provider_text.get("1.0", "end-1c"),
        self.emergency_contact_name_text.get("1.0", "end-1c"),
        self.emergency_contact_number_text.get("1.0", "end-1c"),
        self.allergies_text.get("1.0", "end-1c"),
        self.medical_history_text.get("1.0", "end-1c")
        )
        try:
            self.db.insertPatient(values)
            messagebox.showinfo("Success", "Patient information saved successfully!")
            self.PatientWindow.setTable()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save patient information: {str(e)}")
        self.destroy()
        
    def update(self):
        confirmation = messagebox.askyesno("Confirm Update", "Are you sure you want to update this patient's information?")
        if confirmation:
            values = (
            self.name_text.get("1.0", "end-1c"),
            self.date_of_birth_text.get("1.0", "end-1c"),
            self.gender_text.get("1.0", "end-1c"),
            self.contact_text.get("1.0", "end-1c"),
            self.email_text.get("1.0", "end-1c"),
            self.blood_type_text.get("1.0", "end-1c"),
            self.insurance_provider_text.get("1.0", "end-1c"),
            self.emergency_contact_name_text.get("1.0", "end-1c"),
            self.emergency_contact_number_text.get("1.0", "end-1c"),
            self.allergies_text.get("1.0", "end-1c"),
            self.medical_history_text.get("1.0", "end-1c")
            )
            identifier=self.patient_id_text.get("1.0","end-1c")
            try:
                self.db.updatePatient(values, identifier)
                messagebox.showinfo("Success", "Patient information updated successfully!")
                self.PatientWindow.setTable()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update patient information: {str(e)}")
            self.destroy()
    def delete(self):
        confirmation = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this patient's information?")
        if confirmation:
            identifier=self.patient_id_text.get("1.0","end-1c")
            try:
                self.db.deletePatient(identifier)
                messagebox.showinfo("Success", "Patient information deleted successfully!")
                self.PatientWindow.setTable()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update patient information: {str(e)}")
            self.destroy()
    def clear(self):
        self.patient_id_text.delete("1.0","end")
        self.name_text.delete("1.0", "end")
        self.date_of_birth_text.delete("1.0", "end")
        self.gender_text.delete("1.0", "end")
        self.contact_text.delete("1.0", "end")
        self.email_text.delete("1.0", "end")
        self.blood_type_text.delete("1.0", "end")
        self.insurance_provider_text.delete("1.0", "end")
        self.emergency_contact_name_text.delete("1.0", "end")
        self.emergency_contact_number_text.delete("1.0", "end")
        self.allergies_text.delete("1.0", "end")
        self.medical_history_text.delete("1.0", "end")

    #Called when object is created with parameters 
    def fill_fields(self, values):
            # Split the tuple into individual values
            patient_id, name, date_of_birth, gender, contact_number, email, blood_type, insurance_provider, emergency_contact_name, emergency_contact_number, allergies, medical_history = values

            # Set each text field with the corresponding value
            self.patient_id_text.delete("1.0", "end")
            self.patient_id_text.insert("1.0", patient_id)
            self.name_text.delete("1.0", "end")
            self.name_text.insert("1.0", name)
            self.date_of_birth_text.delete("1.0", "end")
            self.date_of_birth_text.insert("1.0", date_of_birth)
            self.gender_text.delete("1.0", "end")
            self.gender_text.insert("1.0", gender)
            self.contact_text.delete("1.0", "end")
            self.contact_text.insert("1.0", contact_number)
            self.email_text.delete("1.0", "end")
            self.email_text.insert("1.0", email)
            self.blood_type_text.delete("1.0", "end")
            self.blood_type_text.insert("1.0", blood_type)
            self.insurance_provider_text.delete("1.0", "end")
            self.insurance_provider_text.insert("1.0", insurance_provider)
            self.emergency_contact_name_text.delete("1.0", "end")
            self.emergency_contact_name_text.insert("1.0", emergency_contact_name)
            self.emergency_contact_number_text.delete("1.0", "end")
            self.emergency_contact_number_text.insert("1.0", emergency_contact_number)
            self.allergies_text.delete("1.0", "end")
            self.allergies_text.insert("1.0", allergies)
            self.medical_history_text.delete("1.0", "end")
            self.medical_history_text.insert("1.0", medical_history)

if __name__ == "__main__":
    app = EditPatients()
    app.mainloop()
