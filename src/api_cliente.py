'''
Este archivo contiene el codigo que permite al usuario consultar la informacion que requiera del API
Ultima modificacion: 30-04-26
Por: Karla Ivana Cordova Ventura
'''
import requests
import json
import os
from pathlib import Path

key       = "6d8d2d9eef71f7fd269939efa424e373"
dir_datos = Path(__file__).resolve().parent.parent / "datos"
dir_datos.mkdir(parents=True, exist_ok=True)

def verificar_conexion() -> bool:
    try:
        requests.get("https://api.openweathermap.org", timeout=5)
        return True
    except Exception:
        return False

def dato_clima(ciudad):
    ruta_archivo = dir_datos / f"{ciudad}.json"

    if ruta_archivo.exists():
        with open(ruta_archivo, "r") as f:
            return json.load(f)

    if not verificar_conexion():
        print("Error: Se perdió la conexión a internet. Cerrando el programa.")
        exit()

    url = (f"https://api.openweathermap.org/data/2.5/weather"
           f"?q={ciudad}&units=metric&appid={key}")
    try:
        respuesta = requests.get(url, timeout=10)
        datos = respuesta.json()
    except requests.exceptions.ConnectionError:
        print("Error: Se perdió la conexión durante la consulta.")
        exit()
    except requests.exceptions.Timeout:
        print("Error: La consulta tardó demasiado. Verifica tu red e intenta de nuevo.")
        exit()

    # Si la ciudad no existe la API retorna cod 404, no se guarda
    if str(datos.get("cod")) == "404":
        return None

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
    from datetime import datetime

    url = (f"https://api.openweathermap.org/data/2.5/forecast"
           f"?q={ciudad}&units=metric&appid={key}")
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
