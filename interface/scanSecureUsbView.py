import os
import shutil
import tkinter as tk
import importdata
import queue
import threading
from copySuccessView import CopySuccessView

class ScanSecureUsbView(tk.Frame):
    def __init__(self, master, message_queue):
        super().__init__(master)
        self.master = master
        self.configure(bg="#2c3e50")
        self.message_queue = message_queue
        self.create_widgets()
        self.update_messages()
        

    def create_widgets(self):
        message_label = tk.Label(self, text="Scan de la clé sécurisée", font=("bitstream charter", 50), fg="white", bg="#2c3e50")
        message_label.pack(pady=40)

        self.message_text = tk.Text(self, font=("bitstream charter", 30), fg="white", bg="#2c3e50", wrap="word", state="disabled", height=10)
        self.message_text.tag_configure("center", justify='center')
        self.message_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def update_messages(self):
        try:
            message = self.message_queue.get_nowait()
            self.message_text.config(state="normal")
            self.message_text.insert(tk.END, message + "\n", "center")
            self.message_text.config(state="disabled")
            self.message_text.see(tk.END)

            if "Aucun fichier infecté trouvé." in message:
                self.copy_files_to_secure_usb()
                self.master.switch_frame(lambda master: CopySuccessView(master))
            elif "Fichiers infectés trouvés" in message:
                self.master.switch_frame(lambda master: ScanSecureUsbView(master, self.message_queue))

        except queue.Empty:
            pass

        self.after(100, self.update_messages)



    def copy_files_to_secure_usb(self):
        temp_dir = "/tmp/temp_data_import"
        usb_mount_point = importdata.find_usb_mount_point()
        if usb_mount_point:
            for file_name in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, file_name)
                shutil.copy(file_path, usb_mount_point)
            shutil.rmtree(temp_dir)
            importdata.unmount_usb(usb_mount_point, self.message_queue)

    
    def update_messages(self):
        try:
            message = self.message_queue.get_nowait()
            self.message_text.config(state="normal")
            self.message_text.insert(tk.END, message + "\n", "center")
            self.message_text.config(state="disabled")
            self.message_text.see(tk.END)

            if "Aucun fichier infecté trouvé." in message:
                self.copy_files_to_secure_usb()
                self.master.switch_frame(lambda master: CopySuccessView(master))
            

        except queue.Empty:
            pass

        self.after(100, self.update_messages)