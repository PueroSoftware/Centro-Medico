import os
from datetime import date
import customtkinter as ctk
from PIL import Image

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class ResumenFrame(ctk.CTkFrame):
    def __init__(self, master=None, logo_img=None):
        super().__init__(master, fg_color="#1F1F1F")
        self.pack(fill="both", expand=True)

        ruta_raiz = os.path.dirname(__file__)
        ruta_principal = os.path.dirname(ruta_raiz)
        ruta_img = os.path.join(ruta_principal, "img")
        icono = os.path.join(ruta_img, "logo.ico")
        logo = os.path.join(ruta_img, "perfil.png")
        # --- Cabecera con Entry editables ---
        cabecera = ctk.CTkFrame(self, fg_color="#1F1F1F")
        cabecera.pack(fill="x", padx=30, pady=(20, 0))

        ctk.CTkLabel(cabecera, text="🔎 Cédula Paciente:", font=("Roboto", 14), text_color="#E0E0E0") \
            .grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.cedula_paciente = ctk.CTkEntry(cabecera, placeholder_text="Ej: 0912345678")
        self.cedula_paciente.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(cabecera, text="🧑‍⚕️ Cédula Doctor:", font=("Roboto", 14), text_color="#E0E0E0") \
            .grid(row=0, column=2, padx=10, pady=5, sticky="e")
        self.cedula_doctor = ctk.CTkEntry(cabecera, placeholder_text="Ej: 1798765432")
        self.cedula_doctor.grid(row=0, column=3, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(cabecera, text="📆 Fecha:", font=("Roboto", 14), text_color="#E0E0E0") \
            .grid(row=0, column=4, padx=10, pady=5, sticky="e")
        self.fecha = ctk.CTkEntry(cabecera)
        self.fecha.insert(0, str(date.today()))
        self.fecha.grid(row=0, column=5, padx=10, pady=5)

        for i in [1, 3]:
            cabecera.grid_columnconfigure(i, weight=1)

        # --- Contenedor principal: dos columnas ---
        contenedor = ctk.CTkFrame(self, fg_color="#1F1F1F")
        contenedor.pack(fill="both", expand=True, padx=30, pady=20)

        col_izq = ctk.CTkFrame(contenedor, fg_color="#2C2C2C")
        col_der = ctk.CTkFrame(contenedor, fg_color="#2C2C2C")
        col_izq.pack(side="left", fill="both", expand=True, padx=(0, 10))
        col_der.pack(side="left", fill="both", expand=True, padx=(10, 0))

        # --- Columna izquierda: Datos del paciente ---
        ctk.CTkLabel(col_izq, text="👤 DATOS DEL PACIENTE", font=("Roboto", 16, "bold"),
                     text_color="#FFFFFF").pack(anchor="w", padx=15, pady=(5, 10))

        self.label_nombre = self.crear_linea(col_izq, "Nombre:")
        self.label_edad = self.crear_linea(col_izq, "Edad:")
        self.label_cita = self.crear_linea(col_izq, "N° Cita:")

        # --- Columna derecha: Diagnóstico / Tratamiento ---
        ctk.CTkLabel(col_der, text="🩺 DETALLES CLÍNICOS", font=("Roboto", 16, "bold"),
                     text_color="#FFFFFF").pack(anchor="w", padx=15, pady=(5, 10))

        self.label_diagnostico = self.crear_linea(col_der, "Diagnóstico:")
        self.label_tratamiento = self.crear_linea(col_der, "Tratamiento:")
        self.label_observaciones = self.crear_linea(col_der, "Observaciones:")

        # --- Espacio visual y botón PDF ---
        ctk.CTkLabel(col_der, image=logo_img, text="").pack(pady=5)
        # --- Crear imagen y mostrarla ---
        logo_img = ctk.CTkImage(
            light_image=Image.open(logo),
            size=(100, 100)
        )

        ctk.CTkLabel(col_der, image=logo_img, text="").pack(pady=5)
        ctk.CTkButton(
            col_der,
            text="📄 Generar PDF",
            width=180,
            height=35,
            fg_color="#0D47A1",
            hover_color="transparent",
            font=("Roboto", 14, "bold"),
            command=self.generar_pdf
        ).pack(pady=(20, 10), anchor="center")

    def crear_linea(self, master, etiqueta, placeholder="_____________________________"):
        frame = ctk.CTkFrame(master, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(frame, text=etiqueta, width=120, anchor="w", font=("Roboto", 13),
                     text_color="#E0E0E0").pack(side="left")
        campo = ctk.CTkLabel(frame, text=placeholder, font=("Roboto", 13),
                             text_color="#E0E0E0")
        campo.pack(side="left", fill="x", expand=True)
        return campo

    def generar_pdf(self):
        print("📄 Generar PDF con:")
        print("- Cédula paciente:", self.cedula_paciente.get())
        print("- Cédula doctor:", self.cedula_doctor.get())
        print("- Fecha:", self.fecha.get())
        # Aquí puedes conectar tu lógica PDF personalizada


# Prueba independiente
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("950x600")
    app.title("Resumen Médico")
    ResumenFrame(app)
    app.mainloop()
