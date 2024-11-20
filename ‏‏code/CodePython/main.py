import tkinter as tk
from led_ring_app import LedRingApp

FOTO_PATH = "Foto\\Foto\\fotoApp.ico"

if __name__ == "__main__":
    root = tk.Tk()               #Creat the main application window
    root.iconbitmap(FOTO_PATH)   #Foto app
    splash = LedRingApp(root)    #Initalize the LedRingApp class, passong gthe main window
    root.geometry("600x600")     #Set the size of the window
    root.mainloop()

