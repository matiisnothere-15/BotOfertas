import requests
from bs4 import BeautifulSoup

def obtener_paris():
    url = "https://www.paris.cl/electronica/television/"
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")
    productos = []
    for item in soup.select("div.product-tile-wrapper"):
        nombre = item.select_one(".product-name")
        precio = item.select_one(".product-sales-price")
        imagen = item.select_one("img")
        if nombre and precio:
            try:
                productos.append({
                    "nombre": nombre.text.strip(),
                    "precio": int(precio.text.strip().replace("$", "").replace(".", "").replace("Internet", "").strip()),
                    "tienda": "Paris",
                    "url": url,
                    "imagen": imagen.get("src") if imagen else None
                })
            except:
                continue
    return productos
