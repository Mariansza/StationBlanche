import tkinter as tk
import queue
from PIL import Image, ImageTk

class DepollutionResultView(tk.Frame):
    def __init__(self, master, message_queue):
        super().__init__(master)
        self.master = master
        self.message_queue = message_queue
        self.configure(bg="#2c3e50")
        self.image_displayed = False  # Ajouter un flag pour vérifier si l'image est déjà affichée
        self.create_widgets()
        self.update_messages()

    def create_widgets(self):
        # Ajout d'un cadre pour contenir le champ de texte et centrer le bouton "Retour"
        frame = tk.Frame(self, bg="#2c3e50")
        frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        self.message_text = tk.Text(frame, font=("bitstream charter", 30), fg="white", bg="#2c3e50", wrap="word", state="disabled", height=10)
        self.message_text.tag_configure("center", justify='center')
        self.message_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.image_label = tk.Label(self, bg="#2c3e50")  # Label pour afficher l'image
        self.image_label.pack(pady=10)  # Ajout d'espace autour de l'image

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
            
            # Vérifie si le message indique qu'aucun fichier infecté n'a été trouvé
            if "Aucun fichier infecté trouvé." in message:
                self.display_image("images/check.png")  # Remplacez par le chemin de votre image
                self.image_displayed = True  # Mettre à jour le flag

            elif "Fichiers infectés trouvés" in message:
                self.display_image("images/wrong2.png")
                self.image_displayed = True
                
        except queue.Empty:
            pass

        self.after(100, self.update_messages)

    def display_image(self, image_path):
        image = Image.open(image_path)
        image = image.resize((300, 300), Image.LANCZOS)  # Redimensionner l'image si nécessaire
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo  # Pour éviter que l'image soit collectée par le garbage collector
