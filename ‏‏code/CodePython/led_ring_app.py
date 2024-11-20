import tkinter as tk
import math
import threading
import random
from material_button import MaterialButton
from serial_manager import SerialManager
from led_controller import LEDController


SIZE_WIDTH = 600
SIZE_HEIGHT = 600
RESET_TIME = 300
SIZE_LED = 10
NAME_PROJECT = "RGB LED RING"
COLOR_TRUN_OFF = "gray"
BACK_COLOR = "white"
RADIUS = 100
CENTER_X = 300
CENTER_Y = 300
NUM_LED = 12
NUM_LED_OFF = 1
NUM_LED_ON = NUM_LED - NUM_LED_OFF
MAX_NUM_COLOR_OX = 0xFFFFFF
MIN_NUM_COLOR_OX = 0

class LedRingApp:
    def __init__(self, master):
        self.master = master
        self.master.title(NAME_PROJECT)
        self.canvas = tk.Canvas(master, width=SIZE_WIDTH, height=SIZE_HEIGHT, bg=BACK_COLOR)
        self.canvas.pack()

        self.leds = []
        self.radius = RADIUS
        self.center = (CENTER_X, CENTER_Y)
        self.create_leds()
        self.running = True
        self.current_led = 0
        self.num_leds_on = NUM_LED_ON
        self.serial_manager = SerialManager()
        self.start_animation()

        self.label = tk.Label(master, text=NAME_PROJECT, font=("Arial", 16, "bold"), fg="#6200EE")
        self.label.pack(pady=20)

        self.check_connection()

    def create_leds(self):
        """
        This function create the led ring
        :return: None
        """
        for i in range(NUM_LED):
            angle = 2 * math.pi * i / NUM_LED
            x = self.center[0] + self.radius * math.cos(angle)
            y = self.center[1] + self.radius * math.sin(angle)
            led = self.canvas.create_oval(x - SIZE_LED, y - SIZE_LED, x + SIZE_LED, y + SIZE_LED, fill=COLOR_TRUN_OFF)
            self.leds.append(led)

    def start_animation(self):
        self.animate()

    def animate(self):
        """
        This function make led ring animation
        """
        if not self.running:
            #If flage stop
            return
        for i in range(self.num_leds_on):
            led_index = (self.current_led + i) % len(self.leds)  #Calculte the led index
            color = self.random_color()                          #random color for led
            self.canvas.itemconfig(self.leds[led_index], fill=color) #Chenge led color
        self.master.after(RESET_TIME, self.reset_leds)                      #reset led

    def reset_leds(self):
        """This funcrtion reset led to the default color"""
        for i in range(self.num_leds_on):
            led_index = (self.current_led + i) % len(self.leds)
            self.canvas.itemconfig(self.leds[led_index], fill=COLOR_TRUN_OFF) #set color to COLOR_TRUE_OFF
        self.current_led = (self.current_led + 1) % len(self.leds) #Move to the next led
        self.master.after(100, self.animate)

    def random_color(self):
        """Generate a randome color in HEX format"""
        return f'#{random.randint(MIN_NUM_COLOR_OX, MAX_NUM_COLOR_OX):06x}'

    def check_connection(self):
        """Check ardouni conect"""

        threading.Thread(target=self.connect_arduino).start()

    def connect_arduino(self):
        """connect tp arduino"""
        self.serial_manager.connect()
        self.master.after(0, self.show_main_app)

    def show_main_app(self):
        """Display the main application"""
        self.master.destroy()
        main_root = tk.Tk()
        main_root.iconbitmap(FOTO_PATH) #Foto app
        LEDController(main_root, self.serial_manager)
        main_root.mainloop()
