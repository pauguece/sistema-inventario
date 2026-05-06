from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

# Lock para evitar problemas de concurrencia
lock = threading.Lock()

# STOCK GLOBAL DE INGREDIENTES
ingredientes_stock = {
    "Pan": 10,
    "Carne": 10,
    "Queso": 8,
    "Lechuga": 5,
    "Tomate": 5,
    "Tortilla": 10,
    "Pollo": 6,
    "Salsa": 10
}

# PRODUCTOS (2 EJEMPLOS)
productos = [
    {
        "id": 1,
        "nombre": "Hamburguesa",
        "tipo": "COMIDA",
        "ingredientes": [
            {"nombre": "Pan", "cantidad": 1},
            {"nombre": "Carne", "cantidad": 1},
            {"nombre": "Queso", "cantidad": 1},
            {"nombre": "Lechuga", "cantidad": 1},
            {"nombre": "Tomate", "cantidad": 1}
        ]
    },
    {
        "id": 2,
        "nombre": "Tacos de pollo",
        "tipo": "COMIDA",
        "ingredientes": [
            {"nombre": "Tortilla", "cantidad": 2},
            {"nombre": "Pollo", "cantidad": 1},
            {"nombre": "Salsa", "cantidad": 1}
        ]
    }
]

# BUSCAR PRODUCTO
def buscar_producto(id_producto):
    for p in productos:
        if p["id"] == id_producto:
            return p
    return None

# CALCULAR DISPONIBILIDAD
def hay_stock_producto(producto):
    for ing in producto["ingredientes"]:
        disponible = ingredientes_stock.get(ing["nombre"], 0)
        if disponible < ing["cantidad"]:
            return False
    return True

# VALIDAR STOCK (OPCIONAL)
@app.route('/validarStock', methods=['POST'])
def validar_stock():
    data = request.json
    producto_id = data.get("productoId")
    cantidad = data.get("cantidad", 1)

    producto = buscar_producto(producto_id)
    if not producto:
        return jsonify({"exito": False, "mensaje": "Producto no encontrado"}), 404

    for ing in producto["ingredientes"]:
        necesario = ing["cantidad"] * cantidad
        disponible = ingredientes_stock.get(ing["nombre"], 0)

        if disponible < necesario:
            return jsonify({
                "exito": False,
                "mensaje": f"No hay suficiente {ing['nombre']}",
                "stockActual": disponible
            }), 400

    return jsonify({"exito": True, "mensaje": "Stock disponible"})

# DESCONTAR STOCK (CLAVE)
@app.route('/descontarStock', methods=['POST'])
def descontar_stock():
    data = request.json
    productos_req = data.get("productos", [])

    with lock:

        # VALIDAR TODO
        for req in productos_req:
            producto = buscar_producto(req["productoId"])
            if not producto:
                return jsonify({
                    "exito": False,
                    "mensaje": "Producto no encontrado",
                    "stockActual": 0
                }), 404

            for ing in producto["ingredientes"]:
                necesario = ing["cantidad"] * req["cantidad"]
                disponible = ingredientes_stock.get(ing["nombre"], 0)

                if disponible < necesario:
                    return jsonify({
                        "exito": False,
                        "mensaje": f"No hay suficiente {ing['nombre']}",
                        "stockActual": disponible
                    }), 400

        # DESCONTAR TODO
        for req in productos_req:
            producto = buscar_producto(req["productoId"])
            for ing in producto["ingredientes"]:
                necesario = ing["cantidad"] * req["cantidad"]
                ingredientes_stock[ing["nombre"]] -= necesario

        return jsonify({
            "exito": True,
            "mensaje": "Comanda procesada correctamente",
            "stockActual": 0
        })

# AGREGAR STOCK
@app.route('/agregarStock', methods=['POST'])
def agregar_stock():
    data = request.json
    nombre = data.get("ingrediente")
    cantidad = data.get("cantidad")

    ingredientes_stock[nombre] = ingredientes_stock.get(nombre, 0) + cantidad

    return jsonify({
        "exito": True,
        "mensaje": "Stock agregado correctamente",
        "stockActual": ingredientes_stock[nombre]
    })

# OBTENER PRODUCTOS
@app.route('/productos', methods=['GET'])
def get_productos():
    resultado = []

    for p in productos:
        disponible = hay_stock_producto(p)

        resultado.append({
            "id": p["id"],
            "nombre": p["nombre"],
            "tipo": p["tipo"],
            "disponible": disponible,
            "ingredientes": p["ingredientes"] 
        })

    return jsonify(resultado)

# VER STOCK (DEBUG)
@app.route('/stock', methods=['GET'])
def ver_stock():
    return jsonify(ingredientes_stock)

import os
# RUN
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)