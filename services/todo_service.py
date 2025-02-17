from repositories.todo_repository import TodoRepository


class TodoService:
    def __init__(self):
        self.todo_repository = TodoRepository()

    def create_todo(self, title, user_id):
        return self.todo_repository.create(title, user_id)

    def get_all_todos(self, user_id):
        return self.todo_repository.get_all_by_user(user_id)

    def get_todo_by_id(self, todo_id):
        todo = self.todo_repository.get_by_id(todo_id)
        if not todo:
            raise Exception("Todo not found")
        return todo

    def update_todo(self, todo_id, title=None, completed=None):
        todo = self.get_todo_by_id(todo_id)
        return self.todo_repository.update(todo, title, completed)

    def delete_todo(self, todo_id):
        todo = self.get_todo_by_id(todo_id)
        self.todo_repository.delete(todo)
