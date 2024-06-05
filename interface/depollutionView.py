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
        message_label_warning = tk.Label(self, text="ATTENTION \nCette opération supprimera tout fichier infecté trouvé sur la clé.", font=("bitstream charter", 50), fg="red")
        message_label_warning.pack(pady=50)
        
        message_label = tk.Label(self, text="Veuillez d'abord insérer la clé à dépolluer, \n puis cliquez sur \"Dépolluer\".", font=("bitstream charter", 50), fg="white", bg="#2c3e50")
        message_label.pack(pady=40)

        depollute_button = tk.Button(self, text="Dépolluer", font=("bitstream charter", 100), bg="#60C15A", fg="white" , bd=0, highlightthickness=0, width=15, height=2)
        depollute_button.pack(pady=0)
        depollute_button.config(command=lambda: subprocess.run(["python3", "depollution.py"]))

        back_button = tk.Button(self, text="Retour", font=("bitstream charter", 50), bg="#34495e", fg="#ecf0f1", bd=0, highlightthickness=0)
        back_button.place(x=20, y=self.master.winfo_screenheight() - 50, anchor='sw')
        back_button.config(command=self.go_back)

    def go_back(self):
        from mainView import MainView
        self.master.switch_frame(MainView)
