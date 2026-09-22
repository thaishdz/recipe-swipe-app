import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.petitchef.es"
URL = "https://www.petitchef.es/recetas/plato/cottage-pie-pastel-de-carne-y-patatas-receta-inglesa-fid-1578918"

def scrape_recipe(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    try:
        title = soup.select_one("h1.title").get_text(strip=True)
        category = soup.select_one("div.rdbi-item[title^='Tipo'] .rdbii-val").get_text(strip=True)
        difficulty = soup.select_one("div.rdbi-item[title^='Dificultad'] .rdbii-val").get_text(strip=True)
        cooking_time = soup.select_one("div.rdbi-item[title^='Total time'] .rdbii-val").get_text(strip=True)
        ingredients_list = [li.get_text(separator=" ",strip=True) for li in soup.select("ul.ingredients-ul li.il label")]

        steps = []
        for li in soup.select("ul.rd-steps li"):
            img_tag = li.select_one("img")
            image = img_tag["src"] if img_tag else None
            if image and image.startswith("/"):
                image = BASE_URL + image
            
            # saca el texto del li, pero sin el contenido del span.step-img
            text = li.get_text(strip=True)
            steps.append({"image": image, "text": text})

        image_header = soup.select_one("div.carousel-inner img")["src"]
        if image_header.startswith("/"):
            image_header = BASE_URL + image_header

        return {
            "title": title,
            "category": category,
            "difficulty": difficulty,
            "cooking_time": cooking_time,
            "ingredients_list": ingredients_list,
            "steps": steps,
            "image_header": image_header,
        }
    except Exception as error:
        print(f"Error scrapeando {url}: {error}")
        return None

if __name__ == "__main__":
    print(scrape_recipe(URL))