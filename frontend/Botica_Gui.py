import customtkinter
import datetime
from tkcalendar import DateEntry
from fichero.custom_widgets import Entradas_P, Botones_P, Etiqueta_P, Marcos_P
from backend.Bodega_Crud import generar_sku, crear_farmaco, listar_presentaciones, listar_farmacos
from backend.Despacho_Crud import crear_despacho


class BoticaFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.Despacho_Crud = crear_despacho()
        self.carrito_despacho = []
        self.nombre_a_id_farmaco = {}

        # Contenedor general
        cont = customtkinter.CTkFrame(self)
        cont.pack(fill="both", expand=True)
        cont.grid_columnconfigure((0, 1), weight=1)
        cont.grid_rowconfigure(0, weight=1)

        # ----- FRAME IZQUIERDO: BODEGA -----
        frame_izq = Marcos_P(cont, fg_color="#2A2A2A")
        frame_izq.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        frame_izq.grid_columnconfigure((0, 1), weight=1)
        frame_izq.grid_rowconfigure(7, weight=1)

        Etiqueta_P(frame_izq, text="Código SKU:", text_color="white").grid(row=0, column=0, sticky="w")
        self.sku = Entradas_P(frame_izq)
        self.sku.insert(0, generar_sku())
        self.sku.configure(state="readonly")
        self.sku.grid(row=0, column=1, pady=4, padx=10)

        self.campos_ingreso = {}
        for i, campo in enumerate(["Nombre", "Laboratorio", "Cantidad"], start=1):
            Etiqueta_P(frame_izq, text=f"{campo}:", text_color="white").grid(row=i, column=0, sticky="w")
            entrada = Entradas_P(frame_izq)
            entrada.grid(row=i, column=1, pady=4, padx=10)
            self.campos_ingreso[campo] = entrada

        Etiqueta_P(frame_izq, text="Presentación:", text_color="white").grid(row=4, column=0, sticky="w")
        presentaciones = listar_presentaciones() or ["N/A"]
        self.presentacion_cb = customtkinter.CTkComboBox(frame_izq, values=presentaciones)
        self.presentacion_cb.grid(row=4, column=1, padx=10, pady=4)

        Etiqueta_P(frame_izq, text="Fecha Producción:", text_color="white").grid(row=5, column=0, sticky="w")
        self.fecha_caducidad = DateEntry(frame_izq, date_pattern="yyyy-mm-dd")
        self.fecha_caducidad.grid(row=5, column=1, padx=10, pady=4)

        btn_frame_izq = customtkinter.CTkFrame(frame_izq, fg_color="transparent")
        btn_frame_izq.grid(row=6, column=0, columnspan=2, pady=8)
        Botones_P(btn_frame_izq, text="Guardar en Bodega", command=self.guardar_bodega).pack(side="left", padx=5)
        Botones_P(btn_frame_izq, text="Limpiar", command=self.limpiar_formulario).pack(side="left", padx=5)

        self.description_txt = Etiqueta_P(
            frame_izq, text="Aquí aparecerá el estado...", wraplength=300, text_color="gray"
        )
        self.description_txt.grid(row=7, column=0, columnspan=2, sticky="nsew", padx=10, pady=(10, 0))

        # ----- FRAME DERECHO: DESPACHO -----
        frame_der = Marcos_P(cont, fg_color="#2A2A2A")
        frame_der.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        frame_der.grid_columnconfigure((0, 1), weight=1)
        frame_der.grid_rowconfigure(6, weight=1)

        Etiqueta_P(frame_der, text="Cédula Paciente:", text_color="white").grid(row=0, column=0, sticky="w")
        subframe_cedula = customtkinter.CTkFrame(frame_der, fg_color="transparent")
        subframe_cedula.grid(row=0, column=1, sticky="ew", pady=4, padx=5)
        self.cedula_paciente = Entradas_P(subframe_cedula)
        self.cedula_paciente.pack(side="left", fill="x", expand=True)
        Botones_P(subframe_cedula, text="Buscar", command=self.buscar_paciente).pack(side="left", padx=5)

        Etiqueta_P(frame_der, text="Fecha:", text_color="white").grid(row=1, column=0, sticky="w")
        self.fecha_actual = Entradas_P(frame_der)
        self.fecha_actual.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))
        self.fecha_actual.grid(row=1, column=1, pady=4, padx=10)

        Etiqueta_P(frame_der, text="Medicamento:", text_color="white").grid(row=2, column=0, sticky="w")
        self.medicamento_cb = customtkinter.CTkComboBox(frame_der, values=[], command=self.actualizar_info_medicamento)
        self.medicamento_cb.grid(row=2, column=1, pady=4, padx=10)

        Etiqueta_P(frame_der, text="Stock disponible:", text_color="white").grid(row=3, column=0, sticky="w")
        self.stock_disponible = Entradas_P(frame_der, state="readonly")
        self.stock_disponible.grid(row=3, column=1, pady=4, padx=10)

        Etiqueta_P(frame_der, text="Fecha caducidad:", text_color="white").grid(row=4, column=0, sticky="w")
        self.fecha_caducidad_info = Entradas_P(frame_der, state="readonly")
        self.fecha_caducidad_info.grid(row=4, column=1, pady=4, padx=10)

        Etiqueta_P(frame_der, text="Cantidad:", text_color="white").grid(row=5, column=0, sticky="w")
        self.cantidad_entrega = Entradas_P(frame_der)
        self.cantidad_entrega.grid(row=5, column=1, pady=4, padx=10)

        btn_frame_der = customtkinter.CTkFrame(frame_der, fg_color="transparent")
        btn_frame_der.grid(row=6, column=0, columnspan=2, pady=6)
        Botones_P(btn_frame_der, text="Agregar", command=self.agregar_medicamento).pack(side="left", padx=5)
        Botones_P(btn_frame_der, text="Despachar", command=self.despachar).pack(side="left", padx=5)
        Botones_P(btn_frame_der, text="Limpiar", command=self.limpiar_entrega).pack(side="left", padx=5)

        self.descripcion_txt = Etiqueta_P(
            frame_der, text="Carrito vacío...", wraplength=300, text_color="gray"
        )
        self.descripcion_txt.grid(row=7, column=0, columnspan=2, sticky="nsew", padx=10, pady=(10, 0))

        # Cargar lista de medicamentos
        self.cargar_medicamentos()

    # ----- MÉTODOS BODEGA -----
    def guardar_bodega(self):
        try:
            datos = {
                "codigo_farmaco": self.sku.get().strip(),
                "nombre_farmaco": self.campos_ingreso["Nombre"].get().strip(),
                "laboratorio": self.campos_ingreso["Laboratorio"].get().strip(),
                "presentacion": self.presentacion_cb.get().strip(),
                "stock_actual": int(self.campos_ingreso["Cantidad"].get().strip()),
                "fecha_caducidad": self.fecha_caducidad.get_date().isoformat()
            }
            crear_farmaco(datos)
            self.description_txt.configure(text="✅ Medicamento guardado correctamente.", text_color="green")
            self.after(3000, lambda: self.description_txt.configure(text=""))
            self.limpiar_formulario()
            self.cargar_medicamentos()
            self.sku.configure(state="normal")
            self.sku.delete(0, "end")
            self.sku.insert(0, generar_sku())
            self.sku.configure(state="readonly")
        except Exception as e:
            self.description_txt.configure(text=f"❌ Error: {e}", text_color="red")

    def limpiar_formulario(self):
        self.sku.configure(state="normal")
        self.sku.delete(0, "end")
        self.sku.insert(0, generar_sku())
        self.sku.configure(state="readonly")
        for entrada in self.campos_ingreso.values():
            entrada.delete(0, "end")
        self.presentacion_cb.set("")
        self.fecha_caducidad.set_date(datetime.date.today())

    # ----- MÉTODOS DESPACHO -----
    def buscar_paciente(self):
        cedula = self.cedula_paciente.get().strip()
        datos = self.Despacho_Crud.buscar_paciente_por_cedula(cedula)
        if datos:
            self.descripcion_txt.configure(
                text=f"✅ Paciente: {datos['nombres']} {datos['apellido_paterno']} {datos['apellido_materno']}",
                text_color="green"
            )
        else:
            self.descripcion_txt.configure(text="❌ Paciente no encontrado", text_color="red")

    def actualizar_info_medicamento(self, selected_nombre):
        farmacos = listar_farmacos()
        for f in farmacos:
            if f["nombre_farmaco"] == selected_nombre:
                self.stock_disponible.configure(state="normal")
                self.stock_disponible.delete(0, "end")
                self.stock_disponible.insert(0, str(f["stock_actual"]))
                self.stock_disponible.configure(state="readonly")
                self.fecha_caducidad_info.configure(state="normal")
                self.fecha_caducidad_info.delete(0, "end")
                self.fecha_caducidad_info.insert(0, f["fecha_caducidad"])
                self.fecha_caducidad_info.configure(state="readonly")
                break

    def agregar_medicamento(self):
        cedula = self.cedula_paciente.get().strip()
        medicamento = self.medicamento_cb.get().strip()
        cantidad = self.cantidad_entrega.get().strip()
        if not cedula or not medicamento or not cantidad:
            self.descripcion_txt.configure(text="❌ Completa todos los campos", text_color="red")
            return
        self.carrito_despacho.append({"cedula": cedula, "medicamento": medicamento, "cantidad": int(cantidad)})
        resumen = "\n".join(f"{i+1}. {itm['medicamento']} x{itm['cantidad']} (Cédula: {itm['cedula']})"
                            for i, itm in enumerate(self.carrito_despacho))
        self.descripcion_txt.configure(text=resumen, text_color="green")

    def despachar(self):
        try:
            cedula = self.cedula_paciente.get().strip()
            nombre_farmaco = self.medicamento_cb.get().strip()
            cantidad = int(self.cantidad_entrega.get().strip())
            fecha_despacho = datetime.datetime.now().strftime("%Y-%m-%d")
            if nombre_farmaco not in self.nombre_a_id_farmaco:
                self.descripcion_txt.configure(text="❌ Selecciona un medicamento válido.", text_color="red")
                return
            id_farmaco = self.nombre_a_id_farmaco[nombre_farmaco]
            ok, mensaje = self.Despacho_Crud.registrar_despacho(cedula, id_farmaco, cantidad, fecha_despacho)
            if ok:
                self.descripcion_txt.configure(text=f"✅ {mensaje}", text_color="green")
                self.cargar_medicamentos()
                self.limpiar_entrega()
            else:
                self.descripcion_txt.configure(text=f"❌ {mensaje}", text_color="red")
        except Exception as e:
            self.descripcion_txt.configure(text=f"❌ Error al despachar: {e}", text_color="red")

    def limpiar_entrega(self):
        self.cedula_paciente.delete(0, "end")
        self.medicamento_cb.set("")
        self.cantidad_entrega.delete(0, "end")
        self.stock_disponible.configure(state="normal")
        self.stock_disponible.delete(0, "end")
        self.stock_disponible.configure(state="readonly")
        self.fecha_caducidad_info.configure(state="normal")
        self.fecha_caducidad_info.delete(0, "end")
        self.fecha_caducidad_info.configure(state="readonly")
        self.descripcion_txt.configure(text="Carrito vacío...", text_color="gray")
        self.carrito_despacho.clear()

    def cargar_medicamentos(self):
        farmacos = self.Despacho_Crud.lista_farmacos()
        nombres = []
        self.nombre_a_id_farmaco.clear()
        for f in farmacos:
            self.nombre_a_id_farmaco[f["nombre_farmaco"]] = f["id_farmaco"]
            nombres.append(f["nombre_farmaco"])
        self.medicamento_cb.configure(values=nombres)
