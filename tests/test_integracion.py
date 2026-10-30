"""Pruebas de integración HTTP: ruta Flask, filtros y plantilla HTML."""
import re
from unittest.mock import patch
from app import app


PRODUCTOS = [(1, "Arroz", "Alimentos", 5000, 12), (2, "Pan", "Alimentos", 2000, 0), (3, "Leche", "Lácteos", 4000, 0)]


def test_inicio_muestra_productos_existentes():
    with patch("app.obtener_productos", return_value=PRODUCTOS):
        respuesta = app.test_client().get("/")
    assert respuesta.status_code == 200
    assert b"Arroz" in respuesta.data
    assert b"Leche" in respuesta.data


def test_consulta_categoria_filtra_respuesta_html():
    with patch("app.obtener_productos", return_value=PRODUCTOS):
        respuesta = app.test_client().get("/?categoria=Alimentos")
    assert respuesta.status_code == 200
    assert b"Arroz" in respuesta.data
    assert b"Leche" not in respuesta.data


def test_consulta_agotados_filtra_respuesta_html():
    with patch("app.obtener_productos", return_value=PRODUCTOS):
        respuesta = app.test_client().get("/?agotados=1")
    assert respuesta.status_code == 200

    contenido_tabla = re.search(
        rb"<tbody>(.*?)</tbody>",
        respuesta.data,
        re.S
    ).group(1)

    assert b"Pan" in contenido_tabla
    assert b"Leche" in contenido_tabla
    assert b"Arroz" not in contenido_tabla


def test_consulta_combinada_filtra_respuesta_html():
    with patch("app.obtener_productos", return_value=PRODUCTOS):
        respuesta = app.test_client().get("/?categoria=Alimentos&agotados=1")
    assert respuesta.status_code == 200

    contenido_tabla = re.search(
        rb"<tbody>(.*?)</tbody>",
        respuesta.data,
        re.S
    ).group(1)

    assert b"Pan" in contenido_tabla
    assert b"Arroz" not in contenido_tabla
    assert b"Leche" not in contenido_tabla
