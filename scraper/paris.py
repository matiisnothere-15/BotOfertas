import logging
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def obtener_paris() -> list[dict]:
    """Obtiene televisores desde Paris."""
    url = "https://www.paris.cl/electronica/television/"
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        res.raise_for_status()
    except Exception:
        logging.exception("Error solicitando datos a Paris")
        return []

    soup = BeautifulSoup(res.text, "html.parser")
    productos: list[dict] = []
    for item in soup.select("div.product-tile-wrapper"):
        nombre = item.select_one(".product-name")
        precio = item.select_one(".product-sales-price")
        imagen = item.select_one("img")
        enlace = item.find("a", href=True)
        if nombre and precio:
            try:
                productos.append(
                    {
                        "nombre": nombre.text.strip(),
                        "precio": int(
                            precio.text.strip()
                            .replace("$", "")
                            .replace(".", "")
                            .replace("Internet", "")
                            .strip()
                        ),
                        "tienda": "Paris",
                        "url": urljoin(url, enlace["href"]) if enlace else url,
                        "imagen": imagen.get("src") if imagen else None,
                    }
                )
            except Exception:
                logging.exception("Error procesando producto de Paris")
    return productos
