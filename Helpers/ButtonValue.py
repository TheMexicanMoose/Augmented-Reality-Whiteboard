import customtkinter

class ButtonValue:
    def __init__(self, name, command, in_color="", hover_color=""):
        self._name = name
        self._command = command
        self._hover_color = hover_color
        self._in_color = in_color

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, value):
        self._command = value

    @property
    def in_color(self):
        return self._in_color

    @in_color.setter
    def in_color(self, value):
        self._in_color = value

    @property
    def hover_color(self):
        return self._hover_color

    @hover_color.setter
    def hover_color(self, value):
        self._hover_color = value
