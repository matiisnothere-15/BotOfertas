import requests
from bs4 import BeautifulSoup

def obtener_falabella():
    url = "https://www.falabella.com/falabella-cl/category/cat40725/TVs"
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")
    productos = []
    for item in soup.select("li[class*=pod]"):
        nombre = item.select_one(".pod-subTitle")
        precio = item.select_one(".copy10")
        imagen = item.select_one("img")
        if nombre and precio:
            try:
                productos.append({
                    "nombre": nombre.text.strip(),
                    "precio": int(precio.text.strip().replace("$", "").replace(".", "")),
                    "tienda": "Falabella",
                    "url": url,
                    "imagen": imagen.get("src") if imagen else None
                })
            except:
                continue
    return productos
