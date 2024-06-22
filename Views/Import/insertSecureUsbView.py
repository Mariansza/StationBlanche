import tkinter as tk
import threading
import analyse
from Views.Import.scanSecureUsbView import ScanSecureUsbView
import queue
import pyudev
import time

class InsertSecureUsbView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg="#2c3e50")
        self.message_queue = queue.Queue()
        self.create_widgets()
        self.start_usb_monitor()

    def create_widgets(self):
        message_label = tk.Label(self, text="Veuillez maintenant insérer \n la clé sécurisée.", font=("bitstream charter", 60), fg="white", bg="#2c3e50")
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
        if action == 'add':
            self.observer.stop()
            time.sleep(2)
            self.start_depuration_process()

    def start_depuration_process(self):
        self.master.switch_frame(lambda master: ScanSecureUsbView(master, self.message_queue))
        thread = threading.Thread(target=self.run_depuration)
        thread.start()

    def run_depuration(self):
        analyse.main_scan(self.message_queue)
