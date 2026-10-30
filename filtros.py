"""Consultas de inventario sin modificar los registros originales."""


def filtrar_productos(productos, categoria="", solo_agotados=False):
    """Filtra filas (id, nombre, categoria, precio, cantidad) por criterios opcionales."""
    resultado = list(productos)
    if categoria:
        resultado = [p for p in resultado if str(p[2]).casefold() == categoria.casefold()]
    if solo_agotados:
        resultado = [p for p in resultado if p[4] == 0]
    return resultado
