# Sistema de análisis de comidas con Streamlit

El analizador de comidas busca ayudar a las personas a identificar si una comida puede considerarse saludable o no a partir de sus ingredientes. Muchas veces una persona no sabe si la combinación de alimentos que va a consumir tiene demasiadas grasas, pocos nutrientes, mucha azúcar o poca fibra.

El sistema usa inteligencia artificial para analizar los ingredientes escritos por el usuario, calcular sus valores nutricionales y dar una predicción: saludable o no saludable. Además, entrega recomendaciones para mejorar la comida.lit.
# Problema o Necesidad
La necesidad principal es brindar una herramienta sencilla para orientar mejores decisiones alimenticias. No reemplaza a un nutricionista, pero sí ayuda a:

Revisar rápidamente una comida.
Conocer su composición nutricional.
Detectar exceso de grasa, azúcar o baja fibra.
Recibir recomendaciones personalizadas.
Aprender qué ingredientes hacen una comida más saludable.
# Librerías, Frameworks y Recursos Utilizados
Python
Pandas
NumPy
Scikit-learn
Joblib
Streamlit
JSON
Excel

Funciones:
Python: lenguaje principal del proyecto.
Pandas: manejo de datos y creación de tablas.
NumPy: cálculos numéricos.
Scikit-learn: entrenamiento del modelo de Machine Learning.
StandardScaler: normalización de datos nutricionales.
LogisticRegression: modelo de clasificación.
Joblib: guardar el modelo y el escalador en formato .pkl.
Streamlit: creación de la página web.
JSON: almacenamiento de ingredientes y recetas.
Excel: exportación de recetas y datos de entrenamiento.

# Cómo Construyeron El Dataset

El dataset se construyó a partir de:

Ingredientes + valores nutricionales + recetas clasificadas
Primero se creó un archivo de ingredientes con datos como:

proteínas
carbohidratos
azúcares
fibra
grasas
tiempo de preparación
Luego se crearon recetas clasificadas como:

1 = saludable
0 = no saludable
Después, el sistema calcula los nutrientes totales de cada receta sumando los valores de sus ingredientes. También genera variaciones numéricas para ampliar los datos de entrenamiento.

Cantidad De Entradas Utilizadas

# El sistema tiene:

2059 ingredientes en el catálogo
50 recetas base
25 saludables
25 no saludables
Cada receta genera variaciones para entrenar el modelo. Si cada receta genera 120 variaciones:

50 recetas x 120 variaciones = 6000 entradas de entrenamiento aproximadas
Modelo De Machine Learning Utilizado

Se utilizó:

Regresión Logística
Es un modelo de clasificación supervisada. Sirve para predecir si una comida pertenece a una de dos categorías:

Saludable
No saludable
Por Qué Se Eligió Ese Modelo

# Se eligió Regresión Logística porque:

Es adecuada para problemas de clasificación binaria.
Es fácil de interpretar.
Funciona bien con pocos datos estructurados.
Permite obtener probabilidades de predicción.
Es rápida para entrenar y usar en una página web.
Métricas Obtenidas

# El sistema calcula la precisión del modelo usando datos de prueba. La métrica principal es:

Accuracy / Precisión
Esta métrica indica qué porcentaje de predicciones fueron correctas.

También se generan:

Matriz de confusión
Reporte de clasificación
Coeficientes del modelo
Puedes decir:

El modelo fue evaluado usando un conjunto de prueba separado del conjunto de entrenamiento. La métrica principal fue la precisión, que indica el porcentaje de comidas clasificadas correctamente como saludables o no saludables.

# Predicciones Generadas Por El Sistema

El sistema genera predicciones como:

Resultado: Saludable
Confianza del modelo: 87.5%
Score de salud: 8/10
O:

Resultado: No saludable
Confianza del modelo: 91.2%
Score de salud: 4/10
También muestra el desglose nutricional:

Proteínas
Carbohidratos
Azúcares
Fibra
Grasas
Tiempo de preparación
Uso De Las Predicciones Para La Solución

# Las predicciones se usan para construir una herramienta práctica para el usuario. Cuando la persona escribe una comida, el sistema:

Lee los ingredientes.
Busca sus valores nutricionales.
Suma los nutrientes.
Normaliza los datos con StandardScaler.
Envía los datos al modelo IA.
Predice si la comida es saludable o no.
Muestra confianza, score y recomendaciones.
Solución Web

# La solución fue llevada a la web usando:

Streamlit
Streamlit permite convertir el código Python en una aplicación web interactiva. El usuario puede escribir ingredientes o escoger una receta rápida y presionar el botón Analizar.

Frontend y Backend

Frontend:

Es la parte visual de la aplicación. Incluye:

campo para escribir ingredientes
selector de recetas rápidas
botón Analizar
resultado saludable/no saludable
barras de progreso
tabla de nutrientes
recomendaciones
Backend:

Es la parte lógica del sistema. Se encarga de:

cargar ingredientes desde JSON
calcular nutrientes
cargar modelo .pkl
cargar escalador .pkl
normalizar datos
hacer predicción
generar recomendaciones
Reglas y Comportamientos Del Sistema

# Además del modelo IA, el sistema usa reglas para dar recomendaciones. Por ejemplo:

Si la grasa es alta, recomienda reducir aceite, mantequilla o queso.
Si la fibra es baja, recomienda agregar verduras o legumbres.
Si los azúcares son altos, recomienda reducir ingredientes dulces.
Si hay carne roja, recomienda cambiar por pollo, pescado o legumbres.
Así, la IA predice la categoría y las reglas ayudan a explicar cómo mejorar la comida.

# Cómo Funciona La Interfaz Final

La aplicación permite dos formas de uso:

Escribir ingredientes manualmente:
pollo, tomate, lechuga, arroz
Elegir una receta desde “Ejemplo rápido”.
Luego el usuario presiona:

Analizar
El sistema muestra:

Resultado de clasificación
Porcentaje de confianza
Score de salud
Nutrientes calculados
Ingredientes reconocidos
Recomendaciones personalizadas
Objetivo Final

El objetivo del sistema es ayudar al usuario a tomar mejores decisiones alimenticias usando inteligencia artificial. La aplicación convierte datos nutricionales en una respuesta clara, visual y fácil de entender.
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
