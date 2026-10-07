import os
import pandas as pd

# 1. Cargar el archivo CSV utilizando ruta relativa
ruta_csv = os.path.join("data", "sensores_industriales.csv")
df = pd.read_csv(ruta_csv)

print("=== 1. CANTIDAD DE REGISTROS Y SENSORES DISTINTOS ===")
total_registros = len(df)
sensores_distintos = df["id_sensor"].nunique()
print(f"Cantidad total de registros: {total_registros}")
print(f"Cantidad de sensores distintos: {sensores_distintos}\n")

print("=== 2. TEMPERATURA PROMEDIO DE CADA PLANTA ===")
temp_promedio = df.groupby("planta")["temperatura_c"].mean()
print(temp_promedio.to_string())
print("\n")

print("=== 3. TEMPERATURA MÁXIMA Y DATOS CORRESPONDIENTES ===")
max_temp = df["temperatura_c"].max()
# Filtramos por si hay empates
df_max = df[df["temperatura_c"] == max_temp]
print(f"Temperatura máxima encontrada: {max_temp} °C")
print("Detalles del sensor/sensores con la temperatura máxima:")
print(
    df_max[["id_registro", "fecha_hora", "id_sensor", "planta", "temperatura_c"]]
    .to_string(index=False)
)
print("\n")

print("=== 4. LECTURAS CON TEMPERATURA MAYOR QUE 85 °C ===")
alertas = df[df["temperatura_c"] > 85]
total_alertas = len(alertas)
print(f"Total de lecturas con temperatura > 85 °C: {total_alertas}\n")

print("=== 5. PLANTA CON MÁS ALERTAS DE TEMPERATURA ===")
alertas_por_planta = alertas["planta"].value_counts()
print(alertas_por_planta.to_string())
planta_lider = alertas_por_planta.idxmax()
max_cant_alertas = alertas_por_planta.max()
print(
    f"\nLa planta con más alertas es {planta_lider} con {max_cant_alertas}"
    " alertas.\n"
)

print("=== 6. EXPORTAR LECTURAS CON ALERTA ===")
os.makedirs("resultados", exist_ok=True)
ruta_salida = os.path.join("resultados", "alertas.csv")
alertas.to_csv(ruta_salida, index=False)
print(f"Archivo exportado exitosamente en: {ruta_salida}")