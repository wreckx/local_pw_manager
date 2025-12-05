import sqlite3, hashlib
from tkinter import *

window = Tk()
window.title("Password Manager")

# opens a login window on startup to verify user credentials. 
def login_screen():
    window.geometry("400x200")
    
    lbl_login = Label(window, text="Enter Password", font=("Garamond", 14))
    lbl_login.pack(pady=20)
    lbl_login.config(anchor=CENTER)
    
    txt_login = Entry(window, show="*", font=("Garamond", 14), width=25)
    txt_login.pack()
    txt_login.focus()
    
    lbl_error = Label(window, text="", font=("Garamond", 12), fg="red")
    lbl_error.pack()
    
    btn_login = Button(window, text="Submit", width=20, font=("Garamond", 14), command=lambda: verify_password(txt_login.get(), lbl_error))
    btn_login.pack(pady=30)

# Verifies the entered password for admin credentials against the stored password.    
def verify_password(input, label):
    password = "test123"

    if input == password:
        print("Access Granted")
    else:
        label.config(text="Incorrect Password", fg="red")
        
def password_manager():
    pass

login_screen()
window.mainloop()