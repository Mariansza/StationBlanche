import tkinter as tk
from depollutionView import DepollutionView

class MainView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg="#2c3e50")
        self.create_widgets()

    def create_widgets(self):
        button_font = ("bitstream charter", 60)
        button_bg_color = "#34495e"
        button_fg_color = "#ecf0f1"
        button_hover_color = "#1abc9c"

        frame = tk.Frame(self, bg="#2c3e50")
        frame.place(relx=0.5, rely=0.5, anchor='center')

        depollution_button = tk.Button(frame, text="Dépollution", width=20, height=3, font=button_font, bg=button_bg_color, fg=button_fg_color, bd=0, highlightthickness=0)
        depollution_button.pack(pady=20)
        depollution_button.bind("<Enter>", lambda e: depollution_button.configure(bg=button_hover_color))
        depollution_button.bind("<Leave>", lambda e: depollution_button.configure(bg=button_bg_color))
        depollution_button.config(command=self.show_depollution_view)

        import_data_button = tk.Button(frame, text="Import de données", width=20, height=3, font=button_font, bg=button_bg_color, fg=button_fg_color, bd=0, highlightthickness=0)
        import_data_button.pack(pady=20)
        import_data_button.bind("<Enter>", lambda e: import_data_button.configure(bg=button_hover_color))
        import_data_button.bind("<Leave>", lambda e: import_data_button.configure(bg=button_bg_color))

    def show_depollution_view(self):
        self.master.switch_frame(lambda master: DepollutionView(master))

class WelcomeView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg="#2c3e50")
        self.create_widgets()

    def create_widgets(self):
        welcome_label = tk.Label(self, text="Touchez pour commencer", font=("bitstream charter", 70), fg="#ecf0f1", bg="#2c3e50")
        welcome_label.place(relx=0.5, rely=0.5, anchor='center')
        self.bind("<Button-1>", lambda event: self.master.switch_frame(MainView))

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bienvenue")
        self.attributes('-fullscreen', True)
        self._frame = None
        self.switch_frame(WelcomeView)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = Application()
    app.mainloop()