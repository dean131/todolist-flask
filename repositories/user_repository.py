from models import User
from container import db


class UserRepository:
    def get_by_username(self, username):
        return User.query.filter_by(username=username).first()

    def create(self, username, password):
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return user

    def get_by_id(self, user_id):
        return User.query.get(user_id)
