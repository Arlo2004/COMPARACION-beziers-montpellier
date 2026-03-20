import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import os
import sys

def parse_fecha(fecha_str):
    try:
        dt = pd.to_datetime(fecha_str)
        return dt.strftime('%d/%m')
    except:
        return fecha_str

def generar_visualizacion(nombre_estacion, df_plot):
    df_plot = df_plot.copy()
    df_plot['FECHA_STR'] = df_plot['FECHA'].apply(parse_fecha)
    
    # Restamos el umbral (0.2) para que el centro del gráfico sea el riesgo
    df_plot['RR_AJUSTADA'] = df_plot['RR'] - 0.2
    
    sns.set_theme(style="white")
    plt.figure(figsize=(12, 7))
    x = range(len(df_plot))
    ancho = 0.8
    
    color_confort = chr(35) + '4a90e2' # Azul
    color_riesgo = chr(35) + 'ff9f43'  # Naranja
    
    # Creamos las barras usando la columna ajustada
    barras = plt.bar(x, df_plot['RR_AJUSTADA'], width=ancho, color=color_confort, zorder=3)
    
    # Coloreamos de naranja las barras que quedaron por debajo de la línea central (sequía)
    for i, barra in enumerate(barras):
        if df_plot['RR_AJUSTADA'].iloc[i] < 0:
            barra.set_color(color_riesgo)
            
    # Línea central roja sólida exactamente en el umbral de riesgo ajustado (0)
    plt.axhline(0, color='red', linestyle='-', linewidth=2.5, zorder=4)
    
    # Configuración de Ejes (en francés)
    plt.xticks(x, df_plot['FECHA_STR'], rotation=45)
    
    # Título dinámico y en francés
    estacion_fr = "BÉZIERS-VIAS" if "BEZIERS" in nombre_estacion else "MONTPELLIER-AÉROPORT"
    plt.title(f'MONITEUR DE RISQUE RGA : {estacion_fr}\n', pad=20, fontsize=14, fontweight='bold')
    
    # Formatear el eje Y para mostrar los valores originales de lluvia
    # (sumamos 0.2 a la etiqueta para que el centro diga 0.2 y no 0)
    formatter = ticker.FuncFormatter(lambda y, pos: f"{y + 0.2:g}")
    plt.gca().yaxis.set_major_formatter(formatter)
    
    plt.ylabel('Précipitations (mm)', fontsize=12, fontweight='bold')
    
    sns.despine(left=True, bottom=True)
    plt.grid(axis='y', color='gray', linestyle=':', alpha=0.5, zorder=0)
    plt.tight_layout()
    
    os.makedirs('comparativa_ciudades', exist_ok=True)
    n_file = "beziers" if "BEZIERS" in nombre_estacion else "montpellier"
    plt.savefig(f'comparativa_ciudades/pronostico_{n_file}.png', dpi=300)
    plt.close()

def main():
    url = "https://raw.githubusercontent.com/Arlo2004/updated-_recolector/refs/heads/main/herault_pronostico_meteofrance.csv"

    try:
        # dropout las filas que no tengan RR para evitar errores de graficación
        df = pd.read_csv(url).dropna(subset=['RR'])
    except:
        sys.exit(1)
        
    for est in ['BEZIERS-VIAS', 'MONTPELLIER-AEROPORT']:
        df_est = df[df['NOM_POSTE'] == est]
        if not df_est.empty:
            generar_visualizacion(est, df_est)

if __name__ == "__main__":
    main()
    url = "https://raw.githubusercontent.com/Arlo2004/updated-_recolector/refs/heads/main/herault_pronostico_meteofrance.csv"
    
   
