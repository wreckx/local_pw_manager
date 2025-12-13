import customtkinter as ctk
from customtkinter import ThemeManager

class Rolodex(ctk.CTkScrollableFrame):
    
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.columnconfigure(0, minsize=15)
        self.columnconfigure((1,2,3,4), weight=1)
        
        self.color_hover = "#106A43"
        self.color_selected = "#2FA572"
        self.color_unselected = "transparent"

        self.selected_index = None
    
    # used to load all entries from a list of lists to the rolodex.        
    def load_entries(self, entries):
        for widget in self.winfo_children():
            widget.destroy()
        self.selected_index = None

        for i in range(len(entries)):
            cb = ctk.CTkCheckBox(self, text="", width = 15)
            cb.configure(command=lambda r = i: self.select_row(r))
            cb.grid(row=i, column=0, pady=5)
            for j in range(len(entries[i])):
                btn = ctk.CTkButton(self, text=entries[i][j], font=("Roboto", 14), width=2000, 
                                    corner_radius=0, fg_color=self.color_unselected)
                btn.configure(command=lambda r=i: self.click_event(r))
                btn.grid(row=i, column=j+1, pady=5, sticky="w")
                btn.bind("<Enter>", lambda e, r=i: self.hover_leave_event(r, self.color_hover))
                btn.bind("<Leave>", lambda e, r=i: self.hover_leave_event(r, self.color_unselected))
    
    # changes the color of the entire row for any button hovered or left    
    def hover_leave_event(self, row, color):
        for widget in self.winfo_children():
            if widget.grid_info()['row'] == row:
                if isinstance(widget, ctk.CTkCheckBox):
                    if widget.get() == 1:
                        break
                else:
                    widget.configure(fg_color=color)
    
    # action event for buttons. treats buttons as extensions of the checkbox events.
    # executes the action event for checkbox if any button in the same row is triggered.      
    def click_event(self, row):
        for widget in self.winfo_children():
            if widget.grid_info()['row'] == row:
                if isinstance(widget, ctk.CTkCheckBox):
                    widget.toggle()
                else:
                    widget.configure(hover_color = self.color_selected)
    
    # action event for  checkbox. highlights all buttons on the same row as the selected checkbox
    # and sets the selected index to the index of the selected entry. deselects other checkboxes  
    # such that only one entry is selected for any given time.        
    def select_row(self, row):
        for widget in self.winfo_children():
            if widget.grid_info()['row'] == row:
                if isinstance(widget, ctk.CTkButton):
                    widget.configure(fg_color=self.color_selected)
                else:
                    if widget.get() == 1:
                        self.selected_index = row
                    else:
                        self.selected_index = None
            else:
                if isinstance(widget, ctk.CTkButton):
                    widget.configure(fg_color=self.color_unselected)
                if isinstance(widget, ctk.CTkCheckBox):
                    widget.deselect()

    # returns the values of the selected entry in the rolodex and returns it as a list.
    def get_selected_entry(self) -> list:
        entry_list = []
        for widget in self.winfo_children():
            if widget.grid_info()['row'] == self.selected_index:
                if isinstance(widget, ctk.CTkButton):
                    text = widget.cget("text")
                    entry_list.append(text)
        return entry_list
