import datetime
import tkinter.messagebox as msg
import customtkinter as ctk
from tkcalendar import DateEntry
from fichero.MapsView.map_widget import MapWidget
from fichero.custom_widgets import Marcos_P, Etiqueta_P, Entradas_P, Botones_P
from backend.Paciente_Crud import crear_paciente


class PacienteFrame(Marcos_P):
    def __init__(self, master=None):
        super().__init__(master=master, fg_color="#F8F8F8")
        self.pack(fill="both", expand=True)

        # CONTENEDOR GENERAL
        contenedor = Marcos_P(master=self, fg_color="#F8F8F8")
        contenedor.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        contenedor.grid_columnconfigure(0, weight=4) # manejo de ancho de Frame Izquiero
        contenedor.grid_columnconfigure(1, weight=1) # manejo de ancho de Frame Derecho
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

        # CAMPOS DE TEXTO
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

        # COMBOBOX PARA SEXO
        Etiqueta_P(frame_datos, text="Sexo:").pack(anchor="w", pady=(10, 5), padx=10)
        self.combo_sexo = ctk.CTkComboBox(
            master=frame_datos,
            values=["Masculino", "Femenino", "Agenero"],  # Valores del ENUM
            width=200
        )
        self.combo_sexo.set("Agenero")  # Valor por defecto
        self.combo_sexo.pack(padx=10, pady=(0, 10), fill="x")

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

        # BOTONES GUARDAR Y LIMPIAR
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

        # Callback para actualizar dirección desde el mapa
        self.mapa_widget.on_address_change(lambda addr: (
            self.entry_direccion.delete(0, ctk.END),
            self.entry_direccion.insert(0, addr)
        ))

    def guardar_paciente(self):
        """
        Toma datos del formulario, divide apellidos, lee sexo y fecha,
        y llama a Paciente.create() para guardar en la base.
        """
        # Sincroniza la dirección del mapa
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
        sexo = self.combo_sexo.get()  # Nuevo campo

        if not direccion:
            msg.showwarning("Dirección requerida", "⚠️ Debes seleccionar una dirección en el mapa antes de guardar.")
            return

        print("✅ Paciente guardado con:", {
            "cedula_id": cedula,
            "nombre": nombres,
            "apellido_paterno": apellido_paterno,
            "apellido_materno": apellido_materno,
            "fecha_nacimiento": fecha,
            "sexo": sexo,
            "email": email,
            "telefono": telefono,
            "direccion": direccion
        })

        crear_paciente(
        cedula_id=cedula,
        nombres=nombres,
        apellidos=apellidos_completos,
        fecha_nacimiento=fecha,
        sexo=sexo,
        email=email,
        telefono=telefono,
        direccion=direccion
        )

    def limpiar_campos(self):
        """Limpia campos de texto, fecha, dirección y mapa."""
        for campo in self.campos.values():
            campo.delete(0, "end")
        self.combo_sexo.set("Agenero")
        self.fecha_nacimiento.set_date(datetime.date.today())
        self.entry_direccion.delete(0, ctk.END)

        # Limpiar mapa: borrar entrada interna y marcador
        self.mapa_widget.address_entry.delete(0, ctk.END)
        if hasattr(self.mapa_widget, "marker") and self.mapa_widget.marker:
            self.mapa_widget.marker.delete()
            self.mapa_widget.marker = None
        # Recentrar mapa
        self.mapa_widget.map_widget.set_position(-2.170998, -79.922356)
        self.mapa_widget.map_widget.set_zoom(10)


# Ejecución directa para pruebas
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1000x600")
    app.title("Registro de Paciente")
    PacienteFrame(app)
    app.mainloop()
