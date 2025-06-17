def filtrar(lista, max_precio=350000, keywords=None):
    if keywords is None:
        keywords = ["4k", "smart"]

    ofertas = []
    for p in lista:
        nombre = p.get("nombre", "").lower()
        precio = p.get("precio", max_precio + 1)
        if precio <= max_precio and any(k in nombre for k in keywords):
            ofertas.append(p)
    return ofertas
