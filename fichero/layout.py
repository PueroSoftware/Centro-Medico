import os
import customtkinter as ctk
from PIL import Image  # Libreria Imagen
from customtkinter import CTkImage
from datos.router import mostrar_paciente
from fichero.altcentro import alt_centro
from datos.router import mostrar_doctor, mostrar_cita, mostrar_botica, mostrar_resumen


# ---------------------- Clases Base Personalizadas ----------------------
class Botones_P(ctk.CTkButton): pass
class Etiqueta_P(ctk.CTkLabel): pass
class Entradas_P(ctk.CTkEntry): pass
class Cajas_P(ctk.CTkCheckBox): pass
class Marcos_P(ctk.CTkFrame): pass
class R_Botones_P(ctk.CTkRadioButton): pass


# ---------------------- Clase Principal ----------------------
class Ventana_P(ctk.CTk):
    def __init__(self):
        super().__init__()
        ancho, alto = 1320, 680
        alt_centro(self, ancho, alto)
        self.title("Centro Medico")
        self.resizable(False, False)

        # --- Rutas e imágenes ---
        ruta_raiz = os.path.dirname(__file__)
        ruta_principal = os.path.dirname(ruta_raiz)
        ruta_img = os.path.join(ruta_principal, "img")
        icono = os.path.join(ruta_img, "logo.ico")
        logo = os.path.join(ruta_img, "perfil.png")

        if os.path.exists(icono):
            self.iconbitmap(icono)
        else:
            print("¡ERROR! No se encontró el ícono:", icono)

        imagen_ctk = CTkImage(light_image=Image.open(logo), size=(200, 200))

        # --- Marco superior ---
        m_superior = Marcos_P(self, height=10, border_color="#373837")
        m_superior.pack(side="top", fill="x")

        fuente = ctk.CTkFont(family="Roboto", size=20, weight="bold", slant="italic")
        Titulo_P = Etiqueta_P(m_superior, text="Centro Medico Alianza Medica Popular", font=fuente)
        Titulo_P.pack(pady=10)

        # --- Marco inferior ---
        m_sidebar = Marcos_P(self, height=50, border_width=2)
        m_sidebar.pack(side="bottom", fill="x")
        for i in range(8):
            m_sidebar.grid_columnconfigure(i, weight=1)

        # --- Marco principal ---
        m_principal = Marcos_P(self, fg_color="#F8F8F8", border_width=1)
        m_principal.pack(side="top", fill="both", expand=True)
        m_principal.grid_rowconfigure(0, weight=1)
        m_principal.grid_rowconfigure(1, weight=2)
        m_principal.grid_columnconfigure(0, weight=0)
        m_principal.grid_columnconfigure(1, weight=1)

        # --- Cuerpo dinámico ---
        self.m_cuerpo = Marcos_P(m_principal, fg_color="#373837")
        self.m_cuerpo.grid(row=0, column=1, rowspan=2, pady=10, padx=10, sticky="nsew")

        # --- Lado izquierdo ---
        m_izquierdo = Marcos_P(m_principal, width=200, border_width=1, border_color="#fbf8f8")
        m_izquierdo.grid(row=1, column=0, pady=(10, 5), padx=10, sticky="w")
        for i in range(7):
            m_izquierdo.grid_columnconfigure(i, weight=2)

        m1_izquierdo = Marcos_P(m_principal, width=200, height=200, border_width=1, border_color="#fbf8f8")
        m1_izquierdo.grid(row=0, column=0, pady=(5, 10), padx=10, sticky="w")
        m1_izquierdo.grid_propagate(False)

        lbl_logo = Etiqueta_P(m1_izquierdo, image=imagen_ctk, text="")
        lbl_logo.pack(pady=10)

          #
        # --- Botones menú izquierdo ---
        Botones_P(m_izquierdo, text="Paciente", width=180, height=30, command=lambda: mostrar_paciente(self)).pack(pady=10, padx=10)
        Botones_P(m_izquierdo, text="Doctor", width=180, height=30, command=lambda: mostrar_doctor(self)).pack(pady=10,padx=10)
        Botones_P(m_izquierdo, text="Citas", width=180, height=30, command=lambda: mostrar_cita(self)).pack(pady=10,padx=10)
        Botones_P(m_izquierdo, text="Botica", width=180, height=30, command=lambda: mostrar_botica(self)).pack(pady=10,padx=10)
        Botones_P(m_izquierdo, text="Resumen", width=180, height=30, command=lambda: mostrar_resumen(self)).pack(pady=10, padx=10)
                    # --- Botones inferiores ---
        Botones_P(m_sidebar, text="<< Atrás", width=200, height=35).grid(row=0, column=0, pady=10, padx=(20, 5),sticky="w")
        Botones_P(m_sidebar, text="Guardar", width=200, height=35).grid(row=0, column=3, pady=10, padx=5)
        Botones_P(m_sidebar, text="Limpiar", width=200, height=35).grid(row=0, column=4, pady=10, padx=5)
        Botones_P(m_sidebar, text="Avanzar >>", width=200, height=35).grid(row=0, column=7, pady=10, padx=(5, 20),sticky="e")


    def mostrar_frame(self, frame_class):
        for widget in self.m_cuerpo.winfo_children():
            widget.destroy()
        nuevo_frame = frame_class(master=self.m_cuerpo)
        nuevo_frame.pack(fill="both", expand=True)
