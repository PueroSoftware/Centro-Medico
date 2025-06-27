import customtkinter as ctk
import datetime
from Ficheros.custom_widgets import Marcos_P, Etiqueta_P, Entradas_P, Botones_P

class DoctorFrame(Marcos_P) :
    def __init__(self, master=None) :
        super().__init__(master=master, fg_color="#F8F8F8")
        self.pack(fill="both", expand=True)

        # ====================== CONTENEDOR GENERAL ======================
        contenedor = Marcos_P(master=self, fg_color="#F8F8F8")
        contenedor.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ============ CONFIGURACIÓN DE PROPORCIONES MEJORADAS ============
        contenedor.grid_columnconfigure(0, weight=1)  # Frame izquierdo - Formulario (40%)
        contenedor.grid_columnconfigure(1, weight=3)  # Frame derecho - Horarios (40% - más pequeño)
        contenedor.grid_rowconfigure(0, weight=1)
        contenedor.grid_rowconfigure(1, weight=0)  # Fila para botones (altura fija)

        # ================ MARCO IZQUIERDO - FORMULARIO DOCTOR ================
        frame_datos = ctk.CTkScrollableFrame(
            master=contenedor,
            fg_color="#1F1F1F",
            border_color="#444444",
            border_width=1,
            corner_radius=10
        )
        frame_datos.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        frame_datos.grid_columnconfigure(0, weight=1)

        # ==================== TÍTULO DEL FORMULARIO ====================
        Etiqueta_P(
            frame_datos,
            text="👨‍⚕️ REGISTRO DE DOCTOR",
            font=("Roboto", 16, "bold")
        ).pack(pady=(15, 20), fill="x", padx=15)

        # ======================= CAMPOS DEL DOCTOR =======================
        self.campos = {}
        campos = [
            ("Nombres:", 280),
            ("Apellidos:", 280),
            ("Cédula Id:", 200),
            ("Email:", 280),
            ("Teléfono:", 200),
            ("Especialidad:", 280)
        ]

        for etiqueta, ancho in campos :
            Etiqueta_P(frame_datos, text=etiqueta, font=("Roboto", 11)).pack(anchor="w", pady=(8, 2), padx=15)
            entrada = Entradas_P(frame_datos, width=ancho, height=32)
            entrada.pack(pady=(0, 8), padx=15, fill="x")
            self.campos[etiqueta.strip(":")] = entrada

        # ============== MARCO DERECHO - PANEL DE HORARIOS (MÁS COMPACTO) ==============
        frame_horario = ctk.CTkScrollableFrame(
            master=contenedor,
            fg_color="#2B2B2B",
            border_width=1,
            border_color="#555555",
            corner_radius=10
        )
        frame_horario.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        frame_horario.grid_columnconfigure(0, weight=1)
        frame_horario.grid_rowconfigure(3, weight=1)  # Para que el área de configuración se expanda

        # ==================== TÍTULO DEL PANEL HORARIOS ====================
        ctk.CTkLabel(
            frame_horario,
            text="⏰ HORARIOS MÉDICOS",
            font=("Roboto", 16, "bold"),
            text_color="white"
        ).grid(row=0, column=0, pady=(15, 10), sticky="ew")

        # ================ FECHA ACTUAL DEL SISTEMA (SIEMPRE VISIBLE) ================
        fecha_frame = ctk.CTkFrame(frame_horario, fg_color="#1a1a1a", corner_radius=6)
        fecha_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 8))

        # Obtener fecha actual del sistema
        self.fecha_actual = datetime.datetime.now()

        ctk.CTkLabel(
            fecha_frame,
            text="📅 FECHA ACTUAL",
            font=("Roboto", 12, "bold"),
            text_color="white"
        ).pack(pady=(8, 2))

        self.label_fecha_sistema = ctk.CTkLabel(
            fecha_frame,
            text=f"{self.fecha_actual.strftime('%A, %d de %B del %Y')}",
            font=("Roboto", 11),
            text_color="#4CAF50"
        )
        self.label_fecha_sistema.pack(pady=(0, 8))

        # ================ SECCIÓN INFORMACIÓN ACTUAL ================
        info_frame = ctk.CTkFrame(frame_horario, fg_color="#333333", corner_radius=6)
        info_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 8))

        ctk.CTkLabel(
            info_frame,
            text="📋 ESTADO ACTUAL",
            font=("Roboto", 12, "bold"),
            text_color="white"
        ).pack(pady=(8, 3))

        # Labels para mostrar horarios actuales (más compactos)
        self.label_entrada = ctk.CTkLabel(
            info_frame,
            text="🟢 Entrada: No configurado",
            font=("Roboto", 15),
            text_color="gray"
        )
        self.label_entrada.pack(pady=1)

        self.label_salida = ctk.CTkLabel(
            info_frame,
            text="🔴 Salida: No configurado",
            font=("Roboto", 15),
            text_color="gray"
        )
        self.label_salida.pack(pady=1)

        self.label_resumen = ctk.CTkLabel(
            info_frame,
            text="⏱️ Configure los horarios",
            font=("Roboto", 9),
            text_color="gray",
            justify="center"
        )
        self.label_resumen.pack(pady=(2, 8))

        # ================ ÁREA DE CONFIGURACIÓN DE HORARIOS (COMPACTA) ================
        config_frame = ctk.CTkFrame(frame_horario, fg_color="#444444", corner_radius=6)
        config_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=(0, 10))
        config_frame.grid_columnconfigure(0, weight=1)
        config_frame.grid_columnconfigure(1, weight=1)

        # ================ COLUMNA IZQUIERDA - HORARIO ENTRADA ================
        entrada_container = ctk.CTkFrame(config_frame, fg_color="#1a4c96", corner_radius=6)# El .grid()esta bien
        entrada_container.grid(row=0, column=0, sticky="nsew", padx=(8, 4), pady=8)
        entrada_container.grid_columnconfigure(0, weight=1)# Hacemos que la columna interna se expanda
        ctk.CTkLabel(
            entrada_container,
            text="🟢 ENTRADA",
            font=("Roboto", 14, "bold"),
            text_color="white"
        ).pack(pady=(10, 5),fill="x",padx=10) # Añadido fill y padx

        # Selectores más compactos para entrada
        ctk.CTkLabel(entrada_container, text="Fecha:", font=("Roboto", 12), text_color="white").pack()
        # Etiqueta para mostrar la fecha actual fija
        self.label_fecha_fija_entrada = ctk.CTkLabel(
            entrada_container,
            text=self.fecha_actual.strftime("%d/%m/%Y"),  # Formato DÍA/MES/AÑO
            font=("Roboto", 12, "bold"),
            text_color="#87CEEB"  # Un color cian claro para destacar
        )
        self.label_fecha_fija_entrada.pack(pady=(2, 10))

        ctk.CTkLabel(entrada_container, text="Hora:", font=("Roboto", 12), text_color="white").pack()
        self.hora_entrada = ctk.CTkOptionMenu(
            entrada_container,
            values=[f"{h:02d}:00" for h in range(6, 24)],
            width=100
        )
        self.hora_entrada.set("08:00")
        self.hora_entrada.pack(pady=2)

        ctk.CTkLabel(entrada_container, text="Min:", font=("Roboto", 12), text_color="white").pack()
        self.min_entrada = ctk.CTkOptionMenu(
            entrada_container,
            values=["00", "15", "30", "45"],
            width=100
        )
        self.min_entrada.set("00")
        self.min_entrada.pack(pady=2)

        btn_entrada = ctk.CTkButton(
            entrada_container,
            text="✅ Aplicar",
            command=self.aplicar_horario_entrada,
            width=90,
            height=28,
            font=("Roboto", 12)
        )
        btn_entrada.pack(pady=(8, 10))

        # ================ COLUMNA DERECHA - HORARIO SALIDA ================
        salida_container = ctk.CTkFrame(config_frame, fg_color="#961a1a", corner_radius=6)
        salida_container.grid(row=0, column=1, sticky="nsew", padx=(4, 8), pady=8)

        ctk.CTkLabel(
            salida_container,
            text="🔴 SALIDA",
            font=("Roboto", 11, "bold"),
            text_color="white"
        ).pack(pady=(10, 5))

        # Selectores más compactos para salida
        ctk.CTkLabel(salida_container, text="Fecha:", font=("Roboto", 9), text_color="white").pack()
        # Etiqueta para mostrar la fecha actual fija
        self.label_fecha_fija_salida = ctk.CTkLabel(
            salida_container,
            text=self.fecha_actual.strftime("%d/%m/%Y"),  # Formato DÍA/MES/AÑO
            font=("Roboto", 12, "bold"),
            text_color="#87CEEB"  # Un color cian claro para destacar
        )
        self.label_fecha_fija_salida.pack(pady=(2, 10))

        ctk.CTkLabel(salida_container, text="Hora:", font=("Roboto", 9), text_color="white").pack()
        self.hora_salida = ctk.CTkOptionMenu(
            salida_container,
            values=[f"{h:02d}:00" for h in range(6, 24)],
            width=100
        )
        self.hora_salida.set("17:00")
        self.hora_salida.pack(pady=2)

        ctk.CTkLabel(salida_container, text="Min:", font=("Roboto", 9), text_color="white").pack()
        self.min_salida = ctk.CTkOptionMenu(
            salida_container,
            values=["00", "15", "30", "45"],
            width=100
        )
        self.min_salida.set("00")
        self.min_salida.pack(pady=2)

        btn_salida = ctk.CTkButton(
            salida_container,
            text="✅ Aplicar",
            command=self.aplicar_horario_salida,
            width=90,
            height=28,
            font=("Roboto", 12)
        )
        btn_salida.pack(pady=(8, 10))


        # ================ VARIABLES PARA ALMACENAR HORARIOS ================
        self.horario_entrada = None
        self.horario_salida = None


        # ===================== MARCO BOTONES INFERIORES =====================
        frame_btn = ctk.CTkFrame(
            master=contenedor,
            fg_color="transparent"
        )
        frame_btn.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(15, 0))


        # ============ CONFIGURACIÓN DE GRID PARA CENTRAR BOTONES ============
        frame_btn.grid_columnconfigure(0, weight=1)
        frame_btn.grid_columnconfigure(1, weight=0)
        frame_btn.grid_columnconfigure(2, weight=0)
        frame_btn.grid_columnconfigure(3, weight=1)

        # ======================= BOTONES PRINCIPALES =======================
        Botones_P(
            frame_btn,
            text="💾 Guardar Doctor",
            command=self.guardar_datos,
            width=160,
            height=40
        ).grid(row=0, column=1, padx=(0, 15), pady=15)

        Botones_P(
            frame_btn,
            text="🧹 Limpiar Todo",
            command=self.limpiar_campos,
            width=140,
            height=40
        ).grid(row=0, column=2, padx=(15, 0), pady=15)

        # Actualizar fecha cada minuto
        self.actualizar_fecha_sistema()

    # ================ FUNCIÓN PARA ACTUALIZAR FECHA DEL SISTEMA ================
    def actualizar_fecha_sistema(self) :
        """Actualiza la fecha actual del sistema cada minuto"""
        self.fecha_actual = datetime.datetime.now()

        # Formatear fecha en español
        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                 "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

        dia_semana = dias_semana[self.fecha_actual.weekday()]
        mes = meses[self.fecha_actual.month - 1]

        fecha_formateada = f"{dia_semana}, {self.fecha_actual.day} de {mes} del {self.fecha_actual.year}"

        self.label_fecha_sistema.configure(text=fecha_formateada)

        # Programar próxima actualización en 60 segundos
        self.after(60000, self.actualizar_fecha_sistema)

    # ================ FUNCIÓN PARA APLICAR HORARIO DE ENTRADA ================
    def aplicar_horario_entrada(self) :
        """Aplica el horario de entrada seleccionado"""
        try :
            fecha_base = self.fecha_actual
            hora = self.hora_entrada.get()
            minuto = self.min_entrada.get()

            # Crear datetime completo
            self.horario_entrada = fecha_base.replace(
                hour=int(hora.split(':')[0]),
                minute=int(minuto),
                second=0,
                microsecond=0
            )

            # Actualizar label
            self.label_entrada.configure(
                text=f"🟢 Entrada: {hora}:{minuto}",
                text_color="#4CAF50"
            )

            # Actualizar resumen
            self.actualizar_resumen()

            print(f"✅ Horario de entrada: {self.horario_entrada.strftime('%Y-%m-%d %H:%M')}")

        except Exception as e :
            print(f"❌ Error aplicando horario de entrada: {e}")
            self.label_entrada.configure(
                text="❌ Error configurando entrada",
                text_color="#F44336"
            )

    # ================ FUNCIÓN PARA APLICAR HORARIO DE SALIDA ================
    def aplicar_horario_salida(self) :
        """Aplica el horario de salida seleccionado"""
        try :
            fecha_base = self.fecha_actual
            hora = self.hora_salida.get()
            minuto = self.min_salida.get()

            # Crear datetime completo
            self.horario_salida = fecha_base.replace(
                hour=int(hora.split(':')[0]),
                minute=int(minuto),
                second=0,
                microsecond=0
            )

            # Actualizar label
            self.label_salida.configure(
                text=f"🔴 Salida: {hora}:{minuto}",
                text_color="#F44336"
            )

            # Actualizar resumen
            self.actualizar_resumen()

            print(f"✅ Horario de salida: {self.horario_salida.strftime('%Y-%m-%d %H:%M')}")

        except Exception as e :
            print(f"❌ Error aplicando horario de salida: {e}")
            self.label_salida.configure(
                text="❌ Error configurando salida",
                text_color="#F44336"
            )

    # ================ FUNCIÓN PARA ACTUALIZAR RESUMEN ================
    def actualizar_resumen(self) :
        """Actualiza el resumen de horarios"""
        if self.horario_entrada and self.horario_salida :
            # Calcular duración
            duracion = self.horario_salida - self.horario_entrada

            if duracion.total_seconds() > 0 :
                dias = duracion.days
                horas = duracion.total_seconds() / 3600

                if dias > 0 :
                    texto_resumen = f"⏱️ {dias}d {horas:.1f}h total\n✅ Configuración válida"
                else :
                    texto_resumen = f"⏱️ {horas:.1f} horas\n✅ Jornada del día"
                color = "#4CAF50"  # Verde
            else :
                texto_resumen = "⚠️ ERROR: Salida antes que entrada"
                color = "#F44336"  # Rojo

        elif self.horario_entrada :
            texto_resumen = "🟢 Entrada OK\n⚠️ Falta salida"
            color = "#FF9800"  # Naranja

        elif self.horario_salida :
            texto_resumen = "🔴 Salida OK\n⚠️ Falta entrada"
            color = "#FF9800"  # Naranja

        else :
            texto_resumen = "⏱️ Configure los horarios"
            color = "gray"

        self.label_resumen.configure(text=texto_resumen, text_color=color)

    # ================ FUNCIÓN PARA GUARDAR DATOS DEL DOCTOR ================
    def guardar_datos(self) :
        try :
            # ================ OBTENER DATOS DEL FORMULARIO ================
            nombres = self.campos["Nombres"].get().strip()
            apellidos_completos = self.campos["Apellidos"].get().strip()
            apellidos = apellidos_completos.split(" ", 1)
            apellido_paterno = apellidos[0] if apellidos else ""
            apellido_materno = apellidos[1] if len(apellidos) > 1 else ""

            cedula = self.campos["Cédula Id"].get().strip()
            email = self.campos["Email"].get().strip()
            telefono = self.campos["Teléfono"].get().strip()
            especialidad = self.campos["Especialidad"].get().strip()

            # ================ VALIDACIÓN BÁSICA ================
            if not nombres or not apellido_paterno or not cedula :
                print("❌ Error: Campos obligatorios vacíos (Nombres, Apellidos, Cédula)")
                return

            # ================ MOSTRAR DATOS GUARDADOS ================
            print("=" * 80)
            print("✅ DATOS DEL DOCTOR GUARDADOS")
            print("=" * 80)
            print(f"👨‍⚕️ Nombres: {nombres}")
            print(f"👨‍⚕️ Apellidos: {apellido_paterno} {apellido_materno}")
            print(f"🆔 Cédula: {cedula}")
            print(f"📧 Email: {email}")
            print(f"📱 Teléfono: {telefono}")
            print(f"🏥 Especialidad: {especialidad}")
            print(f"📅 Fecha del sistema: {self.fecha_actual.strftime('%Y-%m-%d %H:%M:%S')}")

            # ================ MOSTRAR HORARIOS CON FECHAS COMPLETAS ================
            if self.horario_entrada :
                print(
                    f"🟢 Entrada: {self.horario_entrada.strftime('%Y-%m-%d %H:%M')} ({self.horario_entrada.strftime('%A')})")
            if self.horario_salida :
                print(
                    f"🔴 Salida: {self.horario_salida.strftime('%Y-%m-%d %H:%M')} ({self.horario_salida.strftime('%A')})")

            if self.horario_entrada and self.horario_salida :
                duracion = self.horario_salida - self.horario_entrada
                if duracion.days > 0 :
                    print(f"⏱️ Duración: {duracion.days} días y {duracion.seconds // 3600} horas")
                else :
                    horas = duracion.total_seconds() / 3600
                    print(f"⏱️ Duración: {horas:.1f} horas")

            print("=" * 80)

        except Exception as e :
            print(f"❌ Error guardando datos del doctor: {e}")

    # ================ FUNCIÓN PARA LIMPIAR CAMPOS ================
    def limpiar_campos(self) :
        try :
            # ================ LIMPIAR CAMPOS DEL FORMULARIO ================
            for campo in self.campos.values() :
                campo.delete(0, "end")

            # ================ LIMPIAR HORARIOS ================
            self.horario_entrada = None
            self.horario_salida = None

            # ================ RESETEAR SELECTORES ================
            self.fecha_entrada.set("Hoy")
            self.hora_entrada.set("08:00")
            self.min_entrada.set("00")
            self.fecha_salida.set("Hoy")
            self.hora_salida.set("17:00")
            self.min_salida.set("00")

            # ================ RESETEAR LABELS ================
            self.label_entrada.configure(text="🟢 Entrada: No configurado", text_color="gray")
            self.label_salida.configure(text="🔴 Salida: No configurado", text_color="gray")
            self.label_resumen.configure(text="⏱️ Configure los horarios", text_color="gray")

            print("🧹 Todos los campos han sido limpiados")

        except Exception as e :
            print(f"❌ Error limpiando campos: {e}")