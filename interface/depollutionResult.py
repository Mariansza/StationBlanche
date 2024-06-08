import tkinter as tk
import queue

class DepollutionResultView(tk.Frame):
    def __init__(self, master, message_queue):
        super().__init__(master)
        self.master = master
        self.message_queue = message_queue
        self.configure(bg="#2c3e50")
        self.create_widgets()
        self.update_messages()

    def create_widgets(self):
        # Ajout d'un cadre pour contenir le champ de texte et centrer le bouton "Retour"
        frame = tk.Frame(self, bg="#2c3e50")
        frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        self.message_text = tk.Text(frame, font=("bitstream charter", 30), fg="white", bg="#2c3e50", wrap="word", state="disabled", height=10)
        self.message_text.tag_configure("center", justify='center')
        self.message_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        back_button = tk.Button(self, text="Retour", font=("bitstream charter", 50), bg="#34495e", fg="#ecf0f1", bd=0, highlightthickness=0)
        back_button.pack(pady=20)
        back_button.config(command=self.go_back)

    def go_back(self):
        from depollutionView import DepollutionView
        self.master.switch_frame(lambda master: DepollutionView(master))

    def update_messages(self):
        try:
            message = self.message_queue.get_nowait()
            self.message_text.config(state="normal")
            self.message_text.insert(tk.END, message + "\n", "center")
            self.message_text.config(state="disabled")
            self.message_text.see(tk.END)
        except queue.Empty:
            pass
        self.after(100, self.update_messages)
