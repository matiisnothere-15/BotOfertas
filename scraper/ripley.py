import logging
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def obtener_ripley() -> list[dict]:
    """Obtiene televisores desde Ripley."""
    url = "https://simple.ripley.cl/tecnologia/television-y-video/televisores"
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        res.raise_for_status()
    except Exception:
        logging.exception("Error solicitando datos a Ripley")
        return []

    soup = BeautifulSoup(res.text, "html.parser")
    productos: list[dict] = []
    for item in soup.select("div.catalog-product-item"):
        nombre = item.select_one(".catalog-product-name")
        precio = item.select_one(".catalog-product-price-regular")
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
                        "tienda": "Ripley",
                        "url": urljoin(url, enlace["href"]) if enlace else url,
                        "imagen": imagen.get("src") if imagen else None,
                    }
                )
            except Exception:
                logging.exception("Error procesando producto de Ripley")
    return productos
