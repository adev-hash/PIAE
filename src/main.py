import utils, api_cliente, limpiador_datos, analizador, graficas

try:
	print("Iniciando programa principal")
	utils.barra_carga(2, "Cargando")
	print("\n")
	utils.saludo()

except ImportError:
	print("Error: Módulo utils no encontrado")


#Obtener información de una API publica

ciudad = input("Ingresa la ciudad a analizar: ")

try:
	datos = api_cliente.dato_clima(ciudad)
except ImportError:
	print("Módulo api_cliente no encontrado")

#Temperatura
datos = api_cliente.obtener_temperatura(ciudad)
print(f"Temperatura: {datos}° C")

#Humedad
datos = api_cliente.obtener_humedad(ciudad)
print(f"Humedad: {datos}%")

#Descripcion del clima
datos = api_cliente.obtener_descripcion(ciudad)
print(f"Descripción: {datos}")

#Cantidad de viento
datos = api_cliente.obtener_viento(ciudad)
print(f"Velocidad del Viento: {datos} m/s")


#print(f"Test: La ciudad en los archivos es ")