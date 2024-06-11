import tkinter as tk
import importdata
from insertSecureUsbView import InsertSecureUsbView
import queue

class EjectUsbView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg="#2c3e50")
        self.create_widgets()

    def create_widgets(self):
        message_label = tk.Label(self, text="Veuillez retirer votre clé non sécurisée, puis appuyez sur OK", font=("bitstream charter", 50), fg="white", bg="#2c3e50")
        message_label.grid(row=0, column=0, pady=40)

        ok_button = tk.Button(self, text="OK", font=("bitstream charter", 100), bg="#34495e", fg="#ecf0f1", bd=0, highlightthickness=0, width=15, height=2)
        ok_button.grid(row=1, column=0, pady=20)
        ok_button.config(command=self.unmount_usb_and_proceed)

        # Centrer les widgets dans la fenêtre
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def unmount_usb_and_proceed(self):
        usb_mount_point = importdata.find_usb_mount_point()
        if usb_mount_point:
            importdata.unmount_usb(usb_mount_point, queue.Queue())
        self.master.switch_frame(InsertSecureUsbView)
