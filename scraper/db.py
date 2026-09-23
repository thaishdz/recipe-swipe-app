import sqlite3
import json

DB_PATH = "recipes.db"

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