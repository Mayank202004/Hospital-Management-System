import tkinter as tk
from tkinter import *
from tkinter import ttk
from database import Database
from PIL import Image,ImageTk
import ttkbootstrap as bs
from windows.DoctorWindow import DoctorsWindow
from windows.PatientsWindow import PatientsWindow
from windows.AppointmentsWindow import AppointmentsWindow
from windows.WardsWindow import WardsWindow
from windows.BedsWindow import BedsWindow
from windows.MedicinesWindow import MedicineWindow
from windows.DepartmentWindow import DepartmentWindow
from windows.LabTestsWindow import LabTestsWindow
from windows.LabResultsWindow import LabResultsWindow
from windows.PrescriptionWindow import PrescriptionsWindow
#import windows.docDetails

from windows.login_window import LoginWindow

class HospitalManagementApp:
    def __init__(self, root):
        self.root = root
        self.db = Database("hospital.db")
        self.root.withdraw() #Bug fixed (Where extra Tk window used to show at login)
        self.show_login()

    def show_login(self):
        login_window = tk.Toplevel(self.root)
        login_app = LoginWindow(login_window, self,self.db)
        self.root.wait_window(login_window)

    def start_dashboard(self):
        self.root.deiconify()
        self.root.title("Hospital Management System")
        self.root.attributes("-fullscreen", True)
        self.create_dashboard()

    def create_dashboard(self):
   
        style.configure('Custom.TFrame', background='#5B62F4', relief='flat')
        #navigatorframe
        nav_frame=bs.Frame(self.root,style='Custom.TFrame')
        nav_frame.place(x=0,y=0,width=250,height=900)
        #logo
        img_logo=bs.Image.open(r"asset\logo.png")
        img_logo=img_logo.resize((50,50),Image.Resampling.LANCZOS)
        self.photo_logo=ImageTk.PhotoImage(img_logo)
        self.logo=Label(nav_frame,image=self.photo_logo)
        self.logo.config(background='#5B62F4', foreground='#FFFFFF')
        self.logo.place(x=10,y=10,height=50,width=50)
        style.configure("Custom.TLabel", background="#5B62F4",font=('bauhaus 93', 28,"bold"), foreground='black')
        style.configure('Custom.TLabel2', background='cornflower blue', font=('Helvetica', 90, 'bold'), foreground='black')
        text_label = bs.Label(nav_frame, text="Hospital",style='Custom.TLabel')
        text_label.place(x=70, y=12)

        #============== buttons ===================
        #buttonframe
        self.btn_frame=bs.Frame(nav_frame,style='Custom.TFrame')
        self.btn_frame.place(x=0,y=80,width=240,height=680)
        style.configure('Custom.TButton', background='#5B62F4', foreground='white', font=('Ariel', 12,"bold"), relief="flat")
        button1 = bs.Button(self.btn_frame, text="Home",style="Custom.TButton",command=lambda: self.navigate("Home"))
        button1.pack(side="top", padx=10, pady=5, fill="x")
        button2 = bs.Button(self.btn_frame, text="Doctors",style="Custom.TButton",command=lambda: self.navigate("Doctors"))
        button2.pack(side="top", padx=10, pady=5, fill="x")
        button3 = bs.Button(self.btn_frame, text="Patients",style="Custom.TButton",command=lambda: self.navigate("Patients"))
        button3.pack(side="top", padx=10, pady=5, fill="x")
        button4 = bs.Button(self.btn_frame, text="Appointments",style="Custom.TButton",command=lambda: self.navigate("Appointments"))
        button4.pack(side="top", padx=10, pady=5, fill="x")
        button5 = bs.Button(self.btn_frame, text="Departments",style="Custom.TButton",command=lambda: self.navigate("Departments"))
        button5.pack(side="top", padx=10, pady=5, fill="x")
        button6 = bs.Button(self.btn_frame, text="Wards",style="Custom.TButton",command=lambda: self.navigate("Wards"))
        button6.pack(side="top", padx=10, pady=5, fill="x")
        button7 = bs.Button(self.btn_frame, text="Beds",style="Custom.TButton",command=lambda: self.navigate("Beds"))
        button7.pack(side="top", padx=10, pady=5, fill="x")
        button8 = bs.Button(self.btn_frame, text="Medicines",style="Custom.TButton",command=lambda: self.navigate("Medicines"))
        button8.pack(side="top", padx=10, pady=5, fill="x")
        button9 = bs.Button(self.btn_frame, text="Prescriptions",style="Custom.TButton",command=lambda: self.navigate("Prescriptions"))
        button9.pack(side="top", padx=10, pady=5, fill="x")
        button10 = bs.Button(self.btn_frame, text="Lab Tests",style="Custom.TButton",command=lambda: self.navigate("LabTests"))
        button10.pack(side="top", padx=10, pady=5, fill="x")
        button11 = bs.Button(self.btn_frame, text="Lab Results",style="Custom.TButton",command=lambda: self.navigate("LabResults"))
        button11.pack(side="top", padx=10, pady=5, fill="x")
        #homeframe
        self.img_frame=Frame(self.root,bd=5,relief="flat")
        self.img_frame.place(x=250,y=0,width=1280,height=860)

        #Home_Image
        homeimg=Image.open(r"asset\home.jpg")
        homeimg=homeimg.resize((1280,860),Image.Resampling.LANCZOS)
        self.photo_homeimg=ImageTk.PhotoImage(homeimg)
        self.homeimg=Label(self.img_frame,image=self.photo_homeimg)
        self.homeimg.place(x=0,y=0,width=1280,height=860)
        closebutton=bs.Button(self.img_frame,text="X",style='danger',command=self.close)
        closebutton.place(x=1240,y=5)

    #used to close program
    def close(self):
        #close db connection and close 
        self.db.close_connection()
        self.root.destroy()

    def navigate(self, destination):
        # code to navigate based on the clicked button
        if destination == "Home":
            self.show_home()
        elif destination == "Patients":
            self.show_patients()
        elif destination == "Doctors":
            self.show_doctors()
        elif destination == "Appointments":
            self.show_Appointments()
        elif destination == "Departments":
            self.show_Departments()
        elif destination == "Wards":
            self.show_Wards()
        elif destination == "Beds":  
            self.show_Beds()
        elif destination == "Medicines":  
            self.show_Medicines()
        elif destination == "LabTests":  
            self.show_LabTests()
        elif destination == "LabResults":  
            self.show_LabResults()
        elif destination == "Prescriptions":  
            self.show_Prescriptions()
     

    def show_home(self):
        # Remove any existing content from the main frame
        for widget in self.img_frame.winfo_children():
            widget.destroy()
        #Home_Image
        homeimg=Image.open(r"asset\home.jpg")
        homeimg=homeimg.resize((1280,860),Image.Resampling.LANCZOS)
        self.photo_homeimg=ImageTk.PhotoImage(homeimg)
        self.homeimg=Label(self.img_frame,image=self.photo_homeimg,bg='white')
        self.homeimg.place(x=0,y=0,width=1280,height=860)
        closebutton=bs.Button(self.img_frame,text="X",style='danger',command=self.close)
        closebutton.place(x=1240,y=5)
        

    def show_doctors(self):
        for widget in self.img_frame.winfo_children():
            widget.destroy()
        DoctorsWindow(self.img_frame,self.db)

    def show_patients(self):
        for widget in self.img_frame.winfo_children():
            widget.destroy()
        PatientsWindow(self.img_frame,self.db)

    def show_Appointments(self):
        for widget in self.img_frame.winfo_children():
            widget.destroy()
        AppointmentsWindow(self.img_frame,self.db)

    def show_Departments(self):
        for widget in self.img_frame.winfo_children():
            widget.destroy()
        DepartmentWindow(self.img_frame,self.db)
        

    def show_Wards(self):
        for widget in self.img_frame.winfo_children():
            widget.destroy()
        WardsWindow(self.img_frame,self.db)

    def show_Beds(self):
        for widget in self.img_frame.winfo_children():
            widget.destroy()
        BedsWindow(self.img_frame,self.db)
    
    def show_Medicines(self):
        for widget in self.img_frame.winfo_children():
            widget.destroy()
        MedicineWindow(self.img_frame,self.db)
    
    def show_LabTests(self):
        for widget in self.img_frame.winfo_children():
            widget.destroy()
        LabTestsWindow(self.img_frame,self.db)

    def show_LabResults(self):
        for widget in self.img_frame.winfo_children():
            widget.destroy()
        LabResultsWindow(self.img_frame,self.db)

    def show_Prescriptions(self):
        for widget in self.img_frame.winfo_children():
            widget.destroy()
        PrescriptionsWindow(self.img_frame,self.db)

if __name__ == "__main__":
    root = tk.Tk()
    # style = bs.Style("cosmo")
    style = bs.Style("morph")
    app = HospitalManagementApp(root)
    root.mainloop()
