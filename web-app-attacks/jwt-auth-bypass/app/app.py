from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)

# ⚠️ INTENTIONALLY WEAK SECRET FOR LAB PURPOSES (for the exploit)
SECRET_KEY = "secret123"

# Mock user database for the lab
USERS = {
    "jan":   {"password": "password123", "role": "user"},
    "admin": {"password": "admin123",   "role": "admin"},
}

@app.route("/login", methods=["POST"])
def login():
    # Be defensive about JSON parsing so we don't 500
    data = request.get_json(silent=True) or {}

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400

    user = USERS.get(username)
    if user and user["password"] == password:
        token = jwt.encode(
            {
                "username": username,
                "role": user["role"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            },
            SECRET_KEY,
            algorithm="HS256",
        )
        return jsonify({"token": token})

    return jsonify({"message": "Invalid credentials"}), 401


@app.route("/admin", methods=["GET"])
def admin_panel():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "Token missing"}), 401

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if payload.get("role") == "admin":
            return jsonify({"message": "Welcome to the admin panel!", "payload": payload})
        return jsonify({"message": "Forbidden: admin only"}), 403

    except Exception as e:
        return jsonify({"message": "Token invalid", "error": str(e)}), 401


@app.route("/")
def home():
    return jsonify({"message": "JWT Test App Running"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
