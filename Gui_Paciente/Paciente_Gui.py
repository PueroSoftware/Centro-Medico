import datetime
import tkinter.messagebox as msg

import customtkinter as ctk
from tkcalendar import DateEntry

from Ficheros.MapsView.map_widget import MapWidget
from Ficheros.custom_widgets import Marcos_P, Etiqueta_P, Entradas_P, Botones_P
from Gui_Paciente.Paciente_Crud import Paciente


class PacienteFrame(Marcos_P):
    def __init__(self, master=None):
        super().__init__(master=master, fg_color="#F8F8F8")
        self.pack(fill="both", expand=True)

        # CONTENEDOR GENERAL
        contenedor = Marcos_P(master=self, fg_color="#F8F8F8")
        contenedor.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        contenedor.grid_columnconfigure(0, weight=2)
        contenedor.grid_columnconfigure(1, weight=1)
        contenedor.grid_rowconfigure(0, weight=1)

        # MARCO IZQUIERDO
        frame_datos = ctk.CTkScrollableFrame(
            master=contenedor,
            fg_color="#1F1F1F",
            border_color="#444444",
            border_width=1
        )
        frame_datos.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        frame_datos.grid_columnconfigure(0, weight=1)

        Etiqueta_P(
            frame_datos,
            text="Registro de Paciente",
            font=("Roboto", 16, "bold")
        ).pack(pady=(10, 15), fill="x", padx=10)

        # CAMPOS
        self.campos = {}
        campos = [
            ("Nombres:", 200),
            ("Apellidos:", 200),
            ("Cédula Id:", 100),
            ("Email:", 200),
            ("Teléfono:", 100),

        ]

        for etiqueta, ancho in campos:
            Etiqueta_P(frame_datos, text=etiqueta).pack(anchor="w", pady=2, padx=10)
            entrada = Entradas_P(frame_datos, width=ancho)
            entrada.pack(pady=2, padx=10, fill="x")
            self.campos[etiqueta.strip(":")] = entrada

        # FECHA DE NACIMIENTO
        Etiqueta_P(frame_datos, text="Fecha de Nacimiento:").pack(anchor="w", pady=(10, 5), padx=10)
        self.fecha_nacimiento = DateEntry(
            master=frame_datos,
            date_pattern='yyyy-mm-dd',
            background="darkblue",
            foreground="white",
            borderwidth=2,
            width=18
        )
        self.fecha_nacimiento.pack(padx=10, pady=(0, 10), fill="x")

        # BOTONES
        f_botones = Marcos_P(master=frame_datos, fg_color="transparent")
        f_botones.pack(pady=10)
        Botones_P(f_botones, text="Guardar", command=self.guardar_paciente, width=100, height=32).pack(pady=(5, 10))
        Botones_P(f_botones, text="Limpiar", command=self.limpiar_campos, width=100, height=32).pack(pady=(0, 15))

        # MARCO DERECHO - MAPA
        frame_mapa = Marcos_P(
            master=contenedor,
            fg_color="#E6E6E6",
            border_width=1,
            border_color="#999999"
        )
        frame_mapa.grid(row=0, column=1, sticky="nsew")
        frame_mapa.grid_rowconfigure(1, weight=1)

        Etiqueta_P(frame_mapa, text="Mapa Referencial", font=("Roboto", 14, "bold")).pack(pady=(5, 0))

        self.mapa_widget = MapWidget(master=frame_mapa)
        self.mapa_widget.pack(fill="both", expand=True, padx=10, pady=(0, 5))

        Etiqueta_P(frame_mapa, text="Dirección:").pack(anchor="w", padx=10)
        self.entry_direccion = Entradas_P(frame_mapa, width=400)
        self.entry_direccion.pack(fill="x", padx=10, pady=(0, 10))

        # Callback para que el mapa actualize el campo de dirección automáticamente
        self.mapa_widget.on_address_change(lambda addr: (
            self.entry_direccion.delete(0, ctk.END),
            self.entry_direccion.insert(0, addr)
        ))

    def guardar_paciente(self):

        # Sincroniza la dirección desde el mapa antes de leer el campo
        if hasattr(self.mapa_widget, "address_entry"):
            direccion_mapa = self.mapa_widget.address_entry.get().strip()
            self.entry_direccion.delete(0, ctk.END)
            self.entry_direccion.insert(0, direccion_mapa)
            direccion = self.entry_direccion.get().strip()
        fecha = self.fecha_nacimiento.get_date()
        print("Fecha válida:", fecha.strftime("%Y-%m-%d"))

        nombres = self.campos["Nombres"].get().strip()
        apellidos_completos = self.campos["Apellidos"].get().strip()
        apellidos = apellidos_completos.split(" ", 1)
        apellido_paterno = apellidos[0]
        apellido_materno = apellidos[1] if len(apellidos) > 1 else ""

        cedula = self.campos["Cédula Id"].get().strip()
        email = self.campos["Email"].get().strip()
        telefono = self.campos["Teléfono"].get().strip()

        # Validación visual
        if not direccion:
            msg.showwarning("Dirección requerida", "⚠️ Debes seleccionar una dirección en el mapa antes de guardar.")
            return

        Paciente.create(
            cedula_id=cedula,
            nombre=nombres,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            fecha_nacimiento=fecha,
            email=email,
            telefono=telefono,
            direccion=direccion
        )
        print("✅ Paciente guardado con dirección:", direccion)

    def limpiar_campos(self):
        # Campos de texto
        for campo in self.campos.values():
            campo.delete(0, "end")

        # Fecha
        self.fecha_nacimiento.set_date(datetime.date.today())
        # Dirección del formulario
        self.entry_direccion.delete(0, ctk.END)
        # Limpiar MapWidget
        # 1) borrar entrada interna
        self.mapa_widget.address_entry.delete(0, ctk.END)
        # 2) eliminar marcador si existe
        if hasattr(self.mapa_widget, "marker") and self.mapa_widget.marker:
            self.mapa_widget.marker.delete()
            self.mapa_widget.marker = None

        # 3) reset ear position y zoom
        self.mapa_widget.map_widget.set_position(-2.170998, -79.922356)
        self.mapa_widget.map_widget.set_zoom(10)
