import tkinter as tk
from tkinter import messagebox, Toplevel, Label, Button
import queue
import os
import sys
import threading

from depollutionResult import DepollutionResultView

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import depollution

class DepollutionView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg="#2c3e50")
        self.message_queue = queue.Queue()
        self.create_widgets()

    def create_widgets(self):
        message_label_warning = tk.Label(self, text="ATTENTION \nCette opération supprimera tout fichier infecté trouvé sur la clé.", font=("bitstream charter", 50), bg="#2c3e50", fg="red")
        message_label_warning.pack(pady=50)
        
        message_label = tk.Label(self, text="Veuillez d'abord insérer la clé à dépolluer, \n puis cliquez sur \"Dépolluer\".", font=("bitstream charter", 50), fg="white", bg="#2c3e50")
        message_label.pack(pady=40)

        depollute_button = tk.Button(self, text="Dépolluer", font=("bitstream charter", 100), bg="#60C15A", fg="white" , bd=0, highlightthickness=0, width=15, height=2)
        depollute_button.pack(pady=0)
        depollute_button.config(command=self.start_depuration_process)

        back_button = tk.Button(self, text="Retour", font=("bitstream charter", 50), bg="#34495e", fg="#ecf0f1", bd=0, highlightthickness=0)
        back_button.pack(side=tk.BOTTOM, pady=20)
        back_button.config(command=self.go_back)

    def go_back(self):
        from mainView import MainView
        self.master.switch_frame(MainView)

    def show_custom_error_popup(self, title, message):
        popup = Toplevel(self)
        popup.title(title)
       

        # Get the screen width and height
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()

        # Calculate position
        x = (screen_width // 4) - (1200 // 2)
        y = (screen_height // 2) - (600 // 2)

        # Set the position of the window to the center of the screen
        popup.geometry('%dx%d+%d+%d' % (1200, 600, x, y))

        label = Label(popup, text=message, font=("bitstream charter", 60), fg="black")
        label.pack(pady=20)

        ok_button = Button(popup, text="OK", font=("bitstream charter", 50), fg="black", command=popup.destroy)
        ok_button.pack(pady=20)


    def start_depuration_process(self):
        usb_mount_point = depollution.find_usb_mount_point()
        if not usb_mount_point:
            self.show_custom_error_popup("Erreur", "Aucune clé USB montée \n n'a été trouvée.")
            return
        
        self.master.switch_frame(lambda master: DepollutionResultView(master, self.message_queue))
        # Lance le processus de dépollution dans un nouveau thread
        thread = threading.Thread(target=self.run_depuration)
        thread.start()

    def run_depuration(self):
        usb_mount_point = depollution.find_usb_mount_point()
        if usb_mount_point:
            depollution.main_scan(self.message_queue)
        