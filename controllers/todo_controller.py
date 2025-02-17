from flask import Blueprint, request, jsonify
from services.todo_service import TodoService
from utils.jwt_helper import verify_access_token

todo_bp = Blueprint("todo", __name__)
todo_service = TodoService()


def get_token_from_header():
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split(" ")[1]
    return None


@todo_bp.route("/", methods=["POST"])
def create_todo():
    token = get_token_from_header()
    if not token:
        return jsonify({"error": True, "message": "Access token required"}), 401
    try:
        payload = verify_access_token(token)
        user_id = payload.get("user_id")
    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 401

    data = request.get_json()
    title = data.get("title")
    if not title:
        return jsonify({"error": True, "message": "Title is required"}), 400
    try:
        todo = todo_service.create_todo(title, user_id)
        return (
            jsonify(
                {
                    "message": "Todo created successfully",
                    "data": {
                        "id": todo.id,
                        "title": todo.title,
                        "completed": todo.completed,
                    },
                }
            ),
            201,
        )
    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 400


@todo_bp.route("/", methods=["GET"])
def get_todos():
    token = get_token_from_header()
    if not token:
        return jsonify({"error": True, "message": "Access token required"}), 401
    try:
        payload = verify_access_token(token)
        user_id = payload.get("user_id")
    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 401

    todos = todo_service.get_all_todos(user_id)
    todos_data = [
        {"id": todo.id, "title": todo.title, "completed": todo.completed}
        for todo in todos
    ]
    return jsonify({"message": "Success", "data": todos_data}), 200


@todo_bp.route("/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    token = get_token_from_header()
    if not token:
        return jsonify({"error": True, "message": "Access token required"}), 401
    try:
        verify_access_token(token)
    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 401

    try:
        todo = todo_service.get_todo_by_id(todo_id)
        return (
            jsonify(
                {
                    "message": "Success",
                    "data": {
                        "id": todo.id,
                        "title": todo.title,
                        "completed": todo.completed,
                    },
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 404


@todo_bp.route("/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    token = get_token_from_header()
    if not token:
        return jsonify({"error": True, "message": "Access token required"}), 401
    try:
        verify_access_token(token)
    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 401

    data = request.get_json()
    title = data.get("title")
    completed = data.get("completed")
    try:
        todo = todo_service.update_todo(todo_id, title, completed)
        return (
            jsonify(
                {
                    "message": "Todo updated successfully",
                    "data": {
                        "id": todo.id,
                        "title": todo.title,
                        "completed": todo.completed,
                    },
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 400


@todo_bp.route("/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    token = get_token_from_header()
    if not token:
        return jsonify({"error": True, "message": "Access token required"}), 401
    try:
        verify_access_token(token)
    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 401

    try:
        todo_service.delete_todo(todo_id)
        return jsonify({"message": "Todo deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 400
