import jwt
from datetime import datetime, timedelta
from config import Config


def generate_access_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(seconds=Config.JWT_ACCESS_EXPIRES),
    }
    token = jwt.encode(payload, Config.JWT_ACCESS_SECRET, algorithm="HS256")
    return token


def generate_refresh_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(seconds=Config.JWT_REFRESH_EXPIRES),
    }
    token = jwt.encode(payload, Config.JWT_REFRESH_SECRET, algorithm="HS256")
    return token


def verify_access_token(token):
    try:
        payload = jwt.decode(token, Config.JWT_ACCESS_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Access token expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid access token")


def verify_refresh_token(token):
    try:
        payload = jwt.decode(token, Config.JWT_REFRESH_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Refresh token expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid refresh token")
