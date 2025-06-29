import customtkinter as ctk
from tkcalendar import DateEntry

from Ficheros.custom_widgets import Marcos_P, Etiqueta_P, Entradas_P, Botones_P

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class BoticaFrame(Marcos_P):
    def __init__(self, master=None):
        super().__init__(master=master, fg_color="#1F1F1F")
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        Etiqueta_P(
            self,
            text="💊 GESTIÓN DE BOTICA",
            font=("Roboto", 18, "bold"),
            text_color="#0D47A1"
        ).grid(row=0, column=0, pady=(10, 0))

        cont = Marcos_P(self, fg_color="#1F1F1F")
        cont.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 0))
        cont.grid_rowconfigure(0, weight=1)
        cont.grid_columnconfigure((0, 1), weight=1)

        # --- Ingreso a Bodega ---
        self.frame_ingreso = Marcos_P(cont, fg_color="black", width=400)
        self.frame_ingreso.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=5)
        self.frame_ingreso.grid_columnconfigure((0, 1), weight=1)

        Etiqueta_P(self.frame_ingreso, text="📦 Ingreso a Bodega", font=("Roboto", 16, "bold")) \
            .grid(row=0, column=0, columnspan=2, pady=(10, 10))

        campos_bodega = ["Código", "Nombre", "Presentación", "Laboratorio", "Cantidad"]
        self.campos_ingreso = {}

        for i, campo in enumerate(campos_bodega, start=1):
            Etiqueta_P(self.frame_ingreso, text=f"{campo}:") \
                .grid(row=i, column=0, sticky="e", padx=10, pady=4)
            entrada = Entradas_P(self.frame_ingreso)
            entrada.grid(row=i, column=1, sticky="ew", padx=10, pady=4)
            self.campos_ingreso[campo] = entrada

        Etiqueta_P(self.frame_ingreso, text="Fecha Caducidad:") \
            .grid(row=6, column=0, sticky="e", padx=10, pady=5)
        self.fecha_caducidad = DateEntry(self.frame_ingreso, date_pattern="yyyy-mm-dd")
        self.fecha_caducidad.grid(row=6, column=1, sticky="ew", padx=10, pady=5)

        Botones_P(
            self.frame_ingreso,
            text="Guardar en Bodega",
            command=self.guardar_bodega,
            width=160
        ).grid(row=7, column=0, columnspan=2, pady=10)

        # --- Entrega a Paciente ---
        self.frame_entrega = Marcos_P(cont, fg_color="black", width=500)
        self.frame_entrega.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=5)
        self.frame_entrega.grid_columnconfigure((0, 1), weight=1)

        Etiqueta_P(self.frame_entrega, text="🚚 Entrega a Paciente", font=("Roboto", 16, "bold")) \
            .grid(row=0, column=0, columnspan=2, pady=(10, 10))

        campos_entrega = ["Paciente", "Fecha", "Medicamento", "Cantidad"]
        self.campos_entrega = {}

        for i, campo in enumerate(campos_entrega, start=1):
            Etiqueta_P(self.frame_entrega, text=f"{campo}:") \
                .grid(row=i, column=0, sticky="e", padx=10, pady=4)
            entrada = Entradas_P(self.frame_entrega)
            entrada.grid(row=i, column=1, sticky="ew", padx=10, pady=4)
            self.campos_entrega[campo] = entrada

        Etiqueta_P(self.frame_entrega, text="Fecha Caducidad:") \
            .grid(row=5, column=0, sticky="e", padx=10, pady=5)
        self.fecha_caducidad_entrega = DateEntry(self.frame_entrega, date_pattern="yyyy-mm-dd")
        self.fecha_caducidad_entrega.grid(row=5, column=1, sticky="ew", padx=10, pady=5)

        # Caducado: Sí / No
        Etiqueta_P(self.frame_entrega, text="¿Producto Caducado?") \
            .grid(row=6, column=0, sticky="e", padx=10, pady=4)
        self.radio_caducado = ctk.StringVar(value="No")
        ctk.CTkRadioButton(self.frame_entrega, text="Sí", variable=self.radio_caducado, value="Sí") \
            .grid(row=6, column=1, sticky="w", padx=(10, 80))
        ctk.CTkRadioButton(self.frame_entrega, text="No", variable=self.radio_caducado, value="No") \
            .grid(row=6, column=1, sticky="e", padx=(80, 10))

        # Stock: Sí / No
        Etiqueta_P(self.frame_entrega, text="¿Stock Disponible?") \
            .grid(row=7, column=0, sticky="e", padx=10, pady=4)
        self.radio_stock = ctk.StringVar(value="Sí")
        ctk.CTkRadioButton(self.frame_entrega, text="Sí", variable=self.radio_stock, value="Sí") \
            .grid(row=7, column=1, sticky="w", padx=(10, 80))
        ctk.CTkRadioButton(self.frame_entrega, text="No", variable=self.radio_stock, value="No") \
            .grid(row=7, column=1, sticky="e", padx=(80, 10))

        # Botones en línea
        # --- Botones compactos centrados ---
        frame_botones_entrega = ctk.CTkFrame(self.frame_entrega, fg_color="transparent")
        frame_botones_entrega.grid(row=10, column=0, columnspan=2, pady=10)

        Botones_P(
            frame_botones_entrega,
            text="Agregar",
            command=self.agregar_medicamento,
            width=120
        ).pack(side="left", padx=10)

        Botones_P(
            frame_botones_entrega,
            text="Despachar",
            command=self.despachar_medicamentos,
            width=120
        ).pack(side="left", padx=10)

        # --- Descripción ---
        self.frame_descripcion = Marcos_P(self, fg_color="#1F1F1F", height=140)
        self.frame_descripcion.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.frame_descripcion.grid_columnconfigure(0, weight=1)

        Etiqueta_P(self.frame_descripcion, text="📖 Descripción del Medicamento", font=("Roboto", 14, "bold")) \
            .grid(row=0, column=0, pady=(10, 5))

        self.descripcion_txt = ctk.CTkTextbox(
            self.frame_descripcion,
            height=100,
            fg_color="#E0E0E0",
            text_color="black"
        )
        self.descripcion_txt.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

    # Funciones funcionales
    def guardar_bodega(self):
        datos = {k: v.get().strip() for k, v in self.campos_ingreso.items()}
        datos["Fecha Caducidad"] = self.fecha_caducidad.get_date().isoformat()
        print("📦 Guardando en bodega:", datos)

    def agregar_medicamento(self):
        datos = {k: v.get().strip() for k, v in self.campos_entrega.items()}
        datos["Fecha Caducidad"] = self.fecha_caducidad_entrega.get_date().isoformat()
        datos["Caducado"] = self.radio_caducado.get()
        datos["Stock"] = self.radio_stock.get()
        print("➕ Agregando medicamento:", datos)

    def despachar_medicamentos(self):
        print("🚚 Despachando medicamentos...")

    def mostrar_descripcion(self, nombre_medicamento):
        texto = (
            f"🧾 Medicamento: {nombre_medicamento}\n"
            f"💊 Composición: Paracetamol 500mg\n"
            f"📋 Dosis sugerida: 1 tableta cada 8 horas\n"
            f"📅 Vence: {self.fecha_caducidad_entrega.get_date().isoformat()}\n"
            f"🔍 Observaciones: No administrar con alcohol ni en ayunas prolongadas."
        )
        self.descripcion_txt.delete("1.0", "end")
        self.descripcion_txt.insert("1.0", texto)
