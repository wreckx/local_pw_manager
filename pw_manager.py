import customtkinter
import sys
import mpw_hash
import dbconfig as dbc
from customtkinter import *
from entry_dialog import EntryDialog
from rolodex import Rolodex
from symmetric_encryption import SymmetricEncryption
from pathlib import Path

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
        
        
        self.window: CTkToplevel = None
        self.selected_index = None
        self.selected_button = None
        self.bind_all("<Button-1>", lambda event: self.update_buttons_state())
        
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
        
        self.cryptographer = SymmetricEncryption()
        file = Path("password_key.key")
        
        if file.exists():
            self.cryptographer.load_key(file)
        else:
            self.cryptographer.create_key(file)
        
    def update_buttons_state(self):
        self.selected_index = self.fm_entries.get_selected_entry()
        self.selected_button = self.fm_entries.selected_button
        if self.selected_index is not None:
            # if "<Hidden>" in self.selected_index:
            #     self.selected_index.remove("<Hidden>")
            self.btn_edit.configure(state="normal")
            self.btn_delete.configure(state="normal")
        else:
            self.btn_edit.configure(state="disabled")
            self.btn_delete.configure(state="disabled")
        
        if self.selected_button is not None:
            for button in root.fm_entries.buttons:
                button[3].configure(text="<Hidden>")
            if self.selected_button.grid_info()['column'] == 4:
                show_password()

        
db, cursor = dbc.dbconfig()

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

root = PasswordManager()

# loads all password entries from the database and displays them in the main window.
# appends a <Hidden> field for each record in the database to mask the password display.
def load_entries(frame: Rolodex):        
    query = "SELECT website, username, email FROM passwords;"
    cursor.execute(query)
    res = cursor.fetchall()
    
    res_mod = [list(row) for row in res]
    for row in res_mod:
        row.append("<Hidden>")
    
    frame.load_entries(res_mod)
    
def show_password():
    
    if root.selected_index is None or root.selected_button is None:
        return
    try:
        query = "SELECT password FROM passwords WHERE website = ? AND username = ? AND email = ?;"
        params = (root.selected_index[0], root.selected_index[1], root.selected_index[2])
        cursor.execute(query, params)
        res = cursor.fetchone()
        print(res[0])
        if res is not None and root.selected_button.grid_info()['column'] == 4:
            decrypted_pwd = root.cryptographer.decrypt_passwd(res[0].decode())
            root.selected_button.configure(text=decrypted_pwd)
        else:
            root.selected_button.configure(text="<Hidden>")
    except Exception as e:
        exc_type, exc_value, exc_tb = sys.exc_info()
        line_number = exc_tb.tb_lineno
        print(f"ERROR: {type(e).__name__} on line {line_number}: {e}")
    
# opens a window to set up a new admin password on first run.
def create_pwd_screen():
    root.window = CTkToplevel(root)
    root.window.resizable(False, False)
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
    root.window.resizable(False, False)
    root.window.title("Enter Admin Password")
    root.window.geometry("400x150")
    root.window.grab_set()
    
    txt_login = CTkEntry(root.window, show="*", font=("Roboto", 14), width=250, placeholder_text="Enter Admin Password")
    txt_login.grid(row=0, column=0, columnspan=2, pady=(30, 0), padx=75)
    txt_login.bind('<Return>', lambda event: get_password(txt_login, lbl_error))
    txt_login.focus()
    
    lbl_error = CTkLabel(root.window, text="", font=("Roboto", 12), text_color="red")
    lbl_error.grid(row=1, column=0, columnspan=2, pady=5)
    
    btn_cancel = CTkButton(root.window, text="Cancel", font=("Roboto", 14), width=120, fg_color="red", hover_color="dark red")
    btn_cancel.configure(command=lambda: root.destroy()) # TODO: change action to detect calling method
    btn_cancel.grid(column=0, row=2, padx=(75, 5))
    
    btn_submit = CTkButton(root.window, text="Submit", font=("Roboto", 14), width=120)
    btn_submit.configure(command=lambda: get_password(txt_login, lbl_error))
    btn_submit.grid(column=1, row=2, padx=(5, 75))
    
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
            
        frame.load_entries(res)
        
        if len(res) == 0:
            lbl_nores = CTkLabel(frame, text="No results found.", font=("Roboto", 14))
            lbl_nores.grid(row=0, column=0, columnspan=5, padx=5, pady=5, sticky="ew")
    else:
        load_entries(frame)
    root.update_buttons_state()
        
# Opens a window to add a new password entry (Add button event).    
def add_entry():
    query = "INSERT INTO passwords (website, username, email, password) VALUES (?, ?, ?, ?);"
    
    window = EntryDialog(root)
    window.grab_set()
    window.title("Add New Entry")
    window.btn_submit.configure(text="Add Entry", command=lambda: save_entry(
        window, query,
        window.txt_website.get().lower(),
        window.txt_username.get(),
        window.txt_email.get(),
        window.txt_password.get()
    ))
    
# Opens a window to edit a selected existing password entry (Edit button event).
def edit_entry():
    query_update = "UPDATE passwords SET website = ?, username = ?, email = ?, password = ? WHERE id = ?;"
    try:
        window = EntryDialog(root)
        window.title("Edit Entry")
        window.grab_set()
        
        query_fetch = "SELECT id FROM passwords WHERE website = ? AND username = ? AND email = ?;"
        params = (root.selected_index[0], root.selected_index[1], root.selected_index[2])
        cursor.execute(query_fetch, params)
        res = cursor.fetchone()
        if res is None:
            raise ValueError("No Entry Found")
        
        query_fetch_pwd = "SELECT password FROM passwords WHERE id = ?;"
        cursor.execute(query_fetch_pwd, [res[0]])
        res_pwd = cursor.fetchone()
        
        window.txt_website.insert(0, root.selected_index[0])
        window.txt_username.insert(0, root.selected_index[1])
        window.txt_email.insert(0, root.selected_index[2])
        window.txt_password.insert(0, root.cryptographer.decrypt_passwd(res_pwd[0].decode()))

        window.btn_submit.configure(text="Update Entry", command=lambda: save_entry(
            window, query_update,
            window.txt_website.get().lower(),
            window.txt_username.get(),
            window.txt_email.get(),
            window.txt_password.get(),
            res[0]
        ))
    except Exception as e:
        exc_type, exc_value, exc_tb = sys.exc_info()
        line_number = exc_tb.tb_lineno
        print(f"ERROR: {type(e).__name__} on line {line_number}: {e}")
        
# Opens a window to delete a selected password entry (Delete button event).
def delete_entry():
    window = CTkToplevel(root)
    window.title("Delete Entry")
    window.geometry("400x150")
    window.grab_set()
    
    window.columnconfigure((0, 1), weight = 1)
    
    query_fetch = "SELECT id FROM passwords WHERE website = ? AND username = ? AND email = ?;"
    params = (root.selected_index[0], root.selected_index[1], root.selected_index[2])
    cursor.execute(query_fetch, params)
    res = cursor.fetchone()
    if res is None:
        raise ValueError("No entry found")
    
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
        cursor.execute(query, [res[0]])
        db.commit()
        window.grab_release()
        window.destroy()
        load_entries(root.fm_entries)
        root.update_buttons_state()
    
# Function that gets called for both add and edit buttons in entry dialog windows.
# Checks if website and password are not none, and ensures at least username or password is not none.
# Adds a new entry if idx = None and updates a query otherwise. reloads entries and closes window.
def save_entry(window, query, website, username, email, password, idx = None):
    if website == "" or password == "":
        window.lbl_error.configure(text="Website and Password fields cannot be empty.")
    elif username == "" and email == "":
        window.lbl_error.configure(text="Either Username or Email must be provided.")
    else:
        pwd = root.cryptographer.encrypt_passwd(password)
        if idx is not None:
            cursor.execute(query, (website, username, email, pwd, idx))
        else:
            cursor.execute(query, (website, username, email, pwd))
        db.commit()
        window.grab_release
        window.destroy()
        load_entries(root.fm_entries)
    root.update_buttons_state()



cursor.execute("SELECT id = 1 FROM master_password;")
if cursor.fetchone():
    get_pwd_screen()
else:
    create_pwd_screen()

root.mainloop()