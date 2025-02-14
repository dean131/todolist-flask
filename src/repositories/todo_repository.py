from src.models.todo import Todo, db


class TodoRepository:
    def create_todo(self, title):
        new_todo = Todo(title=title)
        db.session.add(new_todo)
        db.session.commit()
        return new_todo

    def get_all_todos(self):
        return db.session.query(Todo).all()

    def get_todo_by_id(self, todo_id):
        return db.session.get(Todo, todo_id)

    def update_todo(self, todo_id, title=None, completed=None):
        todo = db.session.get(Todo, todo_id)
        if todo is None:
            return None
        if title is not None:
            todo.title = title
        if completed is not None:
            todo.completed = completed
        db.session.commit()
        return todo

    def delete_todo(self, todo_id):
        todo = db.session.get(Todo, todo_id)
        if todo is None:
            return False
        db.session.delete(todo)
        db.session.commit()
        return True
