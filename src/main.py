import utils, api_cliente, limpiador_datos, analizador, graficas


if __name__ == "__main__":
	try:
		print("Iniciando programa principal")
		utils.barra_carga(2, "Cargando")
		print("\n")
		utils.saludo()
		#print("Test, prueba de GitHub y GitHub desktop")
	except ImportError:
		print("Error: Módulos no encontrados")