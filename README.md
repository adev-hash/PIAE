Aplicación climática
Autores
adrianhcavazos@gmail.com 
miguelito.guerra@hotmail.com 
crakmike46@gmail.com 
karla.vencov@gmail.com 
fernandaperez6764@gmail.com
Introducción
Este proyecto consiste en el desarrollo de una aplicación climática utilizando el lenguaje de programación Python. Su propósito es permitir al usuario consultar y analizar datos del clima de diferentes ciudades, con el fin de tomar decisiones informadas sobre actividades futuras, como eventos o salidas.
La aplicación obtiene información en tiempo real mediante el uso de la API de OpenWeather, procesando los datos en formato JSON. Posteriormente, estos datos son filtrados, organizados y analizados para mostrar únicamente la información relevante, como la temperatura, humedad, descripción del clima y velocidad del viento.
Además, el sistema permite estructurar los datos de manera clara y ordenada, facilitando su interpretación y posible visualización mediante herramientas como Excel o bibliotecas gráficas. Esto proporciona al usuario una experiencia más comprensible y útil al momento de consultar el estado del clima.
En conjunto, el proyecto integra conceptos fundamentales de programación como el uso de módulos, estructuras de datos y manejo de APIs, ofreciendo una solución práctica para el análisis climático.
Justificación del API
Para el desarrollo de esta aplicación se eligió la API de OpenWeather, ya que proporciona información climática actualizada y confiable de una gran variedad de ciudades a nivel mundial.
Esta API permite acceder a datos relevantes como la temperatura, humedad, descripción del clima y velocidad del viento, los cuales son fundamentales para el análisis que realiza la aplicación. Además, su uso es sencillo, ya que devuelve la información en formato JSON, lo que facilita su manejo e integración en el lenguaje Python.
Otra razón importante para su elección es que permite realizar consultas mediante el nombre de la ciudad, lo cual resulta práctico para el usuario final. Asimismo, ofrece una buena documentación y acceso gratuito con ciertas limitaciones, lo que la hace ideal para proyectos académicos.
En conclusión, OpenWeather es una herramienta adecuada para este proyecto debido a su facilidad de uso, disponibilidad de datos relevantes y compatibilidad con las tecnologías utilizadas.
Algoritmo y diagrama de flujo
Arquitectura del sistema
La aplicación está estructurada de forma modular, lo que permite dividir el sistema en diferentes componentes encargados de tareas específicas. Esta organización facilita el mantenimiento, la escalabilidad y la comprensión del funcionamiento del programa.
El flujo del sistema inicia cuando el usuario proporciona los datos de entrada, los cuales son:
• Ciudad
• País
• Estado (opcional, dependiendo de la disponibilidad en la API)
• Fecha
A partir de estos datos, el sistema realiza una consulta a la API de OpenWeather para obtener información climática.
Los datos de salida que genera el sistema incluyen:
• Temperatura
• Humedad
• Descripción del clima
• Velocidad del viento
• Datos organizados y estructurados para su análisis
• Posibles gráficas o archivos en Excel para visualización
El sistema se compone de los siguientes módulos:
• main.py: Es el punto de entrada del programa. Se encarga de recibir los datos del usuario y coordinar la ejecución de los demás módulos.
• api_cliente.py: Realiza las solicitudes a la API de OpenWeather utilizando los datos proporcionados. Obtiene la información del clima y la almacena localmente en formato JSON para evitar consultas repetidas.
• limpiador_datos.py: Procesa la información obtenida del API, extrayendo únicamente los datos relevantes como temperatura, humedad, descripción del clima y velocidad del viento. También valida que los datos sean correctos y consistentes.
• analizador.py: Utiliza los datos ya procesados para realizar análisis, como promedios o evaluaciones del clima, con el objetivo de apoyar la toma de decisiones del usuario.
• graficas.py: Genera representaciones visuales de los datos, como gráficas, utilizando exportaciones a Excel con openpyxl.
• utils.py: Contiene funciones auxiliares que mejoran la interacción con el usuario, como la visualización de una barra de carga en la consola y mensajes de bienvenida. Estas funciones no forman parte del procesamiento principal, pero contribuyen a una mejor experiencia de uso.
El flujo general del sistema es el siguiente: el usuario ingresa los datos → main.py coordina el proceso → api_cliente.py obtiene la información → limpiador_datos.py filtra y organiza los datos → analizador.py procesa la información → graficas.py genera visualizaciones.
Esta arquitectura modular permite que cada componente funcione de manera independiente, facilitando futuras mejoras o modificaciones sin afectar el funcionamiento completo del sistema.
Estructuras de datos utilizadas
En el desarrollo de la aplicación se utilizan diferentes estructuras de datos para organizar, almacenar y procesar la información obtenida del API de OpenWeather.
• Diccionarios: Se utilizan para manejar los datos en formato JSON que devuelve la API. Esta estructura permite acceder de manera eficiente a información específica como temperatura, humedad, clima y velocidad del viento mediante claves.
• Listas: Se emplean para almacenar conjuntos de datos, especialmente cuando se procesan múltiples registros del clima. Permiten recorrer y manipular la información de manera ordenada.
• Tuplas: Se utilizan en el módulo limpiador_datos para agrupar datos relacionados, como la fecha, temperatura y descripción del clima. Esto facilita su manejo durante el proceso de limpieza.
• Conjuntos (set): Se utilizan para eliminar datos repetidos, especialmente fechas duplicadas, asegurando que la información procesada sea única y evitando redundancia.
Estas estructuras permiten que el sistema sea eficiente en el manejo de datos, facilitando su procesamiento, validación y posterior análisis.
Módulos desarrollados
Expresiones regulares
En este proyecto, las expresiones regulares se utilizan en el módulo limpiador_datos.py con el objetivo de validar el formato de ciertos datos obtenidos del API, específicamente las fechas.
Las expresiones regulares permiten definir patrones que deben cumplir los datos para ser considerados válidos. En este caso, se emplea un patrón para verificar que las fechas tengan el formato correcto (año-mes-día), es decir, "YYYY-MM-DD".
El patrón utilizado es el siguiente:
\d{4}-\d{2}-\d{2}
Este patrón indica que:
• \d{4}: representa cuatro dígitos correspondientes al año
• \d{2}: representa dos dígitos para el mes
• \d{2}: representa dos dígitos para el día
El uso de expresiones regulares permite asegurar que los datos procesados sean consistentes y válidos antes de ser analizados, evitando errores en etapas posteriores del sistema.
Cabe destacar que las expresiones regulares solo se emplean en el módulo limpiador_datos.py, ya que es el encargado de validar y filtrar los datos. En los demás módulos no es necesario su uso, debido a que trabajan con información previamente validada.

