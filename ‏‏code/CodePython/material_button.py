import tkinter as tk

class MaterialButton(tk.Button):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            font=("Helvetica", 12, "bold"),
            bg="#6200EE", fg="white", relief="flat",
            bd=0, padx=15, pady=8, highlightthickness=0,
            activebackground="#3700B3", activeforeground="white",
            width=20
        )
        self.default_bg = "#6200EE"
        self.default_fg = "white"
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        """"
        This function changes the background color of the button when the mouse cursor hovers over it.
        param event: The event object that contains information about the mouse entering the widget.
        :type event: tkinter.Event
        :return: None
        :time complexity: O(1) (constant time, as it involves a single configuration change)
        """
        self.configure(bg="#3700B3")

    def on_leave(self, event):
        """
        This function restores the default background color of the button when the mouse cursor leaves it.
        :param event: The event object that contains information about the mouse leaving the widget.
        :type event: tkinter.Event
        :return: None
        :time complexity: O(1) (constant time, as it involves a single configuration change)
        """
        self.configure(bg=self.default_bg)
