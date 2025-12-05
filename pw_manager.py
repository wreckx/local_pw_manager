import sqlite3, hashlib
from tkinter import *

window = Tk()
window.title("Password Manager")

def login_screen():
    window.geometry("400x200")
    
    lbl_login = Label(window, text="Enter Password", font=("Garamond", 14))
    lbl_login.pack(pady=20)
    lbl_login.config(anchor=CENTER)
    
    txt_login = Entry(window, show="*", font=("Garamond", 14), width=25)
    txt_login.pack()
    txt_login.focus()
    
    btn_login = Button(window, text="Submit", width=20, font=("Garamond", 14), command=lambda: verify_password(txt_login.get()))
    btn_login.pack(pady=10)
    
def verify_password(input_password):
    print(input_password)

login_screen()
window.mainloop()