from flask import Flask, render_template, request, redirect, url_for
from database import obtener_productos, obtener_conexion
from filtros import filtrar_productos

app = Flask(__name__)


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

    cursor.close()
    conexion.close()

    return redirect(url_for("inicio"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)