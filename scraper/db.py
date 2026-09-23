from pathlib import Path
import sqlite3
import json

DB_PATH = Path(__file__).parent / "recipes.db"

def init_db():
    connection = sqlite3.connect(DB_PATH)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            category TEXT,
            difficulty TEXT,
            cooking_time TEXT,
            image_header TEXT,
            ingredients_list TEXT,
            steps TEXT,
            scraped_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    connection.commit()
    connection.close()

def recipe_exists(url: str) -> bool:
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.execute("SELECT 1 FROM recipes WHERE url = ?", (url,))
    exists = cursor.fetchone() is not None
    connection.close()
    return exists

def save_recipe(recipe: dict, url: str):
    connection = sqlite3.connect(DB_PATH)
    connection.execute("""
        INSERT OR IGNORE INTO recipes (url, title, category, difficulty, cooking_time, image_header, ingredients_list, steps)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        url,
        recipe["title"],
        recipe["category"],
        recipe["difficulty"],
        recipe["cooking_time"],
        recipe["image_header"],
        json.dumps(recipe["ingredients_list"], ensure_ascii=False),
        json.dumps(recipe["steps"], ensure_ascii=False),
    ))
    connection.commit()
    connection.close()


def get_recipes_by_category(category: str, limit: int = 10) -> list[dict]:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.execute(
        "SELECT * FROM recipes WHERE category = ? LIMIT ?",
        (category, limit)
    )
    rows = cursor.fetchall()
    connection.close()

    recipes = []

    for row in rows:
        recipe = dict(row)
        recipe["ingredients_list"] = json.loads(recipe["ingredients_list"])
        recipe["steps"] = json.loads(recipe["steps"])
        recipes.append(recipe)
    return recipes


if __name__ == "__main__":
    recipes = get_recipes_by_category("Postre", limit=3)
    for recipe in recipes:
        print(recipe["title"], "-", recipe["difficulty"])