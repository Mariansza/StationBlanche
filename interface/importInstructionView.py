import tkinter as tk
from importScanView import ImportScanView
import threading
import importdata
import queue

class ImportInstructionView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg="#2c3e50")
        self.message_queue = queue.Queue()
        self.create_widgets()

    def create_widgets(self):
        message_label_warning = tk.Label(self, text="ATTENTION \nCette opération supprimera certains fichiers.", font=("bitstream charter", 50), fg="red", bg="#2c3e50")
        message_label_warning.pack(pady=50)
        
        message_label = tk.Label(self, text="Veuillez insérer la clé non sécurisée.", font=("bitstream charter", 50), fg="white", bg="#2c3e50")
        message_label.pack(pady=40)

        ok_button = tk.Button(self, text="OK", font=("bitstream charter", 100), bg="#34495e", fg="#ecf0f1", bd=0, highlightthickness=0, width=15, height=2)
        ok_button.pack(pady=20)
        ok_button.config(command=self.start_depuration_process)

        back_button = tk.Button(self, text="Retour", font=("bitstream charter", 50), bg="#34495e", fg="#ecf0f1", bd=0, highlightthickness=0)
        back_button.pack(side=tk.BOTTOM, pady=20)
        back_button.config(command=self.go_back)

    def go_back(self):
        from mainView import MainView
        self.master.switch_frame(MainView)

    def start_depuration_process(self):
        # Change la vue immédiatement
        self.master.switch_frame(lambda master: ImportScanView(master, self.message_queue))
        # Lance le processus de dépollution dans un nouveau thread
        thread = threading.Thread(target=self.run_depuration)
        thread.start()

    def run_depuration(self):
        importdata.main_scan(self.message_queue)
