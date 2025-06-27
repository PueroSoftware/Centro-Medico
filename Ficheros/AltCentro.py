def alt_centro(ventana, ancho, alto):
    ventana.update_idletasks()  # Actualiza tamaños internos antes del cálculo
    # Obtener dimensiones de la pantalla
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()

    # Calcular coordenadas para centrar
    x = round(pantalla_ancho / 2) - (ancho / 2)
    y = round(pantalla_alto / 2) - (alto / 2)

    # Aplicar geometría
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
