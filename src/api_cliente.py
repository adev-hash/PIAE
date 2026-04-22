#Este archivo contiene el codigo que permite al usuario consultar la informacion que requiera del API
#Ultima modificacion: 15-04-26
#Por: Karla Ivana Cordova Ventura

import requests
import json
import os

key = "6d8d2d9eef71f7fd269939efa424e373"
# dir_datos es el directorio donde estan los datos solicitados con anterioridad
dir_datos = "datos/"

def dato_clima(ciudad):
    # Obtiene el clima de una ciudad. Primero revisa si ya esta guardado localmente
    nombre_archivo = os.path.join(dir_datos), f"{ciudad}.json"

    if os.path.exists("nombre_archivo"):
        with open("nombre_archivo", "r") as f:
            return json.load(f)

    url = (f"https://api.openweathermap.org/data/2.5/weather"
           f"?q={ciudad}&units=metric&appid={key}")
    respuesta = requests.get(url)
    datos = respuesta.json()

    os.makedirs(dir_datos, exist_ok=True)
    with open("nombre_archivo", "w") as f:
        json.dump(datos, f, indent=2)

    return datos

def obtener_temperatura(ciudad):
    datos = dato_clima(ciudad)
    return datos["main"]["temp"]

def obtener_humedad(ciudad):
    datos = dato_clima(ciudad)
    return datos["main"]["humidity"]

def obtener_descripcion(ciudad):
    datos = dato_clima(ciudad)
    return datos["weather"][0]["description"]

def obtener_viento(ciudad):
    datos = dato_clima(ciudad)
    return datos["wind"]["speed"]
