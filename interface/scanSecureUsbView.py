import os
import shutil
import tkinter as tk
import importdata
import queue
import threading
from copySuccessView import CopySuccessView
from PIL import Image, ImageTk
import itertools
from tkinter import Toplevel, Label, Button, ttk

class ScanSecureUsbView(tk.Frame):
    def __init__(self, master, message_queue):
        super().__init__(master)
        self.master = master
        self.message_queue = message_queue
        self.configure(bg="#2c3e50")
        self.animation_running = True
        self.create_widgets()
        self.update_messages()
        self.animate_loading()  # Commencer l'animation au démarrage

    def create_widgets(self):
        frame = tk.Frame(self, bg="#2c3e50")
        frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        self.message_label = tk.Label(frame, text="\nScan de la clé sécurisée...", font=("bitstream charter", 70), fg="white", bg="#2c3e50")
        self.message_label.pack(pady=10, padx=10)

        self.progress_frame = tk.Frame(self, bg="#2c3e50")
        self.progress_frame.place(relx=0.5, rely=0.6, anchor=tk.CENTER)  # Centre la barre de progression et l'animation

        self.animation_label = tk.Label(self.progress_frame, bg="#2c3e50")
        self.animation_label.pack()

        self.progress_label = tk.Label(self.progress_frame, text="0%", font=("bitstream charter", 40), fg="white", bg="#2c3e50")
        self.progress_label.pack()

        style = ttk.Style()
        style.configure("custom.Horizontal.TProgressbar", foreground='#00D6E0', background='#00D6E0')

        self.progress = ttk.Progressbar(self.progress_frame, style="custom.Horizontal.TProgressbar", orient="horizontal", length=1500, mode="determinate")
        self.progress.pack(pady=10, ipady=20)  # ipady pour augmenter l'épaisseur de la barre
        self.progress["value"] = 0
        self.progress["maximum"] = 100

        back_button = tk.Button(self, text="Retour", font=("bitstream charter", 50), bg="#34495e", fg="#ecf0f1", bd=0, highlightthickness=0)
        back_button.pack(pady=20)
        back_button.config(command=self.go_back)

        # Charger les images pour l'animation
        self.load_animation_images()

    def go_back(self):
        from importInstructionView import ImportInstructionView
        self.master.switch_frame(lambda master: ImportInstructionView(master))

    def update_messages(self):
        try:
            message = self.message_queue.get_nowait()
            if "Progress:" in message:
                progress = float(message.split(":")[1].strip())
                self.progress["value"] = progress
                self.progress_label.config(text=f"{int(progress)}%")

            elif "Aucun fichier infecté trouvé." in message:
                self.animation_running = False  # Stopper l'animation
                self.message_label.config(text="Scan terminé")
                self.show_custom_popup("Information", "Aucun fichier infecté trouvé.")
                self.animation_label.destroy()  # Supprimer l'animation et la barre de progression

            elif "Fichiers infectés trouvés et supprimés" in message:
                self.animation_running = False
                self.message_label.config(text="Scan terminé")
                self.show_custom_popup("Alerte", "Fichiers infectés trouvés et supprimés. Le système est analysé. Une dépollution va être relancée.", fg="red")
                self.message_label.config(text="Analyse du système en cours...")
                self.animation_label.destroy()

            elif "Le système est infecté par un rootkit." in message or "Aucun rootkit trouvé sur le système." in message:
                self.animation_running = False
                from insertSecureUsbView import InsertSecureUsbView
                self.master.switch_frame(lambda master: InsertSecureUsbView(master))
                self.master._frame.start_depuration_process()
        except queue.Empty:
            pass

        self.after(100, self.update_messages)

    def display_image(self, image_path):
        image = Image.open(image_path)
        image = image.resize((300, 300), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo

    def load_animation_images(self):
        self.animation_images = []
        for i in range(1, 31):
            image_path = f"images/loading/{i}.png"
            image = Image.open(image_path)
            image = image.resize((300, 300), Image.LANCZOS)
            self.animation_images.append(ImageTk.PhotoImage(image))
        self.animation_cycle = itertools.cycle(self.animation_images)

    def animate_loading(self):
        if self.animation_running:
            self.animation_label.config(image=next(self.animation_cycle))
            self.after(25, self.animate_loading)  # Changer d'image toutes les 25 ms

    def show_custom_popup(self, title, message, fg="black"):
        popup = Toplevel(self)
        popup.title(title)

        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()

        x = (screen_width // 4) - (1200 // 2)
        y = (screen_height // 2) - (700 // 2)

        popup.geometry('%dx%d+%d+%d' % (1200, 700, x, y))

        label = Label(popup, text=message, font=("bitstream charter", 50), fg=fg)
        label.pack(pady=20)

        if "Aucun fichier infecté trouvé." in message:
            image_path = "images/check.png"
            image = Image.open(image_path)
            image = image.resize((250, 250), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            image_label = Label(popup, image=photo)
            image_label.image = photo
            image_label.pack(pady=10)

        else:
            image_path = "images/wrong2.png"
            image = Image.open(image_path)
            image = image.resize((150, 150), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            image_label = Label(popup, image=photo)
            image_label.image = photo
            image_label.pack(pady=10)

        ok_button = Button(popup, text="OK", font=("bitstream charter", 50), fg="black", command=lambda: self.on_popup_ok(popup, message))
        ok_button.pack(pady=20)

    def on_popup_ok(self, popup, message):
        popup.destroy()
        if "Aucun fichier infecté trouvé." in message:
            self.master.switch_frame(lambda master: CopySuccessView(master))

    def copy_files_to_secure_usb(self):
        temp_dir = "/tmp/temp_data_import"
        usb_mount_point = importdata.find_usb_mount_point()
        if usb_mount_point:
            for file_name in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, file_name)
                shutil.copy(file_path, usb_mount_point)
            shutil.rmtree(temp_dir)
            importdata.unmount_usb(usb_mount_point, self.message_queue)
