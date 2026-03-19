import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import os

def parse_fecha(fecha_str):
    """
    Intenta convertir la fecha a formato DD/MM.
    """
    try:
        # Se asume que matplotlib/pandas puede interpretar el formato entrante
        dt = pd.to_datetime(fecha_str, dayfirst=True)
        return dt.strftime('%d/%m')
    except:
        # Si falla, simplemente devuelve el texto original
        return fecha_str

def generar_visualizacion_rga(nombre_estacion, datos_filtrados):
    """
    Genera el gráfico de comparación climática con efecto espejo 
    para la lluvia y la temperatura media de una estación particular.
    """
    # Copiamos el DataFrame para no alterar el original
    df_plot = datos_filtrados.copy()
    
    # Procesar la fecha para que esté en formato DD/MM
    if 'FECHA' in df_plot.columns:
        df_plot['FECHA_STR'] = df_plot['FECHA'].apply(parse_fecha)
    else:
        print(f"Advertencia: No se encontró la columna FECHA para {nombre_estacion}")
        return
        
    # Invertir la temperatura para lograr el "Efecto espejo"
    df_plot['TM_INVERTIDA'] = df_plot['TM'] * -1
    
    # Configuración de estilo con Seaborn
    sns.set_theme(style="white")
    plt.figure(figsize=(10, 6))
    
    # Posiciones X (una por cada día en el dataset)
    x = range(len(df_plot))
    
    # 1. Gráfico de Lluvia (RR) -> Barras positivas hacia arriba
    plt.bar(x, df_plot['RR'], color='#4a90e2', label='Lluvia (RR) [mm]')
    
    # 2. Gráfico de Temperatura Media (TM) -> Barras negativas hacia abajo
    plt.bar(x, df_plot['TM_INVERTIDA'], color='#ff9f43', label='Temp. Media (TM) [°C]')
    
    # Línea central roja sólida marcando el nivel de cero (0)
    plt.axhline(0, color='red', linestyle='-', linewidth=2)
    
    # Personalización del Eje X: Etiquetas de las fechas rotadas a 45°
    plt.xticks(x, df_plot['FECHA_STR'], rotation=45, ha='right')
    
    # Título dinámico
    plt.title(f'PRONÓSTICO DE RIESGO ESTRUCTURAL: {nombre_estacion}', pad=20, fontsize=14, fontweight='bold')
    
    # Formatear el eje Y para arreglar los valores negativos (mostrándolos de forma positiva/absoluta)
    formatter = ticker.FuncFormatter(lambda y, pos: f"{abs(y):g}")
    plt.gca().yaxis.set_major_formatter(formatter)
    
    # Etiquetas de los ejes
    plt.ylabel('Valores (°C / mm)')
    plt.xlabel('Fecha')
    
    # Posicionamiento de la leyenda
    plt.legend(loc='best')
    
    # Limpieza: eliminar bordes superior y derecho
    sns.despine()
    
    # Ajustar para que las etiquetas no se corten
    plt.tight_layout()
    
    # Directorio de salida
    Directorio_salida = 'comparativa_ciudades'
    os.makedirs(Directorio_salida, exist_ok=True)
    
    # Validar y determinar el nombre correcto del archivo de salida
    estacion_upper = nombre_estacion.upper()
    if 'BEZIERS' in estacion_upper:
        nombre_archivo = 'pronostico_beziers.png'
    elif 'MONTPELLIER' in estacion_upper:
        nombre_archivo = 'pronostico_montpellier.png'
    else:
        nombre_archivo = f"pronostico_{nombre_estacion.lower().replace(' ', '_')}.png"
        
    ruta_guardado = os.path.join(Directorio_salida, nombre_archivo)
    
    # Guardar gráfico limitando el recorte
    plt.savefig(ruta_guardado, dpi=300, bbox_inches='tight')
    plt.close()  # Cerramos la figura para liberar memoria
    print(f"-> Gráfico guardado exitosamente: '{ruta_guardado}'")

def main():
    # URL directa (Raw) del archivo en GitHub
    url_csv = "https://raw.githubusercontent.com/Arlo2004/updated-_recolector/refs/heads/main/herault_pronostico_meteofrance.csv?token=GHSAT0AAAAAADYEPQLLLOXJNGB37LVK3VNU2N4PSPA"
    
    print(f"Descargando datos desde GitHub...")
    try:
        df = pd.read_csv(url_csv)
    except Exception as e:
        print(f"Error al descargar o procesar el archivo CSV: {e}")
        return
        
    # Extraer y analizar datos a 7 días para cada estación solicitada
    estaciones_solicitadas = ['BEZIERS-COURTADE', 'MONTPELLIER-AEROPORT']
    
    for estacion in estaciones_solicitadas:
        # Filtrar por nombre de la estación
        df_estacion = df[df['NOM_POSTE'] == estacion].copy()
        
        if not df_estacion.empty:
            # Seleccionamos únicamente los primeros 7 días con 'head(7)' 
            # (asumiendo que es el pronóstico de los próximos 7 días)
            df_estacion_7_dias = df_estacion.head(7)
            generar_visualizacion_rga(estacion, df_estacion_7_dias)
        else:
            print(f"Nota: No se encontraron datos para la estación '{estacion}'")

if __name__ == "__main__":
    main()
