import re

def extraer_datos(data):
    resultados = []

    for item in data.get("list", []):
        fecha_completa = item.get("dt_txt", "")
        fecha = fecha_completa[:10]

        temp = item.get("main", {}).get("temp", None)
        clima = item.get("weather", [{}])[0].get("description", "")

        resultados.append((fecha, temp, clima))

    return resultados

def validar_fecha(fecha):
    patron = r"\d{4}-\d{2}-\d{2}"
    return re.match(patron, fecha)

def limpiar_datos(datos):
    datos_limpios = []

    for fecha, temp, clima in datos:
        if validar_fecha(fecha) and temp is not None:
            if -50 <= temp <= 60:
                datos_limpios.append((fecha, temp, clima))

    return datos_limpios

def eliminar_repetidos(datos):
    vistos = set()
    resultado = []

    for fecha, temp, clima in datos:
        if fecha not in vistos:
            vistos.add(fecha)
            resultado.append((fecha, temp, clima))

    return resultado

def estructurar_datos(datos):
    estructura = {}

    for fecha, temp, clima in datos:
        estructura[fecha] = {
            "temperatura": temp,
            "clima": clima
        }

    return estructura

def procesar_datos(data):
    datos = extraer_datos(data)
    datos = limpiar_datos(datos)
    datos = eliminar_repetidos(datos)
    datos = estructurar_datos(datos)

    return datos
