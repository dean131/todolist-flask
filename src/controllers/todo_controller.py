from flask import Blueprint, request, jsonify
from src.services.todo_service import TodoService
from src.repositories.todo_repository import TodoRepository

todo_blueprint = Blueprint("todo_blueprint", __name__)

# Inisialisasi repository dan service (Secara sederhana, manual DI)
todo_repository = TodoRepository()
todo_service = TodoService(todo_repository)


# CREATE
@todo_blueprint.route("/todos", methods=["POST"])
def create_todo():
    try:
        data = request.get_json()
        title = data.get("title", "")
        new_todo = todo_service.create_todo(title)
        return (
            jsonify(
                {
                    "message": "Todo created successfully",
                    "data": {
                        "id": new_todo.id,
                        "title": new_todo.title,
                        "completed": new_todo.completed,
                        "created_at": new_todo.created_at,
                        "updated_at": new_todo.updated_at,
                    },
                }
            ),
            201,
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# READ ALL
@todo_blueprint.route("/todos", methods=["GET"])
def get_all_todos():
    try:
        todos = todo_service.get_all_todos()
        results = []
        for t in todos:
            results.append(
                {
                    "id": t.id,
                    "title": t.title,
                    "completed": t.completed,
                    "created_at": t.created_at,
                    "updated_at": t.updated_at,
                }
            )
        return jsonify({"data": results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# READ BY ID
@todo_blueprint.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo_by_id(todo_id):
    try:
        todo = todo_service.get_todo_by_id(todo_id)
        if not todo:
            return jsonify({"error": "Todo not found"}), 404
        return (
            jsonify(
                {
                    "id": todo.id,
                    "title": todo.title,
                    "completed": todo.completed,
                    "created_at": todo.created_at,
                    "updated_at": todo.updated_at,
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# UPDATE
@todo_blueprint.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    try:
        data = request.get_json()
        title = data.get("title")
        completed = data.get("completed")
        updated_todo = todo_service.update_todo(
            todo_id, title=title, completed=completed
        )
        if not updated_todo:
            return jsonify({"error": "Todo not found"}), 404

        return (
            jsonify(
                {
                    "message": "Todo updated successfully",
                    "data": {
                        "id": updated_todo.id,
                        "title": updated_todo.title,
                        "completed": updated_todo.completed,
                        "created_at": updated_todo.created_at,
                        "updated_at": updated_todo.updated_at,
                    },
                }
            ),
            200,
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# DELETE
@todo_blueprint.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    try:
        deleted = todo_service.delete_todo(todo_id)
        if not deleted:
            return jsonify({"error": "Todo not found"}), 404
        return jsonify({"message": "Todo deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
