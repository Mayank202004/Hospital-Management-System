import tkinter as tk
import ttkbootstrap as bs
from ttkbootstrap.constants import *
import tkinter.messagebox as messagebox
import popupWindows.findPatient as fp
import popupWindows.findTest as ft


class AddTestResult(tk.Tk):
    def __init__(self,db,TestResultWindow,values=None):
        super().__init__()
        self.db=db
        self.TestResultWindow=TestResultWindow #To update table in TestsWindow from here
        self.create_widgets()
        if values:
            self.fill_fields(values)

    def create_widgets(self):
        self.title("Add Test Result Details")
        self.geometry("600x550")
        self.configure(bg="cornflowerblue")

        tk.Label(self, text="Test Result Details", font=("Helvetica", 25, "bold"), bg="cornflowerblue").place(x=150, y=20)

        mainframe = tk.Frame(self)  
        mainframe.place(x=30, y=80,width=550,height=450)  
        idframe = tk.Frame(mainframe)  
        idframe.place(x=10, y=15,width=835,height=45)
        nameframe = tk.Frame(mainframe)  
        nameframe.place(x=10, y=55,width=835,height=90)
        frametop = tk.Frame(mainframe)  
        frametop.place(x=40, y=145,width=835,height=195)  
        frame = tk.Frame(mainframe,bg='black')  
        frame.place(x=45, y=370,width=435,height=60) 

        # Create labels and entry fields for doctor details inside the frame
        tk.Label(idframe, text="Result ID:", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=16, pady=5)
        self.result_id_text = tk.Text(idframe, height=1, width=15)
        self.result_id_text.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(nameframe, text="Test ID:", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        self.test_id_text = tk.Text(nameframe, height=1, width=30)
        self.test_id_text.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(nameframe, text="Fetch",command=self.fetchTest).grid(row=0,column=2)
        tk.Label(nameframe, text="Test Name:", font=("Helvetica", 10, "bold")).grid(row=1, column=0, padx=5, pady=5)
        self.test_name_text = tk.Text(nameframe, height=1, width=30)
        self.test_name_text.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(nameframe, text="Find",command=self.findTest).grid(row=1,column=2)
        tk.Label(frametop, text="Patient ID:", font=("Helvetica", 10, "bold")).grid(row=2, column=0, padx=5, pady=5)
        self.patient_id_text = tk.Text(frametop, height=1, width=20)
        self.patient_id_text.grid(row=2, column=1, padx=15, pady=5)
        tk.Button(frametop, text="Fetch",command=self.fetchPatient).grid(row=2,column=2)
        tk.Label(frametop, text="Patient Name:", font=("Helvetica", 10, "bold")).grid(row=3, column=0, padx=5, pady=5)
        self.patient_name_text = tk.Text(frametop, height=1, width=20)
        self.patient_name_text.grid(row=3, column=1, padx=15, pady=5)
        tk.Button(frametop, text="Find",command=self.findPatient).grid(row=3,column=2)
        tk.Label(frametop, text="Result Date (YYYY-MM-DD):", font=("Helvetica", 10, "bold")).grid(row=4, column=0, padx=5, pady=5)
        self.result_date_text = tk.Text(frametop, height=1, width=20)
        self.result_date_text.grid(row=4, column=1, padx=15, pady=5)
        tk.Label(frametop, text="Result Details:", font=("Helvetica", 10, "bold")).grid(row=5, column=0, padx=5, pady=5)
        self.result_details_text = tk.Text(frametop, height=3, width=45)
        self.result_details_text.place(x=195, y=125)
        

        # Create a Save button to save changes
        tk.Button(frame, text="Save", width=10, height=2,command=self.save).place(x=50, y=15)
        tk.Button(frame, text="Update", width=10, height=2,command=self.update).place(x=150, y=15)
        tk.Button(frame, text="Delete", width=10, height=2,command=self.delete).place(x=250, y=15)
        tk.Button(frame, text="Clear", width=10, height=2,command=self.clear).place(x=350, y=15)

    def save(self):
        # Retrieve values from the text fields and create a tuple
        test_id = self.test_id_text.get("1.0", "end-1c").strip()
        patient_id = self.patient_id_text.get("1.0", "end-1c").strip()
        result_date = self.result_date_text.get("1.0", "end-1c").strip()
        result_desc = self.result_details_text.get("1.0", "end-1c").strip()

        # Check if any field is empty
        if not test_id or not patient_id or not result_date or not result_desc:
            messagebox.showerror("Error", "All fields are required!")
            self.focus_force()
            return
        values = (test_id,patient_id,result_date,result_desc)

        try:
            self.db.insertTestResult(values)
            messagebox.showinfo("Success", "Test information added successfully!")
            self.TestResultWindow.setTable()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add test information: {str(e)}")
        self.destroy()

    def update(self):
        confirmation = messagebox.askyesno("Confirm Update", "Are you sure you want to update this test's information?")
        if confirmation:
            values = (
                self.test_name_text.get("1.0", "end-1c"),
                self.deptid_text.get("1.0", "end-1c"),
                self.deptname_text.get("1.0", "end-1c"),
                self.price_text.get("1.0", "end-1c"),   
      
            )
            identifier = self.test_id_text.get("1.0", "end-1c")
            try:
                self.db.updateTestResult(values, identifier)
                messagebox.showinfo("Success", "Test information updated successfully!")
                self.TestResultWindow.setTable()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update test information: {str(e)}")
            self.destroy()

    def delete(self):
        confirmation = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this Tests's information?")
        if confirmation:
            identifier = self.test_id_text.get("1.0", "end-1c")
            try:
                self.db.deleteTestResult(identifier)
                messagebox.showinfo("Success", "Test information deleted successfully!")
                self.TestResultWindow.setTable()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete test information: {str(e)}")
            self.destroy()

    def clear(self):
        self.result_id_text.delete("1.0", "end")
        self.test_id_text.delete("1.0", "end")
        self.test_name_text.delete("1.0", "end")
        self.patient_id_text.delete("1.0", "end")
        self.patient_name_text.delete("1.0", "end")
        self.result_date_text.delete("1.0", "end")
        self.result_details_text.delete("1.0", "end")


    def fill_fields(self, values):
        # Split the tuple into individual values
        result_id, test_id, test_name, patient_id, patient_name, test_date, test_desc = values
        # Set each text field with the corresponding value
        self.result_id_text.delete("1.0", tk.END)
        self.result_id_text.insert("1.0", str(result_id))
        self.test_id_text.delete("1.0", tk.END)
        self.test_id_text.insert("1.0", str(test_id))
        self.test_name_text.delete("1.0", tk.END)
        self.test_name_text.insert("1.0", str(test_name))
        self.patient_id_text.delete("1.0", tk.END)
        self.patient_id_text.insert("1.0", str(patient_id))
        self.patient_name_text.delete("1.0", tk.END)
        self.patient_name_text.insert("1.0", str(patient_name))
        self.result_date_text.delete("1.0", tk.END)
        self.result_date_text.insert("1.0", str(test_date))
        self.result_details_text.delete("1.0", tk.END)
        self.result_details_text.insert("1.0", str(test_desc))

    #Used to set department id and name from find department window
    def setTest(self,id,name):
        self.test_id_text.delete("1.0", tk.END)
        self.test_id_text.insert("1.0", str(id))
        self.test_name_text.delete("1.0", tk.END)
        self.test_name_text.insert("1.0", str(name))

    def setPatient(self,id,name):
        self.patient_id_text.delete("1.0", tk.END)
        self.patient_id_text.insert("1.0", str(id))
        self.patient_name_text.delete("1.0", tk.END)
        self.patient_name_text.insert("1.0", str(name))

    #called when clicked fetch test button
    def fetchTest(self):
        test_id = self.test_id_text.get("1.0", "end-1c")
        test = self.db.get_test_name(test_id)
        if test:
            self.test_name_text.delete("1.0", "end")
            self.test_name_text.insert("1.0", test[0])
        else:
            messagebox.showinfo("No Test Found", f"No Test found with ID: {test_id}")
            self.focus_force()

    #called when clicked fetch patient button
    def fetchPatient(self):
        patient_id = self.patient_id_text.get("1.0", "end-1c")
        patient = self.db.get_patient_name(patient_id)
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
    def findTest(self):
        ft.findTests(self.db,self)


if __name__ == "__main__":
    app = AddTestResult()
    app.mainloop()
