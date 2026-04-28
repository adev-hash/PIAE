import utils, api_cliente, limpiador_datos as ld, analizador, graficas

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
	print("datos en main:", type(datos))
except ImportError:
	print("Módulo api_cliente no encontrado")

#Temperatura
temperatura = api_cliente.obtener_temperatura(ciudad)
print(f"Temperatura: {temperatura}° C")

#Humedad
humedad = api_cliente.obtener_humedad(ciudad)
print(f"Humedad: {humedad}%")

#Descripcion del clima
clima = api_cliente.obtener_descripcion(ciudad)
print(f"Descripción: {clima}")

#Cantidad de viento
viento = api_cliente.obtener_viento(ciudad)
print(f"Velocidad del Viento: {viento} m/s")

#print(f"Test: La ciudad en los archivos es ")


#Limpiar los datos
print("datos en main antes de entrar a ")
datos_limpios = ld.procesar_datos(datos)
print(datos_limpios)

datos_crudos  = api_cliente.dato_clima(ciudad)
datos_limpios = id.procesar_datos(datos_crudos)
fecha, temperatura, clima = analizador.filtrar_datos_climaticos(datos_limpios)
resultado = analizador.recomendacion_de_evento(fecha, clima, temperatura)

if resultado["alerta"]:
    print(f"\n{resultado['alerta']}")
print(resultado["recomendacion"])

graficas.generar_reporte(resultado, datos_crudos, ciudad)