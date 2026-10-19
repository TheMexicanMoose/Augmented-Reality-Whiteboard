import customtkinter
from Helpers.ButtonValue import ButtonValue
from Helpers.Frame import ButtonFrame
from Constants import *


class Whiteboard(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1400x800")
        self._set_appearance_mode("dark")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.title("Whiteboard")

        self.Xpos = 0
        self.Ypos = 0

        self.color = ""

        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame._set_appearance_mode("dark")
        self.main_frame.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")

        self.frame = None

        self.draw_button = customtkinter.CTkButton(self.main_frame, text="draw", command=self.build_color_frame, bg_color="#2B2B2B")
        self.draw_button.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.canvas_frame = customtkinter.CTkFrame(self)
        self.canvas_frame._set_appearance_mode("dark")
        self.canvas_frame.grid(column=1, row=0, padx=10, pady=10, sticky="nsw")

        self.canvas = customtkinter.CTkCanvas(self.canvas_frame, width=800, height=750, bg="white")
        self.canvas.grid(column=1, row=0, padx=200, pady=10)

        self.canvas.bind("<Button-1>", self.last_pos)

        self.canvas.bind("<B1-Motion>", self.handle_draw)

    def build_color_buttons(self):
        buttons = []
        for i,color in enumerate(COLOR_BUTTON_LIST):
            buttons.append(ButtonValue(COLOR_BUTTON_LIST[i],lambda color=color:self.change_color(color),HOVER_COLOR_LIST[i],COLOR_BUTTON_LIST[i]))
        return buttons

    def change_color(self, color):
        self.color = color

    def last_pos(self, event):
        self.Xpos = event.x
        self.Ypos = event.y

    def handle_draw(self, event):
        if not self.frame.get_tag() == "colors":
            return
        self.canvas.create_line(self.Xpos, self.Ypos, event.x, event.y, width=2, fill=self.color)
        self.last_pos(event)

    def handle_rectangle(self, event):
        if not self.frame.get_tag() == "shapes":
            return

    def build_color_frame(self):
        self.frame = ButtonFrame(self,"colors",self.build_color_buttons(),end_command=self.kill_frame,tag="colors")



    def kill_frame(self):
        self.frame = None




if __name__ == "__main__":
    whiteboard = Whiteboard()
    whiteboard.mainloop()
