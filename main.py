from Layouts.layout import Ventana_P
import customtkinter as ctk

if __name__ == "__main__":
    ctk.set_appearance_mode('Dark')  # o "Dark"/"Light"
    ctk.set_default_color_theme("blue")  # o cualquier otro

    app = Ventana_P()
    app.title("Sistema de Gestión Clínica")
    app.geometry("1350x680")
    app.mainloop()
