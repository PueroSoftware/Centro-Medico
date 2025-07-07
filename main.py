import customtkinter as ctk
from fichero.layout import Ventana_P

if __name__ == "__main__":
    ctk.set_appearance_mode('Dark')  # o "Dark"/"Light"
    app = Ventana_P()
    app.title("Sistema de Gestión Clínica")
    app.geometry("1300x650")

    app.mainloop()
