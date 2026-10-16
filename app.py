from datetime import datetime, timezone

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

CATEGORIES = ["Mobiles", "Laptops", "Soundbars", "Printers", "TVs"]

PRODUCTS = [
    {
        "id": 1,
        "name": "Nova X Pro",
        "category": "Mobiles",
        "price": 899.00,
        "in_stock": True,
        "description": "A vivid 6.7-inch AMOLED display, pro-grade camera system, and all-day battery.",
    },
    {
        "id": 2,
        "name": "Orbit Lite 5G",
        "category": "Mobiles",
        "price": 429.00,
        "in_stock": False,
        "description": "Fast 5G performance, a smooth 120 Hz display, and a lightweight design.",
    },
    {
        "id": 3,
        "name": "StudioBook 14",
        "category": "Laptops",
        "price": 1299.00,
        "in_stock": True,
        "description": "A crisp 14-inch display and powerful performance in a slim aluminum body.",
    },
    {
        "id": 4,
        "name": "CreatorBook Pro 16",
        "category": "Laptops",
        "price": 1899.00,
        "in_stock": False,
        "description": "A color-accurate 16-inch screen with dedicated graphics for creative work.",
    },
    {
        "id": 5,
        "name": "CinemaBeam 3.1",
        "category": "Soundbars",
        "price": 349.00,
        "in_stock": True,
        "description": "Immersive Dolby Audio with a wireless subwoofer and easy HDMI eARC setup.",
    },
    {
        "id": 6,
        "name": "StudioBar Mini",
        "category": "Soundbars",
        "price": 179.00,
        "in_stock": False,
        "description": "Room-filling sound in a compact bar with Bluetooth and TV-ready connectivity.",
    },
    {
        "id": 7,
        "name": "PrintMate Color 420",
        "category": "Printers",
        "price": 229.00,
        "in_stock": True,
        "description": "Wireless all-in-one color printing, scanning, and copying for home offices.",
    },
    {
        "id": 8,
        "name": "PrintMate Eco Tank",
        "category": "Printers",
        "price": 319.00,
        "in_stock": False,
        "description": "High-volume printing with refillable ink tanks and mobile app control.",
    },
    {
        "id": 9,
        "name": "LumaView OLED 55",
        "category": "TVs",
        "price": 1499.00,
        "in_stock": True,
        "description": "Deep OLED contrast, cinematic 4K detail, and a beautifully slim profile.",
    },
    {
        "id": 10,
        "name": "LumaView QLED 65",
        "category": "TVs",
        "price": 1199.00,
        "in_stock": False,
        "description": "Bright quantum-dot color, 4K upscaling, and a smooth gaming-ready refresh rate.",
    },
]

# Demo-only storage: notifications are cleared when the Flask process restarts.
RESTOCK_NOTIFICATIONS = []


@app.get("/")
def home():
    return render_template(
        "index.html",
        products=PRODUCTS,
        categories=CATEGORIES,
    )


@app.post("/api/check-item")
def check_item():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "Send a JSON object containing product_id."}), 400

    product_id = payload.get("product_id")
    if isinstance(product_id, bool):
        return jsonify({"error": "product_id must be a valid product ID."}), 400

    try:
        product_id = int(product_id)
    except (TypeError, ValueError):
        return jsonify({"error": "product_id must be a valid product ID."}), 400

    product = next((item for item in PRODUCTS if item["id"] == product_id), None)
    if product is None:
        return jsonify({"error": "Product not found."}), 404

    if product["in_stock"]:
        return jsonify(
            {
                "available": True,
                "product": product,
                "message": "Great news - this item is available.",
            }
        )

    notification = {
        "id": len(RESTOCK_NOTIFICATIONS) + 1,
        "product_id": product["id"],
        "product_name": product["name"],
        "category": product["category"],
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": "Restock requested",
    }
    RESTOCK_NOTIFICATIONS.append(notification)

    return jsonify(
        {
            "available": False,
            "product": product,
            "message": "This item is out of stock. The store owner has been notified.",
            "notification": notification,
        }
    )


@app.get("/api/owner/notifications")
def owner_notifications():
    return jsonify(
        {
            "notifications": list(reversed(RESTOCK_NOTIFICATIONS)),
            "count": len(RESTOCK_NOTIFICATIONS),
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
