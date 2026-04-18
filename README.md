
# Aplicación climática

En este proyecto se utilizará el lenguaje de programación de python para elaborar una aplicación que permita calcular con anticipación la temperatura de los días, meses y años solicitados.
Esto con la fanalidad de poder realizar eventos como fiestas o algun convivio y tener por asegurado el clima de la fecha y dia solicitado. Usaremos las extensiones de openpyxl para poder elaborar los calculos y las gráficas en excel y mathplotlib para visualizarlos.
También llevaremos un ordenamiento de fechas por orden ascendente para que el usuario tenga un visión más comoda  y vea la fecha y mes más corto donde el clima sea más favorable.
Los datos serán extraidos de la libreria de la API  "OpenWeather". Se usaran listas, tuplas y diccionarios para organizar los datos, el uso de las listas serán para las fechas, las tuplas para los datos impresos y los conjuntos para evitar repeticion de fechas, ya que el clima se basará en el promedio diario y en base a una escala numerica se determinará si es buena o mala idea salir ese día, esto para evitar redundancia de datos.
Las respuestas de los APIS seran manejadas con código Json. 
Al final después de imprimir las gráficas y limpiar los datos para una nueva solicitud.


## Authors

- [adrianhcavazos@gmail.com](https://github.com/adev-hash)
- [miguelito.guerra@hotmail.com](https://github.com/adev-hash)
- [crakmike46@gmail.com](https://github.com/adev-hash)
- [karla.vencov@gmail.com](https://github.com/adev-hash)
- [fernandaperez6764@gmail.com](https://github.com/adev-hash)


## API Reference

#### Get all items

```http
  GET /api/items
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api_key` | `string` | **Required**. Your API key |

#### Get item

```http
  GET /api/items/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

#### add(num1, num2)

Takes two numbers and returns the sum.


## Used By

This project is used by the following companies:

- UANL - FCFM / Proyecto Acádemico - No Oficial


## Appendix

Any additional information goes here
