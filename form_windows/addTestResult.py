import tkinter as tk
import ttkbootstrap as bs
from ttkbootstrap.constants import *
import tkinter.messagebox as messagebox
import popupWindows.findDepartment as fd


class AddTest(tk.Tk):
    def __init__(self,db,TestWindow,values=None):
        super().__init__()
        self.db=db
        self.TestWindow=TestWindow #To update table in TestsWindow from here
        self.create_widgets()
        if values:
            self.fill_fields(values)

    def create_widgets(self):
        self.title("Add Test Details")
        self.geometry("600x450")
        self.configure(bg="cornflowerblue")

        tk.Label(self, text="Medical Test Details", font=("Helvetica", 25, "bold"), bg="cornflowerblue").place(x=150, y=20)

        mainframe = tk.Frame(self)  
        mainframe.place(x=30, y=80,width=550,height=350)  
        idframe = tk.Frame(mainframe)  
        idframe.place(x=10, y=15,width=835,height=45)
        nameframe = tk.Frame(mainframe)  
        nameframe.place(x=10, y=55,width=835,height=90)
        frametop = tk.Frame(mainframe)  
        frametop.place(x=40, y=145,width=835,height=145)  
        frame = tk.Frame(mainframe,bg='black')  
        frame.place(x=45, y=270,width=435,height=60) 

        # Create labels and entry fields for doctor details inside the frame
        tk.Label(idframe, text="Test ID:", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=16, pady=5)
        self.test_id_text = tk.Text(idframe, height=1, width=15)
        self.test_id_text.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(nameframe, text="Test Name:", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        self.test_name_text = tk.Text(nameframe, height=1, width=50)
        self.test_name_text.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(nameframe, text="Price:", font=("Helvetica", 10, "bold")).grid(row=1, column=0, padx=5, pady=5)
        self.price_text = tk.Text(nameframe, height=1, width=50)
        self.price_text.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(frametop, text="Department ID:", font=("Helvetica", 10, "bold")).grid(row=2, column=0, padx=5, pady=5)
        self.deptid_text = tk.Text(frametop, height=1, width=20)
        self.deptid_text.grid(row=2, column=1, padx=15, pady=5)
        tk.Button(frametop, text="Fetch",command=self.fetchDepartment).grid(row=2,column=2)
        tk.Label(frametop, text="Department Name:", font=("Helvetica", 10, "bold")).grid(row=3, column=0, padx=5, pady=5)
        self.deptname_text = tk.Text(frametop, height=1, width=20)
        self.deptname_text.grid(row=3, column=1, padx=15, pady=5)
        tk.Button(frametop, text="Find",command=self.findDepartment).grid(row=3,column=2)
        

        # Create a Save button to save changes
        tk.Button(frame, text="Save", width=10, height=2,command=self.save).place(x=50, y=15)
        tk.Button(frame, text="Update", width=10, height=2,command=self.update).place(x=150, y=15)
        tk.Button(frame, text="Delete", width=10, height=2,command=self.delete).place(x=250, y=15)
        tk.Button(frame, text="Clear", width=10, height=2,command=self.clear).place(x=350, y=15)

    def save(self):
        # Retrieve values from the text fields and create a tuple
        test_name = self.test_name_text.get("1.0", "end-1c").strip()
        dept_id = self.deptid_text.get("1.0", "end-1c").strip()
        dept_name = self.deptname_text.get("1.0", "end-1c").strip()
        price = self.price_text.get("1.0", "end-1c").strip()

        # Check if any field is empty
        if not test_name or not dept_id or not dept_name or not price:
            messagebox.showerror("Error", "All fields are required!")
            self.focus_force()
            return
        values = (test_name, price,dept_id)

        try:
            self.db.insertTest(values)
            messagebox.showinfo("Success", "Test information added successfully!")
            self.TestWindow.setTable()
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
                self.db.updateTest(values, identifier)
                messagebox.showinfo("Success", "Test information updated successfully!")
                self.TestWindow.setTable()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update test information: {str(e)}")
            self.destroy()

    def delete(self):
        confirmation = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this Tests's information?")
        if confirmation:
            identifier = self.test_id_text.get("1.0", "end-1c")
            try:
                self.db.deleteTest(identifier)
                messagebox.showinfo("Success", "Test information deleted successfully!")
                self.TestWindow.setTable()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete test information: {str(e)}")
            self.destroy()

    def clear(self):
        self.test_id_text.delete("1.0", "end")
        self.test_name_text.delete("1.0", "end")
        self.price_text.delete("1.0", "end")
        self.deptid_text.delete("1.0", "end")
        self.deptname_text.delete("1.0", "end")


    def fill_fields(self, values):
        # Split the tuple into individual values
        test_id, test_name, test_cost, dept_id, dept_name = values
        # Set each text field with the corresponding value
        self.test_id_text.delete("1.0", tk.END)
        self.test_id_text.insert("1.0", str(test_id))
        self.test_name_text.delete("1.0", tk.END)
        self.test_name_text.insert("1.0", str(test_name))
        self.price_text.delete("1.0", tk.END)
        self.price_text.insert("1.0", str(test_cost))
        self.deptid_text.delete("1.0", tk.END)
        self.deptid_text.insert("1.0", str(dept_id))
        self.deptname_text.delete("1.0", tk.END)
        self.deptname_text.insert("1.0", str(dept_name))

    #Used to set department id and name from find department window
    def setdepartment(self,id,name):
        self.deptid_text.delete("1.0", tk.END)
        self.deptid_text.insert("1.0", str(id))
        self.deptname_text.delete("1.0", tk.END)
        self.deptname_text.insert("1.0", str(name))

    #called when clicked fetch department button
    def fetchDepartment(self):
        dept_id = self.deptid_text.get("1.0", "end-1c")
        dept = self.db.get_department_name(dept_id)
        if dept:
            self.deptname_text.delete("1.0", "end")
            self.deptname_text.insert("1.0", dept[0])
        else:
            messagebox.showinfo("No Department Found", f"No Department found with ID: {dept_id}")
            self.focus_force()

    #Called when clicked find button to open up find department window 
    def findDepartment(self):
        fd.findDepartment(self.db,self)



if __name__ == "__main__":
    app = AddTest()
    app.mainloop()
