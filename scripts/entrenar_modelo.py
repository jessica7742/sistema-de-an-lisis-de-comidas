from __future__ import annotations

import json
import random
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
INGREDIENTES_JSON = DATA_DIR / "ingredientes.json"
MODELO_PATH = MODELS_DIR / "modelo_comidas.pkl"
ESCALADOR_PATH = MODELS_DIR / "escalador_comidas.pkl"
METRICAS_PATH = MODELS_DIR / "metricas_modelo.json"
FEATURE_COLUMNS = [
    "proteinas_g",
    "carbohidratos_g",
    "azucares_g",
    "fibra_g",
    "grasas_g",
    "tiempo_min",
]


RECETAS_SALUDABLES = [
    ["pollo", "lechuga", "tomate", "cebolla"],
    ["pescado", "brocoli", "arroz"],
    ["lentejas", "tomate", "cebolla", "zanahoria"],
    ["huevo", "espinaca", "tomate"],
    ["garbanzos", "lechuga", "tomate"],
    ["quinoa", "aguacate", "tomate"],
    ["pescado", "verduras", "arroz"],
    ["salmon", "brocoli", "quinoa"],
    ["tilapia", "zanahoria", "arroz integral"],
    ["camaron", "aguacate", "tomate", "lechuga"],
    ["tofu", "brocoli", "arroz integral"],
    ["soya texturizada", "tomate", "cebolla", "lechuga"],
    ["frijoles negros", "maiz", "tomate"],
    ["lentejas", "espinaca", "zanahoria"],
    ["garbanzos", "pepino", "tomate"],
    ["huevo", "avena", "aguacate"],
    ["pollo", "papas", "lechuga", "tomate"],
    ["pavo", "quinoa", "brocoli"],
    ["atun", "lechuga", "tomate", "cebolla"],
    ["sardina", "arroz integral", "espinaca"],
    ["trucha", "papas", "brocoli"],
    ["arvejas", "zanahoria", "arroz"],
    ["tofu", "quinoa", "pimenton"],
    ["pollo", "yuca", "ensalada"],
    ["yogur", "avena", "fresa"],
]

RECETAS_NO_SALUDABLES = [
    ["res", "pan", "queso"],
    ["cerdo", "pan", "aceite"],
    ["pasta", "queso", "mantequilla"],
    ["pollo", "pan", "aceite", "queso"],
    ["res", "pasta", "queso"],
    ["cerdo", "pan", "mantequilla"],
    ["res", "papas", "mantequilla"],
    ["cerdo", "yuca", "aceite"],
    ["pollo", "harina de trigo", "aceite"],
    ["queso fresco", "pan", "mantequilla"],
    ["pasta", "aceite", "queso fresco"],
    ["res", "harina de trigo", "queso fresco"],
    ["cerdo", "papas", "queso fresco"],
    ["pan", "mantequilla", "queso"],
    ["salchicha", "pan", "queso"],
    ["res", "aceite", "papas"],
    ["cerdo", "pasta", "mantequilla"],
    ["pollo", "mantequilla", "harina de trigo"],
    ["queso", "mantequilla", "pan"],
    ["res", "yuca", "aceite"],
    ["cerdo", "maiz", "queso fresco"],
    ["pasta", "mantequilla", "aceite"],
    ["pan", "queso fresco", "aceite"],
    ["res", "pan", "mantequilla"],
    ["cerdo", "harina de trigo", "aceite"],
]


def cargar_ingredientes() -> dict[str, dict[str, float]]:
    with INGREDIENTES_JSON.open("r", encoding="utf-8") as archivo:
        return json.load(archivo)


def calcular_nutrientes(ingredientes: list[str], base: dict[str, dict[str, float]]) -> dict[str, float]:
    totales = {columna: 0.0 for columna in FEATURE_COLUMNS}

    for ingrediente in ingredientes:
        datos = base.get(ingrediente)
        if not datos:
            continue

        for columna in FEATURE_COLUMNS:
            totales[columna] += float(datos[columna])

    return totales


def generar_dataset(base: dict[str, dict[str, float]], variaciones_por_receta: int = 120) -> pd.DataFrame:
    random.seed(42)
    np.random.seed(42)
    muestras = []

    recetas = [(receta, 1) for receta in RECETAS_SALUDABLES] + [(receta, 0) for receta in RECETAS_NO_SALUDABLES]

    for ingredientes, saludable in recetas:
        nutrientes_base = calcular_nutrientes(ingredientes, base)

        for _ in range(variaciones_por_receta):
            variacion = np.random.uniform(0.85, 1.15, len(FEATURE_COLUMNS))
            fila = {
                columna: nutrientes_base[columna] * variacion[indice]
                for indice, columna in enumerate(FEATURE_COLUMNS)
            }
            fila["saludable"] = saludable
            fila["ingredientes"] = ", ".join(ingredientes)
            muestras.append(fila)

    return pd.DataFrame(muestras)


def entrenar_y_guardar() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    MODELS_DIR.mkdir(exist_ok=True)

    ingredientes = cargar_ingredientes()
    df = generar_dataset(ingredientes)
    df.to_excel(DATA_DIR / "datos_entrenamiento.xlsx", index=False)

    X = df[FEATURE_COLUMNS].values
    y = df["saludable"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.30,
        random_state=42,
        stratify=y,
    )

    escalador = StandardScaler()
    X_train_scaled = escalador.fit_transform(X_train)
    X_test_scaled = escalador.transform(X_test)

    modelo = LogisticRegression(
        random_state=42,
        max_iter=1000,
        C=1.0,
        class_weight="balanced",
    )
    modelo.fit(X_train_scaled, y_train)

    y_pred = modelo.predict(X_test_scaled)
    precision = accuracy_score(y_test, y_pred)

    metricas = {
        "precision": round(float(precision), 4),
        "muestras_entrenamiento": int(len(X_train)),
        "muestras_prueba": int(len(X_test)),
        "caracteristicas": FEATURE_COLUMNS,
        "matriz_confusion": confusion_matrix(y_test, y_pred).tolist(),
        "reporte_clasificacion": classification_report(y_test, y_pred, output_dict=True),
        "coeficientes": {
            columna: round(float(modelo.coef_[0][indice]), 6)
            for indice, columna in enumerate(FEATURE_COLUMNS)
        },
    }

    joblib.dump(modelo, MODELO_PATH)
    joblib.dump(escalador, ESCALADOR_PATH)

    with METRICAS_PATH.open("w", encoding="utf-8") as archivo:
        json.dump(metricas, archivo, ensure_ascii=False, indent=2)

    print("Modelo entrenado y exportado correctamente.")
    print(f"Modelo: {MODELO_PATH}")
    print(f"Escalador: {ESCALADOR_PATH}")
    print(f"Métricas: {METRICAS_PATH}")
    print(f"Precisión: {precision * 100:.2f}%")


if __name__ == "__main__":
    entrenar_y_guardar()
