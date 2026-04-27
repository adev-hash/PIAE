'''
El módulo limpiador_datos se encarga de procesar los datos obtenidos del api_cliente, eliminando información innecesaria o inválida, validando los datos y estructurándolos en un formato más claro y útil para su posterior análisis
Última modificación: 18/04/2026
Autor: Fernanda Pérez
''' 
import re
from datetime import datetime

#Extrae los datos relevantes del JSON obtenido del API 
def extraer_datos(data): 
    resultados = []

    # Solo datos de clima actual (/weather)
    fecha = datetime.now().strftime("%Y-%m-%d")
    temp = data.get("main", {}).get("temp", None)
    # Se obtiene la descripción del clima del primer elemento de la lista "weather"
# [{}] evita errores si la lista viene vacía
    clima = data.get("weather", [{}])[0].get("description", "")

    resultados.append((fecha, temp, clima))

    return resultados


#Revisa que las fechas extraídas estén en formato YYYY-MM-DD usando expresiones regulares
def validar_fecha(fecha):
    patron = r"^\d{4}-\d{2}-\d{2}$"
    return re.match(patron, fecha)


#Verifica que la temperatura sea real y razonable
def limpiar_datos(datos):
    datos_limpios = []

    for fecha, temp, clima in datos:
        if validar_fecha(fecha) and temp is not None:
            #Se valida que la temperatura esté en un rango razonable
            if -50 <= temp <= 60:
                datos_limpios.append((fecha, temp, clima))

    return datos_limpios


def eliminar_repetidos(datos):
    # Realmente ya no habrá repetidos, pero se deja por consistencia
    vistos = set()
    resultado = []

    for fecha, temp, clima in datos:
        #Si la fecha no se encuentra la añadirá
        if fecha not in vistos:
            vistos.add(fecha)
            resultado.append((fecha, temp, clima))

    return resultado


#Acomoda los datos en un diccionario para facilitar manipulación
def estructurar_datos(datos):
    estructura = {}

    for fecha, temp, clima in datos:
        estructura[fecha] = {
            "temperatura": temp,
            "clima": clima
        }

    return estructura


def procesar_datos(data):
	'''
	Ejecuta todo el proceso de limpieza y organización de datos
	Pasos:
    	   1. Extrae datos del API
    	   2. Limpia datos inválidos
    	   3. Elimina duplicados
    	   4. Estructura la información
	'''
    datos = extraer_datos(data)
    datos = limpiar_datos(datos)
    datos = eliminar_repetidos(datos)
    datos = estructurar_datos(datos)

    return datos
