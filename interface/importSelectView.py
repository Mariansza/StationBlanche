import shutil
import tkinter as tk
from tkinter import filedialog
import importdata 
import os

from ejectUsbView import EjectUsbView

class ImportSelectView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg="#2c3e50")
        self.create_widgets()
        self.selected_files = []
        
        # Ouvrir la fenêtre de sélection de fichiers 1 seconde après l'ouverture de la vue
        self.after(1000, self.select_files)

    def create_widgets(self):
        message_label = tk.Label(self, text="Veuillez sélectionner les fichiers à copier", font=("bitstream charter", 60), fg="white", bg="#2c3e50")
        message_label.pack(pady=40)

        back_button = tk.Button(self, text="Retour", font=("bitstream charter", 50), bg="#34495e", fg="#ecf0f1", bd=0, highlightthickness=0)
        back_button.pack(side=tk.BOTTOM, pady=20)
        back_button.config(command=self.go_back)

    def go_back(self):
        from importInstructionView import ImportInstructionView
        self.master.switch_frame(ImportInstructionView)

    def copy_files(self):
        temp_dir = "/tmp/temp_data_import" 
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        for file in self.selected_files:
            shutil.copy(file, temp_dir)
        self.master.switch_frame(lambda master: EjectUsbView(master))

    def select_files(self):
        usb_mount_point = importdata.find_usb_mount_point()
        if usb_mount_point:
            # Agrandir la fenêtre principale avant d'ouvrir la boîte de dialogue de fichiers
            self.master.geometry("1200x800")  # Par exemple, redimensionner la fenêtre principale

            file_paths = filedialog.askopenfilenames(
                initialdir=usb_mount_point,
                title="Sélectionnez les fichiers à copier",
                filetypes=[("Tous les fichiers", "*.*")],
                multiple=True
            )
            print(f"Selected files: {file_paths}")
            self.selected_files = file_paths
            
            # Copier les fichiers immédiatement après la sélection
            self.copy_files()
        else:
            print("Aucune clé USB montée n'a été trouvée.")
