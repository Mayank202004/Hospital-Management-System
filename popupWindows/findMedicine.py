import tkinter as tk
from tkinter import *
from tkinter import ttk
from ttkbootstrap import Style
import ttkbootstrap as bs


class findMedicines(tk.Tk):
    def __init__(self,db,prescription_window):
        super().__init__()
        self.db = db
        self.create_widgets()
        self.prescription_window = prescription_window

    def create_widgets(self):
        self.title("Find Medicine")
        self.geometry("600x500")
        self.configure(bg="cornflowerblue")

        tk.Label(self, text="Find Medicine", font=("Helvetica", 15, "bold")).place(x=220, y=10)

        #frames setup
        frametop = tk.Frame(self,bg='green')  
        frametop.place(x=20, y=45,width=550,height=50)
        tableframe = tk.Frame(self,bg='black')  
        tableframe.place(x=20, y=100,width=550,height=380)

        #searchby logic
        tk.Label(frametop, text="Searchby:", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        self.searchbycbox=bs.Combobox(frametop,values=['Medicine Name','Manufacturer'])
        self.searchbycbox.set('Medicine Name') # set default as Name
        self.searchbycbox.configure(state="readonly") #To not allow typing in combobox
        self.searchbycbox.grid(row=0,column=1)
        self.searchby_text = tk.Text(frametop, height=1, width=25)
        self.searchby_text.grid(row=0, column=2, padx=20, pady=5)
        self.searchby_text.bind("<KeyRelease>", lambda event: self.fetch_details()) #keyrelease bind to call function 

        #table layout
        # Table creation
        s = ttk.Scrollbar(tableframe, orient=HORIZONTAL)
        s2 = ttk.Scrollbar(tableframe, orient=VERTICAL)
        self.table = ttk.Treeview(tableframe, column=('MedicineID','Name','Manufacturer','Price','MRP'), xscrollcommand=s.set, yscrollcommand=s2.set)

        # Scroll bar setup
        s.pack(side=BOTTOM, fill=X)
        s2.pack(side=RIGHT, fill=Y)
        s.config(command=self.table.xview)
        s2.config(command=self.table.yview)

        style = Style()
        style.configure("Treeview.Heading", background="#5B62F4", foreground="white", font=("Arial", 10, "bold"))

        self.table.heading('MedicineID', text='Medicine ID')
        self.table.heading('Name', text='Medicine Name')
        self.table.heading('Manufacturer', text='Manufacturer')
        self.table.heading('Price', text='Price')
        self.table.heading('MRP', text='MRP')

        self.table.column('MedicineID', width=20)
        self.table.column('Name', width=134)
        self.table.column('Manufacturer', width=133)
        self.table.column('Price', width=133)
        self.table.column('MRP', width=133)
        self.table['show'] = 'headings'
        self.table.pack(fill=BOTH, expand=True)
        self.table.bind("<Double-Button-1>", self.on_select)

    def fetch_details(self):
        self.table.delete(*self.table.get_children()) #clear existing data
        searchby=self.searchbycbox.get()
        if(searchby=="Medicine ID"):
            searchby="MedicineID"
        elif(searchby=='Medicine Name'):
            searchby='MedicineName'
        value = self.searchby_text.get("1.0", "end-1c")
        data = self.db.search_Medicines(searchby,value)
        for medicines in data:
            self.table.insert('', 'end', values=medicines)

    #To return found patient to manageAppointment
    def on_select(self, event=None):
        selection = self.table.selection()
        if selection:
            id = self.table.item(selection[0], 'values')[0]
            name = self.table.item(selection[0], 'values')[1]
            price = self.table.item(selection[0], 'values')[3]
            self.prescription_window.setMedicine(id, name,price)
            self.after(100, self.destroy)

        

        

        


if __name__ == "__main__":
    #stye=bs.Style()
    app = findMedicines()
    app.mainloop()
