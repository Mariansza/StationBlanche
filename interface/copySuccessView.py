import tkinter as tk
from PIL import Image, ImageTk

class CopySuccessView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg="#2c3e50")
        self.create_widgets()

    def create_widgets(self):
        message_label = tk.Label(self, text="Copie correctement effectuée, vous pouvez retirer votre clé", font=("bitstream charter", 50), fg="white", bg="#2c3e50")
        message_label.pack(pady=40)

        self.image_label = tk.Label(self, bg="#2c3e50")  # Label pour afficher l'image
        self.image_label.pack(pady=10)
        self.display_image("images/check.png")
        
        ok_button = tk.Button(self, text="Retour au menu", font=("bitstream charter", 100), bg="#34495e", fg="#ecf0f1", bd=0, highlightthickness=0, width=15, height=2)
        ok_button.pack(pady=20)
        ok_button.config(command=self.go_back)

    def go_back(self):
        from mainView import MainView
        self.master.switch_frame(MainView)

    def display_image(self, image_path):
        image = Image.open(image_path)
        image = image.resize((300, 300), Image.LANCZOS)  # Redimensionner l'image si nécessaire
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo  # Pour éviter que l'image soit collectée par le garbage collector
