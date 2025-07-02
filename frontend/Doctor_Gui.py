import customtkinter as ctk
from tkinter import ttk
from datetime import datetime, date, time
from fichero.custom_widgets import Entradas_P, Botones_P, Marcos_P
from backend.Doctor_Crud import *

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class DoctorGui(Marcos_P):
    def __init__(self, master=None):
        super().__init__(master=master,fg_color="#1F1F1F")
        self.grid(row=0,column=0,sticky="nsew")
        self.columnconfigure((0, 1),weight=1)
        self.rowconfigure(0,weight=1)

        # -------- FORMULARIO IZQUIERDO --------
        frame_form = Marcos_P(self, fg_color="#2A2A2A")
        frame_form.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        frame_form.columnconfigure((0, 1),weight=1)

        campos = ["Nombres", "Apellido Paterno", "Apellido Materno", "Cédula", "Email", "Teléfono"]
        self.entradas = {}
        for i, campo in enumerate(campos):
            ctk.CTkLabel(frame_form, text=f"{campo}:",text_color="white") \
                .grid(row=i, column=0, sticky="e",padx=5,pady=3)
            entry = Entradas_P(frame_form)
            entry.grid(row=i, column=1, sticky="ew",padx=5,pady=3)
            self.entradas[campo.lower().replace(" ", "_")] = entry

        ctk.CTkLabel(frame_form, text="Especialidad:",text_color="white") \
            .grid(row=6, column=0,sticky="e",padx=5,pady=3)


        # Crear combobox
        self.combo_especialidad = ttk.Combobox(frame_form, state="readonly")

        # Cargar especialidades desde la base de datos
        especialidades = obtener_especialidades()
        if especialidades :
            self.combo_especialidad['values'] = especialidades
            self.combo_especialidad.current(0)
        else :
            # Si no hay especialidades en DB, agregar una por defecto
            self.combo_especialidad['values'] = ["General"]
            self.combo_especialidad.current(0)

        self.combo_especialidad.grid(row=6, column=1, sticky="ew", padx=5, pady=3)

        # Entry + botón para registrar especialidad manual
        self.nueva_especialidad_entry = Entradas_P(frame_form)
        self.nueva_especialidad_entry.grid(row=7, column=0, sticky="ew", padx=5, pady=3)
        Botones_P(frame_form, text="Agregar Especialidad", width=140, command=self.registrar_especialidad, text_color="white") \
            .grid(row=7, column=1, sticky="ew", padx=5, pady=3)

        # Botones guardar y limpiar
        botones_frame = ctk.CTkFrame(frame_form, fg_color="transparent")
        botones_frame.grid(row=8, column=0, columnspan=2, pady=10)
        Botones_P(botones_frame, text="Guardar", width=120, command=self.guardar_doctor, text_color="white") \
            .pack(side="left", padx=10)
        Botones_P(botones_frame, text="Limpiar", width=120, command=self.limpiar_campos, text_color="white") \
            .pack(side="left", padx=10)

        # -------- PANEL DERECHO: INGRESO Y SALIDA --------
        panel_derecho = Marcos_P(self)
        panel_derecho.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        panel_derecho.rowconfigure((0, 1), weight=1)
        panel_derecho.columnconfigure(0, weight=1)

        # Ingreso
        self.frame_ingreso = self.crear_panel_movimiento(
            parent=panel_derecho,
            titulo="🟢 Ingreso Médico",
            color="#225E44",
            es_ingreso=True
        )
        # Salida
        self.frame_salida = self.crear_panel_movimiento(
            parent=panel_derecho,
            titulo="🔴 Salida Médico",
            color="#6C1F1F",
            es_ingreso=False
        )

    def crear_panel_movimiento(self, parent, titulo, color, es_ingreso):
        frame = Marcos_P(parent, fg_color=color)
        row = 0 if es_ingreso else 1
        frame.grid(row=row, column=0, sticky="nsew", pady=(0, 15) if es_ingreso else (15, 0), padx=10)
        frame.columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(frame, text=titulo, font=("Roboto", 16, "bold"), text_color="white") \
            .grid(row=0, column=0, columnspan=2, pady=5)

        ctk.CTkLabel(frame, text="Cédula:", text_color="white") \
            .grid(row=1, column=0, sticky="e", padx=5, pady=3)
        entrada_cedula = Entradas_P(frame, width=160)
        entrada_cedula.grid(row=1, column=1, sticky="w", padx=5, pady=3)

        ctk.CTkLabel(frame, text="Fecha y Hora actual:", text_color="white") \
            .grid(row=2, column=0, sticky="e", padx=5, pady=3)

        hora_label = ctk.CTkLabel(frame, text="", text_color="white")
        hora_label.grid(row=2, column=1, sticky="w", padx=5, pady=3)
        self.actualizar_reloj(hora_label)

        if es_ingreso:
            self.cedula_ingreso = entrada_cedula
            self.hora_ingreso_label = hora_label
            Botones_P(frame, text="Registrar Entrada", width=160, command=self.registrar_entrada, text_color="white") \
                .grid(row=3, column=0, columnspan=2, pady=6)
            Botones_P(frame, text="Limpiar", width=160, command=self.limpiar_entrada, text_color="white") \
                .grid(row=4, column=0, columnspan=2, pady=(0, 10))
        else:
            self.cedula_salida = entrada_cedula
            self.hora_salida_label = hora_label
            Botones_P(frame, text="Registrar Salida", width=160, command=self.registrar_salida, text_color="white") \
                .grid(row=3, column=0, columnspan=2, pady=6)
            Botones_P(frame, text="Limpiar", width=160, command=self.limpiar_salida, text_color="white") \
                .grid(row=4, column=0, columnspan=2, pady=(0, 10))

        return frame

    def actualizar_reloj(self, label):
        ahora = datetime.now()
        texto = ahora.strftime("%Y-%m-%d %H:%M:%S")
        label.configure(text=texto)
        label.after(1000, lambda: self.actualizar_reloj(label))

    # ------------ FUNCIONES ORIGINALES ------------
    def guardar_doctor(self) :
        # Tomar datos de las entradas del formulario
        datos = {k : v.get().strip() for k, v in self.entradas.items()}
        datos["especialidad"] = self.combo_especialidad.get()

        # Validar que no haya campos vacíos
        if not all(datos.values()) :
            print("⚠️ Completa todos los campos antes de guardar.")
            return

        # Llamar a la función del backend que inserta el doctor
        crear_doctor(
            cedula=datos["cédula"],
            nombres=datos["nombres"],
            ap_paterno=datos["apellido_paterno"],
            ap_materno=datos["apellido_materno"],
            especialidad=datos["especialidad"],
            email=datos["email"],
            telefono=datos["teléfono"]
        )

        print("✅ Doctor guardado correctamente desde la GUI.")

    ###############################################################################
    def limpiar_campos(self):
        for entrada in self.entradas.values():
            entrada.delete(0, 'end')
        self.combo_especialidad.set('')
        print(" Formulario limpiado.")

    #############################...REGISTRO HORA INGRESO...###################################
    def registrar_entrada(self) :
        cedula = self.cedula_ingreso.get().strip()
        fecha_hora = self.hora_ingreso_label.cget("text")  # texto automático del label
        if cedula :
            fecha_str, hora_str = fecha_hora.split(' ')
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()

            hora = datetime.strptime(hora_str, "%H:%M:%S").time()

            #  llamada real al backend
            registrar_entrada(cedula, fecha, hora)

            print(f" Entrada registrada en DB: {cedula} a las {fecha} {hora}")
        else :
            print("❌ Ingrese cédula para registrar ingreso.")

    #############################...REGISTRO HORA SALIDA...###################################
    def registrar_salida(self) :
        cedula = self.cedula_salida.get().strip()
        fecha_hora = self.hora_salida_label.cget("text")  # texto automático del label
        if cedula :
            fecha_str, hora_str = fecha_hora.split(' ')
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()

            hora = datetime.strptime(hora_str, "%H:%M:%S").time()

            #  llamada real al backend
            registrar_salida(cedula, fecha, hora)

            print(f"✅ Salida registrada en DB: {cedula} a las {fecha} {hora}")
        else :
            print("❌ Ingrese cédula para registrar salida.")

    ###############################################################################
    def limpiar_entrada(self):
        self.cedula_ingreso.delete(0, 'end')
        print(" Campos de ingreso limpiados.")

    def limpiar_salida(self):
        self.cedula_salida.delete(0, 'end')
        print(" Campos de salida limpiados.")

    def registrar_especialidad(self) :
        nueva = self.nueva_especialidad_entry.get().strip()
        if nueva :
            valores = list(self.combo_especialidad['values'])
            if nueva not in valores :
                # Guardar en la base de datos
                crear_especialidad(nueva)
                print(f"✅ Especialidad agregada a la DB: {nueva}")
            else :
                print(f"⚠️ La especialidad ya existe: {nueva}")

            # Recargar la lista desde la base de datos para actualizar el combobox
            especialidades_actualizadas = obtener_especialidades()
            self.combo_especialidad['values'] = especialidades_actualizadas
            self.combo_especialidad.set(nueva)  # Seleccionar la nueva especialidad en el combo
            self.nueva_especialidad_entry.delete(0, 'end')
        else :
            print("❌ Ingrese nombre de especialidad para agregar.")


if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1000x600")
    app.title("Doctor GUI – Registro Médico")
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=1)
    DoctorGui(app)
    app.mainloop()
