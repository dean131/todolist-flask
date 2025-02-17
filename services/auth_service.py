import bcrypt
from repositories.user_repository import UserRepository
from utils.jwt_helper import (
    generate_access_token,
    generate_refresh_token,
    verify_refresh_token,
)


class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()

    def register(self, username, password):
        if self.user_repository.get_by_username(username):
            raise Exception("Username already exists")
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        user = self.user_repository.create(username, hashed.decode("utf-8"))
        return user

    def login(self, username, password):
        user = self.user_repository.get_by_username(username)
        if not user or not bcrypt.checkpw(
            password.encode("utf-8"), user.password.encode("utf-8")
        ):
            raise Exception("Invalid credentials")
        access_token = generate_access_token(user.id)
        refresh_token = generate_refresh_token(user.id)
        return {
            "user": user,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    def refresh(self, refresh_token):
        payload = verify_refresh_token(refresh_token)
        user_id = payload.get("user_id")
        new_access = generate_access_token(user_id)
        new_refresh = generate_refresh_token(user_id)
        return {"access_token": new_access, "refresh_token": new_refresh}
