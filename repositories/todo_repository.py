from models import Todo
from container import db


class TodoRepository:
    def create(self, title, user_id):
        todo = Todo(title=title, user_id=user_id)
        db.session.add(todo)
        db.session.commit()
        return todo

    def get_all_by_user(self, user_id):
        return Todo.query.filter_by(user_id=user_id).all()

    def get_by_id(self, todo_id):
        return Todo.query.get(todo_id)

    def update(self, todo, title=None, completed=None):
        if title is not None:
            todo.title = title
        if completed is not None:
            todo.completed = completed
        db.session.commit()
        return todo

    def delete(self, todo):
        db.session.delete(todo)
        db.session.commit()
