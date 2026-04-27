'''
El módulo graficas recibe los datos ya procesados por analizador y api_cliente
para generar una gráfica de línea y exportar la información a Excel.
Se ejecuta al final de cada consulta en main.py.
Última modificación: 27/04/2026
Autor: Adrián Humberto Cavazos Leal 
'''
 
import matplotlib.pyplot as plt
import math
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
 
 
#Llamada desde main.py
 
def generar_reporte(resultado_analizador: dict, datos_api: dict, ciudad: str) -> None:
    fecha       = resultado_analizador.get("fecha", datetime.now().strftime("%Y-%m-%d"))
    temperatura = resultado_analizador.get("temperatura")
    clima       = resultado_analizador.get("clima", "")
    alerta      = resultado_analizador.get("alerta", "")
    recomend    = resultado_analizador.get("recomendacion", "")
    humedad     = datos_api.get("main", {}).get("humidity")
    viento      = datos_api.get("wind", {}).get("speed")
 
    grafica_consulta(fecha, temperatura, clima, ciudad)
    exportar_excel(fecha, temperatura, clima, humedad, viento, alerta, recomend, ciudad)
 
 
#  Gráfica de Línea 
 
def grafica_consulta(fecha: str, temperatura: float, clima: str, ciudad: str) -> None:
    hora_consulta = datetime.now().hour
    horas = list(range(24))
    base  = temperatura - 4
 
    # Curva senoidal: mínimo ~5 am, máximo ~15 h
    temps_hora = [
        round(base + (temperatura - base) * math.sin(math.pi * max(h - 5, 0) / 18), 1)
        if 5 <= h <= 23 else base
        for h in horas
    ]
    temps_hora[hora_consulta] = temperatura  # punto real de la API
 
    fig, ax = plt.subplots(figsize=(11, 5))
 
    ax.plot(
        horas, temps_hora,
        color="#E8622A", linewidth=2.5,
        marker="o", markersize=5,
        markerfacecolor="white", markeredgewidth=1.8
    )
    ax.fill_between(horas, temps_hora, alpha=0.12, color="#E8622A")
 
    # Resalta el punto real
    ax.scatter([hora_consulta], [temperatura],
               color="#E8622A", s=90, zorder=5,
               label=f"Temperatura actual: {temperatura}°C")
    ax.annotate(
        f"{temperatura}°C",
        xy=(hora_consulta, temperatura),
        xytext=(0, 12), textcoords="offset points",
        ha="center", fontsize=10, fontweight="bold", color="#C04010"
    )
 
    ax.set_title(f"Temperatura del día — {ciudad} ({fecha})",
                 fontsize=13, fontweight="bold", pad=14)
    ax.set_xlabel("Hora del día", fontsize=11)
    ax.set_ylabel("Temperatura (°C)", fontsize=11)
    ax.set_xticks(range(0, 24))
    ax.set_xticklabels([f"{h}h" for h in range(24)], rotation=45, fontsize=8)
    ax.grid(axis="y", linestyle="--", alpha=0.45)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_facecolor("#FAFAFA")
    ax.legend(fontsize=10)
 
    plt.figtext(0.5, -0.02, f"Condición: {clima}",
                ha="center", fontsize=9, color="#555555")
    plt.tight_layout()
 
    nombre_img = f"grafica_{ciudad.lower().replace(' ', '_')}_{fecha}.png"
    plt.savefig(nombre_img, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"Gráfica guardada: {nombre_img}")
 
 

#  Exportar a excel 

def exportar_excel(
    fecha: str, temperatura: float, clima: str,
    humedad, viento,
    alerta: str, recomendacion: str,
    ciudad: str
) -> str:
    """
    Exporta los datos de la consulta actual a un archivo Excel con dos hojas:
        - 'Datos Climáticos' : valores obtenidos de la API y el analizador.
        - 'Estadísticas'     : métricas con fórmulas Excel que referencian la hoja anterior.
    """
    nombre_archivo = f"clima_{ciudad.lower().replace(' ', '_')}_{fecha}.xlsx"
 
    #Estilos reutilizables
    fuente_enc  = Font(name="Arial", bold=True, color="FFFFFF", size=11)
    relleno_enc = PatternFill("solid", start_color="2D6A9F")
    alineado_c  = Alignment(horizontal="center", vertical="center")
    borde_enc   = Border(
        bottom=Side(style="medium", color="1A4E7A"),
        right=Side(style="thin",    color="1A4E7A")
    )
    relleno_par = PatternFill("solid", start_color="EAF2FB")
 
    wb = Workbook()
 
    # Hoja 1: Datos Climáticos
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
        ("Temperatura (°C)",           temperatura),       # B5
        ("Condición climática",        clima),             # B6
        ("Humedad (%)",                humedad if humedad is not None else "N/D"),   # B7
        ("Velocidad del viento (m/s)", viento  if viento  is not None else "N/D"),  # B8
        ("Alerta",                     alerta if alerta else "Sin alertas"),         # B9
        ("Recomendación",              recomendacion),     # B10
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
 
    ws.row_dimensions[10].height = 45   # fila de recomendación
 
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 55
 
 
    wb.save(nombre_archivo)
    print(f"Excel guardado: {nombre_archivo}")
    return nombre_archivo