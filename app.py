import logging
import time

from flask import Flask, Response, g, render_template, request, redirect, url_for
from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST,
)

from database import obtener_productos, obtener_conexion
from filtros import filtrar_productos

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

app.logger.setLevel(logging.INFO)

HTTP_REQUESTS = Counter(
    "http_requests_total",
    "Total de solicitudes HTTP",
    ["method", "endpoint", "http_status"],
)

HTTP_ERRORS = Counter(
    "http_errors_total",
    "Total de respuestas HTTP con error",
    ["method", "endpoint", "http_status"],
)

HTTP_IN_PROGRESS = Gauge(
    "http_requests_in_progress",
    "Solicitudes HTTP en curso",
    ["method", "endpoint"],
)

HTTP_REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "Duracion de las solicitudes HTTP en segundos",
    ["method", "endpoint"],
)


@app.before_request
def iniciar_medicion():
    if request.path == "/metrics":
        return

    g.inicio_solicitud = time.perf_counter()
    g.endpoint_metrica = request.url_rule.rule if request.url_rule else "desconocido"

    HTTP_IN_PROGRESS.labels(
        method=request.method,
        endpoint=g.endpoint_metrica,
    ).inc()


@app.after_request
def finalizar_medicion(response):
    if request.path == "/metrics":
        return response

    if not hasattr(g, "inicio_solicitud"):
        return response

    metodo = request.method
    endpoint = g.endpoint_metrica
    estado = str(response.status_code)

    HTTP_REQUESTS.labels(
        method=metodo,
        endpoint=endpoint,
        http_status=estado,
    ).inc()

    if response.status_code >= 400:
        HTTP_ERRORS.labels(
            method=metodo,
            endpoint=endpoint,
            http_status=estado,
        ).inc()

    HTTP_REQUEST_DURATION.labels(
        method=metodo,
        endpoint=endpoint,
    ).observe(time.perf_counter() - g.inicio_solicitud)

    HTTP_IN_PROGRESS.labels(
        method=metodo,
        endpoint=endpoint,
    ).dec()

    return response


@app.get("/metrics")
def metricas():
    return Response(generate_latest(), content_type=CONTENT_TYPE_LATEST)

@app.route("/")
def inicio():
    todos_los_productos = obtener_productos()
    categoria = request.args.get("categoria", "").strip()
    solo_agotados = request.args.get("agotados") == "1"
    categorias = sorted({str(p[2]) for p in todos_los_productos if p[2] is not None}, key=str.casefold)
    productos = filtrar_productos(todos_los_productos, categoria, solo_agotados)

    return render_template(
        "index.html",
        productos=productos,
        total_productos=len(todos_los_productos),
        categorias=categorias,
        categoria_seleccionada=categoria,
        solo_agotados=solo_agotados
    )


@app.route("/agregar", methods=["POST"])
def agregar_producto():
    nombre = request.form["nombre"]
    categoria = request.form["categoria"]
    precio = request.form["precio"]
    cantidad = request.form["cantidad"]

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        INSERT INTO productos (nombre, categoria, precio, cantidad)
        VALUES (%s, %s, %s, %s)
        """,
        (nombre, categoria, precio, cantidad)
    )

    conexion.commit()

    app.logger.info(
        "Producto agregado | nombre=%s | categoria=%s",
        nombre,
        categoria,
    )

    cursor.close()
    conexion.close()

    return redirect(url_for("inicio"))


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_producto(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    if request.method == "POST":

        nombre = request.form["nombre"]
        categoria = request.form["categoria"]
        precio = request.form["precio"]
        cantidad = request.form["cantidad"]

        cursor.execute(
            """
            UPDATE productos
            SET nombre = %s,
                categoria = %s,
                precio = %s,
                cantidad = %s
            WHERE id = %s
            """,
            (nombre, categoria, precio, cantidad, id)
        )

        conexion.commit()

        app.logger.info(
            "Producto actualizado | id=%s | nombre=%s",
            id,
            nombre,
        )

        cursor.close()
        conexion.close()

        return redirect(url_for("inicio"))

    cursor.execute(
        "SELECT * FROM productos WHERE id = %s",
        (id,)
    )

    producto = cursor.fetchone()

    cursor.close()
    conexion.close()

    return render_template(
        "editar.html",
        producto=producto
    )

@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar_producto(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM productos WHERE id = %s",
        (id,)
    )

    conexion.commit()

    app.logger.info(
        "Producto eliminado | id=%s",
        id,
    )

    cursor.close()
    conexion.close()

    return redirect(url_for("inicio"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)