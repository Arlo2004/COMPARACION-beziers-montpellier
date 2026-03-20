import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import os

def parse_fecha(fecha_str):
    try:
        dt = pd.to_datetime(fecha_str)
        return dt.strftime('%d/%m')
    except:
        return fecha_str

def generar_visualizacion(nombre_estacion, df_plot):
    df_plot = df_plot.copy()
    df_plot['FECHA_STR'] = df_plot['FECHA'].apply(parse_fecha)
    
    sns.set_theme(style="whitegrid")
    fig, ax1 = plt.subplots(figsize=(12, 7))
    
    x = range(len(df_plot))
    
    color_rr = chr(35) + '4a90e2'
    color_tm = chr(35) + 'ff9f43'
    
    # Eje 1: Lluvia (Barras) - El 0 está abajo
    ax1.bar(x, df_plot['RR'], color=color_rr, label='Precipitación (mm)', alpha=0.8)
    ax1.set_ylabel('Precipitación (mm)', color=color_rr, fontweight='bold')
    
    # Marcador de sequía: Línea roja en 0.2 y sombreado inferior
    ax1.axhline(0.2, color='red', linestyle='--', linewidth=1.5, label='Umbral RGA (0.2mm)')
    ax1.axhspan(0, 0.2, color='red', alpha=0.1)
    
    # Eje 2: Temperatura (Línea) para que no se superponga con las barras
    ax2 = ax1.twinx()
    ax2.plot(x, df_plot['TM'], color=color_tm, marker='o', linewidth=2, label='Temp. Media (°C)')
    ax2.set_ylabel('Temperatura Media (°C)', color=color_tm, fontweight='bold')
    
    # Configuración de escalas (para que el 0 siempre sea la base)
    ax1.set_ylim(0, max(df_plot['RR'].max() + 1, 2))
    ax2.set_ylim(0, max(df_plot['TM'].max() + 5, 30))
    
    # Eje X con todas las fechas del CSV
    ax1.set_xticks(x)
    ax1.set_xticklabels(df_plot['FECHA_STR'], rotation=45)
    
    plt.title(f'MONITOR DE RIESGO ESTRUCTURAL RGA: {nombre_estacion}', pad=20, fontsize=14, fontweight='bold')
    
    # Unificar leyendas
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1+h2, l1+l2, loc='upper left')
    
    plt.tight_layout()
    os.makedirs('comparativa_ciudades', exist_ok=True)
    n_file = "beziers" if "BEZIERS" in nombre_estacion else "montpellier"
    plt.savefig(f'comparativa_ciudades/pronostico_{n_file}.png', dpi=300)
    plt.close()

def main():
    # URL Publica (ya que el repo es publico
    url = "https://raw.githubusercontent.com/Arlo2004/updated-_recolector/refs/heads/main/herault_pronostico_meteofrance.csv"
    
    try:
        df = pd.read_csv(url).dropna(subset=['RR', 'TM'])
    except:
        return
    
    # Nombres exactos de tus estaciones
    for est in ['BEZIERS-VIAS', 'MONTPELLIER-AEROPORT']:
        # Filtramos y quitamos el .tail() para que salgan todos los dias de la URL
        df_est = df[df['NOM_POSTE'] == est]
        if not df_est.empty:
            generar_visualizacion(est, df_est)

if __name__ == "__main__":
    main()
    

