# Funciones/pdf_widget.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


class GeneradorPDF :
    def __init__(self, datos: dict, ruta_archivo: str) :
        self.datos = datos
        self.ruta = ruta_archivo

    def exportar(self) :
        c = canvas.Canvas(self.ruta, pagesize=A4)
        ancho, alto = A4
        y = alto - 50

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y, "📋 Detalles de la Cita")
        y -= 30

        c.setFont("Helvetica", 12)
        for campo, valor in self.datos.items() :
            c.drawString(50, y, f"{campo.capitalize().replace('_', ' ')}: {valor}")
            y -= 20

        c.save()
        return self.ruta
