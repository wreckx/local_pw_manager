import sqlite3, hashlib
import mpw_hash
import dbconfig as dbc
from tkinter import *

db, cursor = dbc.dbconfig()

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
def get_pwd_screen():
    window.geometry("400x200")
    
    lbl_login = Label(window, text="Enter Password", font=("Garamond", 14))
    lbl_login.pack(pady=20)
    lbl_login.config(anchor=CENTER)
    
    txt_login = Entry(window, show="*", font=("Garamond", 14), width=25)
    txt_login.pack()
    txt_login.focus()
    
    lbl_error = Label(window, text="", font=("Garamond", 12), fg="red")
    lbl_error.pack()
    
    btn_login = Button(window, text="Submit", width=20, font=("Garamond", 14), command=lambda: get_password(txt_login.get(), lbl_error))
    btn_login.pack(pady=30)

# Creates a master password and stores it in the database.    
def create_password(text1, text2, label):

    if text1.get() == text2.get() and text1.get() != "":
        query = "INSERT INTO master_password (password) VALUES (?);"
        hashed_pwd = mpw_hash.hash_pwd(text1.get())
        cursor.execute(query, (hashed_pwd,))
        db.commit()
        password_manager()
    else:
        label.config(text="Passwords do not match. Please try again.")
        text1.delete(0, 'end')
        text2.delete(0, 'end')
        text1.focus()

# Verifies the entered password against the stored hash in the database.        
def get_password(password: str, label):
    query = "SELECT password FROM master_password WHERE id = 1;"
    cursor.execute(query)
    res = cursor.fetchone()
    hashed_pwd = res[0]
    if (mpw_hash.verify_pwd(password, hashed_pwd)):
        password_manager()
    else:
        label.config(text="Incorrect Password. Please try again.")
    
def password_manager():
    for widget in window.winfo_children():
        widget.destroy()
    
    window.geometry("700x500")
    lbl_title = Label(window, text="Personal Password Manager", font=("Garamond", 18))
    lbl_title.pack(pady=10)
    lbl_title.config(anchor=CENTER)
    
    fm_search = Frame(window)
    fm_search.pack(fill='x', padx=10)
    fm_search.columnconfigure(0, weight=1)
    
    txt_search = Entry(fm_search, font=("Garamond", 14))
    txt_search.grid(row=0, column=0, pady=5, columnspan=3, sticky='ew')
    
    btn_search = Button(fm_search, text="Search", font=("Garamond", 14))
    btn_search.grid(row=0, column=3, padx=10, pady=5, sticky='w')
    
    fm_entries = Frame(window, borderwidth=1, relief="solid")
    fm_entries.pack(fill='x', padx=10)
    fm_entries.columnconfigure((0,1,2,3), weight=1)
    
    lbl_site = Label(fm_entries, text="Website", font=("Garamond", 14))
    lbl_site.grid(row=0, column=0, pady=5, sticky='ew')
    
    lbl_username = Label(fm_entries, text="Username", font=("Garamond", 14))
    lbl_username.grid(row=0, column=1, pady=5, sticky='ew')
    
    lbl_email = Label(fm_entries, text="Email", font=("Garamond", 14))
    lbl_email.grid(row=0, column=2, pady=5, sticky='ew')
    
    lbl_password = Label(fm_entries, text="Password", font=("Garamond", 14))
    lbl_password.grid(row=0, column=3, pady=5, sticky='ew')

#password_manager()
#create_pwd_screen()
cursor.execute("SELECT * FROM master_password;")
if cursor.fetchall():
    get_pwd_screen()
else:
    create_pwd_screen()

window.mainloop()