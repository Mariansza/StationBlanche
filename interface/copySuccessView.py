import tkinter as tk
from PIL import Image, ImageTk
import importdata

import pyudev

class CopySuccessView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg="#2c3e50")
        self.create_widgets()
        self.start_usb_monitor()

    def create_widgets(self):
        # Create a frame to contain the widgets and center it
        frame = tk.Frame(self, bg="#2c3e50")
        frame.place(relx=0.5, rely=0.5, anchor='center')

        message_label = tk.Label(frame, text="Copie correctement effectuée. \nVous pouvez retirer votre clé", font=("bitstream charter", 70), fg="white", bg="#2c3e50")
        message_label.pack(pady=40)

        self.image_label = tk.Label(frame, bg="#2c3e50")
        self.image_label.pack(pady=10)
        self.display_image("images/check.png")

    def display_image(self, image_path):
        image = Image.open(image_path)
        image = image.resize((300, 300), Image.LANCZOS)  # Redimensionner l'image si nécessaire
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo  # Pour éviter que l'image soit collectée par le garbage collector

    def start_usb_monitor(self):
        self.context = pyudev.Context()
        self.monitor = pyudev.Monitor.from_netlink(self.context)
        self.monitor.filter_by(subsystem='block', device_type='partition')
        self.observer = pyudev.MonitorObserver(self.monitor, self.usb_event)
        self.observer.start()

    def usb_event(self, action, device):
        if action == 'remove':
            self.observer.stop()
            from mainView import MainView
            self.master.switch_frame(MainView)
