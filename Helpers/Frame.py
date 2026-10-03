import customtkinter

class ButtonFrame(customtkinter.CTkFrame):
    def __init__(self, master, title, value, end_command,tag):
        super().__init__(master)
        self.title = title
        self.values = value
        self.end_command = end_command
        self.buttons = []
        self._set_appearance_mode("dark")

        self.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsw")

        self.title = customtkinter.CTkLabel(self,text=self.title)
        self.title.grid(row=0, column=0, sticky="ew")

        self.tag= tag



        for i,value in enumerate(self.values):
            button = customtkinter.CTkButton(self,text=value.name,command=value.command,fg_color=value.in_color,hover_color=value.hover_color,bg_color="#2B2B2B")
            button.grid(row=i+1,column=0,padx=10, pady=(10, 0), sticky="ew")
            self.buttons.append(button)

        self.exit_button = customtkinter.CTkButton(self,text="Exit",command=self.on_end,bg_color="#2B2B2B")
        self.exit_button.grid(row=len(self.buttons)+1,column=0,padx=10, pady=(10, 0),sticky="ew")


    def on_end(self):
        self.end_command()
        self.destroy()

    def get_tag(self):
        return self.tag



