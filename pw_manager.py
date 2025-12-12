import customtkinter
import sys
import mpw_hash
import dbconfig as dbc
from customtkinter import *
from entry_dialog import EntryDialog
from rolodex import Rolodex

"""
Program prompts user to create a master password on first run. This password is hashed and stored in the database.
On subsequent runs, the user is prompted to enter the master password to access the password manager.
Only users who know the master password can view, add, edit, or delete stored password entries.
"""

class PasswordManager(CTk):
    def __init__(self):
        super().__init__()
            
        self.title("Password Manager")
        self.geometry("800x500")
        
        self.window = None
        self.selected_index = None
        self.bind("<Button-1>", lambda event: update_buttons_state())
        
        lbl_title = CTkLabel(self, text="Password Manager", font=("Roboto", 18))
        lbl_title.pack(pady=10)
        lbl_title.configure(anchor=CENTER)
        
        self.fm_search = CTkFrame(self)
        self.fm_search.pack(fill='x', padx=10)
        self.fm_search.columnconfigure(0, weight=1)
        
        self.txt_search = CTkEntry(self.fm_search, font=("Roboto", 14), placeholder_text="Search for website, username, or email...")
        self.txt_search.grid(row=0, column=0, padx=5, pady=(0, 10), columnspan=2, sticky="ew")
        self.txt_search.bind('<Return>', lambda event: search_entries(self.txt_search.get()))
        
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
        fm_lbls.columnconfigure(0, weight=0)
        fm_lbls.columnconfigure((1,2,3,4), weight=1)
        
        fm_lbl_cb = CTkCheckBox(fm_lbls, text="", width = 15)
        fm_lbl_cb.grid(row=0, column=0, padx=5)

        lbl_entries = ["Website", "Username", "Email", "Password"]
        for i in range(len(lbl_entries)):
            lbl = CTkLabel(fm_lbls, text=lbl_entries[i], font=("Roboto", 14), width=50)
            lbl.grid(row=0, column=i+1, padx=5, sticky="ew")
        
        self.fm_entries = Rolodex(self)
        self.fm_entries.pack(fill='both', expand=True, padx=10, pady=10)

        
db, cursor = dbc.dbconfig()

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

root = PasswordManager()

# loads all password entries from the database and displays them in the main window.        
def load_entries(frame: Rolodex):        
    query = "SELECT website, username, email, password FROM passwords;"
    cursor.execute(query)
    res = cursor.fetchall()
    frame.load_entries(res)

# opens a window to set up a new admin password on first run.
def create_pwd_screen():
    root.window = CTkToplevel(root)
    root.window.title("Create Admin Password")
    root.window.geometry ("400x200")
    root.window.grab_set()
    
    txt_create = CTkEntry(root.window, show="*", font=("Roboto", 14), width=250, placeholder_text="Create Admin Password")
    txt_create.pack(pady=(40, 10))
    txt_create.focus()
    
    txt_confirm = CTkEntry(root.window, show="*", font=("Roboto", 14), width=250, placeholder_text="Confirm Admin Password")
    txt_confirm.pack()
    
    lbl_error = CTkLabel(root.window, text="", font=("Roboto", 12), text_color="red")
    lbl_error.pack()
    
    btn_create = CTkButton(root.window, text="Create Password", width=250, font=("Roboto", 14), command=lambda: create_password(txt_create, txt_confirm, lbl_error))
    btn_create.pack(pady=(0, 15))
    
    root.window.protocol("WM_DELETE_WINDOW", sys.exit)

# opens a window to prompt for the master password on startup to verify user credentials. 
def get_pwd_screen():
    root.window = CTkToplevel(root)
    root.window.title("Enter Admin Password")
    root.window.geometry("400x200")
    root.window.grab_set()
    
    txt_login = CTkEntry(root.window, show="*", font=("Roboto", 14), width=250, placeholder_text="Enter Admin Password")
    txt_login.pack(pady=(40, 0))
    txt_login.bind('<Return>', lambda event: get_password(txt_login.get(), lbl_error))
    txt_login.focus()
    
    lbl_error = CTkLabel(root.window, text="", font=("Roboto", 12), text_color="red")
    lbl_error.pack()
    
    btn_login = CTkButton(root.window, text="Submit", width=250, font=("Roboto", 14), command=lambda: get_password(txt_login, lbl_error))
    btn_login.pack()
    
    root.window.protocol("WM_DELETE_WINDOW", sys.exit)

# Creates a master password and stores it in the database (button event).    
def create_password(text1, text2, label):

    if text1.get() == text2.get() and text1.get() != "":
        query = "INSERT INTO master_password (password) VALUES (?);"
        hashed_pwd = mpw_hash.hash_pwd(text1.get())
        cursor.execute(query, (hashed_pwd,))
        db.commit()
        load_entries(root.fm_entries)
        root.window.destroy()
    else:
        label.configure(text="Passwords do not match. Please try again.")
        text1.delete(0, 'end')
        text2.delete(0, 'end')
        text1.focus()

# Verifies the entered password against the stored hash in the database (button event).        
def get_password(text: CTkEntry, label):
    query = "SELECT password FROM master_password WHERE id = 1;"
    cursor.execute(query)
    res = cursor.fetchone()
    hashed_pwd = res[0]
    if (mpw_hash.verify_pwd(text.get(), hashed_pwd)):
        load_entries(root.fm_entries)
        root.window.destroy()
    else:
        label.configure(text="Incorrect Password. Please try again.")
        text.delete(0, 'end')
        text.focus()
        

# Searches for password entries matching the search term and displays them. Returns all entries if search term is empty.
def search_entries(search_term: str, frame: Rolodex = root.fm_entries):
    if search_term != "":
        query = "SELECT website, username, email, password FROM passwords WHERE website LIKE ? OR username LIKE ? OR email LIKE ?;"
        cursor.execute(query, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        res = cursor.fetchall()
            
        if len(res) == 0:
            lbl_nores = CTkLabel(frame, text="No results found.", font=("Roboto", 14))
            lbl_nores.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
            return
        else:
            for widget in frame.winfo_children():
                widget.destroy()
            frame.load_entries(res)        
    else:
        load_entries(frame)
        
# Opens a window to add a new password entry (Add button event).    
def add_entry():
    query = "INSERT INTO passwords (website, username, email, password) VALUES (?, ?, ?, ?);"
    
    window = EntryDialog(root)
    window.grab_set()
    window.title("Add New Entry")
    window.btn_submit.configure(text="Add Entry", command=lambda: save_entry(
        window, query,
        window.txt_website.get().capitalize(),
        window.txt_username.get(),
        window.txt_email.get(),
        window.txt_password.get()
    ))
    
# TODO: FIX UPDATE FUNCTION (INSERTS)
# Opens a window to edit a selected existing password entry (Edit button event).
def edit_entry():
    query_update = "UPDATE passwords SET website = ?, username = ?, email = ?, password = ? WHERE id = ?;"
    idx = root.selected_index + 1
    try:
        window = EntryDialog(root)
        window.title("Edit Entry")
        window.grab_set()
        
        query_fetch = "SELECT website, username, email, password FROM passwords WHERE id=?;"
        cursor.execute(query_fetch, [idx])
        res = cursor.fetchone()
        
        window.txt_website.insert(0, res[0])
        window.txt_username.insert(0, res[1])
        window.txt_email.insert(0, res[2])
        window.txt_password.insert(0, res[3])

        window.btn_submit.configure(text="Update Entry", command=lambda: save_entry(
            window, query_update,
            window.txt_website.get().capitalize(),
            window.txt_username.get(),
            window.txt_email.get(),
            window.txt_password.get(),
            idx
        ))
    except Exception as e:
        exc_type, exc_value, exc_tb = sys.exc_info()
        line_number = exc_tb.tb_lineno
        print(f"ERROR: {type(e).__name__} on line {line_number}: {e}")
        

# TODO FIX DELETE ENTRY FUNCTION
# Opens a window to delete a selected password entry (Delete button event).
def delete_entry():
    window = CTkToplevel(root)
    window.title("Delete Entry")
    window.geometry("400x150")
    window.grab_set()
    
    window.columnconfigure((0, 1), weight = 1)
    
    lbl_confirm = CTkLabel(window, text="Are you sure you want to delete this entry?", font=("Roboto", 14))
    lbl_confirm.grid(column=0, row=0, padx=20, pady=(30, 10), sticky="ew", columnspan=2)
    
    btn_cancel = CTkButton(window, text="Cancel", font=("Roboto", 14), width=200)
    btn_cancel.configure(command=lambda: window.destroy())
    btn_cancel.grid(column=0, row=1, padx=(50, 10), pady=10)
    
    btn_del = CTkButton(window, text="Delete", font=("Roboto", 14), width=200, fg_color="red", hover_color="dark red")
    btn_del.configure(command=lambda: confirm_delete())
    btn_del.grid(column=1, row=1, padx=(10, 50), pady=10)
    
    def confirm_delete():
        query = "DELETE FROM passwords WHERE id = ?;"
        cursor.execute(query, [root.selected_index + 1])
        db.commit()
        window.grab_release
        window.destroy()
        load_entries(root.fm_entries)
    

def save_entry(window, query, website, username, email, password, idx = None):
    if website == "" or password == "":
        window.lbl_error.configure(text="Website and Password fields cannot be empty.")
    elif username == "" and email == "":
        window.lbl_error.configure(text="Either Username or Email must be provided.")
    else:
        if idx is not None:
            cursor.execute(query, (website, username, email, password, idx))
        else:
            cursor.execute(query, (website, username, email, password))
        db.commit()
        window.grab_release
        window.destroy()

# TODO: Fix function to update button states based on selection
def update_buttons_state():
    root.selected_index = root.fm_entries.get_selected_index()
    if root.selected_index is not None:
        root.btn_edit.configure(state="normal")
        root.btn_delete.configure(state="normal")
    else:
        root.btn_edit.configure(state="disabled")
        root.btn_delete.configure(state="disabled")

cursor.execute("SELECT id = 1 FROM master_password;")
if cursor.fetchone():
    get_pwd_screen()
else:
    create_pwd_screen()

root.mainloop()