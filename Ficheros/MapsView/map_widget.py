
import customtkinter as ctk
from tkintermapview import TkinterMapView
from geopy.geocoders import OpenCage
from geopy.exc import GeocoderUnavailable

class MapWidget(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)

        self.geolocator = OpenCage(api_key="e1a1dee5881840d4aa9b75eecbd49c3e")
        self.marker = None
        self._address_callback = None
        self.current_address = ""  # ← almacena dirección

        self.address_entry = ctk.CTkEntry(self, placeholder_text="Ingresa una dirección", width=400)
        self.address_entry.pack(pady=(10, 5))

        search_button = ctk.CTkButton(self, text="Buscar dirección", command=self.search_address)
        search_button.pack(pady=(0, 10))

        self.map_widget = TkinterMapView(self, width=800, height=600, corner_radius=10)
        self.map_widget.pack(fill="both", expand=True, padx=10, pady=10)

        self.map_widget.set_position(-2.170998, -79.922356)
        self.map_widget.set_zoom(20)

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
                    self.current_address = address  # ← actualiza dirección
                    if self._address_callback:
                        self._address_callback(address)
            except GeocoderUnavailable:
                print("Servicio no disponible.")

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
                self.current_address = address  # ← actualiza dirección

                if self._address_callback:
                    self._address_callback(address)
        except GeocoderUnavailable:
            print("Servicio no disponible.")

    def on_address_change(self, callback):
        self._address_callback = callback

    def get_address(self):  # ← método para obtener dirección
        return self.current_address
