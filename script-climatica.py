import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import os
import sys

def parse_fecha(fecha_str):
    try:
        dt = pd.to_datetime(fecha_str, dayfirst=True)
        return dt.strftime('%d/%m')
    except Exception:
        return fecha_str

def generar_visualizacion(nombre_estacion, df_plot):
    if 'FECHA' not in df_plot.columns:
        print(f"Error: Columna FECHA no encontrada para {nombre_estacion}")
        return
        
    df_plot['FECHA_STR'] = df_plot['FECHA'].apply(parse_fecha)
    df_plot['TM_INVERTIDA'] = df_plot['TM'] * -1
    
    sns.set_theme(style="white")
    plt.figure(figsize=(10, 6))
    
    x = range(len(df_plot))
    
    color_lluvia = chr(35) + '4a90e2'
    color_temp = chr(35) + 'ff9f43'
    
    plt.bar(x, df_plot['RR'], color=color_lluvia, label='Lluvia (RR)')
    plt.bar(x, df_plot['TM_INVERTIDA'], color=color_temp, label='Temp. Media (TM)')
    
    plt.axhline(0.2, color='red', linestyle='-', linewidth=2, label='Umbral Equilibrio (0.2)')
    plt.axhspan(0, 0.2, color='red', alpha=0.1, label='Zona Sequia (< 0.2)')
    
    max_rr = df_plot['RR'].max() if not df_plot['RR'].empty else 0
    plt.axhspan(0.2, max(max_rr + 1, 5), color='blue', alpha=0.05, label='Zona Humedad (> 0.2)')
    
    plt.xticks(x, df_plot['FECHA_STR'], rotation=45, ha='right')
    
    plt.title(f'PRONÓSTICO DE RIESGO RGA: {nombre_estacion}', pad=20, fontsize=14, fontweight='bold')
    
    formatter = ticker.FuncFormatter(lambda y, pos: f"{abs(y):g}")
    plt.gca().yaxis.set_major_formatter(formatter)
    
    plt.ylabel('Valores (' + chr(176) + 'C / mm)')
    plt.xlabel('Fecha')
    
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    sns.despine()
    plt.tight_layout()
    
    os.makedirs('comparativa_ciudades', exist_ok=True)
    
    nombre_archivo_base = "beziers" if "BEZIERS" in nombre_estacion else "montpellier"
    ruta = os.path.join('comparativa_ciudades', f'pronostico_{nombre_archivo_base}.png')
    
    plt.savefig(ruta, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Grafico generado: {ruta}")

def main():
    url = "https://raw.githubusercontent.com/Arlo2004/updated-_recolector/main/herault_pronostico_meteofrance.csv"
    print(f"Descargando datos desde: {url}")
    
    try:
        df = pd.read_csv(url)
        print("Columnas detectadas:", df.columns.tolist())
    except Exception as e:
        print(f"Fallo al leer CSV: {e}")
        sys.exit(1)
        
    for est in ['BEZIERS-VIAS', 'MONTPELLIER-AEROPORT']:
        df_est = df[df['NOM_POSTE'] == est].copy()
        if not df_est.empty:
            print(f"Procesando datos para {est}")
            generar_visualizacion(est, df_est.tail(7))
        else:
            print(f"Alerta: No hay datos para {est}")

if __name__ == "__main__":
    main()
