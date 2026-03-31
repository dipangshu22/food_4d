from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Temporary in-memory storage (replace with DB later)
foods = [
    {"id": 1, "name": "Chicken Biryani", "price": 249, "category": "Indian"},
]

orders = []
order_id_counter = 1000


# ─── MENU ─────────────────────────────

@app.route("/foods", methods=["GET"])
def get_foods():
    return jsonify(foods)


@app.route("/foods", methods=["POST"])
def add_food():
    data = request.json
    foods.append(data)
    return jsonify({"message": "Food added"})


# ─── ORDERS ───────────────────────────

@app.route("/orders", methods=["GET"])
def get_orders():
    return jsonify(orders)


@app.route("/orders", methods=["POST"])
def create_order():
    global order_id_counter
    data = request.json

    order_id_counter += 1
    order = {
        "id": order_id_counter,
        "items": data["items"],
        "status": "pending"
    }

    orders.append(order)
    return jsonify(order)


@app.route("/orders/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    data = request.json
    for order in orders:
        if order["id"] == order_id:
            order["status"] = data["status"]
            return jsonify({"message": "Updated"})
    return jsonify({"error": "Order not found"}), 404


# ─── ADMIN LOGIN ──────────────────────

@app.route("/login", methods=["POST"])
def login():
    data = request.json

    if data["username"] == "admin" and data["password"] == "crave2024":
        return jsonify({"success": True})
    
    return jsonify({"success": False}), 401


# ─── RUN ──────────────────────────────

if __name__ == "__main__":
    app.run(debug=True)