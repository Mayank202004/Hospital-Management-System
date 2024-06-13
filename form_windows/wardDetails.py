import tkinter as tk
import ttkbootstrap as bs
from ttkbootstrap.constants import *
import tkinter.messagebox as messagebox
import popupWindows.findDepartment as fd


class AddWard(tk.Tk):
    def __init__(self,db,parentWindow,values=None):
        super().__init__()
        self.db=db
        self.parentWindow=parentWindow #To update table in TestsWindow from here
        self.create_widgets()
        if values:
            self.fill_fields(values)

    def create_widgets(self):
        self.title("Add Ward Details")
        self.geometry("600x400")
        self.configure(bg="cornflowerblue")

        tk.Label(self, text="Ward Details", font=("Helvetica", 25, "bold"), bg="cornflowerblue").place(x=200, y=20)

        mainframe = tk.Frame(self)  
        mainframe.place(x=30, y=80,width=550,height=300)  
        idframe = tk.Frame(mainframe)  
        idframe.place(x=10, y=15,width=835,height=45)
        nameframe = tk.Frame(mainframe)  
        nameframe.place(x=10, y=55,width=835,height=120)
        #frametop = tk.Frame(mainframe)  
        #frametop.place(x=40, y=145,width=835,height=145)  
        frame = tk.Frame(mainframe,bg='black')  
        frame.place(x=45, y=200,width=435,height=60) 

        # Create labels and entry fields for doctor details inside the frame
        tk.Label(idframe, text="Ward ID:", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=16, pady=5)
        self.ward_id_text = tk.Text(idframe, height=1, width=15)
        self.ward_id_text.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(nameframe, text="Ward Name:", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        self.ward_name_text = tk.Text(nameframe, height=1, width=50)
        self.ward_name_text.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(nameframe, text="Ward Type:", font=("Helvetica", 10, "bold")).grid(row=1, column=0, padx=5, pady=5)
        self.ward_type_text = tk.Text(nameframe, height=1, width=50)
        self.ward_type_text.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(nameframe, text="Capacity:", font=("Helvetica", 10, "bold")).grid(row=2, column=0, padx=5, pady=5)
        self.capacity_text = tk.Text(nameframe, height=1, width=50)
        self.capacity_text.grid(row=2, column=1, padx=15, pady=5)


        # Create a Save button to save changes
        tk.Button(frame, text="Save", width=10, height=2,command=self.save).place(x=50, y=15)
        tk.Button(frame, text="Update", width=10, height=2,command=self.update).place(x=150, y=15)
        tk.Button(frame, text="Delete", width=10, height=2,command=self.delete).place(x=250, y=15)
        tk.Button(frame, text="Clear", width=10, height=2,command=self.clear).place(x=350, y=15)

    def save(self):
        # Retrieve values from the text fields and create a tuple
        ward_name = self.ward_name_text.get("1.0", "end-1c").strip()
        ward_type = self.ward_type_text.get("1.0", "end-1c").strip()
        capacity = self.capacity_text.get("1.0", "end-1c").strip()

        # Check if any field is empty
        if not ward_name or not ward_type or not capacity:
            messagebox.showerror("Error", "All fields are required!")
            self.focus_force()
            return
        values = (ward_name, ward_type,capacity)
        try:
            self.db.insertWard(values)
            messagebox.showinfo("Success", "Ward information added successfully!")
            self.parentWindow.setTable()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add ward information: {str(e)}")
        self.destroy()

    def update(self):
        confirmation = messagebox.askyesno("Confirm Update", "Are you sure you want to update this ward's information?")
        if confirmation:
            ward_id=self.ward_id_text.get("1.0", "end-1c").strip()
            ward_name = self.ward_name_text.get("1.0", "end-1c").strip()
            ward_type = self.ward_type_text.get("1.0", "end-1c").strip()
            capacity = self.capacity_text.get("1.0", "end-1c").strip()

            if not ward_name or not ward_type or not capacity or not ward_id:
                messagebox.showerror("Error", "All fields are required!")
                self.focus_force()
                return
        
            values = (
                ward_name,
                ward_type,
                capacity
            )
            try:
                self.db.updateWard(values, ward_id)
                messagebox.showinfo("Success", "Ward information updated successfully!")
                self.parentWindow.setTable()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update ward information: {str(e)}")
            self.destroy()

    def delete(self):
        confirmation = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this Ward's information?")
        if confirmation:
            identifier = self.ward_id_text.get("1.0", "end-1c")
            try:
                self.db.deleteWard(identifier)
                messagebox.showinfo("Success", "ward information deleted successfully!")
                self.parentWindow.setTable()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete ward information: {str(e)}")
            self.destroy()

    def clear(self):
        self.ward_id_text.delete("1.0", "end")
        self.ward_name_text.delete("1.0", "end")
        self.ward_type_text.delete("1.0", "end")
        self.capacity_text.delete("1.0", "end")

    def fill_fields(self, values):
        # Split the tuple into individual values
        ward_id, ward_name, ward_type, capacity = values
        # Set each text field with the corresponding value
        self.ward_id_text.delete("1.0", tk.END)
        self.ward_id_text.insert("1.0", str(ward_id))
        self.ward_name_text.delete("1.0", tk.END)
        self.ward_name_text.insert("1.0", str(ward_name))
        self.ward_type_text.delete("1.0", tk.END)
        self.ward_type_text.insert("1.0", str(ward_type))
        self.capacity_text.delete("1.0", tk.END)
        self.capacity_text.insert("1.0", str(capacity))



if __name__ == "__main__":
    app = AddWard()
    app.mainloop()
