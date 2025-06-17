def filtrar(lista, max_precio=350000, resoluciones=["4k", "smart"]):
    ofertas = []
    for p in lista:
        nombre = p["nombre"].lower()
        if p["precio"] <= max_precio and any(r in nombre for r in resoluciones):
            ofertas.append(p)
    return ofertas
