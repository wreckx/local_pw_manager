import customtkinter
import mpw_hash
import dbconfig as dbc
from customtkinter import *

db, cursor = dbc.dbconfig()

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

root = CTk()
root.title("Password Manager")

# creates a window to set up a new admin password on first run.
def create_pwd_screen():
    root.geometry ("400x200")
    
    txt_create = CTkEntry(root, show="*", font=("Roboto", 14), width=250, placeholder_text="Create Admin Password")
    txt_create.pack(pady=(40, 10))
    txt_create.focus()
    
    txt_confirm = CTkEntry(root, show="*", font=("Roboto", 14), width=250, placeholder_text="Confirm Admin Password")
    txt_confirm.pack()
    
    lbl_error = CTkLabel(root, text="", font=("Roboto", 12), text_color="red")
    lbl_error.pack()
    
    btn_create = CTkButton(root, text="Create Password", width=250, font=("Roboto", 14), command=lambda: create_password(txt_create, txt_confirm, lbl_error))
    btn_create.pack(pady=(0, 15))

# opens a login window on startup to verify user credentials. 
def get_pwd_screen():
    root.geometry("400x200")
    
    txt_login = CTkEntry(root, show="*", font=("Roboto", 14), width=250, placeholder_text="Enter Admin Password")
    txt_login.pack(pady=(40, 0))
    txt_login.focus()
    
    lbl_error = CTkLabel(root, text="", font=("Roboto", 12), text_color="red")
    lbl_error.pack()
    
    btn_login = CTkButton(root, text="Submit", width=250, font=("Roboto", 14), command=lambda: get_password(txt_login.get(), lbl_error))
    btn_login.pack()

# Creates a master password and stores it in the database.    
def create_password(text1, text2, label):

    if text1.get() == text2.get() and text1.get() != "":
        query = "INSERT INTO master_password (password) VALUES (?);"
        hashed_pwd = mpw_hash.hash_pwd(text1.get())
        cursor.execute(query, (hashed_pwd,))
        db.commit()
        password_manager()
    else:
        label.configure(text="Passwords do not match. Please try again.")
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
        label.configure(text="Incorrect Password. Please try again.")
    
def password_manager():
    for widget in root.winfo_children():
        widget.destroy()
    
    root.geometry("700x500")
    lbl_title = CTkLabel(root, text="Password Manager", font=("Roboto", 18))
    lbl_title.pack(pady=10)
    lbl_title.configure(anchor=CENTER)
    
    fm_search = CTkFrame(root)
    fm_search.pack(fill='x', padx=10)
    fm_search.columnconfigure(0, weight=1)
    
    txt_search = CTkEntry(fm_search, font=("Roboto", 14), placeholder_text="Search for website, username, or email...")
    txt_search.grid(row=0, column=0, padx=5, pady=10, columnspan=3, sticky='ew')
    
    btn_search = CTkButton(fm_search, text="Search", font=("Roboto", 14))
    btn_search.grid(row=0, column=3, padx=5, pady=10, sticky='w')
    
    fm_entries = CTkFrame(root)
    fm_entries.pack(fill='x', padx=10)
    fm_entries.columnconfigure((0,1,2,3), weight=1)
    
    lbl_site = CTkLabel(fm_entries, text="Website", font=("Roboto", 14))
    lbl_site.grid(row=0, column=0, pady=5, sticky='ew')
    
    lbl_username = CTkLabel(fm_entries, text="Username", font=("Roboto", 14))
    lbl_username.grid(row=0, column=1, pady=5, sticky='ew')
    
    lbl_email = CTkLabel(fm_entries, text="Email", font=("Roboto", 14))
    lbl_email.grid(row=0, column=2, pady=5, sticky='ew')
    
    lbl_password = CTkLabel(fm_entries, text="Password", font=("Roboto", 14))
    lbl_password.grid(row=0, column=3, pady=5, sticky='ew')

#password_manager()
#create_pwd_screen()
cursor.execute("SELECT * FROM master_password;")
if cursor.fetchall():
    get_pwd_screen()
else:
    create_pwd_screen()

root.mainloop()