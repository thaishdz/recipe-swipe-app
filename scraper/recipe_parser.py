import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.petitchef.es"
TEST_URL = "https://www.petitchef.es/recetas/plato/cottage-pie-pastel-de-carne-y-patatas-receta-inglesa-fid-1578918"

def scrape_recipe(url):
    try:
        response = requests.get(url, timeout=10)  # fail after 10s instead of hanging forever
        response.raise_for_status()  # raise on 4xx/5xx so error pages aren't parsed as recipes
        soup = BeautifulSoup(response.text, "html.parser")

        return {
            "title": get_title(soup),
            "category": get_category(soup),
            "difficulty": get_difficulty(soup),
            "cooking_time": get_cooking_time(soup),
            "ingredients_list": get_ingredients_list(soup),
            "steps": get_steps(soup),
            "image_header": get_image_header(soup),
        }
    except Exception as error:
        print(f"Error scrapeando {url}: {error}")
        return None

def absolute_url(src): 
    if src and src.startswith("/"): # "/imgupl/recipe/cottage-pie.jpg"
        return BASE_URL + src
    return src

def get_text_selector(page, selector):
    element = page.select_one(selector)
    return element.get_text(strip=True) if element else None

def get_title(page):
    return get_text_selector(page, "h1.title")

def get_category(page):
    return get_text_selector(page, "div.rdbi-item[title^='Tipo'] .rdbii-val")

def get_difficulty(page):
    return get_text_selector(page, "div.rdbi-item[title^='Dificultad'] .rdbii-val")

def get_cooking_time(page):
    return get_text_selector(page, "div.rdbi-item[title^='Total time'] .rdbii-val")

def get_ingredients_list(page):
    return [li.get_text(separator=" ", strip=True) for li in page.select("ul.ingredients-ul li.il label")]

def get_steps(page):
    steps = []
    for li in page.select("ul.rd-steps li"):
        img_tag = li.select_one("img")
        image = absolute_url(img_tag.get("src") if img_tag else None)
        text = li.get_text(strip=True)
        steps.append({"image": image, "text": text})
    return steps

def get_image_header(page):
    image_tag = page.select_one("div.carousel-inner img")
    return absolute_url(image_tag.get("src") if image_tag else None)

if __name__ == "__main__":
    print(scrape_recipe(TEST_URL))
