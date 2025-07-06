from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

class GeneradorPDF:
    def __init__(self, datos: dict, ruta_archivo: str):
        self.datos = datos
        self.ruta = ruta_archivo

    def exportar(self):
        c = canvas.Canvas(self.ruta, pagesize=A4)
        ancho, alto = A4
        margen_x = 50
        margen_y = 50
        max_ancho_texto = ancho - 2 * margen_x
        espacio_linea = 14
        y = alto - margen_y

        c.setFont("Helvetica-Bold", 16)
        c.drawString(margen_x, y, "📋 Detalles de la Cita")
        y -= 30

        c.setFont("Helvetica", 12)
        text_obj = c.beginText()
        text_obj.setTextOrigin(margen_x, y)
        text_obj.setLeading(espacio_linea)  # espacio entre líneas

        for campo, valor in self.datos.items():
            texto = f"{campo.capitalize().replace('_', ' ')}: {valor}"
            # Dividir texto largo en líneas que quepan
            lineas = simpleSplit(texto, "Helvetica", 12, max_ancho_texto)
            for linea in lineas:
                if text_obj.getY() < margen_y:
                    c.drawText(text_obj)
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    text_obj = c.beginText()
                    text_obj.setTextOrigin(margen_x, alto - margen_y)
                    text_obj.setLeading(espacio_linea)
                text_obj.textLine(linea)
        c.drawText(text_obj)

        c.save()
        return self.ruta
