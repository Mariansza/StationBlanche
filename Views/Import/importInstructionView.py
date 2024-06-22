import tkinter as tk
from Views.Import.importScanView import ImportScanView
import threading
import analyse
import queue
import pyudev
import time

class ImportInstructionView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg="#2c3e50")
        self.message_queue = queue.Queue()
        self.create_widgets()
        self.start_usb_monitor()
        self.start_timer()

    def create_widgets(self):
        message_label_warning = tk.Label(self, text="ATTENTION \nCette opération supprimera tout \nfichier infecté trouvé sur la clé.", font=("bitstream charter", 80), fg="red", bg="#2c3e50")
        message_label_warning.grid(row=0, column=0, pady=50)

        message_label = tk.Label(self, text="Veuillez insérer la clé non sécurisée.", font=("bitstream charter", 60), fg="white", bg="#2c3e50")
        message_label.grid(row=1, column=0, pady=40)


        back_button = tk.Button(self, text="Retour", font=("bitstream charter", 50), bg="#34495e", fg="#ecf0f1", bd=0, highlightthickness=0)
        back_button.grid(row=3, column=0, pady=20, sticky='s')
        back_button.config(command=self.go_back)

        # Centrer les widgets dans la fenêtre
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def go_back(self):
        from mainView import MainView
        self.master.switch_frame(MainView)

    def start_usb_monitor(self):
        self.context = pyudev.Context()
        self.monitor = pyudev.Monitor.from_netlink(self.context)
        self.monitor.filter_by(subsystem='block', device_type='partition')
        self.observer = pyudev.MonitorObserver(self.monitor, self.usb_event)
        self.observer.start()

    def usb_event(self, action, device):
        if action == 'add':
            self.observer.stop()
            self.stop_timer()
            time.sleep(2)
            self.master.switch_frame(lambda master: ImportScanView(master, self.message_queue))
            # Lance le processus de dépollution dans un nouveau thread
            thread = threading.Thread(target=self.run_depuration)
            thread.start()

    def run_depuration(self):
        analyse.main_scan(self.message_queue)

    def start_timer(self):
        self.timer_id = self.after(60000, self.go_back)  # 60 secondes pour retourner à MainView

    def stop_timer(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
