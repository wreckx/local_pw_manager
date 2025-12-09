from customtkinter import *
import secrets

class EntryDialog(CTkToplevel):
	
	def __init__(self, parent):
		super().__init__(parent)
		self.geometry("500x250")
		
		lbl_website = CTkLabel(self, text="Website:", font=("Roboto", 14))
		lbl_website.grid(row=0, column=0, padx=(20,10), pady=(20, 10))
		self.txt_website = CTkEntry(self, font=("Roboto", 14), width=250, placeholder_text="Enter website")
		self.txt_website.grid(row=0, column=1, pady=(20, 10), sticky="ew", columnspan=2)
		
		lbl_username = CTkLabel(self, text="Username:", font=("Roboto", 14))
		lbl_username.grid(row=1, column=0, padx=(20,10), pady=(0, 10))
		self.txt_username = CTkEntry(self, font=("Roboto", 14), width=250, placeholder_text="Enter username")
		self.txt_username.grid(row=1, column=1, pady=(0, 10), sticky="ew", columnspan=2)
		
		lbl_email = CTkLabel(self, text="Email:", font=("Roboto", 14))
		lbl_email.grid(row=2, column=0, padx=(20,10), pady=(0, 10))
		self.txt_email = CTkEntry(self, font=("Roboto", 14), width=250, placeholder_text="Enter email address")
		self.txt_email.grid(row=2, column=1, pady=(0, 10), sticky="ew", columnspan=2)
		
		lbl_password = CTkLabel(self, text="Password:", font=("Roboto", 14))
		lbl_password.grid(row=3, column=0, padx=(20,10))
		self.txt_password = CTkEntry(self, font=("Roboto", 14), width=250, placeholder_text="Enter password")
		self.txt_password.grid(row=3, column=1)
		btn_password = CTkButton(self, text="Generate", font=("Roboto", 14), width=125)
		btn_password.configure(command=lambda: self.generate_pwd())
		btn_password.grid(row=3, column=2, padx=(5,0))
		
		self.lbl_error = CTkLabel(self, text="", font=("Roboto", 12), text_color="red")
		self.lbl_error.grid(row=4, column=0, columnspan=3)

		self.btn_submit = CTkButton(self, font=("Roboto", 14), width=250)
		self.btn_submit.grid(row=5, column=1, columnspan=2, pady=(0, 15), sticky="ew")


	def generate_pwd(self, length=12):
		pwd = secrets.token_urlsafe(length)
		self.txt_password.delete(0, 'end')
		self.txt_password.insert(0, pwd)
