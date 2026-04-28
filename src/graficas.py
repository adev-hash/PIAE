# Módulo de gráficas y exportación a Excel.
# Última modificación: 27/04/2026

import matplotlib.pyplot as plt
import math
from pathlib import Path
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# Carpeta de salida junto al script
_DIR_SALIDA = Path(__file__).resolve().parent / "reportes"
_DIR_SALIDA.mkdir(parents=True, exist_ok=True)


def generar_reporte(resultado_analizador: dict, datos_api: dict, ciudad: str) -> None:
    # Punto de entrada: llamar desde main.py después de cada consulta
    import api_cliente
    #print("Esto debe generar el reporte")

    fecha       = resultado_analizador.get("fecha", datetime.now().strftime("%Y-%m-%d"))
    temperatura = resultado_analizador.get("temperatura")
    clima       = resultado_analizador.get("clima", "")
    alerta      = resultado_analizador.get("alerta", "")
    recomend    = resultado_analizador.get("recomendacion", "")
    humedad     = datos_api.get("main", {}).get("humidity")
    viento      = datos_api.get("wind", {}).get("speed")

    puntos_forecast = api_cliente.obtener_forecast(ciudad)

    grafica_consulta(fecha, temperatura, clima, ciudad, puntos_forecast)
    exportar_excel(fecha, temperatura, clima, humedad, viento, alerta, recomend, ciudad)


def _curva_24h(temp_actual: float) -> list:
    # Curva senoidal: mínimo ~5 am, máximo ~15 h
    hora_actual = datetime.now().hour
    base = temp_actual - 4

    temps = [
        round(base + (temp_actual - base) * math.sin(math.pi * max(h - 5, 0) / 18), 1)
        if 5 <= h <= 23 else base
        for h in range(24)
    ]
    temps[hora_actual] = temp_actual  # valor exacto en la hora actual
    return temps


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

    # Punto de la hora actual
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


def exportar_excel(
    fecha: str, temperatura: float, clima: str,
    humedad, viento, alerta: str, recomendacion: str, ciudad: str
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
    ws = wb.active
    ws.title = "Datos Climáticos"

    # Título
    ws.merge_cells("A1:B1")
    ws["A1"].value     = f"Reporte Climático — {ciudad}"
    ws["A1"].font      = Font(name="Arial", bold=True, size=13, color="1A3A5C")
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws["A1"].fill      = PatternFill("solid", start_color="D6E8F7")
    ws.row_dimensions[1].height = 28

    # Encabezados
    for col, texto in enumerate(["Parámetro", "Valor"], start=1):
        c = ws.cell(row=2, column=col, value=texto)
        c.font = fuente_enc; c.fill = relleno_enc
        c.alignment = alineado_c; c.border = borde_enc
    ws.row_dimensions[2].height = 22

    # Datos
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

    # Nota al pie
    nota_fila = len(filas_datos) + 4
    ws.cell(nota_fila, 1, f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M')}").font = \
        Font(name="Arial", size=9, italic=True, color="888888")

    wb.save(nombre_archivo)
    print(f"Excel guardado: {nombre_archivo}")
    return str(nombre_archivo)