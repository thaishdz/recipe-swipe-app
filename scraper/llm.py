import requests

def get_category(user_input: str) -> str:
    categories = ["Plato", "Entrante", "Aperitivo", "Merienda", "Postre", "Acompañamiento", "Otro", "Bebida"]

    prompt = f"""Clasifica la petición de un usuario en UNA de estas categorías: {", ".join(categories)}

Ejemplos:
"algo rápido para desayunar" → Plato
"quiero algo dulce después de comer" → Postre
"tengo sed" → Bebida
"algo para picar antes de la cena" → Aperitivo

Ahora clasifica: "{user_input}"
Categoría:
"""
    payload = {
        "model": "qwen2.5:7b",
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0} # ollama's default is 0.8
    }

    try:
        response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=30)
        response.raise_for_status()

        category = response.json()["response"].strip()
        for c in categories:
            if c.lower() in category.lower():
                return c
        return "Otro"
    except requests.exceptions.RequestException as error:
        raise RuntimeError("The AI model is not available. Is Ollama running?") from error


if __name__ == "__main__":
    print(get_category("quiero algo rapido para cenar"))