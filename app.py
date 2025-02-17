from flask import Flask, jsonify
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.exceptions import HTTPException
from container import db

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Registrasi blueprint
    from controllers.auth_controller import auth_bp
    from controllers.todo_controller import todo_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(todo_bp, url_prefix="/todos")

    # Handler error HTTPException
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        response = e.get_response()
        response.data = jsonify({"error": True, "message": e.description}).data
        response.content_type = "application/json"
        return response

    # Handler error umum
    @app.errorhandler(Exception)
    def handle_exception(e):
        return jsonify({"error": True, "message": str(e)}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=3000)
