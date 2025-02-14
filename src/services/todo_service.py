class TodoService:
    def __init__(self, repository):
        self.repository = repository

    def create_todo(self, title):
        if not title or title.strip() == "":
            raise ValueError("Title is required")
        return self.repository.create_todo(title=title)

    def get_all_todos(self):
        return self.repository.get_all_todos()

    def get_todo_by_id(self, todo_id):
        todo = self.repository.get_todo_by_id(todo_id)
        if not todo:
            return None
        return todo

    def update_todo(self, todo_id, title=None, completed=None):
        # Contoh validasi tambahan
        if title is not None and title.strip() == "":
            raise ValueError("Title cannot be empty")
        return self.repository.update_todo(todo_id, title=title, completed=completed)

    def delete_todo(self, todo_id):
        return self.repository.delete_todo(todo_id)
