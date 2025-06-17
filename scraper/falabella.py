import logging
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def obtener_falabella() -> list[dict]:
    """Obtiene la lista de televisores desde Falabella."""
    url = "https://www.falabella.com/falabella-cl/category/cat40725/TVs"
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        res.raise_for_status()
    except Exception:
        logging.exception("Error solicitando datos a Falabella")
        return []

    soup = BeautifulSoup(res.text, "html.parser")
    productos: list[dict] = []
    for item in soup.select("li[class*=pod]"):
        nombre = item.select_one(".pod-subTitle")
        precio = item.select_one(".copy10")
        imagen = item.select_one("img")
        enlace = item.find("a", href=True)
        if nombre and precio:
            try:
                productos.append(
                    {
                        "nombre": nombre.text.strip(),
                        "precio": int(
                            precio.text.strip().replace("$", "").replace(".", "")
                        ),
                        "tienda": "Falabella",
                        "url": urljoin(url, enlace["href"]) if enlace else url,
                        "imagen": imagen.get("src") if imagen else None,
                    }
                )
            except Exception:
                logging.exception("Error procesando producto de Falabella")
    return productos
