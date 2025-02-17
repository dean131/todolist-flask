from flask import Blueprint, request, jsonify
from services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)
auth_service = AuthService()


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return (
            jsonify({"error": True, "message": "Username and password are required"}),
            400,
        )
    try:
        user = auth_service.register(username, password)
        return (
            jsonify(
                {
                    "message": "User registered successfully",
                    "data": {"id": user.id, "username": user.username},
                }
            ),
            201,
        )
    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 400


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return (
            jsonify({"error": True, "message": "Username and password are required"}),
            400,
        )
    try:
        result = auth_service.login(username, password)
        return (
            jsonify(
                {
                    "message": "Login successful",
                    "data": {
                        "user": {
                            "id": result["user"].id,
                            "username": result["user"].username,
                        },
                        "access_token": result["access_token"],
                        "refresh_token": result["refresh_token"],
                    },
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 401


@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    data = request.get_json()
    refresh_token = data.get("refresh_token")
    if not refresh_token:
        return jsonify({"error": True, "message": "Refresh token is required"}), 400
    try:
        tokens = auth_service.refresh(refresh_token)
        return jsonify({"message": "Token refreshed", "data": tokens}), 200
    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 401
