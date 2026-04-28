'''
Módulo: graficas.py
'''

import matplotlib

matplotlib.use('Agg') 

import matplotlib.pyplot as plt
import math
from pathlib import Path
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# Configuración de rutas universal con Pathlib (ESTO ERA LO QUE FALTABA)
_BASE_DIR = Path(__file__).resolve().parent
_DIR_SALIDA = _BASE_DIR / "reportes"
_DIR_SALIDA.mkdir(parents=True, exist_ok=True)

def generar_reporte(resultado_analizador: dict, datos_api: dict, ciudad: str) -> None:
    """Coordina la generación de la gráfica y el Excel."""
    try:
        import api_cliente
    except ImportError:
        print("Error crítico: No se encontró 'api_cliente.py' en la carpeta.")
        return

    fecha = resultado_analizador.get("fecha", datetime.now().strftime("%Y-%m-%d"))
    temperatura = resultado_analizador.get("temperatura", 0)
    clima = resultado_analizador.get("clima", "Desconocido")
    alerta = resultado_analizador.get("alerta", "")
    recomend = resultado_analizador.get("recomendacion", "")
    
    humedad = datos_api.get("main", {}).get("humidity", "N/A")
    viento = datos_api.get("wind", {}).get("speed", "N/A")

    # Obtener datos del forecast
    puntos_forecast = api_cliente.obtener_forecast(ciudad)

    # Ejecución blindada: si uno falla, el otro intenta seguir
    try:
        grafica_consulta(fecha, temperatura, clima, ciudad, puntos_forecast)
    except Exception as e:
        print(f"[-] Error en gráfica: {e}")

    try:
        exportar_excel(fecha, temperatura, clima, humedad, viento, alerta, recomend, ciudad)
    except Exception as e:
        print(f"[-] Error en Excel: {e}")

def _interpolar_24h(puntos_reales: dict, temp_actual: float) -> list:
    """Genera la curva de temperatura para el gráfico."""
    hora_actual = datetime.now().hour
    base = temp_actual - 4
    return [
        round(base + (temp_actual - base) * math.sin(math.pi * max(h - 5, 0) / 18), 1)
        if 5 <= h <= 23 else base
        for h in range(24)
    ]

def grafica_consulta(fecha, temperatura, clima, ciudad, puntos_forecast):
    """Crea y guarda la imagen PNG de la gráfica."""
    hora_actual = datetime.now().hour
    horas = list(range(24))
    temps_24h = _interpolar_24h(puntos_forecast, temperatura)
    temps_24h[hora_actual] = temperatura # Forzar valor exacto actual

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(horas, temps_24h, color="#E8622A", linewidth=2.5, zorder=2)
    ax.fill_between(horas, temps_24h, alpha=0.15, color="#E8622A")

    # Punto de la hora actual
    ax.scatter([hora_actual], [temperatura], color="#C04010", s=100, zorder=5)
    ax.annotate(f"{temperatura}°C", xy=(hora_actual, temperatura), xytext=(0, 10),
                textcoords="offset points", ha="center", fontweight="bold", color="#C04010")

    ax.set_title(f"Pronóstico: {ciudad} ({fecha})", fontsize=14, fontweight="bold")
    ax.set_xticks(range(24))
    ax.set_xticklabels([f"{h}h" for h in range(24)], rotation=45, fontsize=8)
    ax.set_facecolor("#F9F9F9")
    ax.grid(True, axis='y', linestyle='--', alpha=0.5)

    plt.tight_layout()

    # Guardado seguro
    nombre_img = f"grafica_{ciudad.lower().replace(' ', '_')}_{fecha}.png"
    ruta_img = _DIR_SALIDA / nombre_img
    
    plt.savefig(str(ruta_img), dpi=150)
    plt.close(fig) # Liberar memoria inmediatamente
    print(f"[+] Gráfica guardada: {ruta_img.name}")

def exportar_excel(fecha, temperatura, clima, humedad, viento, alerta, recomendacion, ciudad):
    """Genera el archivo .xlsx con los datos procesados."""
    nombre_xls = f"clima_{ciudad.lower().replace(' ', '_')}_{fecha}.xlsx"
    ruta_xls = _DIR_SALIDA / nombre_xls

    wb = Workbook()
    ws = wb.active
    ws.title = "Reporte Climático"

    # Estilos
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill("solid", start_color="2D6A9F")

    # Estructura del Excel
    ws.merge_cells("A1:B1")
    ws["A1"] = f"REPORTE DETALLADO - {ciudad.upper()}"
    ws["A1"].font = Font(size=14, bold=True)
    
    headers = ["PARÁMETRO", "VALOR"]
    ws.append([]) # Fila vacía
    ws.append(headers)
    
    for cell in ws[3]:
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center")

    filas = [
        ("Fecha", fecha),
        ("Ciudad", ciudad),
        ("Temperatura", f"{temperatura}°C"),
        ("Condición", clima),
        ("Humedad", f"{humedad}%"),
        ("Viento", f"{viento} m/s"),
        ("Alertas", alerta if alerta else "Sin alertas"),
        ("Recomendación", recomendacion)
    ]

    for p, v in filas:
        ws.append([p, v])

    # Ajuste de columnas
    ws.column_dimensions["A"].width = 25
    ws.column_dimensions["B"].width = 50
    
    wb.save(str(ruta_xls))
    print(f"[+] Excel guardado: {ruta_xls.name}")
    return str(ruta_xls)
 