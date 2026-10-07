# Informe Técnico: Análisis de Sensores Industriales y Big Data

## 5. Las 5 V aplicadas al proyecto

La siguiente tabla detalla cómo se manifiestan las dimensiones del Big Data dentro del sistema de monitoreo industrial desarrollado:

| Dimensión V | Relación con el Sistema de Sensores | Ejemplo Concreto | Origen del Ejemplo |
| :--- | :--- | :--- | :--- |
| **Volumen** | Se refiere al gran volumen de datos masivos generados de forma masiva por la infraestructura de sensores instalada en las plantas. | Los **100,000 registros** de telemetría procesados en el archivo `sensores_industriales.csv` que abarcan múltiples lecturas de las 4 plantas. | **CSV actual** |
| **Velocidad** | Alude a la alta frecuencia temporal y la rapidez con la que los sensores emiten y transmiten nuevas mediciones de estado. | La recepción continua de flujos de datos en tiempo real (streaming) segundo a segundo para detectar fallas críticas al instante. | **Futura ampliación** |
| **Variedad** | Representa la diversidad de formatos, tipos y estructuras de datos generados en el ecosistema operativo de las plantas. | Integrar los datos tabulares actuales con registros de texto no estructurado, como reportes de mantenimiento o bitácoras de los técnicos. | **Futura ampliación** |
| **Veracidad** | Involucra la incertidumbre, calidad, ruido o posibles errores de calibración presentes en las mediciones físicas capturadas. | Identificar lecturas atípicas o picos de temperatura erróneos causados por fallas eléctricas transitorias del sensor y no por calor real. | **CSV actual** (gestión de datos simulados) |
| **Valor** | Representa la utilidad de negocio e inteligencia analítica obtenida al transformar los datos crudos en decisiones operativas. | Detectar que la **Planta 3 acumuló 1,777 alertas** de temperatura superior a 85 °C para justificar intervenciones de mantenimiento preventivo. | **CSV actual** (resultado del análisis) |

## 6. Tipos de datos y procesamiento tradicional

### Clasificación de los elementos
* **El CSV de sensores:** **Estructurado**, ya que posee un formato tabular estricto con filas, columnas definidas y un esquema relacional claro.
* **Un mensaje JSON enviado por un sensor:** **Semiestructurado**, debido a que organiza la información mediante pares de clave-valor y etiquetas jerárquicas sin un esquema tabular fijo.
* **Una fotografía de una máquina:** **No estructurado**, por tratarse de un archivo multimedia de imagen compuesto por píxeles y matrices visuales sin una estructura de texto predefinida.
* **El texto libre de un reporte de mantenimiento:** **No estructurado**, dado que consiste en redacción en lenguaje natural elaborada por los operarios sin un formato rígido o preestablecido.

### ¿Por qué 100,000 registros no convierten automáticamente al archivo en Big Data?
Tener 100,000 registros representa un volumen moderado de datos que una computadora personal común y una biblioteca tradicional como `pandas` procesan en pocos segundos en memoria RAM (en este caso, el archivo pesa pocos megabytes). El concepto de **Big Data** no depende exclusivamente de una cantidad numérica fija de filas, sino de superar las capacidades de almacenamiento, procesamiento y gestión de una sola máquina (las famosas "V" de volumen, velocidad y variedad superadas).

### Limitaciones al aumentar la escala
Si el sistema evoluciona y se escala masivamente (por ejemplo, millones de registros por segundo desde cientos de plantas simultáneas), aparecerían las siguientes limitaciones técnicas:
1. **Saturación de Memoria RAM:** Un archivo de gigabytes o terabytes ya no cabría en la memoria principal de una computadora estándar, provocando desbordamientos (*Out of Memory*).
2. **Cuellos de botella en procesamiento secuencial:** Herramientas tradicionales basadas en un único núcleo de procesamiento (*single-node*) como Pandas colapsarían al intentar calcular agregaciones o filtros pesados.
3. **Infraestructura y latencia de red:** La transferencia y almacenamiento centralizado tradicional se volverían ineficientes, requiriendo arquitecturas distribuidas (como Apache Spark o clústeres en la nube).

---

## 7. Batch y Streaming

* **Tipo de procesamiento realizado y justificación:** El programa desarrollado implementa **procesamiento por lotes (Batch)**. Esto se justifica porque el script lee de forma estática un archivo CSV ya almacenado (`sensores_industriales.csv`), procesando los 100,000 registros de manera global en una sola ejecución secuencial.
* **Enfoque para emitir alertas pocos segundos después de recibir una lectura > 85 °C:** Se debe utilizar un enfoque de **Streaming (procesamiento en tiempo real)**. Dado que la criticidad exige una respuesta inmediata para prevenir fallos operativos, el sistema requiere una arquitectura basada en eventos (con herramientas como Apache Kafka o Apache Flink) que analice cada lectura en el preciso instante en que es generada y transmitida por el sensor.
* **Enfoque para generar un resumen al terminar el día:** Se debe utilizar un enfoque **Batch (por lotes)**. Al tratarse de un reporte periódico diferido (que no requiere inmediatez segundo a segundo), es sumamente eficiente acumular la información de toda la jornada y procesarla en un bloque consolidado al cierre del día.

---

## 8. Lambda y Kappa

* **Escenario A (combinar ruta que recalcula el historial por lotes con otra que procesa mediciones recientes rápidamente):** Corresponde a la **Arquitectura Lambda**. 
  * *Justificación:* Utiliza una capa de procesamiento por lotes (*Batch Layer*) para corregir y analizar todo el historial con precisión, combinada con una capa de velocidad (*Speed Layer*) que procesa los datos en tiempo real para minimizar la latencia de las alertas recientes. Ambas se unifican en una capa de servicio (*Serving Layer*).
  * *Diagrama conceptual:*
    [Ingesta de Datos] ---> [Capa de Batch] ---> [Capa de Servicio] ---> [Vista Consolidada]
                    ---> [Capa de Velocidad] ---^
* **Escenario B (una sola lógica de procesamiento de eventos y conservar las mediciones para volver a procesarlas cuando sea necesario):** Corresponde a la **Arquitectura Kappa**.
  * *Justificación:* Elimina la doble ruta de procesamiento de Lambda y maneja absolutamente todo el flujo (tanto histórico como en tiempo real) a través de un único motor de procesamiento de streams (como Apache Flink o Kafka Streams) que almacena los datos de forma inmutable para permitir reanalizarlos reteniéndolos o reproduciéndolos cuando se requiera.
  * *Diagrama conceptual:*
    [Ingesta de Datos] ---> [Log de Eventos / Storage (Kafka)] ---> [Stream Processing Engine] ---> [Vista / Salida]

---

## 9. Analítica descriptiva, predictiva y prescriptiva

* **Descriptiva (¿Qué pasó?):** 
  1. Se analizaron un total de **100,000 registros** provenientes de **40 sensores** distintos distribuidos en 4 plantas operativas[cite: 6].
  2. La **Planta 3** acumuló el mayor número crítico de incidentes con **1,777 alertas** de temperatura superior a 85 °C[cite: 6].
* **Predictiva (¿Qué podría pasar?):** 
  * *Pregunta:* ¿En qué momento exacto del próximo mes fallará mecánicamente el sensor de la Planta 3 que registró las temperaturas máximas de 104.99 °C[cite: 6]?
  * *Datos adicionales necesarios:* Historial de mantenimientos previos de la maquinaria, registros de vibración mecánica de los motores, consumo eléctrico en amperios y bitácoras de fallas anteriores asociadas a ese identificador de sensor.
* **Prescriptiva (¿Qué acción debería tomar la empresa?):** 
  * *Acción propuesta:* Programar una inspección técnica presencial y el reemplazo preventivo del componente de enfriamiento en la Planta 3 antes de que concluya la semana operativa.
  * *Información a revisar previamente:* Correlacionar el histórico de falsos positivos o errores de calibración eléctrica del sensor, verificar la disponibilidad de refacciones en el inventario y analizar el costo financiero asociado a un paro parcial de la planta frente al riesgo de daño crítico por sobrecalentamiento.