from db import init_db, save_recipe, recipe_exists
from sitemap import get_recipe_urls
from recipe_parser import scrape_recipe
import time

urls = get_recipe_urls(limit=50)

init_db()

for url in urls:
    if not recipe_exists(url):
        recipe = scrape_recipe(url)
        if recipe:
            save_recipe(recipe,url)
            print(f"Saved: {recipe['title']}")
            time.sleep(1)  # pausa de 1 segundo entre requests, para que no me baneen la IP (rate limiting)