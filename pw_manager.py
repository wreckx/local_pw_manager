import sqlite3, hashlib
import mpw_hash
from tkinter import *

window = Tk()
window.title("Password Manager")

# creates a window to set up a new admin password on first run.
def create_pwd_screen():
    window.geometry ("400x200")
    
    lbl_create = Label(window, text="Create Admin Password", font=("Garamond", 14))
    lbl_create.pack()
    lbl_create.config(anchor=CENTER)
    
    txt_create = Entry(window, show="*", font=("Garamond", 14), width=25)
    txt_create.pack()
    txt_create.focus()
    
    lbl_confirm = Label(window, text="Confirm Password", font=("Garamond", 14))
    lbl_confirm.pack()
    
    txt_confirm = Entry(window, show="*", font=("Garamond", 14), width=25)
    txt_confirm.pack()
    
    lbl_error = Label(window, text="", font=("Garamond", 12), fg="red")
    lbl_error.pack()
    
    btn_create = Button(window, text="Create Password", width=20, font=("Garamond", 14), command=lambda: create_password(txt_create, txt_confirm, lbl_error))
    btn_create.pack(pady=15)

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
    
    btn_login = Button(window, text="Submit", width=20, font=("Garamond", 14), command=lambda: mpw_hash.verify_pwd(txt_login.get()))
    btn_login.bind("<Enter>", mpw_hash.verify_pwd(txt_login.get()))
    btn_login.pack(pady=30)

# Verifies the entered password for admin credentials against the stored password.    
def create_password(text1, text2, label):

    if text1.get() == text2.get():
        print(mpw_hash.hash_pwd(text1.get())) # For testing purposes only. Remove in production. Import hashed password into the database.
    else:
        label.config(text="Passwords do not match. Please try again.")
        text1.delete(0, 'end')
        text2.delete(0, 'end')
        text1.focus()
        
def password_manager():
    window.geometry("600x400")
    lbl_title = Label(window, text="Personal Password Manager", font=("Garamond", 18))
    lbl_title.pack(pady=10)
    lbl_title.config(anchor=CENTER)
    
    txt_search = Entry(window, font=("Garamond", 14), width=30, show="Enter username/website/email to search")
    txt_search.pack(side="left")
    
    btn_search = Button(window, text="Search", width=15, font=("Garamond", 14))
    btn_search.pack(side="right")

#password_manager()
create_pwd_screen()
window.mainloop()