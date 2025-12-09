import customtkinter
import mpw_hash
import dbconfig as dbc
from customtkinter import *
from entry_dialog import EntryDialog

"""
Program prompts user to create a master password on first run. This password is hashed and stored in the database.
On subsequent runs, the user is prompted to enter the master password to access the password manager.
Only users who know the master password can view, add, edit, or delete stored password entries.
"""

class PasswordManager(CTk):
    def __init__(self):
        super().__init__()
        
        for widget in self.winfo_children():
            widget.destroy()
            
        self.title("Password Manager")
        self.geometry("700x500")
        
        lbl_title = CTkLabel(self, text="Password Manager", font=("Roboto", 18))
        lbl_title.pack(pady=10)
        lbl_title.configure(anchor=CENTER)
        
        self.fm_search = CTkFrame(self)
        self.fm_search.pack(fill='x', padx=10)
        self.fm_search.columnconfigure(0, weight=1)
        
        self.txt_search = CTkEntry(self.fm_search, font=("Roboto", 14), placeholder_text="Search for website, username, or email...")
        self.txt_search.grid(row=0, column=0, padx=5, pady=(0, 10), columnspan=2, sticky="ew")
        
        self.btn_search = CTkButton(self.fm_search, text="Search", font=("Roboto", 14), width=75)
        self.btn_search.configure(command=lambda: search_entries(self.txt_search.get()))
        self.btn_search.grid(row=0, column=1, padx=2, pady=(0, 10))
        
        self.btn_add = CTkButton(self.fm_search, text="Add", font=("Roboto", 14), width=75)
        self.btn_add.configure(command=lambda: add_entry())
        self.btn_add.grid(row=0, column=2, padx=2, pady=(0, 10))
        
        self.btn_edit = CTkButton(self.fm_search, text="Edit", font=("Roboto", 14), width=75)
        self.btn_edit.configure(state="disabled")
        self.btn_edit.configure(command=lambda: edit_entry())
        self.btn_edit.grid(row=0, column=3, padx=2, pady=(0, 10))
        
        self.btn_delete = CTkButton(self.fm_search, text="Delete", font=("Roboto", 14), width=75, fg_color="red", hover_color="dark red")
        self.btn_delete.configure(state="disabled")
        self.btn_delete.configure(command=lambda: delete_entry())
        self.btn_delete.grid(row=0, column=4, padx=2, pady=(0, 10))
        
        fm_lbls = CTkFrame(self)
        fm_lbls.pack(fill='x', padx=10)
        fm_lbls.columnconfigure((0,1,2,3), weight=1)

        lbl_entries = ["Website", "Username", "Email", "Password"]
        for i in range(len(lbl_entries)):
            lbl = CTkLabel(fm_lbls, text=lbl_entries[i], font=("Roboto", 14))
            lbl.grid(row=0, column=i, padx=5, sticky="ew")
        
        self.fm_entries = CTkScrollableFrame(self)
        self.fm_entries.pack()
        self.fm_entries.pack(fill='both', expand=True, padx=10, pady=10)
        self.fm_entries.columnconfigure((0,1,2,3), weight=1)
        
db, cursor = dbc.dbconfig()

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

root = PasswordManager()

# loads all password entries from the database and displays them in the main window.        
def load_entries(frame: CTkFrame):
    query = "SELECT website, username, email, password FROM passwords;"
    cursor.execute(query)
    res = cursor.fetchall()
    for i in range(len(res)):
        for j in range(len(res[i])):
            lbl = CTkLabel(frame, text=res[i][j], font=("Roboto", 14))
            lbl.grid(row=i, column=j, padx=5, pady=5, sticky="ew")

# opens a window to set up a new admin password on first run.
def create_pwd_screen():
    window = CTkToplevel(root)
    window.title("Create Admin Password")
    window.geometry ("400x200")
    window.grab_set()
    
    txt_create = CTkEntry(window, show="*", font=("Roboto", 14), width=250, placeholder_text="Create Admin Password")
    txt_create.pack(pady=(40, 10))
    txt_create.focus()
    
    txt_confirm = CTkEntry(window, show="*", font=("Roboto", 14), width=250, placeholder_text="Confirm Admin Password")
    txt_confirm.pack()
    
    lbl_error = CTkLabel(window, text="", font=("Roboto", 12), text_color="red")
    lbl_error.pack()
    
    btn_create = CTkButton(window, text="Create Password", width=250, font=("Roboto", 14), command=lambda: [create_password(txt_create, txt_confirm, lbl_error), window.destroy()])
    btn_create.pack(pady=(0, 15))

# opens a window to prompt for the master password on startup to verify user credentials. 
def get_pwd_screen():
    window = CTkToplevel(root)
    window.title("Enter Admin Password")
    window.geometry("400x200")
    window.grab_set()
    
    txt_login = CTkEntry(window, show="*", font=("Roboto", 14), width=250, placeholder_text="Enter Admin Password")
    txt_login.pack(pady=(40, 0))
    txt_login.focus()
    
    lbl_error = CTkLabel(window, text="", font=("Roboto", 12), text_color="red")
    lbl_error.pack()
    
    btn_login = CTkButton(window, text="Submit", width=250, font=("Roboto", 14), command=lambda: [get_password(txt_login.get(), lbl_error), window.destroy()])
    btn_login.pack()

# Creates a master password and stores it in the database (button event).    
def create_password(text1, text2, label):

    if text1.get() == text2.get() and text1.get() != "":
        query = "INSERT INTO master_password (password) VALUES (?);"
        hashed_pwd = mpw_hash.hash_pwd(text1.get())
        cursor.execute(query, (hashed_pwd,))
        db.commit()
    else:
        label.configure(text="Passwords do not match. Please try again.")
        text1.delete(0, 'end')
        text2.delete(0, 'end')
        text1.focus()

# Verifies the entered password against the stored hash in the database (button event).        
def get_password(password: str, label):
    query = "SELECT password FROM master_password WHERE id = 1;"
    cursor.execute(query)
    res = cursor.fetchone()
    hashed_pwd = res[0]
    if (mpw_hash.verify_pwd(password, hashed_pwd)):
        load_entries(root.fm_entries)
    else:
        label.configure(text="Incorrect Password. Please try again.")

# Searches for password entries matching the search term and displays them. Returns all entries if search term is empty.
def search_entries(search_term: str, frame: CTkFrame = root.fm_entries):
    for widget in frame.winfo_children():
        widget.destroy()
    
    if search_term != "":
        query = "SELECT website, username, email, password FROM passwords WHERE website LIKE ? OR username LIKE ? OR email LIKE ?;"
        cursor.execute(query, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        res = cursor.fetchall()
            
        if len(res) == 0:
            lbl_nores = CTkLabel(frame, text="No results found.", font=("Roboto", 14))
            lbl_nores.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
            return
        else:        
            for i in range(len(res)):
                for j in range(len(res[i])):
                    lbl = CTkLabel(frame, text=res[i][j], font=("Roboto", 14))
                    lbl.grid(row=i, column=j, padx=5, pady=5, sticky="ew")
    else:
        load_entries(frame)
        
# Opens a window to add a new password entry (Add button event).    
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
            load_entries(root.fm_entries)

# Opens a window to edit a selected existing password entry (Edit button event).
def edit_entry():
    window = EntryDialog(root)
    window.grab_set()

# Opens a window to delete a selected password entry (Delete button event).
def delete_entry():
    pass

# password_manager()

cursor.execute("SELECT * FROM master_password;")
if cursor.fetchall():
    get_pwd_screen()
else:
    create_pwd_screen()
    

root.mainloop()