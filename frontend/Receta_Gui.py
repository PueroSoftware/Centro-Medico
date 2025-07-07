import os
from datetime import date
import customtkinter as ctk
from PIL import Image
from backend.Receta_Crud import RecetaCrud
from fichero.pdf_widget import GeneradorPdfRecetas

class ResumenFrame(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master, fg_color="#1F1F1F")
        self.pack(fill="both", expand=True)
        self.receta_crud = RecetaCrud()# Conecta con el Backend
        # Rutas
        ruta_raiz = os.path.dirname(__file__)
        ruta_principal = os.path.dirname(ruta_raiz)
        ruta_img = os.path.join(ruta_principal, "img")
        logo = os.path.join(ruta_img, "perfil.png")

        # --- Cabecera con dos botones ---
        cabecera = ctk.CTkFrame(self, fg_color="#1F1F1F")
        cabecera.pack(fill="x", padx=30, pady=(20, 0))

        ctk.CTkLabel(cabecera, text="🔎 Cédula Paciente:", font=("Roboto", 14),
                     text_color="#E0E0E0").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.cedula_paciente = ctk.CTkEntry(cabecera, placeholder_text="Ej: 0912345678")
        self.cedula_paciente.grid(row=0, column=1, padx=10, pady=5,sticky="w")

        # Botón Buscar
        ctk.CTkButton(cabecera, text="Buscar", command=self.buscar_paciente).grid(
            row=0, column=1, padx=5, pady=5)

        # Botón Generar PDF
        ctk.CTkButton(cabecera, text=" Generar PDF", command=self.generar_pdf).grid(
            row=0, column=3, padx=10, pady=5)

        # Ajustar columnas
        cabecera.grid_columnconfigure(1, weight=1)

        # --- Contenedor principal ---
        contenedor = ctk.CTkFrame(self, fg_color="#1F1F1F")
        contenedor.pack(fill="both", expand=True, padx=30, pady=20)

        col_izq = ctk.CTkFrame(contenedor, fg_color="#2C2C2C")
        col_der = ctk.CTkFrame(contenedor, fg_color="#2C2C2C")
        col_izq.pack(side="left", fill="both", expand=True, padx=(0, 10))
        col_der.pack(side="left", fill="both", expand=True, padx=(10, 0))

        # --- Columna izquierda ---
        ctk.CTkLabel(col_izq, text="👤 DATOS DEL PACIENTE", font=("Roboto", 18, "bold"),
                     text_color="#FFFFFF").pack(anchor="w", padx=15, pady=(5, 10))

        self.label_nombre = self.crear_linea(col_izq, "Nombre:")
        self.label_edad = self.crear_linea(col_izq, "Edad:")
        self.label_genero = self.crear_linea(col_izq, "Género:")
        self.label_cita = self.crear_linea(col_izq, "Fecha de Cita:")

        # Nueva línea: Fecha (debajo de Cita)
        self.label_fecha = self.crear_linea(col_izq, " Fecha Actual:")

        # --- Columna derecha ---
        ctk.CTkLabel(col_der, text="🩺 DETALLES CLÍNICOS", font=("Roboto", 18, "bold"),
                     text_color="#FFFFFF").pack(anchor="w", padx=15, pady=(5, 10))

        # Nueva línea: Especialidad (debajo del título)
        self.label_especialidad = self.crear_linea(col_der, "Especialidad:")

        self.label_diagnostico = self.crear_linea(col_der, "Diagnóstico:")
        self.label_tratamiento = self.crear_linea(col_der, "Tratamiento:")
        self.label_observaciones = self.crear_linea(col_der, "Observaciones:")

        # --- Logo ---
        logo_img = ctk.CTkImage(light_image=Image.open(logo), size=(100, 100))
        ctk.CTkLabel(col_der, image=logo_img, text="").pack(pady=5)

    def crear_linea(self, master, etiqueta, placeholder="__________________________"):
        frame = ctk.CTkFrame(master, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(frame, text=etiqueta, width=120, anchor="w",
                     font=("Roboto", 13), text_color="#E0E0E0").pack(side="left")
        campo = ctk.CTkLabel(frame, text=placeholder, font=("Roboto", 13),
                             text_color="#E0E0E0")
        campo.pack(side="left", fill="x", expand=True)
        return campo

    def buscar_paciente(self) :
        cedula = self.cedula_paciente.get().strip()
        resumen = self.receta_crud.obtener_resumen_completo(cedula)
        if resumen :
            self.label_nombre.configure(text=resumen.get("nombre_completo", "N/A"))
            self.label_edad.configure(text=str(resumen.get("edad", "N/A")))
            self.label_genero.configure(text=resumen.get("genero", "N/A"))
            self.label_cita.configure(text=resumen.get("fecha_cita", "N/A"))
            self.label_fecha.configure(text=str(date.today()))
            self.label_especialidad.configure(text=resumen.get("especialidad_doctor", "N/A"))
            self.label_diagnostico.configure(text=resumen.get("diagnostico", "N/A"))
            self.label_tratamiento.configure(text=resumen.get("tratamiento", "N/A"))
            self.label_observaciones.configure(text=resumen.get("observaciones", "N/A"))

        else :
            self.label_nombre.configure(text="No encontrado")
            self.label_edad.configure(text="N/A")
            self.label_genero.configure(text="N/A")
            self.label_cita.configure(text="N/A")
            self.label_fecha.configure(text="N/A")
            self.label_especialidad.configure(text="N/A")
            self.label_diagnostico.configure(text="N/A")
            self.label_tratamiento.configure(text="N/A")
            self.label_observaciones.configure(text="N/A")

    def generar_pdf(self) :
        cedula = self.cedula_paciente.get().strip()
        if not cedula :
            print("❌ Por favor ingrese una cédula")
            return

        resumen = self.receta_crud.obtener_resumen_completo(cedula)
        if resumen :
            ruta_pdf = self.receta_crud.generar_pdf(resumen, cedula)
            if ruta_pdf :
                # Opcional: abrir el PDF automáticamente
                if os.name == 'nt' :  # Windows
                    os.startfile(ruta_pdf)
                else :  # Mac/Linux
                    opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
                    subprocess.call([opener, ruta_pdf])
        else :
            print("❌ No se encontró paciente para generar PDF.")

# --- Prueba independiente ---
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("950x600")
    app.title("Resumen Médico")
    ResumenFrame(app)
    app.mainloop()
