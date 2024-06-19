import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as bs
from PIL import Image,ImageTk

class LoginWindow:
    def __init__(self, root, app, db):
        self.root = root
        self.app = app
        self.db = db
        self.root.title("Login")
        self.root.geometry("500x300")
        homeimg=Image.open(r"asset\login.png")
        homeimg=homeimg.resize((300,300),Image.Resampling.LANCZOS)
        self.photo_homeimg=ImageTk.PhotoImage(homeimg)
        self.homeimg=tk.Label(root,image=self.photo_homeimg)
        self.homeimg.place(x=0,y=0,width=300,height=300)
        self.username_label = tk.Label(root, text="Username")
        self.username_label.place(x=330,y=40)
        self.username_entry = tk.Entry(root)
        self.username_entry.place(x=330,y=70)
        
        self.password_label = tk.Label(root, text="Password")
        self.password_label.place(x=330,y=110)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.place(x=330,y=140)
        
        self.login_button = tk.Button(root, text="Login", command=self.check_login)
        self.login_button.place(x=330,y=170)
        self.root.deiconify()

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username=="" or password=="":
            messagebox.showerror("Error", "All fields are required")
            return
        if self.db.verify_user(username, password)==True:
        #if username=='admin' and password=='123':
            self.root.destroy()
            self.app.start_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials")
            return
