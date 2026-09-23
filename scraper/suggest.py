from llm import get_category
from db import get_recipes_by_category


def suggest_recipes(user_input: str, limit: int = 5) -> list:
    category = get_category(user_input)
    return get_recipes_by_category(category, limit)


if __name__ == "__main__":
    results = suggest_recipes("quiero algo para almorzar fresquito")
    for result in results:
        print(result["title"])