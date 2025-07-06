from backend.Paciente_Crud import buscar_paciente_por_cedula
from backend.Cita_Crud import insertar_cita
from fichero.custom_widgets import Marcos_P, Etiqueta_P, Entradas_P, Botones_P
from fichero.pdf_widget import GeneradorPDF
from datetime import date
from tkinter import filedialog
import customtkinter as ctk
from tkcalendar import DateEntry
from backend.Doctor_Crud import obtener_especialidades_unicas

class CitaFrame(Marcos_P):
    def __init__(self, master=None):
        super().__init__(master=master, fg_color="black")
        self.pack(fill="both", expand=True)
        self.contador_turno = 1
        self.datos_para_pdf = None

        contenedor = Marcos_P(master=self, fg_color="black")
        contenedor.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        contenedor.grid_columnconfigure(0, weight=1)
        contenedor.grid_columnconfigure(1, weight=3)
        contenedor.grid_rowconfigure(0, weight=1)
        contenedor.grid_rowconfigure(1, weight=0)

        # Panel izquierdo
        formulario = ctk.CTkScrollableFrame(contenedor, fg_color="#1F1F1F", corner_radius=10, width=200)
        formulario.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=5)
        formulario.grid_columnconfigure(0, weight=1)

        Etiqueta_P(formulario, text="Citas Paciente:", text_color="white", font=("Roboto", 20, "bold")).pack(anchor="w", padx=10, pady=(5, 10))
        Etiqueta_P(formulario, text=" Cedula Id:", font=("Roboto", 12)).pack(anchor="w", padx=10, pady=(10, 0))
        self.cedula_usario = Entradas_P(formulario)
        self.cedula_usario.pack(padx=10, fill="x")
        Botones_P(formulario, text="Buscar paciente", width=120, command=self.buscar_paciente).pack(padx=10, pady=(5, 10))

        # Datos paciente
        marco_info = Marcos_P(formulario, fg_color="#111111", border_color="white", border_width=1)
        marco_info.pack(fill="x", padx=10, pady=10)
        Etiqueta_P(marco_info, text="Información del Paciente:", font=("Roboto", 13, "bold")).pack(anchor="w", padx=10, pady=(5, 5))

        self.campos = {}
        for campo in ["Nombres:", "Apellidos:"]:
            Etiqueta_P(marco_info, text=campo).pack(anchor="w", padx=10)
            entry = Entradas_P(marco_info)
            entry.pack(padx=10, pady=5, fill="x")
            self.campos[campo.strip(":")] = entry

        Etiqueta_P(formulario, text="Especialidad:", font=("Roboto", 12)).pack(anchor="w", padx=10, pady=(10, 0))
        especialidades = obtener_especialidades_unicas()
        self.combo_especialidad = ctk.CTkComboBox(
            formulario,
            values=especialidades,
            state="readonly"
        )
        #self.combo_especialidad = ctk.CTkComboBox(formulario, values=["Pediatría", "Cardiología", "Dermatología"], state="readonly")
        self.combo_especialidad.pack(padx=10, fill="x")

        # Fecha y hora
        marco_fecha_hora = Marcos_P(formulario, fg_color="#111111", border_color="white", border_width=1)
        marco_fecha_hora.pack(fill="x", padx=10, pady=10)
        Etiqueta_P(marco_fecha_hora, text="Fecha Cita:", font=("Roboto", 12, "bold")).pack(anchor="w", padx=10, pady=(5, 2))

        self.date_entry = DateEntry(marco_fecha_hora, date_pattern="yyyy-mm-dd", width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.pack(padx=(60, 10), pady=(0, 10))

        Etiqueta_P(marco_fecha_hora, text="Hora Cita:", font=("Roboto", 12, "bold")).pack(anchor="w", padx=10, pady=(5, 2))
        frame_hora = ctk.CTkFrame(marco_fecha_hora, fg_color="transparent")
        frame_hora.pack(padx=10, pady=(0, 10), fill="x")
        self.hora_entry = Entradas_P(frame_hora, width=60)
        self.hora_entry.pack(side="left", padx=(0, 5))
        self.min_entry = Entradas_P(frame_hora, width=60)
        self.min_entry.pack(side="left")
        self.hora_entry.insert(0, "06")
        self.min_entry.insert(0, "00")

        # Panel derecho
        panel_derecho = ctk.CTkFrame(contenedor, fg_color="#1F1F1F", corner_radius=10)
        panel_derecho.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=5)
        panel_derecho.grid_columnconfigure(0, weight=1)

        Etiqueta_P(panel_derecho, text="Motivo Cita", font=("Roboto", 14, "bold")).pack(pady=(10, 5))

        marco_derecho_interno = Marcos_P(panel_derecho, fg_color="#1F1F1F")
        marco_derecho_interno.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.motivo_text = ctk.CTkTextbox(marco_derecho_interno, height=200, fg_color="white", text_color="black", border_width=1)
        self.motivo_text.pack(fill="both", expand=True, pady=(0, 10))

        Etiqueta_P(marco_derecho_interno, text="Ticket-Turno", font=("Roboto", 16, "bold"), text_color="white").pack(anchor="w", pady=(5, 2))
        marco_ticket = Marcos_P(marco_derecho_interno, fg_color="#ffffff", width=400, height=160, border_color="white", border_width=2)
        marco_ticket.pack(anchor="w", pady=(0, 10), ipadx=10, ipady=10)

        self.ticket_label = Etiqueta_P(marco_ticket, text="---", text_color="black", font=("Courier New", 24, "bold"), anchor="center")
        self.ticket_label.pack(padx=10, pady=5)

        self.botn_pdf = ctk.CTkButton(panel_derecho, text="Exportar Pdf", width=120, height=40, command=self.exportar_pdf)
        self.botn_pdf.pack(pady=(5, 10))

        # Botones inferior
        frame_botones = ctk.CTkFrame(contenedor, fg_color="black")
        frame_botones.grid(row=1, column=0, columnspan=2, pady=(10, 5), padx=10, sticky="ew")
        Botones_P(frame_botones, text="Guardar", width=150, command=self.guardar_datos).pack(side="left", padx=20)
        Botones_P(frame_botones, text="Limpiar", width=150, command=self.limpiar_campos).pack(side="left", padx=20)

    def buscar_paciente(self):
        cedula = self.cedula_usario.get().strip()
        paciente = buscar_paciente_por_cedula(cedula)
        print(f"🧪 Paciente encontrado: {paciente}")  # Útil para depurar
        print("Contenido paciente['nombres']:", paciente['nombres'])

        if paciente :
            # Usamos .get() con fallback a "" por si algún valor es None
            nombre = paciente.get("nombres") or ""
            apellido_paterno = paciente.get("apellido_paterno") or ""
            apellido_materno = paciente.get("apellido_materno") or ""
            apellidos = f"{apellido_paterno} {apellido_materno}".strip()

            self.campos["Nombres"].delete(0, "end")
            self.campos["Nombres"].insert(0, nombre)

            self.campos["Apellidos"].delete(0, "end")
            self.campos["Apellidos"].insert(0, apellidos)

            print("✅ Paciente encontrado y datos cargados.")
        else :
            print(f"⚠️ Paciente con cédula {cedula} no encontrado.")

    def guardar_datos(self):
        turno_str = f"A{self.contador_turno:03}"
        self.ticket_label.configure(text=turno_str)

        cedula = self.cedula_usario.get().strip()
        especialidad = self.combo_especialidad.get()
        fecha = self.date_entry.get()
        hora = f"{self.hora_entry.get()}:{self.min_entry.get()}:00"  # formato TIME
        motivo_original = self.motivo_text.get("1.0", "end").strip()
        motivo = f"{motivo_original} (Turno: {turno_str})"

        resultado = insertar_cita(cedula, especialidad, fecha, hora, motivo)

        if resultado:
            print("✅ Cita guardada en la base de datos.")
            self.datos_para_pdf = {
                "id_paciente": cedula,
                "nombres": self.campos["Nombres"].get(),
                "apellidos": self.campos["Apellidos"].get(),
                "fecha": fecha,
                "hora": f"{self.hora_entry.get()}:{self.min_entry.get()}",
                "motivo": motivo,
                "turno": turno_str
            }
            self.contador_turno += 1
        else:
            print("❌ No se pudo guardar la cita.")

    def limpiar_campos(self):
        self.cedula_usario.delete(0, "end")
        self.motivo_text.delete("1.0", "end")
        for campo in self.campos.values():
            campo.delete(0, "end")
        self.hora_entry.delete(0, "end")
        self.hora_entry.insert(0, "06")
        self.min_entry.delete(0, "end")
        self.min_entry.insert(0, "00")
        self.date_entry.set_date(date.today())
        self.ticket_label.configure(text="---")
        self.datos_para_pdf = None

    def exportar_pdf(self):
        if not self.datos_para_pdf:
            print("⚠️ Primero debes guardar los datos.")
            return

        archivo = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            title="Guardar cita como PDF"
        )
        if not archivo:
            return

        pdf = GeneradorPDF(self.datos_para_pdf, archivo)
        ruta_final = pdf.exportar()
        print(f"✅ PDF generado en: {ruta_final}")
