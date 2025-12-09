import customtkinter
import mpw_hash
import dbconfig as dbc
import secrets
from customtkinter import *
from entry_dialog import EntryDialog

db, cursor = dbc.dbconfig()

customtkinter.set_appearance_mode("dark")
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
    txt_search.grid(row=0, column=0, padx=5, pady=(0, 10), columnspan=2, sticky="ew")
    
    btn_search = CTkButton(fm_search, text="Search", font=("Roboto", 14), width=75)
    btn_search.configure(command=lambda: search_entries(txt_search.get()))
    btn_search.grid(row=0, column=1, padx=2, pady=(0, 10))
    
    btn_add = CTkButton(fm_search, text="Add", font=("Roboto", 14), width=75)
    btn_add.configure(command=lambda: add_entry())
    btn_add.grid(row=0, column=2, padx=2, pady=(0, 10))
    
    btn_edit = CTkButton(fm_search, text="Edit", font=("Roboto", 14), width=75)
    btn_edit.configure(state="disabled")
    btn_edit.configure(command=lambda: edit_entry())
    btn_edit.grid(row=0, column=3, padx=2, pady=(0, 10))
    
    btn_delete = CTkButton(fm_search, text="Delete", font=("Roboto", 14), width=75, fg_color="red", hover_color="dark red")
    btn_delete.configure(state="disabled")
    btn_delete.configure(command=lambda: delete_entry())
    btn_delete.grid(row=0, column=4, padx=2, pady=(0, 10))
    
    fm_lbls = CTkFrame(root)
    fm_lbls.pack(fill='x', padx=10)
    fm_lbls.columnconfigure((0,1,2,3), weight=1)

    lbl_entries = ["Website", "Username", "Email", "Password"]
    for i in range(len(lbl_entries)):
        lbl = CTkLabel(fm_lbls, text=lbl_entries[i], font=("Roboto", 14))
        lbl.grid(row=0, column=i, padx=5, sticky="ew")
        
    load_entries()
    
def load_entries():
    fm_entries = CTkScrollableFrame(root)
    fm_entries.pack()
    fm_entries.pack(fill='both', padx=10)
    fm_entries.columnconfigure((0,1,2,3), weight=1)
    
    query = "SELECT website, username, email, password FROM passwords;"
    cursor.execute(query)
    res = cursor.fetchall()
    for i in range(len(res)):
        for j in range(len(res[i])):
            lbl = CTkLabel(fm_entries, text=res[i][j], font=("Roboto", 14))
            lbl.grid(row=i, column=j, padx=5, pady=5, sticky="ew")

def search_entries(search_term: str):
    if search_term != "":
        pass
    pass
    
def add_entry():
    window = EntryDialog(root)
    window.grab_set()
    window.title("Add New Entry")
    window.btn_submit.configure(text="Save Entry", command=lambda: save_entry(
        window.txt_website.get(),
        window.txt_username.get(),
        window.txt_email.get(),
        window.txt_password.get()
    ))
        
    def save_entry(website, username, email, password):
        if website == "" or password == "":
            window.lbl_error.configure(text="Website and Password fields cannot be empty.")
        elif username == "" and email == "":
            window.lbl_error.configure(text="Either Username or Email must be provided.")
        else:
            query = "INSERT INTO passwords (website, username, email, password) VALUES (?, ?, ?, ?);"
            cursor.execute(query, (website, username, email, password))
            db.commit()
            window.grab_release
            window.destroy()
            load_entries()


def edit_entry():
    pass

def delete_entry():
    pass

# password_manager()
# add_entry()

cursor.execute("SELECT * FROM master_password;")
if cursor.fetchall():
    get_pwd_screen()
else:
    create_pwd_screen()

root.mainloop()