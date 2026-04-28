# Módulo de gráficas y exportación a Excel.
# Última modificación: 28/04/2026
# Autor: Adrián Humberto Cavazos Leal

import matplotlib.pyplot as plt
import math
import json
from pathlib import Path
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# Carpeta de salida junto al script
_DIR_SALIDA = Path(__file__).resolve().parent / "reportes"
_DIR_SALIDA.mkdir(parents=True, exist_ok=True)

# JSON que acumula hasta 4 ciudades para la comparativa
_HISTORIAL_JSON = Path(__file__).resolve().parent / "historial_comparativa.json"
_MAX_CIUDADES   = 4


# Historial de guardados

def _cargar_historial() -> list:
    if _HISTORIAL_JSON.exists():
        with open(_HISTORIAL_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def _guardar_historial(historial: list) -> None:
    with open(_HISTORIAL_JSON, "w", encoding="utf-8") as f:
        json.dump(historial, f, ensure_ascii=False, indent=2)

def _registrar_ciudad(ciudad: str, temperatura: float) -> list:
    # Agrega la ciudad al historial. Al llegar a 4 se reinicia.
    historial = _cargar_historial()

    if len(historial) >= _MAX_CIUDADES:
        historial = []  # reinicio

    # Evita duplicados: reemplaza si la ciudad ya está
    historial = [c for c in historial if c["ciudad"].lower() != ciudad.lower()]

    historial.append({
        "ciudad":  ciudad,
        "media":   round(temperatura, 1),
        "maxima":  round(temperatura + 4, 1),
        "minima":  round(temperatura - 4, 1),
        "fecha":   datetime.now().strftime("%Y-%m-%d")
    })

    _guardar_historial(historial)
    return historial


# Punto de entrada

def generar_reporte(resultado_analizador: dict, datos_api: dict, ciudad: str) -> None:
    import api_cliente

    fecha       = resultado_analizador.get("fecha", datetime.now().strftime("%Y-%m-%d"))
    temperatura = resultado_analizador.get("temperatura")
    clima       = resultado_analizador.get("clima", "")
    alerta      = resultado_analizador.get("alerta", "")
    recomend    = resultado_analizador.get("recomendacion", "")
    humedad     = datos_api.get("main", {}).get("humidity")
    viento      = datos_api.get("wind", {}).get("speed")

# Registrar ciudad y obtener historial actualizado
    historial = _registrar_ciudad(ciudad, temperatura)

    puntos_forecast = api_cliente.obtener_forecast(ciudad)

    grafica_consulta(fecha, temperatura, clima, ciudad, puntos_forecast)
    exportar_excel(fecha, temperatura, clima, humedad, viento, alerta, recomend, ciudad, historial)

    # Gráfica comparativa solo si hay más de una ciudad
    if len(historial) > 1:
        grafica_comparativa(historial)


# Curva senoidal

def _curva_24h(temp_actual: float) -> list:
    hora_actual = datetime.now().hour
    base = temp_actual - 4
    temps = [
        round(base + (temp_actual - base) * math.sin(math.pi * max(h - 5, 0) / 18), 1)
        if 5 <= h <= 23 else base
        for h in range(24)
    ]
    temps[hora_actual] = temp_actual
    return temps


# Gráfica 1:

def grafica_consulta(
    fecha: str, temperatura: float, clima: str,
    ciudad: str, puntos_forecast: dict
) -> None:
    hora_actual = datetime.now().hour
    horas       = list(range(24))
    temps_24h   = _curva_24h(temperatura)

    fig, ax = plt.subplots(figsize=(11, 5))

    ax.plot(horas, temps_24h, color="#E8622A", linewidth=2.5, zorder=2)
    ax.fill_between(horas, temps_24h, alpha=0.12, color="#E8622A")

    ax.scatter([hora_actual], [temperatura], color="#C04010", s=100, zorder=5,
               label=f"Ahora ({hora_actual}h): {temperatura}°C")
    ax.annotate(f"{temperatura}°C",
                xy=(hora_actual, temperatura),
                xytext=(0, 13), textcoords="offset points",
                ha="center", fontsize=10, fontweight="bold", color="#C04010")

    ax.set_title(f"Temperatura del día — {ciudad} ({fecha})", fontsize=13, fontweight="bold", pad=14)
    ax.set_xlabel("Hora del día", fontsize=11)
    ax.set_ylabel("Temperatura (°C)", fontsize=11)
    ax.set_xticks(range(0, 24))
    ax.set_xticklabels([f"{h}h" for h in range(24)], rotation=45, fontsize=8)
    ax.grid(axis="y", linestyle="--", alpha=0.45)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_facecolor("#FAFAFA")

    plt.figtext(0.5, -0.02, f"Condición: {clima}", ha="center", fontsize=9, color="#555555")
    plt.tight_layout()

    nombre_img = _DIR_SALIDA / f"grafica_{ciudad.lower().replace(' ', '_')}_{fecha}.png"
    plt.savefig(nombre_img, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"Gráfica guardada: {nombre_img}")


# Gráfica 2

def grafica_comparativa(historial: list) -> None:
    ciudades = [r["ciudad"]  for r in historial]
    maximas  = [r["maxima"]  for r in historial]
    medias   = [r["media"]   for r in historial]
    minimas  = [r["minima"]  for r in historial]

    x      = range(len(ciudades))
    ancho  = 0.22
    offset = [-ancho, 0, ancho]

    fig, ax = plt.subplots(figsize=(10, 5))

    barras = [
        (maximas, "#D94F3D", "T. máxima °C"),
        (medias,  "#4DA87B", "T. media °C"),
        (minimas, "#3A7FBF", "T. mínima °C"),
    ]

    for i, (valores, color, etiqueta) in enumerate(barras):
        posiciones = [xi + offset[i] for xi in x]
        ax.bar(posiciones, valores, width=ancho, color=color,
               label=etiqueta, alpha=0.85, zorder=2)

    ax.set_title("Comparativa de temperaturas por ciudad", fontsize=13, fontweight="bold", pad=14)
    ax.set_ylabel("Temperatura (°C)", fontsize=11)
    ax.set_xticks(list(x))
    ax.set_xticklabels(ciudades, fontsize=10)
    ax.grid(axis="y", linestyle="--", alpha=0.4, zorder=1)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_facecolor("#FAFAFA")
    ax.legend(fontsize=9, loc="upper right")

    plt.tight_layout()

    fecha_hoy  = datetime.now().strftime("%Y-%m-%d")
    nombre_img = _DIR_SALIDA / f"comparativa_{fecha_hoy}.png"
    plt.savefig(nombre_img, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"Gráfica comparativa guardada: {nombre_img}")


#Excel

def exportar_excel(
    fecha: str, temperatura: float, clima: str,
    humedad, viento, alerta: str, recomendacion: str,
    ciudad: str, historial: list
) -> str:
    nombre_archivo = _DIR_SALIDA / f"clima_{ciudad.lower().replace(' ', '_')}_{fecha}.xlsx"

    # Estilos
    fuente_enc  = Font(name="Arial", bold=True, color="FFFFFF", size=11)
    relleno_enc = PatternFill("solid", start_color="2D6A9F")
    alineado_c  = Alignment(horizontal="center", vertical="center")
    borde_enc   = Border(bottom=Side(style="medium", color="1A4E7A"),
                         right=Side(style="thin", color="1A4E7A"))
    relleno_par = PatternFill("solid", start_color="EAF2FB")

    wb = Workbook()

    # ── Hoja 1: Datos Climáticos
    ws = wb.active
    ws.title = "Datos Climáticos"

    ws.merge_cells("A1:B1")
    ws["A1"].value     = f"Reporte Climático — {ciudad}"
    ws["A1"].font      = Font(name="Arial", bold=True, size=13, color="1A3A5C")
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws["A1"].fill      = PatternFill("solid", start_color="D6E8F7")
    ws.row_dimensions[1].height = 28

    for col, texto in enumerate(["Parámetro", "Valor"], start=1):
        c = ws.cell(row=2, column=col, value=texto)
        c.font = fuente_enc; c.fill = relleno_enc
        c.alignment = alineado_c; c.border = borde_enc
    ws.row_dimensions[2].height = 22

    filas_datos = [
        ("Fecha de consulta",          fecha),
        ("Ciudad",                     ciudad),
        ("Temperatura (°C)",           temperatura),
        ("Condición climática",        clima),
        ("Humedad (%)",                humedad if humedad is not None else "N/D"),
        ("Velocidad del viento (m/s)", viento  if viento  is not None else "N/D"),
        ("Alerta",                     alerta if alerta else "Sin alertas"),
        ("Recomendación",              recomendacion),
    ]

    for i, (param, valor) in enumerate(filas_datos):
        fila = i + 3
        ws.cell(fila, 1, param).font = Font(name="Arial", size=10, bold=True)
        celda_val = ws.cell(fila, 2, valor)
        celda_val.font      = Font(name="Arial", size=10)
        celda_val.alignment = Alignment(wrap_text=True, vertical="top")
        if i % 2 == 0:
            ws.cell(fila, 1).fill = relleno_par
            celda_val.fill        = relleno_par
        ws.row_dimensions[fila].height = 18

    ws.row_dimensions[10].height = 45
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 55

    nota_fila = len(filas_datos) + 4
    ws.cell(nota_fila, 1, f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M')}").font = \
        Font(name="Arial", size=9, italic=True, color="888888")

    # ── Hoja 2: Comparativa (solo si hay más de una ciudad)
    if len(historial) > 1:
        ws2 = wb.create_sheet("Comparativa")

        ws2.merge_cells("A1:D1")
        ws2["A1"].value     = "Comparativa de Temperaturas"
        ws2["A1"].font      = Font(name="Arial", bold=True, size=13, color="1A3A5C")
        ws2["A1"].alignment = Alignment(horizontal="center", vertical="center")
        ws2["A1"].fill      = PatternFill("solid", start_color="D6E8F7")
        ws2.row_dimensions[1].height = 28

        for col, texto in enumerate(["Ciudad", "T. Máxima (°C)", "T. Media (°C)", "T. Mínima (°C)"], start=1):
            c = ws2.cell(row=2, column=col, value=texto)
            c.font = fuente_enc; c.fill = relleno_enc
            c.alignment = alineado_c; c.border = borde_enc
        ws2.row_dimensions[2].height = 22

        for i, registro in enumerate(historial):
            fila = i + 3
            valores = [registro["ciudad"], registro["maxima"], registro["media"], registro["minima"]]
            for col, valor in enumerate(valores, start=1):
                celda = ws2.cell(fila, col, valor)
                celda.font      = Font(name="Arial", size=10)
                celda.alignment = Alignment(horizontal="center")
                if i % 2 == 0:
                    celda.fill = relleno_par
            ws2.row_dimensions[fila].height = 18

        for col, ancho in zip("ABCD", [20, 18, 18, 18]):
            ws2.column_dimensions[col].width = ancho

        nota2 = len(historial) + 4
        ws2.cell(nota2, 1, f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M')}").font = \
            Font(name="Arial", size=9, italic=True, color="888888")

    wb.save(nombre_archivo)
    print(f"Excel guardado: {nombre_archivo}")
    return str(nombre_archivo)