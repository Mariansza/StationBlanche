import tkinter as tk
from tkinter import messagebox
import subprocess

class DepollutionView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg="#2c3e50")
        self.create_widgets()

    def create_widgets(self):
        message_label_warning = tk.Label(self, text="ATTENTION \nCette opération supprimera tout fichier infecté trouvé sur la clé.", font=("Arial", 30), fg="red")
        message_label_warning.pack(pady=50)
        
        message_label = tk.Label(self, text="Veuillez d'abord insérer la clé à dépolluer, puis cliquez sur \"Dépolluer\".", font=("Arial", 30), fg="white", bg="#2c3e50")
        message_label.pack(pady=40)

        depollute_button = tk.Button(self, text="Dépolluer", font=("Arial", 30), bg="#34495e", fg="#ecf0f1", bd=0, highlightthickness=0)
        depollute_button.pack(pady=20)
        depollute_button.config(command=lambda: subprocess.run(["python3", "depollution.py"]))

        back_button = tk.Button(self, text="Retour", font=("Arial", 20), bg="#34495e", fg="#ecf0f1", bd=0, highlightthickness=0)
        back_button.pack(side='bottom', pady=20)
        back_button.config(command=self.go_back)

    def go_back(self):
        from mainView import MainView
        self.master.switch_frame(MainView)
