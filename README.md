# Sistema de análisis de comidas con Streamlit

Este proyecto toma un modelo de inteligencia artificial entrenado, lo guarda en formato `.pkl`, guarda también el `StandardScaler`, usa un archivo JSON de ingredientes y ofrece una aplicación web con Streamlit.

## Estructura

```text
.
├── app.py
├── data/
│   └── ingredientes.json
├── models/
│   ├── modelo_comidas.pkl
│   ├── escalador_comidas.pkl
│   └── metricas_modelo.json
├── scripts/
│   └── entrenar_modelo.py
└── requirements.txt
```

## Instalación

```bash
pip install -r requirements.txt
```

## Entrenar y guardar el modelo

```bash
python scripts/generar_catalogo_ingredientes.py
python scripts/entrenar_modelo.py
```

Este comando genera:

- `data/ingredientes.json` con más de 2000 ingredientes
- `models/modelo_comidas.pkl`
- `models/escalador_comidas.pkl`
- `models/metricas_modelo.json`
- `data/datos_entrenamiento.xlsx`

## Ejecutar la aplicación web

```bash
streamlit run app.py
```

La aplicación permite escribir ingredientes separados por coma, calcula los nutrientes, aplica el escalador, ejecuta el modelo y muestra:

- Resultado saludable o no saludable
- Porcentaje de confianza
- Score de salud
- Desglose nutricional
- Gráfico de barras
- Recomendaciones personalizadas
