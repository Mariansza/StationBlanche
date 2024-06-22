import tkinter as tk
from tkinter import Button, Label, Toplevel, ttk
import queue
from PIL import Image, ImageTk
import itertools
import pyudev

class DepollutionResultView(tk.Frame):
    def __init__(self, master, message_queue):
        super().__init__(master)
        self.master = master
        self.message_queue = message_queue
        self.configure(bg="#2c3e50")
        self.image_displayed = False
        self.animation_running = True
        self.create_widgets()
        self.update_messages()
        self.animate_loading() 
        self.popup = None
        self.start_usb_monitor()

    def create_widgets(self):
        frame = tk.Frame(self, bg="#2c3e50")
        frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        self.message_label = tk.Label(frame, text="\n Dépollution en cours, veuillez patienter...", font=("bitstream charter", 70), fg="white", bg="#2c3e50")
        self.message_label.pack(pady=10, padx=10)

        # Frame pour la barre de progression, le pourcentage et l'animation
        self.progress_frame = tk.Frame(self, bg="#2c3e50")
        self.progress_frame.place(relx=0.5, rely=0.6, anchor=tk.CENTER)  # Centre la barre de progression et l'animation

        self.animation_label = tk.Label(self.progress_frame, bg="#2c3e50")
        self.animation_label.pack()

        self.progress_label = tk.Label(self.progress_frame, text="0%", font=("bitstream charter", 40), fg="white", bg="#2c3e50")
        self.progress_label.pack()

        style = ttk.Style()
        style.configure("custom.Horizontal.TProgressbar", foreground='#00D6E0', background='#00D6E0')

        self.progress = ttk.Progressbar(self.progress_frame, style="custom.Horizontal.TProgressbar", orient="horizontal", length=1500, mode="determinate")
        self.progress.pack(pady=10, ipady=20)
        self.progress["value"] = 0
        self.progress["maximum"] = 100

        back_button = tk.Button(self, text="Retour", font=("bitstream charter", 50), bg="#34495e", fg="#ecf0f1", bd=0, highlightthickness=0)
        back_button.pack(pady=20)
        back_button.config(command=self.go_back)

        # Charger les images pour l'animation
        self.load_animation_images()

    def go_back(self):
        from Views.Dépollution.depollutionView import DepollutionView
        self.master.switch_frame(lambda master: DepollutionView(master))

    def update_messages(self):
        try:
            message = self.message_queue.get_nowait()
            if "Progress:" in message:
                progress = float(message.split(":")[1].strip())
                self.progress["value"] = progress
                self.progress_label.config(text=f"{int(progress)}%")

            elif "Aucun fichier infecté trouvé." in message:
                self.animation_running = False 
                self.message_label.config(text="Dépollution terminée")
                self.show_custom_popup("Information", "Aucun fichier infecté trouvé. \n Vous pouvez retirer votre clé.")
                self.animation_label.destroy()  

            elif "Fichiers infectés trouvés et supprimés" in message:
                self.animation_running = False
                self.message_label.config(text="Dépollution terminée")
                self.show_custom_popup("Alerte", "Fichiers infectés trouvés et\n supprimés. Le système est analysé. \n Une dépollution va être relancée.", fg="red")
                self.message_label.config(text="Analyse du système en cours...")
                self.animation_label.destroy()

            elif "Le système est infecté par un rootkit." in message or "Aucun rootkit trouvé sur le système." in message:
                self.animation_running = False
                from Views.Dépollution.depollutionView import DepollutionView
                self.master.switch_frame(DepollutionView)
                self.master._frame.usb_event('add', None)
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
            self.after(25, self.animate_loading)  

    def show_custom_popup(self, title, message, fg="black"):
        self.popup = Toplevel(self)
        self.popup.title(title)

       
        master_x = self.master.winfo_x()
        master_y = self.master.winfo_y()
        master_width = self.master.winfo_width()
        master_height = self.master.winfo_height()

       
        popup_width = 1200
        popup_height = 700
        x = master_x + (master_width // 2) - (popup_width // 2)
        y = master_y + (master_height // 2) - (popup_height // 2)

        self.popup.geometry('%dx%d+%d+%d' % (popup_width, popup_height, x, y))

        label = Label(self.popup, text=message, font=("bitstream charter", 50), fg=fg)
        label.pack(pady=20)

        if "Aucun fichier infecté trouvé." in message:
            image_path = "images/check.png"
            image = Image.open(image_path)
            image = image.resize((250, 250), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            image_label = Label(self.popup, image=photo)
            image_label.image = photo
            image_label.pack(pady=10)

        else:
            image_path = "images/wrong2.png"
            image = Image.open(image_path)
            image = image.resize((150, 150), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            image_label = Label(self.popup, image=photo)
            image_label.image = photo
            image_label.pack(pady=10)

        ok_button = Button(self.popup, text="OK", font=("bitstream charter", 50), fg="black", command=self.popup.destroy)
        ok_button.pack(pady=20)

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
            if self.popup is not None:  
                self.popup.destroy()
                self.popup = None
