'''
Módulo: graficas.py
'''

import matplotlib
# Configura Matplotlib para que no dependa de una interfaz gráfica (evita bloqueos)
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import math
from pathlib import Path
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side


def generar_reporte(resultado_analizador: dict, datos_api: dict, ciudad: str) -> None:
    """Función principal con manejo de errores por etapa."""
    try:
        import api_cliente
    except ImportError:
        print("Error: No se encontró el módulo 'api_cliente'.")
        return

    fecha = resultado_analizador.get("fecha", datetime.now().strftime("%Y-%m-%d"))
    temperatura = resultado_analizador.get("temperatura")
    clima = resultado_analizador.get("clima", "")
    alerta = resultado_analizador.get("alerta", "")
    recomend = resultado_analizador.get("recomendacion", "")
    
    humedad = datos_api.get("main", {}).get("humidity")
    viento = datos_api.get("wind", {}).get("speed")

    # Obtener puntos del forecast
    puntos_forecast = api_cliente.obtener_forecast(ciudad)

    # Ejecución independiente para que un error no mate al otro
    try:
        grafica_consulta(fecha, temperatura, clima, ciudad, puntos_forecast)
    except Exception as e:
        print(f"Error generando gráfica: {e}")

    try:
        exportar_excel(fecha, temperatura, clima, humedad, viento, alerta, recomend, ciudad)
    except Exception as e:
        print(f"Error exportando Excel: {e}")


def _interpolar_24h(puntos_reales: dict, temp_actual: float) -> list:
    """Cálculo de curva senoidal de temperatura."""
    hora_actual = datetime.now().hour
    base = temp_actual - 4
    temps = [
        round(base + (temp_actual - base) * math.sin(math.pi * max(h - 5, 0) / 18), 1)
        if 5 <= h <= 23 else base
        for h in range(24)
    ]
    temps[hora_actual] = temp_actual
    return temps


def grafica_consulta(fecha: str, temperatura: float, clima: str, ciudad: str, puntos_forecast: dict) -> None:
    """Genera y guarda la gráfica sin bloquear la ejecución."""
    hora_actual = datetime.now().hour
    horas = list(range(24))
    temps_24h = _interpolar_24h(puntos_forecast, temperatura)

    fig, ax = plt.subplots(figsize=(11, 5))
    
    # Estética de la gráfica
    ax.plot(horas, temps_24h, color="#E8622A", linewidth=2.5, zorder=2)
    ax.fill_between(horas, temps_24h, alpha=0.12, color="#E8622A")

    # Destacar punto actual
    ax.scatter([hora_actual], [temperatura], color="#C04010", s=100, zorder=5)
    ax.annotate(f"{temperatura}°C", xy=(hora_actual, temperatura), xytext=(0, 10),
                textcoords="offset points", ha="center", fontweight="bold", color="#C04010")

    ax.set_title(f"Pronóstico Diario: {ciudad} ({fecha})", fontsize=13, fontweight="bold")
    ax.set_xticks(range(0, 24))
    ax.set_xticklabels([f"{h}h" for h in range(24)], rotation=45, fontsize=8)
    ax.set_facecolor("#FAFAFA")
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    plt.tight_layout()

    # Guardado seguro con Path
    nombre_limpio = ciudad.lower().replace(' ', '_')
    ruta_img = _DIR_SALIDA / f"grafica_{nombre_limpio}_{fecha}.png"
    
    plt.savefig(ruta_img, dpi=150, bbox_inches="tight")
    plt.close(fig)  # Libera la memoria RAM
    print(f"Gráfica guardada en: {ruta_img.name}")


def exportar_excel(fecha, temperatura, clima, humedad, viento, alerta, recomendacion, ciudad) -> str:
    """Exportación profesional a Excel con openpyxl."""
    nombre_limpio = ciudad.lower().replace(' ', '_')
    ruta_excel = _DIR_SALIDA / f"clima_{nombre_limpio}_{fecha}.xlsx"

    wb = Workbook()
    ws = wb.active
    ws.title = "Reporte"

    # Estilos básicos
    fuente_h = Font(name="Arial", bold=True, color="FFFFFF")
    relleno_h = PatternFill("solid", start_color="2D6A9F")
    
    # Encabezados
    ws.merge_cells("A1:B1")
    ws["A1"] = f"REPORTE: {ciudad}"
    ws["A1"].font = Font(bold=True, size=14)
    
    ws["A2"], ws["B2"] = "PARÁMETRO", "VALOR"
    for cell in [ws["A2"], ws["B2"]]:
        cell.font = fuente_h
        cell.fill = relleno_h
        cell.alignment = Alignment(horizontal="center")

    # Datos
    datos = [
        ("Fecha", fecha),
        ("Temperatura", f"{temperatura}°C"),
        ("Condición", clima),
        ("Humedad", f"{humedad}%"),
        ("Viento", f"{viento} m/s"),
        ("Alertas", alerta if alerta else "Ninguna"),
        ("Recomendación", recomendacion)
    ]

    for i, (k, v) in enumerate(datos, start=3):
        ws.cell(row=i, column=1, value=k).font = Font(bold=True)
        ws.cell(row=i, column=2, value=v).alignment = Alignment(wrap_text=True)

    ws.column_dimensions["A"].width = 20
    ws.column_dimensions["B"].width = 50

    wb.save(str(ruta_excel))
    print(f" Excel generado en: {ruta_excel.name}")
    return str(ruta_excel)
 