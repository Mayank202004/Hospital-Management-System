import tkinter as tk
import ttkbootstrap as bs
from ttkbootstrap.constants import *
import tkinter.messagebox as messagebox


class EditMedicines(tk.Tk):
    def __init__(self,db,MedicinesWindow,values=None):
        super().__init__()
        self.db=db
        self.MedicinesWindow=MedicinesWindow #To update table in MedicinesWindow from here
        self.create_widgets()
        if values:
            self.fill_fields(values)

    def create_widgets(self):
        self.title("Edit Medicines Details")
        self.geometry("600x450")
        self.configure(bg="cornflowerblue")

        tk.Label(self, text="Medicine Detail", font=("Helvetica", 25, "bold"), bg="cornflowerblue").place(x=180, y=20)

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
        tk.Label(idframe, text="Medicine ID:", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=16, pady=5)
        self.medicine_id_text = tk.Text(idframe, height=1, width=15)
        self.medicine_id_text.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(nameframe, text="Medicine Name:", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        self.medicine_name_text = tk.Text(nameframe, height=1, width=50)
        self.medicine_name_text.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(nameframe, text="Manufacturer:", font=("Helvetica", 10, "bold")).grid(row=1, column=0, padx=5, pady=5)
        self.manufacturer_text = tk.Text(nameframe, height=1, width=50)
        self.manufacturer_text.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(frametop, text="Price:", font=("Helvetica", 10, "bold")).grid(row=2, column=0, padx=5, pady=5)
        self.price_text = tk.Text(frametop, height=1, width=20)
        self.price_text.grid(row=2, column=1, padx=15, pady=5)
        tk.Label(frametop, text="MRP:", font=("Helvetica", 10, "bold")).grid(row=3, column=0, padx=5, pady=5)
        self.mrp_text = tk.Text(frametop, height=1, width=20)
        self.mrp_text.grid(row=3, column=1, padx=15, pady=5)
        tk.Label(frametop, text="QTY:", font=("Helvetica", 10, "bold")).grid(row=4, column=0, padx=5, pady=5)
        self.qty_text = tk.Text(frametop, height=1, width=20)
        self.qty_text.grid(row=4, column=1, padx=15, pady=5)
        

        # Create a Save button to save changes
        tk.Button(frame, text="Save", width=10, height=2,command=self.save).place(x=50, y=15)
        tk.Button(frame, text="Update", width=10, height=2,command=self.update).place(x=150, y=15)
        tk.Button(frame, text="Delete", width=10, height=2,command=self.delete).place(x=250, y=15)
        tk.Button(frame, text="Clear", width=10, height=2,command=self.clear).place(x=350, y=15)

    def save(self):
    # Retrieve values from the text fields and create a tuple
        values = (
            self.medicine_name_text.get("1.0", "end-1c"),
            self.manufacturer_text.get("1.0", "end-1c"),
            self.price_text.get("1.0", "end-1c"),
            self.mrp_text.get("1.0", "end-1c"),
            self.qty_text.get("1.0", "end-1c"),
         
        )
        try:
            self.db.insertMedicine(values)
            messagebox.showinfo("Success", "Medicine information added successfully!")
            self.MedicinesWindow.setTable()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add medicine information: {str(e)}")
        self.destroy()

    def update(self):
        confirmation = messagebox.askyesno("Confirm Update", "Are you sure you want to update this medicine's information?")
        if confirmation:
            values = (
                self.medicine_name_text.get("1.0", "end-1c"),
            self.manufacturer_text.get("1.0", "end-1c"),
            self.price_text.get("1.0", "end-1c"),
            self.mrp_text.get("1.0", "end-1c"),
            self.qty_text.get("1.0", "end-1c"),
      
            )
            identifier = self.medicine_id_text.get("1.0", "end-1c")
            try:
                self.db.updateMedicine(values, identifier)
                messagebox.showinfo("Success", "Medicine information updated successfully!")
                self.MedicinesWindow.setTable()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update medicine information: {str(e)}")
            self.destroy()

    def delete(self):
        confirmation = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this medicine's information?")
        if confirmation:
            identifier = self.medicine_id_text.get("1.0", "end-1c")
            try:
                self.db.deleteMedicine(identifier)
                messagebox.showinfo("Success", "medicine information deleted successfully!")
                self.MedicinesWindow.setTable()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete medicine information: {str(e)}")
            self.destroy()

    def clear(self):
        self.medicine_id_text.delete("1.0", "end")
        self.medicine_name_text.delete("1.0", "end")
        self.manufacturer_text.delete("1.0", "end")
        self.price_text.delete("1.0", "end")
        self.mrp_text.delete("1.0", "end")
        self.qty_text.delete("1.0", "end")



    def fill_fields(self, values):
        # Split the tuple into individual values
        medicine_id, medicine_name, manufacturer, price, mrp, qty = values
        # Set each text field with the corresponding value
        self.medicine_id_text.delete("1.0", tk.END)
        self.medicine_id_text.insert("1.0", str(medicine_id))
        self.medicine_name_text.delete("1.0", tk.END)
        self.medicine_name_text.insert("1.0", str(medicine_name))
        self.manufacturer_text.delete("1.0", tk.END)
        self.manufacturer_text.insert("1.0", str(manufacturer))
        self.price_text.delete("1.0", tk.END)
        self.price_text.insert("1.0", str(price))
        self.mrp_text.delete("1.0", tk.END)
        self.mrp_text.insert("1.0", str(mrp))
        self.qty_text.delete("1.0", tk.END)
        self.qty_text.insert("1.0", str(qty))



if __name__ == "__main__":
    app = EditMedicines()
    app.mainloop()
