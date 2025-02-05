import jwt
from datetime import datetime, timedelta
from django.conf import settings


def generate_jwt(user):
    """
    Генерирует JWT токен для пользователя.
    """
    payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': datetime.utcnow() + settings.JWT_EXPIRATION_DELTA,
        'iat': datetime.utcnow(),
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token

def decode_jwt(token):
    """
    Проверяет JWT токен.
    """

    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")
    except jwt.DecodeError:
        raise Exception("Invalid token")