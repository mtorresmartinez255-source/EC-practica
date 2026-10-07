# Análisis de Sensores Industriales

Proyecto reproducible para el análisis de mediciones de temperatura y vibración de máquinas en cuatro plantas industriales utilizando Python.

## Objetivo
Analizar 100,000 registros de sensores industriales simulados para extraer métricas clave, identificar temperaturas máximas, contar alertas de temperatura (superiores a 85 °C) y exportar los resultados relevantes[cite: 1, 5].

## Descripción de los Datos
* **Naturaleza de los datos:** Los datos son **simulados**[cite: 1].
* **Volumen:** 100,000 registros de telemetría de sensores[cite: 1].
* **Variables principales:**
  * `id_registro`: Identificador único de la medición[cite: 1].
  * `fecha_hora`: Fecha y hora exacta de la lectura[cite: 1].
  * `id_sensor`: Identificador del sensor[cite: 1].
  * `planta`: Planta industrial donde está instalado el sensor (Planta 1 a 4)[cite: 1].
  * `temperatura_c`: Temperatura registrada en grados Celsius[cite: 1].
  * `vibracion_mm_s`: Vibración registrada en milímetros por segundo[cite: 1].

## Requisitos e Instalación
Tener Python instalado. Sigue estos pasos en tu terminal para configurar el entorno:

1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/mtorresmartinez255-source/EC-practica.git](https://github.com/mtorresmartinez255-source/EC-practica.git)
   cd EC-practica