from flask import Flask, request, jsonify
import threading

app = Flask(__name__, static_folder='static', static_url_path='')

# Lock para evitar problemas de concurrencia
lock = threading.Lock()

# STOCK GLOBAL DE INGREDIENTES
ingredientes_stock = {
    "Jugo de tomate": 10,
    "Vodka": 10,
    "Hielo": 50,
    "Apio": 10,
    "Fresa": 10,
    "Crema batida": 10,
    "Ron": 10,
    "Refresco de cola": 10,
    "Limón": 15,
    "Cereza": 10,
    "Café": 10,
    "Hierbabuena": 10,
    "Piña": 10,
    "Crema de coco": 10,
    "Jugo de naranja": 10,
    "Whiskey": 10,
    "Aceite": 20,
    "Sal": 20,
    "Pollo": 15,
    "Salsa": 15,
    "Queso": 15,
    "Totopos": 10,
    "Frijoles": 10,
    "Maíz palomero": 10,
    "Mantequilla": 10,
    "Papas": 20,
    "Sazonador": 10,
    "Aceitunas": 10,
    "Pollo empanizado": 10,
    "Ketchup": 10,
    "Tortilla": 20,
    "Pan": 10,
    "Carne": 15,
    "Lechuga": 10,
    "Tomate": 10,
    "Pepperoni": 10,
    "Aderezo César": 10
}

# PRODUCTOS 
productos = [
    # BEBIDAS
    {"id": 1, "nombre": "Bloody Mary", "precio": 120.0, "disponible": True, "tiempoPreparacion": 600, "tipo": "BEBIDA", "imagen": "/img/producto_Bebida_blodyMary.png",
     "ingredientes": [
         {"nombre": "Jugo de tomate", "cantidad": 1},
         {"nombre": "Vodka", "cantidad": 1},
         {"nombre": "Hielo", "cantidad": 1},
         {"nombre": "Apio", "cantidad": 1}
     ]},

    {"id": 2, "nombre": "Cóctel Rosa", "precio": 110.0, "disponible": True, "tiempoPreparacion": 450, "tipo": "BEBIDA", "imagen": "/img/producto_Bebida_coctelRosa.png",
     "ingredientes": [
         {"nombre": "Fresa", "cantidad": 1},
         {"nombre": "Crema batida", "cantidad": 1},
         {"nombre": "Hielo", "cantidad": 1}
     ]},

    {"id": 3, "nombre": "Cuba Libre", "precio": 100.0, "disponible": True, "tiempoPreparacion": 300, "tipo": "BEBIDA", "imagen": "/img/producto_Bebida_cuba.png",
     "ingredientes": [
         {"nombre": "Ron", "cantidad": 1},
         {"nombre": "Refresco de cola", "cantidad": 1},
         {"nombre": "Limón", "cantidad": 1},
         {"nombre": "Hielo", "cantidad": 1}
     ]},

    {"id": 4, "nombre": "Margarita Fresa", "precio": 130.0, "disponible": True, "tiempoPreparacion": 500, "tipo": "BEBIDA", "imagen": "/img/producto_Bebida_margaritaFresa.png",
     "ingredientes": [
         {"nombre": "Fresa", "cantidad": 1},
         {"nombre": "Limón", "cantidad": 1},
         {"nombre": "Hielo", "cantidad": 1}
     ]},

    {"id": 5, "nombre": "Margarita Limón", "precio": 125.0, "disponible": True, "tiempoPreparacion": 480, "tipo": "BEBIDA", "imagen": "/img/producto_Bebida_MargaritaLimon.png",
     "ingredientes": [
         {"nombre": "Limón", "cantidad": 1},
         {"nombre": "Hielo", "cantidad": 1}
     ]},

    {"id": 6, "nombre": "Martini", "precio": 140.0, "disponible": True, "tiempoPreparacion": 300, "tipo": "BEBIDA", "imagen": "/img/producto_Bebida_martini.png",
     "ingredientes": [
         {"nombre": "Vodka", "cantidad": 1},
         {"nombre": "Cereza", "cantidad": 1}
     ]},

    {"id": 7, "nombre": "Martini Café", "precio": 145.0, "disponible": False, "tiempoPreparacion": 350, "tipo": "BEBIDA", "imagen": "/img/producto_Bebida_martiniCafe.png",
     "ingredientes": [
         {"nombre": "Café", "cantidad": 1},
         {"nombre": "Vodka", "cantidad": 1},
         {"nombre": "Crema batida", "cantidad": 1}
     ]},

    {"id": 8, "nombre": "Mojito", "precio": 115.0, "disponible": True, "tiempoPreparacion": 420, "tipo": "BEBIDA", "imagen": "/img/producto_Bebida_mojito.png",
     "ingredientes": [
         {"nombre": "Ron", "cantidad": 1},
         {"nombre": "Hierbabuena", "cantidad": 1},
         {"nombre": "Limón", "cantidad": 1},
         {"nombre": "Hielo", "cantidad": 1}
     ]},

    {"id": 9, "nombre": "Piña Colada", "precio": 135.0, "disponible": True, "tiempoPreparacion": 550, "tipo": "BEBIDA", "imagen": "/img/producto_Bebida_piñaColada.png",
     "ingredientes": [
         {"nombre": "Piña", "cantidad": 1},
         {"nombre": "Crema de coco", "cantidad": 1},
         {"nombre": "Hielo", "cantidad": 1},
         {"nombre": "Cereza", "cantidad": 1},
         {"nombre": "Crema batida", "cantidad": 1}
     ]},

    {"id": 10, "nombre": "Sex On The Beach", "precio": 150.0, "disponible": True, "tiempoPreparacion": 500, "tipo": "BEBIDA", "imagen": "/img/producto_Bebida_sexOnTheBeach.png",
     "ingredientes": [
         {"nombre": "Jugo de naranja", "cantidad": 1},
         {"nombre": "Vodka", "cantidad": 1},
         {"nombre": "Hielo", "cantidad": 1},
         {"nombre": "Cereza", "cantidad": 1}
     ]},

    {"id": 11, "nombre": "Whiskey", "precio": 160.0, "disponible": True, "tiempoPreparacion": 200, "tipo": "BEBIDA", "imagen": "/img/producto_Bebida_whiskey.png",
     "ingredientes": [
         {"nombre": "Whiskey", "cantidad": 1},
         {"nombre": "Hielo", "cantidad": 1}
     ]},

    # BOTANAS
    {"id": 12, "nombre": "Aros de cebolla", "precio": 80.0, "disponible": True, "tiempoPreparacion": 900, "tipo": "BOTANA", "imagen": "/img/producto_Botana_arosDeCebolla.jpg",
     "ingredientes": [
         {"nombre": "Aros de cebolla", "cantidad": 1},
         {"nombre": "Aceite", "cantidad": 1},
         {"nombre": "Sal", "cantidad": 1}
     ]},

    {"id": 13, "nombre": "Boneless", "precio": 120.0, "disponible": True, "tiempoPreparacion": 1200, "tipo": "BOTANA", "imagen": "/img/producto_Botana_boneless.png",
     "ingredientes": [
         {"nombre": "Pollo", "cantidad": 1},
         {"nombre": "Salsa", "cantidad": 1}
     ]},

    {"id": 14, "nombre": "Cacahuates", "precio": 50.0, "disponible": True, "tiempoPreparacion": 300, "tipo": "BOTANA", "imagen": "/img/producto_Botana_cacahuates.png",
     "ingredientes": [
         {"nombre": "Sal", "cantidad": 1}
     ]},

    {"id": 15, "nombre": "Dedos de queso", "precio": 90.0, "disponible": True, "tiempoPreparacion": 900, "tipo": "BOTANA", "imagen": "/img/producto_Botana_dedosDeQueso.png",
     "ingredientes": [
         {"nombre": "Queso", "cantidad": 1},
         {"nombre": "Aceite", "cantidad": 1}
     ]},

    {"id": 16, "nombre": "Nachos", "precio": 100.0, "disponible": True, "tiempoPreparacion": 900, "tipo": "BOTANA", "imagen": "/img/producto_Botana_nachos.png",
     "ingredientes": [
         {"nombre": "Totopos", "cantidad": 1},
         {"nombre": "Queso", "cantidad": 1},
         {"nombre": "Frijoles", "cantidad": 1},
         {"nombre": "Salsa", "cantidad": 1}
     ]},

    {"id": 17, "nombre": "Palomitas", "precio": 60.0, "disponible": True, "tiempoPreparacion": 600, "tipo": "BOTANA", "imagen": "/img/producto_Botana_palomitas.png",
     "ingredientes": [
         {"nombre": "Maíz palomero", "cantidad": 1},
         {"nombre": "Mantequilla", "cantidad": 1},
         {"nombre": "Sal", "cantidad": 1}
     ]},

    {"id": 18, "nombre": "Papas sazonadas", "precio": 85.0, "disponible": True, "tiempoPreparacion": 900, "tipo": "BOTANA", "imagen": "/img/producto_Botana_papasSazonadas.png",
     "ingredientes": [
         {"nombre": "Papas", "cantidad": 1},
         {"nombre": "Sazonador", "cantidad": 1}
     ]},

    {"id": 19, "nombre": "Papas francesas", "precio": 80.0, "disponible": True, "tiempoPreparacion": 900, "tipo": "BOTANA", "imagen": "/img/producto_Botana_papasFrancesas.png",
     "ingredientes": [
         {"nombre": "Papas", "cantidad": 1},
         {"nombre": "Sal", "cantidad": 1}
     ]},

    {"id": 20, "nombre": "Papas", "precio": 70.0, "disponible": True, "tiempoPreparacion": 800, "tipo": "BOTANA", "imagen": "/img/producto_Botana_papas.png",
     "ingredientes": [
         {"nombre": "Papas", "cantidad": 1}
     ]},

    {"id": 21, "nombre": "Aceitunas", "precio": 65.0, "disponible": True, "tiempoPreparacion": 300, "tipo": "BOTANA", "imagen": "/img/producto_Botana_aceitunas.png",
     "ingredientes": [
         {"nombre": "Aceitunas", "cantidad": 1}
     ]},

    {"id": 22, "nombre": "Nuggets", "precio": 95.0, "disponible": True, "tiempoPreparacion": 900, "tipo": "BOTANA", "imagen": "/img/producto_Botana_nuggets.png",
     "ingredientes": [
         {"nombre": "Pollo empanizado", "cantidad": 1},
         {"nombre": "Ketchup", "cantidad": 1}
     ]},

    # COMIDAS
    {"id": 23, "nombre": "Quesadilla", "precio": 90.0, "disponible": True, "tiempoPreparacion": 800, "tipo": "COMIDA", "imagen": "/img/producto_Comida_quesadilla.png",
     "ingredientes": [
         {"nombre": "Tortilla", "cantidad": 1},
         {"nombre": "Queso", "cantidad": 1}
     ]},

    {"id": 24, "nombre": "Hamburguesa de carne", "precio": 130.0, "disponible": True, "tiempoPreparacion": 1200, "tipo": "COMIDA", "imagen": "/img/producto_Comida_hamburguesa.png",
     "ingredientes": [
         {"nombre": "Pan", "cantidad": 1},
         {"nombre": "Carne", "cantidad": 1},
         {"nombre": "Queso", "cantidad": 1},
         {"nombre": "Lechuga", "cantidad": 1},
         {"nombre": "Tomate", "cantidad": 1},
         {"nombre": "Ketchup", "cantidad": 1}
     ]},

    {"id": 25, "nombre": "Pizza de Pepperoni", "precio": 150.0, "disponible": True, "tiempoPreparacion": 1500, "tipo": "COMIDA", "imagen": "/img/producto_Comida_pizza.png",
     "ingredientes": [
         {"nombre": "Queso", "cantidad": 1},
         {"nombre": "Pepperoni", "cantidad": 1},
         {"nombre": "Salsa", "cantidad": 1}
     ]},

    {"id": 26, "nombre": "Tacos", "precio": 100.0, "disponible": True, "tiempoPreparacion": 900, "tipo": "COMIDA", "imagen": "/img/producto_Comida_tacos.png",
     "ingredientes": [
         {"nombre": "Tortilla", "cantidad": 1},
         {"nombre": "Carne", "cantidad": 1},
         {"nombre": "Salsa", "cantidad": 1},
         {"nombre": "Sal", "cantidad": 1}
     ]},

    {"id": 27, "nombre": "Ensalada César", "precio": 110.0, "disponible": True, "tiempoPreparacion": 700, "tipo": "COMIDA", "imagen": "/img/producto_Comida_ensaladaCesar.png",
     "ingredientes": [
         {"nombre": "Lechuga", "cantidad": 1},
         {"nombre": "Pollo", "cantidad": 1},
         {"nombre": "Aderezo César", "cantidad": 1}
     ]},

    {"id": 28, "nombre": "Filete de carne", "precio": 180.0, "disponible": True, "tiempoPreparacion": 1600, "tipo": "COMIDA", "imagen": "/img/producto_Comida_fileteDeCarne.png",
     "ingredientes": [
         {"nombre": "Carne", "cantidad": 1},
         {"nombre": "Sal", "cantidad": 1},
         {"nombre": "Aceite", "cantidad": 1}
     ]}
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
        disponible = p["disponible"] and hay_stock_producto(p)

        resultado.append({
            "id": p["id"],
            "nombre": p["nombre"],
            "tipo": p["tipo"],
            "precio": p["precio"],
            "tiempoPreparacion": p["tiempoPreparacion"],
            "imagen": p["imagen"],
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