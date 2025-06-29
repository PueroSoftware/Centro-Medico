# import datetime
import os
from datetime import datetime
from tkinter import filedialog

import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage
from tkcalendar import DateEntry

from Ficheros.Pdf_Widget import GeneradorPDF
from Ficheros.custom_widgets import Marcos_P, Etiqueta_P, Entradas_P, Botones_P


class CitaFrame(Marcos_P):
    def __init__(self, master=None):
        super().__init__(master=master, fg_color="black")
        self.pack(fill="both", expand=True)

        # --- Rutas e imágenes ---
        ruta_raiz = os.path.dirname(__file__)
        ruta_principal = os.path.dirname(ruta_raiz)
        ruta_img = os.path.join(ruta_principal, "img")

        # ========== CONTENEDOR PRINCIPAL ==========
        contenedor = Marcos_P(master=self, fg_color="black")
        contenedor.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        contenedor.grid_columnconfigure(0, weight=3)  # panel izquierdo
        contenedor.grid_columnconfigure(1, weight=2)  # motivo + PDF
        contenedor.grid_rowconfigure(0, weight=1)  # cuerpo
        contenedor.grid_rowconfigure(1, weight=0)  # Botones abajo

        # ========== FORMULARIO (IZQUIERDA) ==========
        formulario = ctk.CTkScrollableFrame(contenedor, fg_color="#1F1F1F", corner_radius=10, width=200)
        formulario.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=5)
        formulario.grid_columnconfigure(0, weight=1)

        # --- Código Cita y Código Paciente ---
        Etiqueta_P(formulario, text="Código Cita:", font=("Roboto", 12)).pack(anchor="w", padx=10, pady=(10, 0))
        self.codigo_cita = Entradas_P(formulario)
        self.codigo_cita.pack(padx=10, fill="x")

        Etiqueta_P(formulario, text="Código Paciente:", font=("Roboto", 12)).pack(anchor="w", padx=10, pady=(10, 0))
        self.codigo_paciente = Entradas_P(formulario)
        self.codigo_paciente.pack(padx=10, fill="x")

        # --- Información del Paciente ---
        marco_info = Marcos_P(formulario, fg_color="#111111", border_color="white", border_width=1)
        marco_info.pack(fill="x", padx=10, pady=10)

        Etiqueta_P(marco_info, text="Información del Paciente:", font=("Roboto", 13, "bold")).pack(anchor="w", padx=10,
                                                                                                   pady=(5, 5))

        self.campos = {}
        for campo in ["Nombres:", "Apellidos:", "Cedula Id:"]:
            Etiqueta_P(marco_info, text=campo).pack(anchor="w", padx=10)
            entry = Entradas_P(marco_info)
            entry.pack(padx=10, pady=5, fill="x")
            self.campos[campo.strip(":")] = entry

        # --- Fecha y Hora Cita ---
        marco_fecha_hora = Marcos_P(formulario, fg_color="#111111", border_color="white", border_width=1)
        marco_fecha_hora.pack(fill="x", padx=10, pady=10)
        Etiqueta_P(marco_fecha_hora, text="Fecha Cita:", font=("Roboto", 12, "bold")).pack(anchor="w", padx=10,
                                                                                           pady=(5, 2))

        self.date_entry = DateEntry(marco_fecha_hora, date_pattern="yyyy-mm-dd", width=12, background='darkblue',
                                    foreground='white', borderwidth=2)
        self.date_entry.pack(padx=10, pady=(0, 10))
        self.date_entry.place(relx=0.5, rely=0.5, anchor="center")

        Etiqueta_P(marco_fecha_hora, text="Hora Cita:", font=("Roboto", 12, "bold")).pack(anchor="w", padx=10,
                                                                                          pady=(5, 2))

        frame_hora = ctk.CTkFrame(marco_fecha_hora, fg_color="transparent")
        frame_hora.pack(padx=10, pady=(0, 10), fill="x")

        self.hora_entry = Entradas_P(frame_hora, width=60)
        self.hora_entry.pack(side="left", padx=(0, 5))
        self.min_entry = Entradas_P(frame_hora, width=60)
        self.min_entry.pack(side="left")
        self.hora_entry.insert(0, "06")
        self.min_entry.insert(0, "00")

        # ========== PANEL DERECHO: MOTIVO Y PDF ==========
        panel_derecho = ctk.CTkFrame(contenedor, fg_color="#1F1F1F", corner_radius=10)
        panel_derecho.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=5)

        Etiqueta_P(panel_derecho, text="Motivo Cita", font=("Roboto", 14, "bold")).pack(padx=10, pady=10,
                                                                                        anchor="center")
        self.motivo_text = ctk.CTkTextbox(panel_derecho, width=600, height=300, fg_color="white", text_color="black",
                                          border_width=1)

        self.motivo_text.pack(padx=10, pady=(0, 10))

        # --- Ruta al ícono PDF ---
        ruta_icono_pdf = os.path.join(ruta_img, "pdf.png")

        try:
            self.icono_pdf = CTkImage(
                light_image=Image.open(ruta_icono_pdf),
                size=(120, 70)
            )

            self.botn_pdf = ctk.CTkButton(
                panel_derecho,
                image=self.icono_pdf,
                text="",
                width=130,
                height=80,
                fg_color="transparent",
                hover_color="#f0f0f0",
                command=self.exportar_pdf  # Esta función la defines más abajo
            )
            self.botn_pdf.pack(pady=(5, 10))

        except FileNotFoundError:
            self.icono_pdf = None
            print(f"⚠️ Advertencia: La imagen 'pdf.png' no se encontró en: {ruta_icono_pdf}")

        # ========== BOTONES INFERIORES ==========
        frame_botones = ctk.CTkFrame(contenedor, fg_color="black")
        frame_botones.grid(row=1, column=0, columnspan=2, pady=(10, 5), padx=10, sticky="ew")

        Botones_P(frame_botones, text="Guardar", width=150, command=self.guardar_datos).pack(side="left", padx=20)
        Botones_P(frame_botones, text="Limpiar", width=150, command=self.limpiar_campos).pack(side="left", padx=20)

    def guardar_datos(self):
        datos_cita = {
            "codigo_cita": self.codigo_cita.get(),
            "codigo_paciente": self.codigo_paciente.get(),
            "nombres": self.campos["Nombres"].get(),
            "apellidos": self.campos["Apellidos"].get(),
            "cedula_id": self.campos["Cedula Id"].get(),
            "fecha": self.date_entry.get(),
            "hora": f"{self.hora_entry.get()}:{self.min_entry.get()}",
            "motivo": self.motivo_text.get("1.0", "end").strip()
        }

        print("📋 Datos recopilados:")
        for clave, valor in datos_cita.items():
            print(f"{clave}: {valor}")

        # Guardar los datos para posterior uso (por ejemplo, exportar_pdf)
        self.datos_para_pdf = datos_cita

    def limpiar_campos(self):
        self.codigo_cita.delete(0, "end")
        self.codigo_paciente.delete(0, "end")
        self.motivo_text.delete("1.0", "end")

        for campo in self.campos.values():
            campo.delete(0, "end")

        self.hora_entry.delete(0, "end")
        self.hora_entry.insert(0, "06")
        self.min_entry.delete(0, "end")
        self.min_entry.insert(0, "00")
        self.date_entry.set_date(datetime.date.today())

        # Limpia datos temporales si existen
        if hasattr(self, "datos_para_pdf"):
            del self.datos_para_pdf

        # Opcional: enfocar en el primer campo
        self.codigo_cita.focus()

    def exportar_pdf(self):
        try:
            datos = self.datos_para_pdf
        except AttributeError:
            print("⚠️ Debes guardar los datos antes de exportar el PDF.")
            return

        archivo = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            title="Guardar cita como PDF"
        )

        if not archivo:
            return

        pdf = GeneradorPDF(datos, archivo)
        ruta_final = pdf.exportar()

        print(f"✅ PDF guardado exitosamente en: {ruta_final}")
