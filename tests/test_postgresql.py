"""Pruebas de integración reales entre Flask y PostgreSQL."""

import os
import uuid

import psycopg2
import pytest

from app import app


@pytest.fixture
def conexion_pruebas(monkeypatch):
    """Conecta exclusivamente a la base de datos de pruebas."""

    nombre_bd = os.getenv("TEST_DB_NAME")

    if nombre_bd != "inventario_test":
        pytest.fail(
            "Seguridad: TEST_DB_NAME debe ser inventario_test."
        )

    monkeypatch.setenv("DB_NAME", nombre_bd)

    conexion = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=nombre_bd,
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

    yield conexion

    conexion.rollback()
    conexion.close()


def test_crud_real_postgresql(conexion_pruebas):
    """Registra, consulta, edita y elimina un producto real."""

    cliente = app.test_client()
    nombre = f"Producto prueba {uuid.uuid4().hex[:8]}"
    producto_id = None

    try:
        # 1. Registrar producto desde Flask
        respuesta = cliente.post(
            "/agregar",
            data={
                "nombre": nombre,
                "categoria": "Pruebas",
                "precio": "1000",
                "cantidad": "5",
            },
        )

        assert respuesta.status_code == 302

        # 2. Consultar directamente en PostgreSQL
        with conexion_pruebas.cursor() as cursor:
            cursor.execute(
                "SELECT id, nombre, cantidad FROM productos WHERE nombre = %s",
                (nombre,),
            )
            producto = cursor.fetchone()

        assert producto is not None
        producto_id = producto[0]
        assert producto[1] == nombre
        assert producto[2] == 5

        # 3. Editar mediante Flask
        respuesta = cliente.post(
            f"/editar/{producto_id}",
            data={
                "nombre": nombre,
                "categoria": "Pruebas",
                "precio": "1500",
                "cantidad": "8",
            },
        )

        assert respuesta.status_code == 302

        with conexion_pruebas.cursor() as cursor:
            cursor.execute(
                "SELECT precio, cantidad FROM productos WHERE id = %s",
                (producto_id,),
            )
            precio, cantidad = cursor.fetchone()

        assert float(precio) == 1500
        assert cantidad == 8

        # 4. Eliminar mediante Flask
        respuesta = cliente.post(f"/eliminar/{producto_id}")

        assert respuesta.status_code == 302

        with conexion_pruebas.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM productos WHERE id = %s",
                (producto_id,),
            )
            assert cursor.fetchone() is None

    finally:
        # Limpieza adicional si falla alguna comprobación.
        if producto_id is not None:
            conexion_pruebas.rollback()
            with conexion_pruebas.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM productos WHERE id = %s",
                    (producto_id,),
                )
            conexion_pruebas.commit()