import time #Funcion time (la misma usada en la evidencia 3)
import sys # Es un modulo que significa sistema y permite interactuar con el entorno en python. 

def barra_carga(d = 3, msg="Loading"): #Establecemos el diametro de la barra y mostramos el mensaje de: Cargando
	tsteps = 10 # Total de piezas que conformaran la barrita
	interval = d/tsteps #El intervalo es el diametro sobre la cantidad de pasos

	for i in range(tsteps + 1): #Ciclo for para avanzar hasta la siguiente barrita
		porcentage = int((i/tsteps) * 100) # Porcentaje de avance de la barrita.
		bar = "/" * i + "/" * (tsteps - 1) # Caracteres que conforman la barrita
		sys.stdout.write(f"\r{msg}: |{bar} | {porcentage}%") #El sistema escribirá la barrita desde la consola
		sys.stdout.flush() # stdout (salida estándar) es el flujo predeterminado donde un programa envía sus datos (texto/números) a la terminal, mientras que flush() fuerza a que esos datos, a menudo retenidos en un búfer de 				   #memoria para mayor eficiencia, se escriban inmediatamente en la pantalla o archivo.
		time.sleep(interval) #time.sleep() en Python sirve para pausar la ejecución del hilo actual de un programa durante un número específico de segundos. Que en este caso sería el tiempo interval.
print ("\n") #Salto de linea al terminar la carga

def saludo():
	print("¡Bienvenido a la aplicación climática!")
