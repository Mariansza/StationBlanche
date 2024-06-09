import tkinter as tk
import queue
import threading
import importdata
from importSelectView import ImportSelectView


class ImportScanView(tk.Frame):
    def __init__(self, master, message_queue):
        super().__init__(master)
        self.master = master
        self.configure(bg="#2c3e50")
        self.message_queue = message_queue
        self.create_widgets()
        self.update_messages()

    def create_widgets(self):
        message_label = tk.Label(self, text="Scan de la clé non sécurisée", font=("bitstream charter", 50), fg="white", bg="#2c3e50")
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
                self.master.switch_frame(lambda master: ImportSelectView(master))
            elif "Fichiers infectés trouvés" in message:
                self.master.switch_frame(lambda master: ImportScanView(master))

        except queue.Empty:
            pass

        self.after(100, self.update_messages)

   
