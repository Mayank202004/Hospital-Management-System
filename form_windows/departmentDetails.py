import tkinter as tk
import ttkbootstrap as bs
from ttkbootstrap.constants import *
import tkinter.messagebox as messagebox
import popupWindows.findDoctor as fd


class AddDepartment(tk.Tk):
    def __init__(self,db,ParentWindow,values=None):
        super().__init__()
        self.db=db
        self.ParentWindow=ParentWindow #To update table in TestsWindow from here
        self.create_widgets()
        if values:
            self.fill_fields(values)

    def create_widgets(self):
        self.title("Add Department Details")
        self.geometry("600x400")
        self.configure(bg="cornflowerblue")

        tk.Label(self, text="Department Details", font=("Helvetica", 25, "bold"), bg="cornflowerblue").place(x=150, y=20)

        mainframe = tk.Frame(self)  
        mainframe.place(x=30, y=80,width=550,height=300)  
        idframe = tk.Frame(mainframe)  
        idframe.place(x=10, y=15,width=835,height=45)
        nameframe = tk.Frame(mainframe)  
        nameframe.place(x=10, y=55,width=835,height=90)
        frametop = tk.Frame(mainframe)  
        frametop.place(x=40, y=105,width=835,height=145)  
        frame = tk.Frame(mainframe,bg='black')  
        frame.place(x=45, y=195,width=435,height=60) 

        # Create labels and entry fields for doctor details inside the frame
        tk.Label(idframe, text="Department ID:", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=16, pady=5)
        self.dept_id_text = tk.Text(idframe, height=1, width=15)
        self.dept_id_text.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(nameframe, text="Department Name:", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        self.dept_name_text = tk.Text(nameframe, height=1, width=50)
        self.dept_name_text.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frametop, text="HOD ID:", font=("Helvetica", 10, "bold")).grid(row=2, column=0, padx=5, pady=5)
        self.hod_id_text = tk.Text(frametop, height=1, width=20)
        self.hod_id_text.grid(row=2, column=1, padx=15, pady=5)
        tk.Button(frametop, text="Fetch",command=self.fetchHOD).grid(row=2,column=2)
        tk.Label(frametop, text="HOD Name:", font=("Helvetica", 10, "bold")).grid(row=3, column=0, padx=5, pady=5)
        self.hod_name_text = tk.Text(frametop, height=1, width=20)
        self.hod_name_text.grid(row=3, column=1, padx=15, pady=5)
        tk.Button(frametop, text="Find",command=self.findHOD).grid(row=3,column=2)
        

        # Create a Save button to save changes
        tk.Button(frame, text="Save", width=10, height=2,command=self.save).place(x=50, y=15)
        tk.Button(frame, text="Update", width=10, height=2,command=self.update).place(x=150, y=15)
        tk.Button(frame, text="Delete", width=10, height=2,command=self.delete).place(x=250, y=15)
        tk.Button(frame, text="Clear", width=10, height=2,command=self.clear).place(x=350, y=15)

    def save(self):
        # Retrieve values from the text fields and create a tuple
        dept_name = self.dept_name_text.get("1.0", "end-1c").strip()
        hod_id = self.hod_id_text.get("1.0", "end-1c").strip()

        # Check if any field is empty
        if not dept_name or not hod_id:
            messagebox.showerror("Error", "All fields are required!")
            self.focus_force()
            return
        values = (dept_name, hod_id)

        try:
            self.db.insertDepartment(values)
            messagebox.showinfo("Success", "Department information added successfully!")
            self.ParentWindow.setTable()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add department information: {str(e)}")
        self.destroy()

    def update(self):
        confirmation = messagebox.askyesno("Confirm Update", "Are you sure you want to update this department's information?")
        if confirmation:
            dept_name = self.dept_name_text.get("1.0", "end-1c").strip()
            hod_id = self.hod_id_text.get("1.0", "end-1c").strip()
            dept_id = self.dept_id_text.get("1.0", "end-1c").strip()
            values = (
                dept_name,
                hod_id
            )
            try:
                self.db.updateDepartment(values, dept_id)
                messagebox.showinfo("Success", "Department information updated successfully!")
                self.ParentWindow.setTable()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update department information: {str(e)}")
            self.destroy()

    def delete(self):
        confirmation = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this deparmtent's information?")
        if confirmation:
            identifier = self.dept_id_text.get("1.0", "end-1c")
            # Check if any field is empty
            if not identifier:
                messagebox.showerror("Error", "Department ID is compulsory!")
                self.focus_force()
                return
            try:
                self.db.deleteDepartment(identifier)
                messagebox.showinfo("Success", "Department information deleted successfully!")
                self.ParentWindow.setTable()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete department information: {str(e)}")
            self.destroy()

    def clear(self):
        self.dept_id_text.delete("1.0", "end")
        self.dept_name_text.delete("1.0", "end")
        self.hod_id_text.delete("1.0", "end")
        self.hod_name_text.delete("1.0", "end")


    def fill_fields(self, values):
        # Split the tuple into individual values
        dept_id, dept_name, hod_id, hod_name = values
        # Set each text field with the corresponding value
        self.dept_id_text.delete("1.0", tk.END)
        self.dept_id_text.insert("1.0", str(dept_id))
        self.dept_name_text.delete("1.0", tk.END)
        self.dept_name_text.insert("1.0", str(dept_name))
        self.hod_id_text.delete("1.0", tk.END)
        self.hod_id_text.insert("1.0", str(hod_id))
        self.hod_name_text.delete("1.0", tk.END)
        self.hod_name_text.insert("1.0", str(hod_name))

    #Used to set hod id and name from find doctor window
    def setDoctor(self,id,name):
        self.hod_id_text.delete("1.0", tk.END)
        self.hod_id_text.insert("1.0", str(id))
        self.hod_name_text.delete("1.0", tk.END)
        self.hod_name_text.insert("1.0", str(name))

    #called when clicked fetch hod button
    def fetchHOD(self):
        doc_id = self.hod_id_text.get("1.0", "end-1c")
        doc = self.db.get_doctor_name(doc_id)
        if doc:
            self.hod_name_text.delete("1.0", "end")
            self.hod_name_text.insert("1.0", doc)
        else:
            messagebox.showinfo("No Doctor Found", f"No Doctor found with ID: {doc_id}")
            self.focus_force()

    #Called when clicked find button to open up find doctor window 
    def findHOD(self):
        fd.findDoctors(self.db,self)



if __name__ == "__main__":
    app = AddDepartment()
    app.mainloop()
