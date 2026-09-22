import requests
from bs4 import BeautifulSoup


SITEMAP_URL = "https://www.petitchef.es/upload_data/sitemaps/recipe-es.xml"


def get_recipe_urls(limit=10):
    response = requests.get(SITEMAP_URL)
    soup = BeautifulSoup(response.text, "xml")
    urls = [loc.get_text(strip=True) for loc in soup.select("url > loc")]
    return urls[:limit]

if __name__ == "__main__":
    urls = get_recipe_urls(limit=50)
    print(len(urls))
    print(urls[:3])