import tkinter as tk
import ttkbootstrap as bs
import popupWindows.findPatient as fp
import popupWindows.findDoctor as fd
import tkinter.messagebox as messagebox

class EditAppointment(tk.Tk):
    def __init__(self,AppointmentWindow,values=None,db=None):
        super().__init__()
        self.db=db
        self.AppointmentWindow=AppointmentWindow
        self.create_widgets()
        if values:
            self.fill_fields(values)

    def create_widgets(self):
        self.title("Edit Doctor Details")
        self.geometry("1000x500")
        self.configure(bg="cornflowerblue")
        tk.Label(self, text="Appointment Detail", font=("Helvetica", 25, "bold"),bg="cornflower blue").place(x=350, y=20)

        mainframe = tk.Frame(self)  
        mainframe.place(x=80, y=100,width=850,height=390)  
        frametop = tk.Frame(mainframe,bg='black')  
        frametop.place(x=10, y=15,width=835,height=140)  
        addressframe = tk.Frame(mainframe,bg='green')  
        addressframe.place(x=10, y=160,width=835,height=130) 
        frame = tk.Frame(mainframe,bg='red')  
        frame.place(x=10, y=295,width=835,height=60) 

      
        # Create labels and entry fields for doctor details inside the frame
        tk.Label(frametop, text="Appointment ID:", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        self.app_id_text = tk.Text(frametop, height=1, width=15)
        self.app_id_text.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frametop, text="Patient ID:", font=("Helvetica", 10, "bold")).grid(row=1, column=0, padx=5, pady=5)
        self.patientid_text = tk.Text(frametop, height=1, width=15)
        self.patientid_text.grid(row=1, column=1, padx=5, pady=5)
        fetch_button = tk.Button(frametop, text="Fetch",command=self.fetchPatient)
        fetch_button.grid(row=1, column=2, padx=5, pady=5)
        tk.Label(frametop, text="Patient Name:", font=("Helvetica", 10, "bold")).grid(row=1, column=3, padx=5, pady=5)
        self.patient_name_text = tk.Text(frametop, height=1, width=30)
        self.patient_name_text.grid(row=1, column=4, padx=5, pady=5)
        findbutton = tk.Button(frametop, text="Find Patient",command=self.findPatient)
        findbutton.grid(row=1, column=5, padx=5, pady=5)
        tk.Label(frametop, text="Doctor ID:", font=("Helvetica", 10, "bold")).grid(row=2, column=0, padx=5, pady=5)
        self.doc_id_text = tk.Text(frametop, height=1, width=15)
        self.doc_id_text.grid(row=2, column=1, padx=5, pady=5)
        fetch_button2 = tk.Button(frametop, text="Fetch",command=self.fetchDoctor)
        fetch_button2.grid(row=2, column=2, padx=5, pady=5)
        tk.Label(frametop, text="Doctor Name:", font=("Helvetica", 10, "bold")).grid(row=2, column=3, padx=5, pady=5)
        self.doc_name_text = tk.Text(frametop, height=1, width=30)
        self.doc_name_text.grid(row=2, column=4, padx=5, pady=5)
        findbutton2 = tk.Button(frametop, text="Find Doctor",command=self.findDoctor)
        findbutton2.grid(row=2, column=5, padx=5, pady=5)

        tk.Label(addressframe, text="Appointment Date:", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        self.date_text = tk.Text(addressframe, height=1, width=30)
        self.date_text.grid(row=0, column=1, padx=1, pady=5)
        tk.Label(addressframe, text="Reason:", font=("Helvetica", 10, "bold")).grid(row=1, column=0, padx=5, pady=5)
        self.reason_text = tk.Text(addressframe, height=1, width=30)
        self.reason_text.grid(row=1, column=1, padx=1, pady=5)
        tk.Label(addressframe, text="Status:", font=("Helvetica", 10, "bold")).grid(row=2, column=0, padx=5, pady=5)
        self.status_text = tk.Text(addressframe, height=1, width=30)
        self.status_text.grid(row=2, column=1, padx=5, pady=5)
        
        # Create a Save button to save changes
        tk.Button(frame, text="Save", width=10, height=2,command=self.save).place(x=50, y=10)
        tk.Button(frame, text="Update", width=10, height=2,command=self.update).place(x=150, y=10)
        tk.Button(frame, text="Delete", width=10, height=2,command=self.delete).place(x=250, y=10)
        tk.Button(frame, text="Clear", width=10, height=2,command=self.clear).place(x=350, y=10)

    def save(self):
        values = (
            self.patientid_text.get("1.0", "end-1c"),
            self.doc_id_text.get("1.0", "end-1c"),
            self.date_text.get("1.0", "end-1c"),
            self.reason_text.get("1.0", "end-1c"),
            self.status_text.get("1.0", "end-1c")
        )
        try:
            self.db.insertAppointment(values)
            messagebox.showinfo("Success", "Appointment added successfully!")
            self.AppointmentWindow.setTable()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add appointment: {str(e)}")
        self.destroy()
    
    def update(self):
        confirmation = messagebox.askyesno("Confirm Update", "Are you sure you want to update this appointment's information?")
        if confirmation:
            values = (
                self.patientid_text.get("1.0", "end-1c"),
                self.doc_id_text.get("1.0", "end-1c"),
                self.date_text.get("1.0", "end-1c"),
                self.reason_text.get("1.0", "end-1c"),
                self.status_text.get("1.0", "end-1c")
            )
            identifier = self.app_id_text.get("1.0", "end-1c")
            try:
                self.db.updateAppointment(values, identifier)
                messagebox.showinfo("Success", "Appointment information updated successfully!")
                self.AppointmentWindow.setTable()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update appointment information: {str(e)}")
            self.destroy()
    
    def delete(self):
        confirmation = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this appointment's information?")
        if confirmation:
            identifier = self.app_id_text.get("1.0", "end-1c")
            try:
                self.db.deleteAppointment(identifier)
                messagebox.showinfo("Success", "Appointment information deleted successfully!")
                self.AppointmentWindow.setTable()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete appointment information: {str(e)}")
            self.destroy()
    
    def clear(self):
        self.app_id_text.delete("1.0","end")
        self.patientid_text.delete("1.0", "end"),
        self.patient_name_text.delete("1.0","end"),
        self.doc_id_text.delete("1.0", "end"),
        self.doc_name_text.delete("1.0","end"),
        self.date_text.delete("1.0", "end"),
        self.reason_text.delete("1.0", "end"),
        self.status_text.delete("1.0", "end")


    def fill_fields(self, values):
        # Split the tuple into individual values
        appointment_id, patient_id, patient_name, doctor_id, doctor_name, appointment_date, reason, status = values
        
        # Set each text field with the corresponding value
        self.app_id_text.delete("1.0", tk.END)
        self.app_id_text.insert("1.0", str(appointment_id))
        
        self.patientid_text.delete("1.0", tk.END)
        self.patientid_text.insert("1.0", str(patient_id))
        
        self.patient_name_text.delete("1.0", tk.END)
        self.patient_name_text.insert("1.0", str(patient_name))
        
        self.doc_id_text.delete("1.0", tk.END)
        self.doc_id_text.insert("1.0", str(doctor_id))
        
        self.doc_name_text.delete("1.0", tk.END)
        self.doc_name_text.insert("1.0", str(doctor_name))
        
        self.date_text.delete("1.0", tk.END)
        self.date_text.insert("1.0", str(appointment_date))
        
        self.reason_text.delete("1.0", tk.END)
        self.reason_text.insert("1.0", str(reason))
        
        self.status_text.delete("1.0", tk.END)
        self.status_text.insert("1.0", str(status))

    def findPatient(self):
        fp.findPatients(self.db,self)
    
    def setPatient(self,id,name):
        self.patientid_text.delete("1.0", tk.END)
        self.patientid_text.insert("1.0", str(id))
        self.patient_name_text.delete("1.0", tk.END)
        self.patient_name_text.insert("1.0", str(name))

    def findDoctor(self):
        fd.findDoctors(self.db,self)
    
    def setDoctor(self,id,name):
        self.doc_id_text.delete("1.0", tk.END)
        self.doc_id_text.insert("1.0", str(id))
        self.doc_name_text.delete("1.0", tk.END)
        self.doc_name_text.insert("1.0", str(name))

    def fetchPatient(self):
        patient_id = self.patientid_text.get("1.0", "end-1c")
        patient_name = self.db.get_patient_name(patient_id)
        if patient_name:
            self.patient_name_text.delete("1.0", "end")
            self.patient_name_text.insert("1.0", patient_name)
        else:
            messagebox.showinfo("No Patient Found", f"No patient found with ID: {patient_id}")
    
    def fetchDoctor(self):
        doctor_id = self.doc_id_text.get("1.0", "end-1c")
        doctor_name = self.db.get_doctor_name(doctor_id)
        if doctor_name:
            self.doc_name_text.delete("1.0", "end")
            self.doc_name_text.insert("1.0", doctor_name)
        else:
            messagebox.showinfo("No Doctor Found", f"No doctor found with ID: {doctor_id}")



    

        


if __name__ == "__main__":
    stye=bs.Style()
    app = EditAppointment()
    app.mainloop()
