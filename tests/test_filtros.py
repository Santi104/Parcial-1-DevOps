from filtros import filtrar_productos


PRODUCTOS = [
    (1, "Arroz", "Alimentos", 5000, 12),
    (2, "Leche", "Lácteos", 4000, 0),
    (3, "Pan", "Alimentos", 2000, 0),
]


def test_sin_filtros_conserva_todos_los_productos():
    assert filtrar_productos(PRODUCTOS) == PRODUCTOS


def test_filtro_categoria_muestra_solo_coincidencias():
    assert [p[1] for p in filtrar_productos(PRODUCTOS, "Alimentos")] == ["Arroz", "Pan"]


def test_categoria_no_existente_devuelve_lista_vacia():
    assert filtrar_productos(PRODUCTOS, "Aseo") == []


def test_categoria_no_distingue_mayusculas():
    assert len(filtrar_productos(PRODUCTOS, "alimentos")) == 2


def test_productos_agotados_son_los_de_cantidad_cero():
    assert [p[1] for p in filtrar_productos(PRODUCTOS, solo_agotados=True)] == ["Leche", "Pan"]


def test_combinar_categoria_y_agotados():
    assert [p[1] for p in filtrar_productos(PRODUCTOS, "Alimentos", True)] == ["Pan"]


def test_filtrar_no_modifica_la_lista_original():
    original = PRODUCTOS.copy()
    filtrar_productos(PRODUCTOS, "Lácteos", True)
    assert PRODUCTOS == original
