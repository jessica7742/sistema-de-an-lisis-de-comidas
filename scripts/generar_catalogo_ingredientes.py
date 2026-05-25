from __future__ import annotations

import json
import random
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
INGREDIENTES_JSON = DATA_DIR / "ingredientes.json"
FEATURE_COLUMNS = [
    "proteinas_g",
    "carbohidratos_g",
    "azucares_g",
    "fibra_g",
    "grasas_g",
    "tiempo_min",
]

TARGET_GENERADOS = 2000

BASES = {
    "pollo": [31, 0, 0, 0, 3.6, 25, "carne"],
    "res": [26, 0, 0, 0, 8.5, 30, "carne"],
    "cerdo": [27, 0, 0, 0, 9, 35, "carne"],
    "pavo": [29, 0, 0, 0, 2, 25, "carne"],
    "salchicha": [12, 2, 1, 0, 22, 8, "embutido"],
    "salmon": [20, 0, 0, 0, 13, 18, "pescado"],
    "tilapia": [26, 0, 0, 0, 2.7, 15, "pescado"],
    "atun": [23, 0, 0, 0, 1, 10, "pescado"],
    "sardina": [25, 0, 0, 0, 11, 12, "pescado"],
    "trucha": [21, 0, 0, 0, 6, 16, "pescado"],
    "camaron": [24, 0.2, 0, 0, 0.3, 8, "marisco"],
    "huevo": [13, 1, 1, 0, 3.5, 10, "proteina"],
    "tofu": [8, 1.9, 0.6, 0.3, 4.8, 10, "proteina vegetal"],
    "soya texturizada": [50, 30, 7, 14, 1, 15, "proteina vegetal"],
    "lentejas": [9, 20, 2, 8, 0.4, 30, "legumbre"],
    "garbanzos": [8, 27, 3, 7, 0.6, 35, "legumbre"],
    "frijoles negros": [8.9, 23.7, 0.3, 8.7, 0.5, 40, "legumbre"],
    "arvejas": [5.4, 14, 5.7, 5.1, 0.4, 20, "legumbre"],
    "arroz": [2.7, 28, 0.1, 0.4, 0.1, 20, "grano"],
    "arroz integral": [2.6, 23, 0.4, 1.8, 0.9, 35, "grano"],
    "quinoa": [4.4, 21.3, 0.9, 2.8, 1.9, 20, "grano"],
    "avena": [13.2, 67.7, 1, 10.1, 6.5, 8, "grano"],
    "maiz": [3.4, 19, 3.2, 2.7, 1.5, 20, "grano"],
    "harina de trigo": [10, 76, 0.3, 2.7, 1, 0, "grano"],
    "pasta": [5, 30, 1, 1.5, 0.5, 12, "grano"],
    "pan": [9, 49, 5, 2.5, 1.5, 5, "grano"],
    "papas": [2, 17, 0.8, 2.2, 0.1, 25, "tuberculo"],
    "yuca": [1.4, 38, 1.7, 1.8, 0.3, 30, "tuberculo"],
    "batata": [1.6, 20, 4.2, 3, 0.1, 25, "tuberculo"],
    "platano": [1.1, 23, 12, 2.6, 0.3, 10, "fruta"],
    "tomate": [0.9, 3.9, 2.6, 1.2, 0.1, 5, "verdura"],
    "lechuga": [1.4, 2.9, 1.4, 1.3, 0.1, 3, "verdura"],
    "ensalada": [1.5, 6, 2.5, 2.5, 0.2, 5, "verdura"],
    "cebolla": [1.1, 9.3, 4.2, 1.7, 0.1, 10, "verdura"],
    "zanahoria": [0.9, 9.6, 4.7, 2.8, 0.1, 8, "verdura"],
    "brocoli": [2.8, 7, 1.5, 2.6, 0.4, 12, "verdura"],
    "espinaca": [2.9, 3.6, 0.4, 2.2, 0.4, 5, "verdura"],
    "coliflor": [1.9, 5, 1.9, 2, 0.3, 12, "verdura"],
    "pepino": [0.7, 3.6, 1.7, 0.5, 0.1, 3, "verdura"],
    "calabacin": [1.2, 3.1, 2.5, 1, 0.3, 8, "verdura"],
    "pimenton": [1, 6, 4.2, 2.1, 0.3, 7, "verdura"],
    "champiñones": [3.1, 3.3, 2, 1, 0.3, 10, "verdura"],
    "aguacate": [2, 9, 0.7, 6.7, 2.1, 5, "fruta"],
    "manzana": [0.3, 14, 10, 2.4, 0.2, 2, "fruta"],
    "banano": [1.1, 23, 12, 2.6, 0.3, 2, "fruta"],
    "pera": [0.4, 15, 10, 3.1, 0.1, 2, "fruta"],
    "naranja": [0.9, 12, 9, 2.4, 0.1, 2, "fruta"],
    "fresa": [0.7, 7.7, 4.9, 2, 0.3, 2, "fruta"],
    "leche": [3.4, 5, 5, 0, 3.3, 0, "lacteo"],
    "yogur": [10, 4, 4, 0, 3, 0, "lacteo"],
    "queso fresco": [18, 2, 1, 0, 20, 0, "lacteo"],
    "mantequilla": [0.9, 0.1, 0.1, 0, 81, 0, "grasa"],
    "aceite": [0, 0, 0, 0, 14, 0, "grasa"],
    "almendras": [21, 22, 4.4, 12.5, 49, 0, "fruto seco"],
    "mani": [26, 16, 4, 8.5, 49, 0, "fruto seco"],
}

PREPARACIONES = [
    "natural",
    "cocido",
    "asado",
    "horneado",
    "al vapor",
    "salteado",
    "guisado",
    "en sopa",
    "en ensalada",
    "a la plancha",
    "sin sal",
    "bajo en grasa",
    "integral",
    "con especias",
    "con ajo",
    "con cebolla",
    "con tomate",
    "con verduras",
    "con hierbas",
    "picado",
    "rallado",
    "en cubos",
    "molido",
    "en pure",
    "seco",
    "hidratado",
    "fermentado",
    "tostado",
    "light",
    "organico",
    "campesino",
    "criollo",
    "fresco",
    "maduro",
    "verde",
    "con limon",
    "con cilantro",
    "con perejil",
    "con comino",
    "con pimienta",
    "con paprika",
    "con oregano",
    "con albahaca",
]


def convertir_fila(valores: list[float | str]) -> dict[str, float | str]:
    datos = {columna: valores[indice] for indice, columna in enumerate(FEATURE_COLUMNS)}
    datos["categoria"] = valores[-1]
    return datos


def variante_nutricional(base: list[float | str], preparacion: str, rng: random.Random) -> dict[str, float | str]:
    datos = convertir_fila(base)
    factor = rng.uniform(0.88, 1.12)

    if preparacion in {"frito", "salteado"}:
        datos["grasas_g"] = float(datos["grasas_g"]) + 4
    if preparacion == "bajo en grasa":
        datos["grasas_g"] = float(datos["grasas_g"]) * 0.55
    if preparacion == "integral":
        datos["fibra_g"] = float(datos["fibra_g"]) * 1.35
    if preparacion in {"en sopa", "al vapor"}:
        datos["grasas_g"] = float(datos["grasas_g"]) * 0.9

    for columna in FEATURE_COLUMNS:
        datos[columna] = round(max(0, float(datos[columna]) * factor), 2)

    datos["categoria"] = str(datos["categoria"])
    return datos


def cargar_actuales() -> dict[str, dict[str, float | str]]:
    if not INGREDIENTES_JSON.exists():
        return {}

    with INGREDIENTES_JSON.open("r", encoding="utf-8") as archivo:
        return json.load(archivo)


def generar_catalogo() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    rng = random.Random(42)
    ingredientes = cargar_actuales()
    generados = 0

    for base_nombre, valores in BASES.items():
        ingredientes.setdefault(base_nombre, convertir_fila(valores))

    for base_nombre, valores in BASES.items():
        for preparacion in PREPARACIONES:
            if generados >= TARGET_GENERADOS:
                break

            nombre = f"{base_nombre} {preparacion}"
            if nombre in ingredientes:
                continue

            ingredientes[nombre] = variante_nutricional(valores, preparacion, rng)
            generados += 1

        if generados >= TARGET_GENERADOS:
            break

    contador = 1
    bases_items = list(BASES.items())
    while generados < TARGET_GENERADOS:
        base_nombre, valores = bases_items[contador % len(bases_items)]
        nombre = f"{base_nombre} preparacion {contador:04d}"
        if nombre not in ingredientes:
            ingredientes[nombre] = variante_nutricional(valores, "natural", rng)
            generados += 1
        contador += 1

    with INGREDIENTES_JSON.open("w", encoding="utf-8") as archivo:
        json.dump(ingredientes, archivo, ensure_ascii=False, indent=2)

    print(f"Ingredientes generados: {generados}")
    print(f"Total en catalogo: {len(ingredientes)}")
    print(f"Archivo actualizado: {INGREDIENTES_JSON}")


if __name__ == "__main__":
    generar_catalogo()
