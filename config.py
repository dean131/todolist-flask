import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///db.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_SECRET = os.getenv("JWT_ACCESS_SECRET", "access-secret-key")
    JWT_REFRESH_SECRET = os.getenv("JWT_REFRESH_SECRET", "refresh-secret-key")
    JWT_ACCESS_EXPIRES = int(os.getenv("JWT_ACCESS_EXPIRES", 900))  # 15 menit
    JWT_REFRESH_EXPIRES = int(os.getenv("JWT_REFRESH_EXPIRES", 604800))  # 7 hari
