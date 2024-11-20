import tkinter as tk
from tkinter import colorchooser, simpledialog
from material_button import MaterialButton
import threading

# Constants for UI elements
TITLE_TEXT = "LED Controller"
TITLE_FONT = ("Helvetica", 16, "bold")
BUTTON_FONT = ("Helvetica", 12)
BACKGROUND_COLOR = "#6200EE"
TEXT_COLOR = "white"
BUTTON_PADDING = 10
BUTTON_SPACING = 20
ARROW_BUTTON_SPACING = 20

# Constants for pages
PAGE_1 = 0
PAGE_2 = 1

# Constants for commands
COMMAND_RAINBOW = '1'
COMMAND_PULSE = 'pulse:'
COMMAND_COLOR_WIPE = '3'
COMMAND_RANDOM_SPARKLE = '4'
COMMAND_COLOR_CHASE = 'chase:'
COMMAND_STOP = 'stop'

# Constants for pulse parameters
PULSE_MIN_SPEED = 1
PULSE_DEFAULT_SPEED = 1
PULSE_MIN_INTERVAL = 0
PULSE_DEFAULT_INTERVAL = 1000
#FOTO_PATH = "Foto\\Foto\\fotoApp.ico"
# Constants for dialog titles
DIALOG_TITLE_COLOR_PICKER = "Choose a color"
DIALOG_TITLE_PULSE_SPEED = "Speed"
DIALOG_TITLE_PULSE_INTERVAL = "Interval"
DIALOG_TITLE_CHASE_COLOR = "Choose a color"
DIALOG_TITLE_STOP_EFFECT = "Stop Effect"

# Constants for button texts
BUTTON_TEXT_RAINBOW = "🌈 Rainbow"
BUTTON_TEXT_PULSE = "🔄 Pulse"
BUTTON_TEXT_COLOR_WIPE = "🖌 Color Wipe"
BUTTON_TEXT_RANDOM_SPARKLE = "✨ Random Sparkle"
BUTTON_TEXT_COLOR_CHASE = "🏃 Color Chase"
BUTTON_TEXT_CHOOSE_COLOR = "🎨 Choose Color"
BUTTON_TEXT_STOP = "⛔ Stop"

class LEDController:
    def __init__(self, master, serial_manager):
        """
        Initializes the LED controller, sets up the UI, and starts the read thread for serial communication.
        :param master: The root window or parent widget for the UI.
        :type master: tk.Tk
        :param serial_manager: The serial communication manager for sending and receiving commands.
        :type serial_manager: SerialManager
        :return: None
        Time: O(1)
        """
        self.master = master
        self.master.title(TITLE_TEXT)
        self.ser_manager = serial_manager
        self.page_number = PAGE_1
        self.pulse_running = False
        self.pulse_interval = PULSE_DEFAULT_INTERVAL
        self.pulse_delay = 0

        # Initialize UI components
        self.label = self.create_title_label()
        self.arrow_frame = self.create_arrow_frame()
        self.buttons_frame = self.create_buttons_frame()

        # Initialize buttons and threading
        self.create_buttons()
        self.start_read_thread()

    def create_title_label(self):
        """
        Creates the title label for the main window.
        :return: A Label widget with the title text.
        :rtype: tk.Label
        Time: O(1)
        """
        return tk.Label(self.master, text=TITLE_TEXT, font=TITLE_FONT, fg=BACKGROUND_COLOR)

    def create_arrow_frame(self):
        """
        Creates a frame for navigation buttons (previous and next).
        :return: The frame containing the arrow buttons.
        :rtype: tk.Frame
        Time: O(1)
        """
        arrow_frame = tk.Frame(self.master)
        arrow_frame.pack(pady=ARROW_BUTTON_SPACING)
        self.create_arrow_buttons(arrow_frame)
        return arrow_frame

    def create_arrow_buttons(self, arrow_frame):
        """
        Creates the previous and next arrow buttons inside the provided frame.
        :param arrow_frame: The frame where the buttons will be placed.
        :type arrow_frame: tk.Frame
        :return: None
        Time: O(1)
        """
        self.prev_button = self.create_arrow_button(arrow_frame, "<", self.previous_page, column=0)
        self.next_button = self.create_arrow_button(arrow_frame, ">", self.next_page, column=1)

    def create_arrow_button(self, parent_frame, text, command, column):
        """
        Creates a button with arrow text and attaches a command to navigate pages.
        :param parent_frame: The frame to place the button in.
        :type parent_frame: tk.Frame
        :param text: The text to display on the button (arrow).
        :type text: str
        :param command: The command to execute when the button is clicked.
        :type command: callable
        :return: The created button.
        :rtype: tk.Button
        Time: O(1)
        """
        button = tk.Button(
            parent_frame, text=text, command=command,
            font=BUTTON_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR,
            relief="flat", padx=BUTTON_PADDING, pady=BUTTON_PADDING
        )
        button.grid(row=0, column=column, padx=ARROW_BUTTON_SPACING)

        return button
    def create_buttons_frame(self):
        """
        Creates the frame where all action buttons are placed.
        :return: The frame for action buttons.
        :rtype: tk.Frame
        Time: O(1)
        """
        buttons_frame = tk.Frame(self.master)
        buttons_frame.pack()
        return buttons_frame

    def create_buttons(self):
        """
        Creates buttons for both pages (page 1 and page 2).
        :return: None
        Time: O(1)
        """
        self.buttons_page_1 = self.create_page_1_buttons()
        self.buttons_page_2 = self.create_page_2_buttons()
        self.show_page(self.page_number)

    def create_page_1_buttons(self):
        """
        Creates buttons for the first page of the LED controller.
        :return: List of buttons with their text and command.
        :rtype: list of tuples (str, callable)
        Time: O(1)
        """
        return [
            (BUTTON_TEXT_RAINBOW, self.send_rainbow_command),
            (BUTTON_TEXT_PULSE, self.open_pulse_dialog),
            (BUTTON_TEXT_COLOR_WIPE, self.send_color_wipe_command),
            (BUTTON_TEXT_RANDOM_SPARKLE, self.send_random_sparkle_command)
        ]

    def create_page_2_buttons(self):
        """
        Creates buttons for the second page of the LED controller.
        :return: List of buttons with their text and command.
        :rtype: list of tuples (str, callable)
        Time: O(1)
        """
        return [
            (BUTTON_TEXT_COLOR_CHASE, self.open_chase_dialog),
            (BUTTON_TEXT_CHOOSE_COLOR, self.open_color_picker),
            (BUTTON_TEXT_STOP, self.stop_effect)
        ]

    def show_page(self, page_number):
        """
        Displays the buttons corresponding to the current page number.
        :param page_number: The page number to display (either PAGE_1 or PAGE_2).
        :type page_number: int
        :return: None
        Time: O(1)
        """
        self.clear_existing_buttons()
        self.display_buttons_for_page(page_number)

    def clear_existing_buttons(self):
        """
        Clears all existing buttons from the current page.
        :return: None
        Time: O(m), where m is the number of buttons on the page.
        """
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

    def display_buttons_for_page(self, page_number):
        """
        Displays the buttons for the selected page.
        :param page_number: The page number to display (either PAGE_1 or PAGE_2).
        :type page_number: int
        :return: None
        Time: O(n), where n is the number of buttons on the page.
        """
        buttons = self.buttons_page_1 if page_number == PAGE_1 else self.buttons_page_2
        for button in buttons:
            self.create_button(button[0], button[1])

    def create_button(self, text, command):
        """
        Creates a button with the given text and command, and adds it to the UI.
        :param text: The text to display on the button.
        :type text: str
        :param command: The command to execute when the button is clicked.
        :type command: callable
        :return: None
        Time: O(1)
        """
        if callable(command):
            btn = MaterialButton(self.buttons_frame, text=text, command=command)
        else:
            btn = MaterialButton(self.buttons_frame, text=text, command=lambda c=command: self.send_command(c))
        btn.pack(pady=BUTTON_SPACING)

    def previous_page(self):
        """
        Navigates to the previous page, if possible.
        :return: None
        Time: O(1)
        """
        if self.page_number > PAGE_1:
            self.page_number -= 1
            self.show_page(self.page_number)

    def next_page(self):
        """
        Navigates to the next page, if possible.
        :return: None
        Time: O(1)
        """
        if self.page_number < PAGE_2:
            self.page_number += 1
            self.show_page(self.page_number)

    def send_command(self, command):
        """
        Sends a command to the serial manager after stopping any pulse effect.
        :param command: The command to send to the serial manager.
        :type command: str
        :return: None
        Time: O(1)
        """
        self.stop_pulse()
        if command.startswith(COMMAND_PULSE):
            self.start_pulse(command)
        else:
            self.ser_manager.send_command(command)

    def start_pulse(self, command):
        """
        Starts the pulse effect if it is not already running.
        :param command: The pulse command to start.
        :type command: str
        :return: None
        Time: O(1)
        """
        if not self.pulse_running:
            self.pulse_running = True
            self.send_pulse_command(command)
    def send_pulse_command(self, command):
        """
        Sends the pulse command to the serial manager repeatedly.
        :param command: The pulse command to send.
        :type command: str
        :return: None
        Time: O(1)
        """
        if self.pulse_running:
            self.ser_manager.send_command(command)
            self.master.after(self.pulse_interval + self.pulse_delay, lambda: self.send_pulse_command(command))

    def stop_pulse(self):
        """
        Stops the pulse effect.
        :return: None
        Time: O(1)
        """
        self.pulse_running = False

    def open_color_picker(self):
        """
        Opens a color picker dialog to choose a color and send it to the LED controller.
        :return: None
        Time: O(1)
        """
        color = colorchooser.askcolor(title=DIALOG_TITLE_COLOR_PICKER)[1]
        if color:
            rgb = self.hex_to_rgb(color)
            self.send_color_command(rgb)

    def open_pulse_dialog(self):
        """
        Opens a dialog to set pulse parameters (color, speed, and interval).
        :return: None
        Time: O(1)
        """
        color = colorchooser.askcolor(title=DIALOG_TITLE_COLOR_PICKER)[1]
        if color:
            rgb = self.hex_to_rgb(color)
            speed = self.ask_for_pulse_speed()
            if speed:
                self.pulse_interval = speed * 1000
                interval = self.ask_for_pulse_interval()
                if interval is not None:
                    self.pulse_delay = interval
                    command = f'{COMMAND_PULSE}{rgb[0]},{rgb[1]},{rgb[2]},{speed}'
                    self.start_pulse(command)

    def ask_for_pulse_speed(self):
        """
        Opens a dialog to ask the user for the pulse speed in seconds.
        :return: The pulse speed entered by the user (in seconds), or None if canceled.
        :rtype: int or None
        Time: O(1)
        """
        return simpledialog.askinteger(DIALOG_TITLE_PULSE_SPEED, "Enter pulse speed (seconds):", minvalue=PULSE_MIN_SPEED, initialvalue=PULSE_DEFAULT_SPEED)

    def ask_for_pulse_interval(self):
        """
        Opens a dialog to ask the user for the pulse interval in milliseconds.
        :return: The pulse interval entered by the user (in milliseconds), or None if canceled.
        :rtype: int or None
        Time: O(1)
        """
        return simpledialog.askinteger(DIALOG_TITLE_PULSE_INTERVAL, "Enter interval between pulses (milliseconds):", minvalue=PULSE_MIN_INTERVAL, initialvalue=PULSE_DEFAULT_INTERVAL)

    def hex_to_rgb(self, hex_color):
        """
        Converts a hexadecimal color string to an RGB tuple.
        :param hex_color: The hexadecimal color string to convert (e.g., '#FF5733').
        :type hex_color: str
        :return: A tuple of integers representing the RGB values.
        :rtype: tuple[int, int, int]
        Time: O(1)
        """
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    def start_read_thread(self):
        """
        Starts a background thread to handle serial communication and read data from the serial port.
        :return: None
        Time: O(1)
        """
        threading.Thread(target=self.ser_manager.read_from_serial, daemon=True).start()

    def open_chase_dialog(self):
        """
        Opens a color picker dialog to choose a color for the color chase effect.
        :return: None
        Time: O(1)
        """
        color = colorchooser.askcolor(title=DIALOG_TITLE_CHASE_COLOR)[1]
        if color:
            rgb = self.hex_to_rgb(color)
            command = f'{COMMAND_COLOR_CHASE}{rgb[0]},{rgb[1]},{rgb[2]}'
            self.send_command(command)

    def stop_effect(self):
        """
        Stops any ongoing effect (rainbow, pulse, color wipe, etc.).
        :return: None
        Time: O(1)
        """
        self.send_command(COMMAND_STOP)

    def send_rainbow_command(self):
        """
        Sends the rainbow effect command to the serial manager.
        :return: None
        Time: O(1)
        """
        self.ser_manager.send_command(COMMAND_RAINBOW)

    def send_color_wipe_command(self):
        """
        Sends the color wipe effect command to the serial manager.
        :return: None
        Time: O(1)
        """
        self.ser_manager.send_command(COMMAND_COLOR_WIPE)

    def send_random_sparkle_command(self):
        """
        Sends the random sparkle effect command to the serial manager.
        :return: None
        Time: O(1)
        """
        self.ser_manager.send_command(COMMAND_RANDOM_SPARKLE)

    def send_color_command(self, rgb):
        """
        Sends the RGB color command to the serial manager.
        :param rgb: The RGB color to send.
        :type rgb: tuple[int, int, int]
        :return: None
        Time: O(1)
        """
        command = f'rgb:{rgb[0]},{rgb[1]},{rgb[2]}'
        self.ser_manager.send_command(command)
