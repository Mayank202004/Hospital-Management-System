import tkinter as tk
import ttkbootstrap as bs
from ttkbootstrap.constants import *
import tkinter.messagebox as messagebox
import re

class EditDoctors(tk.Tk):
    def __init__(self,db,DoctorWindow,values=None):
        super().__init__()
        self.db=db
        self.DoctorWindow=DoctorWindow #To update table in DoctorWindow from here
        self.create_widgets()
        if values:
            self.fill_fields(values)

    def create_widgets(self):
        self.title("Edit Doctor Details")
        self.geometry("1000x500")
        self.configure(bg="cornflowerblue")

        tk.Label(self, text="Doctor Detail", font=("Helvetica", 25, "bold"), bg="cornflowerblue").place(x=400, y=20)

        mainframe = tk.Frame(self)  
        mainframe.place(x=80, y=100,width=850,height=390)  
        frametop = tk.Frame(mainframe)  
        frametop.place(x=10, y=15,width=835,height=90)  
        addressframe = tk.Frame(mainframe)  
        addressframe.place(x=10, y=93,width=835,height=45) 
        frame = tk.Frame(mainframe)  
        frame.place(x=10, y=135,width=835,height=270) 

        # Create labels and entry fields for doctor details inside the frame
        tk.Label(frametop, text="Doctor ID:", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        self.doctor_id_text = tk.Text(frametop, height=1, width=15)
        self.doctor_id_text.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frametop, text="First Name:", font=("Helvetica", 10, "bold")).grid(row=0, column=2, padx=5, pady=5)
        self.first_name_text = tk.Text(frametop, height=1, width=30)
        self.first_name_text.grid(row=0, column=3, padx=5, pady=5)
        tk.Label(frametop, text="Last Name:", font=("Helvetica", 10, "bold")).grid(row=0, column=4, padx=5, pady=5)
        self.last_name_text = tk.Text(frametop, height=1, width=30)
        self.last_name_text.grid(row=0, column=5, padx=5, pady=5)
        tk.Label(frametop, text="Specialization:", font=("Helvetica", 10, "bold")).grid(row=1, column=0, padx=5, pady=5)
        self.specialization_text = tk.Text(frametop, height=1, width=15)
        self.specialization_text.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(frametop, text="Contact:", font=("Helvetica", 10, "bold")).grid(row=1, column=2, padx=5, pady=5)
        self.contact_text = tk.Text(frametop, height=1, width=30)
        self.contact_text.grid(row=1, column=3, padx=5, pady=5)
        tk.Label(frametop, text="Email:", font=("Helvetica", 10, "bold")).grid(row=1, column=4, padx=5, pady=5)
        self.email_text = tk.Text(frametop, height=1, width=30)
        self.email_text.grid(row=1, column=5, padx=5, pady=5)
        tk.Label(addressframe, text="Address:", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        self.address_text = tk.Text(addressframe, height=1, width=120)
        self.address_text.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frame, text="Gender:", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        self.gender_text = tk.Text(frame, height=1, width=25)
        self.gender_text.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frame, text="Date of Birth:", font=("Helvetica", 10, "bold")).grid(row=0, column=2, padx=5, pady=5)
        self.date_of_birth_text = tk.Text(frame, height=1, width=25)
        self.date_of_birth_text.grid(row=0, column=3, padx=5, pady=5)
        tk.Label(frame, text="Joining Date:", font=("Helvetica", 10, "bold")).grid(row=1, column=0, padx=5, pady=5)
        self.joining_date_text = tk.Text(frame, height=1, width=25)
        self.joining_date_text.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(frame, text="Qualification:", font=("Helvetica", 10, "bold")).grid(row=2, column=0, padx=5, pady=5)
        self.qualification_text = tk.Text(frame, height=1, width=25)
        self.qualification_text.grid(row=2, column=1, padx=5, pady=5)
        tk.Label(frame, text="Experience:", font=("Helvetica", 10, "bold")).grid(row=3, column=0, padx=5, pady=5)
        self.experience_text = tk.Text(frame, height=1, width=25)
        self.experience_text.grid(row=3, column=1, padx=5, pady=5)
        tk.Label(frame, text="Department:", font=("Helvetica", 10, "bold")).grid(row=4, column=0, padx=5, pady=5)
        self.department_text = tk.Text(frame, height=1, width=25)
        self.department_text.grid(row=4, column=1, padx=5, pady=5)

        # Create a Save button to save changes
        tk.Button(frame, text="Save", width=10, height=2,command=self.save).place(x=50, y=210)
        tk.Button(frame, text="Update", width=10, height=2,command=self.update).place(x=150, y=210)
        tk.Button(frame, text="Delete", width=10, height=2,command=self.delete).place(x=250, y=210)
        tk.Button(frame, text="Clear", width=10, height=2,command=self.clear).place(x=350, y=210)

    def save(self):
    # Retrieve values from the text fields and create a tuple
        values = (
            self.first_name_text.get("1.0", "end-1c"),
            self.last_name_text.get("1.0", "end-1c"),
            self.specialization_text.get("1.0", "end-1c"),
            self.contact_text.get("1.0", "end-1c"),
            self.email_text.get("1.0", "end-1c"),
            self.address_text.get("1.0", "end-1c"),
            self.gender_text.get("1.0", "end-1c"),
            self.date_of_birth_text.get("1.0", "end-1c"),
            self.joining_date_text.get("1.0", "end-1c"),
            self.qualification_text.get("1.0", "end-1c"),
            self.experience_text.get("1.0", "end-1c"),
            self.department_text.get("1.0", "end-1c")
        )
        if not values[0].replace(" ", "").isalpha():
            messagebox.showerror("Validation Error","First Name must include only alphabets")
            self.focus_force() # force the docWindow to stay at front or else it goes behind main window
            return
        elif not values[1].replace(" ", "").isalpha():
            messagebox.showerror("Validation Error","Last Name must include only alphabets")
            self.focus_force() # force the docWindow to stay at front or else it goes behind main window
            return
        elif not values[2].replace(" ", "").isalpha():
            messagebox.showerror("Validation Error","Specialization must include only alphabets")
            self.focus_force() # force the docWindow to stay at front or else it goes behind main window
            return
        elif  not (values[3].isdigit() and len(values[3])==10):
            messagebox.showerror("Validation Error","Contact number must include only 10 digits")
            self.focus_force() # force the docWindow to stay at front or else it goes behind main window
            return
        #USed regular Expressions to match email id pattern
        elif not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", values[4]):
            messagebox.showerror("Validation Error","Enter proper Email ID")
            self.focus_force() # force the docWindow to stay at front or else it goes behind main window
            return
        elif values[6].lower() not in ['male','female','other']:
            messagebox.showerror("Validation Error","Gender must be within male/female/other only")
            self.focus_force() # force the docWindow to stay at front or else it goes behind main window
            return
        #used regular expressions to match dob pattern
        elif not re.match(r"^\d{4}-\d{2}-\d{2}$",values[7]):
            messagebox.showerror("Validation Error","DOB must be in format YYYY-MM-DD")
            self.focus_force() # force the docWindow to stay at front or else it goes behind main window
            return
        elif not re.match(r"^\d{4}-\d{2}-\d{2}$",values[8]):
            messagebox.showerror("Validation Error","Joining Date must be in format YYYY-MM-DD")
            self.focus_force() # force the docWindow to stay at front or else it goes behind main window
            return
        try:
            self.db.insertDoctor(values)
            messagebox.showinfo("Success", "Doctor information added successfully!")
            self.DoctorWindow.setTable()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add doctor information: {str(e)}")
        self.destroy()

    def update(self):
        confirmation = messagebox.askyesno("Confirm Update", "Are you sure you want to update this doctor's information?")
        if confirmation:
            values = (
                self.first_name_text.get("1.0", "end-1c"),
                self.last_name_text.get("1.0", "end-1c"),
                self.specialization_text.get("1.0", "end-1c"),
                self.contact_text.get("1.0", "end-1c"),
                self.email_text.get("1.0", "end-1c"),
                self.address_text.get("1.0", "end-1c"),
                self.gender_text.get("1.0", "end-1c"),
                self.date_of_birth_text.get("1.0", "end-1c"),
                self.joining_date_text.get("1.0", "end-1c"),
                self.qualification_text.get("1.0", "end-1c"),
                self.experience_text.get("1.0", "end-1c"),
                self.department_text.get("1.0", "end-1c")
            )
            identifier = self.doctor_id_text.get("1.0", "end-1c")
            try:
                self.db.updateDoctor(values, identifier)
                messagebox.showinfo("Success", "Doctor information updated successfully!")
                self.DoctorWindow.setTable()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update doctor information: {str(e)}")
            self.destroy()

    def delete(self):
        confirmation = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this doctor's information?")
        if confirmation:
            identifier = self.doctor_id_text.get("1.0", "end-1c")
            try:
                self.db.deleteDoctor(identifier)
                messagebox.showinfo("Success", "Doctor information deleted successfully!")
                self.DoctorWindow.setTable()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete doctor information: {str(e)}")
            self.destroy()

    def clear(self):
        self.doctor_id_text.delete("1.0", "end")
        self.first_name_text.delete("1.0", "end")
        self.last_name_text.delete("1.0", "end")
        self.specialization_text.delete("1.0", "end")
        self.contact_text.delete("1.0", "end")
        self.email_text.delete("1.0", "end")
        self.address_text.delete("1.0", "end")
        self.gender_text.delete("1.0", "end")
        self.date_of_birth_text.delete("1.0", "end")
        self.joining_date_text.delete("1.0", "end")
        self.qualification_text.delete("1.0", "end")
        self.experience_text.delete("1.0", "end")
        self.department_text.delete("1.0", "end")


    def fill_fields(self, values):
        # Split the tuple into individual values
        doctor_id, first_name, last_name, specialization, contact_number, email, address, gender, date_of_birth, joining_date, qualification, experience, department = values
        # Set each text field with the corresponding value
        self.doctor_id_text.delete("1.0", tk.END)
        self.doctor_id_text.insert("1.0", str(doctor_id))
        self.first_name_text.delete("1.0", tk.END)
        self.first_name_text.insert("1.0", str(first_name))
        self.last_name_text.delete("1.0", tk.END)
        self.last_name_text.insert("1.0", str(last_name))
        self.specialization_text.delete("1.0", tk.END)
        self.specialization_text.insert("1.0", str(specialization))
        self.contact_text.delete("1.0", tk.END)
        self.contact_text.insert("1.0", str(contact_number))
        self.email_text.delete("1.0", tk.END)
        self.email_text.insert("1.0", str(email))
        self.address_text.delete("1.0", tk.END)
        self.address_text.insert("1.0", str(address))
        self.gender_text.delete("1.0", tk.END)
        self.gender_text.insert("1.0", str(gender))
        self.date_of_birth_text.delete("1.0", tk.END)
        self.date_of_birth_text.insert("1.0", str(date_of_birth))
        self.joining_date_text.delete("1.0", tk.END)
        self.joining_date_text.insert("1.0", str(joining_date))
        self.qualification_text.delete("1.0", tk.END)
        self.qualification_text.insert("1.0", str(qualification))
        self.experience_text.delete("1.0", tk.END)
        self.experience_text.insert("1.0", str(experience))
        self.department_text.delete("1.0", tk.END)
        self.department_text.insert("1.0", str(department))


        


if __name__ == "__main__":
    app = EditDoctors()
    app.mainloop()
