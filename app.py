from flask import Flask
from src.models.todo import db
from src.controllers.todo_controller import todo_blueprint
from dotenv import load_dotenv
import os


def create_app():
    load_dotenv()
    app = Flask(__name__)

    db_url = os.getenv("DATABASE_URL", "sqlite:///default.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(todo_blueprint)
    return app


if __name__ == "__main__":
    flask_app = create_app()
    APP_PORT = os.getenv("APP_PORT", 5000)
    flask_app.run(debug=True, port=APP_PORT)
