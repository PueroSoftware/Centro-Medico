import customtkinter as ctk
from tkintermapview import TkinterMapView
from geopy.geocoders import OpenCage
from geopy.exc import GeocoderUnavailable

# Configuración de apariencia
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MapApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Mapa con Geocodificación")
        self.geometry("1000x800")

        # Inicializar geolocalizador y marcador
        self.geolocator = OpenCage(api_key="e1a1dee5881840d4aa9b75eecbd49c3e")
        #self.geolocator = Nominatim(user_agent="geoapiExercises")
        self.marker = None

        # --- FRAME PRINCIPAL ---
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Entrada de dirección
        self.address_entry = ctk.CTkEntry(main_frame, placeholder_text="Ingresa una dirección", width=500)
        self.address_entry.pack(pady=(10, 5))

        # Botón de búsqueda
        search_button = ctk.CTkButton(main_frame, text="Buscar dirección", command=self.search_address)
        search_button.pack(pady=(0, 10))

        # --- FRAME DEL MAPA ---
        map_frame = ctk.CTkFrame(main_frame)
        map_frame.pack(fill="both", expand=True)

        self.map_widget = TkinterMapView(map_frame, width=960, height=680, corner_radius=10)
        self.map_widget.pack(fill="both", expand=True)

        # Mapa: configuración inicial
        self.map_widget.set_position(-2.170998, -79.922356)  # Latitud y Longitud de Guayaquil, Ecuador
        self.map_widget.set_zoom(10)

        # Click derecho para añadir marcador
        self.map_widget.add_right_click_menu_command(
            label="Añadir marcador",
            command=self.add_marker_event,
            pass_coords=True
        )

    def search_address(self):
        address = self.address_entry.get().strip()
        if address:
            try:
                location = self.geolocator.geocode(address)
                if location:
                    self.map_widget.set_position(location.latitude, location.longitude)
                    self.map_widget.set_zoom(16)
                    if self.marker:
                        self.marker.delete()
                    self.marker = self.map_widget.set_marker(location.latitude, location.longitude, text=address)
                else:
                    print("Dirección no encontrada.")
            except GeocoderUnavailable:
                print("Servicio de geocodificación no disponible.")

    def add_marker_event(self, coords):
        if self.marker:
            self.marker.delete()

        self.marker = self.map_widget.set_marker(coords[0], coords[1])

        try:
            location = self.geolocator.reverse((coords[0], coords[1]), exactly_one=True)
            if location:
                address = location.address
                self.address_entry.delete(0, ctk.END)
                self.address_entry.insert(0, address)
            else:
                print("No se pudo obtener la dirección para las coordenadas.")
        except GeocoderUnavailable:
            print("Servicio de geocodificación no disponible.")

if __name__ == "__main__":
    app = MapApp()
    app.mainloop()
