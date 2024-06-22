import tkinter as tk
import analyse
from Views.Import.insertSecureUsbView import InsertSecureUsbView
import pyudev
import threading
import queue

class EjectUsbView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg="#2c3e50")
        self.create_widgets()
        self.start_usb_monitor()

    def create_widgets(self):
        message_label = tk.Label(self, text="Veuillez retirer votre clé non sécurisée.", font=("bitstream charter", 60), fg="white", bg="#2c3e50")
        message_label.grid(row=0, column=0, pady=40)

        # Centrer les widgets dans la fenêtre
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def start_usb_monitor(self):
        self.context = pyudev.Context()
        self.monitor = pyudev.Monitor.from_netlink(self.context)
        self.monitor.filter_by(subsystem='block', device_type='partition')
        self.observer = pyudev.MonitorObserver(self.monitor, self.usb_event)
        self.observer.start()

    def usb_event(self, action, device):
        if action == 'remove':
            self.observer.stop()
            self.master.switch_frame(InsertSecureUsbView)
