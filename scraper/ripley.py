import requests
from bs4 import BeautifulSoup

def obtener_ripley():
    url = "https://simple.ripley.cl/tecnologia/television-y-video/televisores"
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")
    productos = []
    for item in soup.select("div.catalog-product-item"):
        nombre = item.select_one(".catalog-product-name")
        precio = item.select_one(".catalog-product-price-regular")
        imagen = item.select_one("img")
        if nombre and precio:
            try:
                productos.append({
                    "nombre": nombre.text.strip(),
                    "precio": int(precio.text.strip().replace("$", "").replace(".", "")),
                    "tienda": "Ripley",
                    "url": url,
                    "imagen": imagen.get("src") if imagen else None
                })
            except:
                continue
    return productos
