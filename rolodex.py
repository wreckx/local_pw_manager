import customtkinter as ctk

class Rolodex(ctk.CTkScrollableFrame):
    
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.columnconfigure(0, minsize=15)
        self.columnconfigure((1,2,3,4), weight=1)
        
        self.color_hover = "#106A43"
        self.color_selected = "#2FA572"
        self.color_unselected = "transparent"

        self.selected_row_index: int = None
        self.selected_button: ctk.CTkButton = None
        
        self.buttons: list[list[ctk.CTkButton]] = []
        self.checkboxes: list[ctk.CTkCheckBox] = []
    
    # used to load all entries from a list of lists to the rolodex.
    # clears all previous entries before loading new ones. each widget is added 
    # to its own respective list for easier reference later on.        
    def load_entries(self, entries):
        self.reset_rolodex_state()

        for i in range(len(entries)):
            cb = ctk.CTkCheckBox(self, text="", width = 15)
            cb.configure(command=lambda r = i: self.select_row(r))
            cb.grid(row=i, column=0, pady=5)
            
            self.checkboxes.append(cb)
            self.buttons.append([])
            
            for j in range(len(entries[i])):
                btn = ctk.CTkButton(self, text=entries[i][j], font=("Roboto", 14), width=2000, 
                                    corner_radius=0, fg_color=self.color_unselected)
                btn.grid(row=i, column=j+1, pady=5, sticky="w")
                btn.configure(command=lambda r=i, c=j: self.click_event(r, c))
                btn.bind("<Enter>", lambda e, r=i: self.hover_leave_event(r, self.color_hover))
                btn.bind("<Leave>", lambda e, r=i: self.hover_leave_event(r, self.color_unselected))
                self.buttons[i].append(btn)
    
    # changes the color of the entire row for any button hovered or left    
    def hover_leave_event(self, row, color):       
        for button in self.buttons[row]:
            if self.checkboxes[row].get() == 1:
                break
            button.configure(fg_color=color)
                
    # action event for buttons. treats buttons as extensions of the checkbox events.
    # executes the action event for checkbox if any button in the same row is triggered.      
    def click_event(self, row, column):
        self.selected_button = self.buttons[row][column]
        self.checkboxes[row].toggle()
        
        for button in self.buttons[row]:
            button.configure(hover_color = self.color_selected)
    
    # action event for  checkbox. highlights all buttons on the same row as the selected checkbox
    # and sets the selected index to the index of the selected entry. deselects other checkboxes  
    # such that only one entry is selected for any given time.        
    def select_row(self, row):
        if self.checkboxes[row].get() == 1:
            self.selected_row_index = row
            for button in self.buttons[row]:
                button.configure(fg_color=self.color_selected)
        else:
            self.selected_row_index = None
                
        for i, cb in enumerate(self.checkboxes):
            if i == row:
                continue
            cb.deselect()
            for button in self.buttons[i]:
                button.configure(fg_color=self.color_unselected)

    # returns the values of the selected entry in the rolodex and returns it as a list.
    def get_selected_entry(self) -> list:
        entry_list = []
        if self.selected_row_index == None:
            return None

        for button in self.buttons[self.selected_row_index]:
            text = button.cget("text")
            entry_list.append(text)

        return entry_list
    
    # resets the rolodex to its initial state by clearing all widgets and resetting
    # all relevant attributes.
    def reset_rolodex_state(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.selected_row_index: int = None
        self.selected_button: ctk.CTkButton = None
        self.buttons: list[list[ctk.CTkButton]] = []
        self.checkboxes: list[ctk.CTkCheckBox] = []