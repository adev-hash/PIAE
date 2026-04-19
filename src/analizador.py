'''
El modulo analizador de datos se encarga de procesar la información climática obtenida del módulo de limpieza de datos y generar recomendaciones para eventos al aire libre.
Última modificación: 19/04/2026
Autor: Massimo Vazquez
''' 


def filtrar_datos_climaticos(diccionario_limpio):

    if not diccionario_limpio:
        return None, None, None

    lista_fechas = list(diccionario_limpio.keys())
    fecha = lista_fechas[0]
    datos = diccionario_limpio[fecha]
    temperatura = datos.get("temperatura")
    clima = datos.get("clima")

    return fecha, temperatura, clima

def recomendacion_de_evento(fecha,clima,temperatura):

    alerta = ""
    recomendacion = ""

    if "rain" in clima or "lluvia" in clima or "storm" in clima:
        alerta = "Alerta de clima adverso: Se esperan lluvias o tormentas."
        recomendacion = "Recomendación: Considera posponer el evento o trasladarlo a un lugar cubierto,lleva paraguas o impermeable."
    elif temperatura >= 35 
        alerta = "Alerta de clima extremo: Temperaturas muy altas."
        recomendacion = "Recomendación: Considera posponer el evento o trasladarlo a un lugar con aire acondicionado, mantente hidratado y evita la exposición prolongada al sol."
    elif temperatura <= 5:
        alerta = "Alerta de clima extremo: Temperaturas muy bajas."
        recomendacion = "Recomendación: Considera posponer el evento o trasladarlo a un lugar con calefacción, vístete con ropa abrigada y evita la exposición prolongada al frío."
    elif temperatura >= 20 and temperatura < 35 and "clear" in clima:
        recomendacion = "Recomendación: Aprovecha el buen clima para realizar el evento al aire libre condiciones ideales."
    else:
        recomendacion = "Recomendación: El clima es normal, puedes proceder con el evento sin mayores preocupaciones."
    return {
        "fecha": fecha,
        "clima": clima,
        "temperatura": temperatura,
        "alerta": alerta, 
        "recomendacion": recomendacion}
