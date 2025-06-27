import customtkinter as ctk
from tkcalendar import DateEntry
import datetime


class HoraPicker(ctk.CTkFrame) :
    def __init__(self, master=None, label="Hora", hora_inicial=None) :
        super().__init__(master)

        # Inicializar hora y minuto
        if hora_inicial :
            self.hora = hora_inicial.hour
            self.minuto = hora_inicial.minute
        else :
            now = datetime.datetime.now()
            self.hora = now.hour
            self.minuto = now.minute

        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=1)

        # Etiqueta principal
        ctk.CTkLabel(
            self,
            text=label,
            font=("Roboto", 13, "bold")
        ).grid(row=0, column=0, columnspan=5, pady=(5, 10))

        # Botones para incrementar
        ctk.CTkButton(
            self,
            text="▲",
            width=30,
            height=25,
            command=self.incrementar_hora
        ).grid(row=1, column=1, padx=2)

        ctk.CTkButton(
            self,
            text="▲",
            width=30,
            height=25,
            command=self.incrementar_minuto
        ).grid(row=1, column=3, padx=2)

        # Labels para mostrar hora y minuto
        self.label_hora = ctk.CTkLabel(
            self,
            text=f"{self.hora:02d}",
            font=("Roboto", 16, "bold")
        )
        self.label_hora.grid(row=2, column=1, padx=5, pady=5)

        ctk.CTkLabel(
            self,
            text=":",
            font=("Roboto", 16, "bold")
        ).grid(row=2, column=2, pady=5)

        self.label_min = ctk.CTkLabel(
            self,
            text=f"{self.minuto:02d}",
            font=("Roboto", 16, "bold")
        )
        self.label_min.grid(row=2, column=3, padx=5, pady=5)

        # Botones para decrementar
        ctk.CTkButton(
            self,
            text="▼",
            width=30,
            height=25,
            command=self.decrementar_hora
        ).grid(row=3, column=1, padx=2)

        ctk.CTkButton(
            self,
            text="▼",
            width=30,
            height=25,
            command=self.decrementar_minuto
        ).grid(row=3, column=3, padx=2)

    def incrementar_hora(self) :
        self.hora = (self.hora + 1) % 24
        self.label_hora.configure(text=f"{self.hora:02d}")

    def decrementar_hora(self) :
        self.hora = (self.hora - 1) % 24
        self.label_hora.configure(text=f"{self.hora:02d}")

    def incrementar_minuto(self) :
        self.minuto = (self.minuto + 5) % 60
        self.label_min.configure(text=f"{self.minuto:02d}")

    def decrementar_minuto(self) :
        self.minuto = (self.minuto - 5) % 60
        self.label_min.configure(text=f"{self.minuto:02d}")

    def get_hora(self) :
        """Retorna un objeto datetime.time con la hora seleccionada"""
        return datetime.time(self.hora, self.minuto)

    def set_hora(self, hora, minuto) :
        """Establece una hora específica"""
        self.hora = hora % 24
        self.minuto = minuto % 60
        self.label_hora.configure(text=f"{self.hora:02d}")
        self.label_min.configure(text=f"{self.minuto:02d}")


class FechaHoraPicker(ctk.CTkFrame) :
    """Widget completo que combina fecha y hora"""

    def __init__(self, master=None, label="Fecha y Hora", fecha_inicial=None) :
        super().__init__(master)

        # Configurar grid principal
        self.grid_columnconfigure(0, weight=1)

        # Título del widget
        ctk.CTkLabel(
            self,
            text=label,
            font=("Roboto", 14, "bold")
        ).grid(row=0, column=0, pady=(10, 5), sticky="w")

        # Frame para fecha
        frame_fecha = ctk.CTkFrame(self)
        frame_fecha.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        ctk.CTkLabel(frame_fecha, text="Fecha:", font=("Roboto", 12)).pack(anchor="w", padx=5, pady=(5, 0))
        self.date_entry = DateEntry(
            frame_fecha,
            date_pattern="yyyy-mm-dd",
            width=12
        )
        if fecha_inicial :
            self.date_entry.set_date(fecha_inicial.date())
        else :
            self.date_entry.set_date(datetime.datetime.now().date())
        self.date_entry.pack(padx=5, pady=(0, 5), fill="x")

        # Frame para hora
        frame_hora = ctk.CTkFrame(self)
        frame_hora.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

        self.hora_picker = HoraPicker(
            frame_hora,
            label="Hora:",
            hora_inicial=fecha_inicial if fecha_inicial else None
        )
        self.hora_picker.pack(padx=5, pady=5, fill="x")

    def get_fecha_hora(self) :
        """Retorna un objeto datetime completo"""
        fecha = self.date_entry.get_date()
        hora = self.hora_picker.get_hora()
        return datetime.datetime.combine(fecha, hora)

    def set_fecha_hora(self, fecha_hora) :
        """Establece una fecha y hora específica"""
        self.date_entry.set_date(fecha_hora.date())
        self.hora_picker.set_hora(fecha_hora.hour, fecha_hora.minute)


class RegistroHorarioWidget(ctk.CTkFrame) :
    """Widget completo para registro de horarios con entrada y salida"""

    def __init__(self, master=None) :
        super().__init__(master)

        # Configurar grid
        self.grid_columnconfigure(0, weight=1)

        # Título principal
        ctk.CTkLabel(
            self,
            text="📅 REGISTRO DE HORARIOS",
            font=("Roboto", 16, "bold")
        ).grid(row=0, column=0, pady=(15, 20))

        # Frame para entrada
        frame_entrada = ctk.CTkFrame(self, fg_color="#1a4c96")
        frame_entrada.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        frame_entrada.grid_columnconfigure(0, weight=1)

        self.entrada_picker = FechaHoraPicker(
            frame_entrada,
            label="🟢 ENTRADA",
            fecha_inicial=datetime.datetime.now().replace(hour=8, minute=0)
        )
        self.entrada_picker.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        # Frame para salida
        frame_salida = ctk.CTkFrame(self, fg_color="#961a1a")
        frame_salida.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        frame_salida.grid_columnconfigure(0, weight=1)

        self.salida_picker = FechaHoraPicker(
            frame_salida,
            label="🔴 SALIDA",
            fecha_inicial=datetime.datetime.now().replace(hour=17, minute=0)
        )
        self.salida_picker.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        # Botón de guardar
        self.btn_guardar = ctk.CTkButton(
            self,
            text="💾 GUARDAR REGISTRO",
            command=self.guardar_registro,
            width=200,
            height=40,
            font=("Roboto", 14, "bold")
        )
        self.btn_guardar.grid(row=3, column=0, pady=20)

        # Callback personalizable
        self.callback_guardar = None

    def set_callback_guardar(self, callback) :
        """Establece una función callback para cuando se guarde el registro"""
        self.callback_guardar = callback

    def guardar_registro(self) :
        """Función interna para guardar el registro"""
        try :
            entrada = self.entrada_picker.get_fecha_hora()
            salida = self.salida_picker.get_fecha_hora()

            # Validación básica
            if salida <= entrada :
                print("❌ Error: La hora de salida debe ser posterior a la de entrada")
                return

            # Mostrar información
            print("=" * 50)
            print("📅 REGISTRO DE HORARIO GUARDADO")
            print("=" * 50)
            print(f"🟢 Entrada: {entrada.strftime('%Y-%m-%d %H:%M')}")
            print(f"🔴 Salida:  {salida.strftime('%Y-%m-%d %H:%M')}")

            # Calcular duración
            duracion = salida - entrada
            horas = duracion.total_seconds() / 3600
            print(f"⏱️  Duración: {horas:.1f} horas")
            print("=" * 50)

            # Llamar callback personalizado si existe
            if self.callback_guardar :
                self.callback_guardar(entrada, salida)

        except Exception as e :
            print(f"❌ Error guardando registro: {e}")

    def get_entrada(self) :
        """Retorna la fecha/hora de entrada"""
        return self.entrada_picker.get_fecha_hora()

    def get_salida(self) :
        """Retorna la fecha/hora de salida"""
        return self.salida_picker.get_fecha_hora()

    def limpiar(self) :
        """Limpia y resetea los campos"""
        ahora = datetime.datetime.now()
        self.entrada_picker.set_fecha_hora(ahora.replace(hour=8, minute=0))
        self.salida_picker.set_fecha_hora(ahora.replace(hour=17, minute=0))