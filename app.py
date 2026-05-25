from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
INGREDIENTES_PATH = DATA_DIR / "ingredientes.json"
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

SINONIMOS = {
    "pechuga": "pollo",
    "pechuga de pollo": "pollo",
    "muslo": "pollo",
    "pollo": "pollo",
    "carne": "res",
    "carne de res": "res",
    "carne molida": "res",
    "ternera": "res",
    "salmón": "salmon",
    "salmon": "salmon",
    "tilapia": "tilapia",
    "merluza": "pescado",
    "atún": "pescado",
    "atun": "pescado",
    "camarón": "camaron",
    "camaron": "camaron",
    "camarones": "camaron",
    "brócoli": "brocoli",
    "jitomate": "tomate",
    "palta": "aguacate",
    "huevos": "huevo",
    "papa": "papas",
    "patata": "papas",
    "maíz": "maiz",
    "choclo": "maiz",
    "harina": "harina de trigo",
    "trigo": "harina de trigo",
    "yogurt": "yogur",
    "queso": "queso fresco",
}


@st.cache_data
def cargar_ingredientes() -> dict[str, dict[str, float]]:
    with INGREDIENTES_PATH.open("r", encoding="utf-8") as archivo:
        return json.load(archivo)


@st.cache_resource
def cargar_modelo_y_escalador():
    modelo = joblib.load(MODELO_PATH)
    escalador = joblib.load(ESCALADOR_PATH)
    return modelo, escalador


@st.cache_data
def cargar_metricas() -> dict:
    if not METRICAS_PATH.exists():
        return {}

    with METRICAS_PATH.open("r", encoding="utf-8") as archivo:
        return json.load(archivo)


def normalizar_ingredientes(texto: str) -> list[str]:
    ingredientes = []

    for ingrediente in texto.split(","):
        nombre = ingrediente.lower().strip()
        if not nombre:
            continue
        ingredientes.append(SINONIMOS.get(nombre, nombre))

    return ingredientes


def calcular_nutrientes(ingredientes: list[str], base_ingredientes: dict[str, dict[str, float]]) -> tuple[dict[str, float], list[str], list[str]]:
    totales = {columna: 0.0 for columna in FEATURE_COLUMNS}
    encontrados = []
    no_encontrados = []

    for ingrediente in ingredientes:
        datos = base_ingredientes.get(ingrediente)

        if not datos:
            no_encontrados.append(ingrediente)
            continue

        encontrados.append(ingrediente)
        for columna in FEATURE_COLUMNS:
            totales[columna] += float(datos[columna])

    return totales, encontrados, no_encontrados


def calcular_score_salud(nutrientes: dict[str, float], cantidad_ingredientes: int) -> int:
    score = 0

    if nutrientes["fibra_g"] > 5:
        score += 2
    if nutrientes["grasas_g"] < 10:
        score += 2
    if nutrientes["azucares_g"] < 10:
        score += 2
    if nutrientes["proteinas_g"] > 15:
        score += 1
    if cantidad_ingredientes >= 3:
        score += 1
    if nutrientes["carbohidratos_g"] <= 60:
        score += 1
    if nutrientes["tiempo_min"] <= 45:
        score += 1

    return min(10, max(0, score))


def generar_recomendaciones(resultado: dict) -> list[str]:
    nutrientes = resultado["nutrientes"]
    encontrados = set(resultado["ingredientes_encontrados"])
    recomendaciones = []

    if nutrientes["grasas_g"] > 15:
        recomendaciones.append("Reduce ingredientes altos en grasa como aceite, mantequilla o mucho queso.")
    if nutrientes["fibra_g"] < 5:
        recomendaciones.append("Agrega verduras o legumbres para subir la fibra: brocoli, lechuga, lentejas o garbanzos.")
    if nutrientes["azucares_g"] > 12:
        recomendaciones.append("Baja los ingredientes con más azúcar y acompaña con verduras frescas.")
    if "res" in encontrados or "cerdo" in encontrados:
        recomendaciones.append("Puedes cambiar carne roja o cerdo por pollo, pescado o legumbres.")
    if "queso" in encontrados or "queso fresco" in encontrados:
        recomendaciones.append("Modera la cantidad de queso o usa una versión más baja en grasa.")
    if resultado["score_saludabilidad"] >= 8:
        recomendaciones.append("La combinación está muy bien balanceada. Mantén proteínas, fibra y grasas moderadas.")
    if not recomendaciones:
        recomendaciones.append("La comida está en un punto intermedio: mejora el balance agregando una verdura y una fuente de fibra.")

    return recomendaciones


def analizar_comida(texto_ingredientes: str) -> dict:
    base_ingredientes = cargar_ingredientes()
    modelo, escalador = cargar_modelo_y_escalador()

    ingredientes = normalizar_ingredientes(texto_ingredientes)
    nutrientes, encontrados, no_encontrados = calcular_nutrientes(ingredientes, base_ingredientes)

    if not encontrados:
        raise ValueError("No se reconoció ningún ingrediente de la lista.")

    X_usuario = np.array([[nutrientes[columna] for columna in FEATURE_COLUMNS]])
    X_usuario_scaled = escalador.transform(X_usuario)

    prediccion = int(modelo.predict(X_usuario_scaled)[0])
    probabilidades = modelo.predict_proba(X_usuario_scaled)[0]
    confianza = float(probabilidades[prediccion])
    score = calcular_score_salud(nutrientes, len(encontrados))

    resultado = {
        "saludable": bool(prediccion),
        "confianza": confianza,
        "score_saludabilidad": score,
        "nutrientes": nutrientes,
        "ingredientes_encontrados": encontrados,
        "ingredientes_no_encontrados": no_encontrados,
    }
    resultado["recomendaciones"] = generar_recomendaciones(resultado)

    return resultado


def mostrar_desglose_nutricional(nutrientes: dict[str, float]) -> None:
    etiquetas = {
        "proteinas_g": "Proteínas",
        "carbohidratos_g": "Carbohidratos",
        "azucares_g": "Azúcares",
        "fibra_g": "Fibra",
        "grasas_g": "Grasas",
        "tiempo_min": "Tiempo",
    }

    cols = st.columns(3)
    for indice, columna in enumerate(FEATURE_COLUMNS):
        unidad = "min" if columna == "tiempo_min" else "g"
        cols[indice % 3].metric(etiquetas[columna], f"{nutrientes[columna]:.1f} {unidad}")

    chart_data = {
        etiquetas[columna]: nutrientes[columna]
        for columna in FEATURE_COLUMNS
        if columna != "tiempo_min"
    }
    st.bar_chart(chart_data)


def main() -> None:
    st.set_page_config(page_title="Analizador de comidas", page_icon="AI", layout="centered")

    st.title("Analizador inteligente de comidas")
    st.caption("Predice si una comida es saludable a partir de sus ingredientes y valores nutricionales.")

    if not MODELO_PATH.exists() or not ESCALADOR_PATH.exists():
        st.error(
            "Faltan los archivos del modelo. Ejecuta primero: python scripts/entrenar_modelo.py"
        )
        st.stop()

    metricas = cargar_metricas()
    if metricas:
        st.info(f"Modelo cargado. Precisión de prueba: {metricas.get('precision', 0) * 100:.2f}%")

    ejemplos = {
        "Ensalada de pollo": "pollo, lechuga, tomate, cebolla, aguacate",
        "Hamburguesa": "res, pan, queso, aceite",
        "Pescado con verduras": "salmon, brocoli, zanahoria, arroz",
        "Camarones con quinoa": "camaron, quinoa, tomate, aguacate",
        "Almuerzo tradicional": "pollo, papas, yuca, lechuga, tomate",
        "Bowl saludable": "garbanzos, aguacate, tomate, lechuga",
    }

    usar_ejemplo = st.checkbox("Usar ejemplo rápido", value=False)
    valor_inicial = ""

    if usar_ejemplo:
        ejemplo = st.selectbox("Ejemplos rápidos", list(ejemplos.keys()))
        valor_inicial = ejemplos[ejemplo]

    ingredientes = st.text_area(
        "Ingredientes separados por coma",
        value=valor_inicial,
        placeholder="Ejemplo: pollo, tomate, lechuga, cebolla",
        height=100,
    )

    if st.button("Analizar", type="primary", use_container_width=True):
        try:
            resultado = analizar_comida(ingredientes)
        except ValueError as error:
            st.warning(str(error))
            return

        st.divider()
        estado = "Saludable" if resultado["saludable"] else "No saludable"
        st.subheader(f"Resultado: {estado}")
        st.metric("Confianza del modelo", f"{resultado['confianza'] * 100:.1f}%")

        st.write("Score de salud")
        st.progress(resultado["score_saludabilidad"] / 10)
        st.write(f"{resultado['score_saludabilidad']}/10")

        st.subheader("Desglose nutricional")
        mostrar_desglose_nutricional(resultado["nutrientes"])

        st.subheader("Ingredientes reconocidos")
        st.write(", ".join(resultado["ingredientes_encontrados"]))

        if resultado["ingredientes_no_encontrados"]:
            st.warning(
                "Ingredientes no reconocidos: "
                + ", ".join(resultado["ingredientes_no_encontrados"])
            )

        st.subheader("Recomendaciones personalizadas")
        for recomendacion in resultado["recomendaciones"]:
            st.write(f"- {recomendacion}")

    with st.expander("Ingredientes disponibles"):
        ingredientes_disponibles = sorted(cargar_ingredientes().keys())
        st.write(", ".join(ingredientes_disponibles))


if __name__ == "__main__":
    main()
