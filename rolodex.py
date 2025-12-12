import customtkinter as ctk

class Rolodex(ctk.CTkScrollableFrame):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.columnconfigure(0, minsize=15)
        self.columnconfigure((1,2,3,4), weight=1)
        
        self.color_selected = "green"
        self.color_unselected = "transparent"
        self.color_hover = "dark green"
        
        self.selected_index = None
            
    def load_entries(self, entries):
        for i in range(len(entries)):
            cb = ctk.CTkCheckBox(self, text="", width = 15, fg_color=self.color_selected)
            cb.configure(command=lambda r = i: self.select_row(r))
            cb.grid(row=i, column=0, pady=5)
            for j in range(len(entries[i])):
                btn = ctk.CTkButton(self, text=entries[i][j], font=("Roboto", 14), width=2000, 
                                    corner_radius=0, fg_color=self.color_unselected)
                btn.configure(command=lambda r=i: self.click_event(r))
                btn.grid(row=i, column=j+1, pady=5, sticky="w")
                btn.bind("<Enter>", lambda e, r=i: self.hover_leave_event(r, self.color_hover))
                btn.bind("<Leave>", lambda e, r=i: self.hover_leave_event(r, self.color_unselected))
        
    def hover_leave_event(self, row, color):
        for widget in self.winfo_children():
            if widget.grid_info()['row'] == row:
                if isinstance(widget, ctk.CTkCheckBox):
                    if widget.get() == 1:
                        break
                else:
                    widget.configure(fg_color=color)
          
    def click_event(self, row):
        for widget in self.winfo_children():
            if widget.grid_info()['row'] == row:
                if isinstance(widget, ctk.CTkCheckBox):
                    widget.toggle()
                    if widget.get() == 1:
                        self.selected_index = row
                        print(f"Selected index: {self.selected_index}")
                    else:
                        self.selected_index = None
                        print(f"Selected index: {self.selected_index}")
            else:
                if isinstance(widget, ctk.CTkButton):
                    widget.configure(fg_color=self.color_unselected)
                if isinstance(widget, ctk.CTkCheckBox):
                    widget.deselect()
            
    def select_row(self, row):
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                if widget.grid_info()['row'] == row:
                    widget.configure(fg_color=self.color_selected)


    def get_selected_index(self):
        return self.selected_index
        
        

# entries = [["Facebook", "rjlv", "sample@gmail.com", "password123"],
#            ["Instagram", "rex", "xxx@gmail.com", "mypassword"],
#            ["Twitter", "wreckx", "puma@gmail.com", "letmein"]]


# root = ctk.CTk()
# root.geometry("600x400")
# rolodex = Rolodex(root)
# rolodex.pack(fill='both', expand=True)

# rolodex.load_entries(entries)

# root.mainloop()