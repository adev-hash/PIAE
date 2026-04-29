'''
Este archivo contiene el codigo que permite al usuario consultar la informacion que requiera del API
Ultima modificacion: 27/04/2026
Por: Karla Ivana Cordova Ventura
'''
import requests
import json
import os
from datetime import datetime

key = "6d8d2d9eef71f7fd269939efa424e373"

#Esta es la key que usa la suscripción.
key2 = "64e5e1c01b176ce25da569b8627e31a9"

# dir_datos es el directorio donde estan los datos solicitados con anterioridad
dir_datos = "datos/"

def dato_clima(ciudad):
    # Obtiene el clima de una ciudad. Primero revisa si ya esta guardado localmente
    ruta_archivo = f"{dir_datos}{ciudad}.json"

    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, "r") as f:
            return json.load(f)

    url = (f"https://api.openweathermap.org/data/2.5/weather"
           f"?q={ciudad}&units=metric&appid={key}")
    respuesta = requests.get(url)
    datos = respuesta.json()

    os.makedirs(dir_datos, exist_ok=True)
    with open(ruta_archivo, "w") as f:
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

def obtener_forecast(ciudad):
  
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={ciudad}&units=metric&appid={key}"
 
    try:
        respuesta = requests.get(url)
        datos = respuesta.json()
    except Exception:
        return {}
 
    if datos.get("cod") != "200":
        return {}
 
    hoy = datetime.now().strftime("%Y-%m-%d")
    puntos = {}
 
    for entrada in datos.get("list", []):
        dt_txt = entrada.get("dt_txt", "")
        if dt_txt.startswith(hoy):
            hora = int(dt_txt[11:13])
            temp = entrada["main"]["temp"]
            puntos[hora] = round(temp, 1)
 
    return puntos