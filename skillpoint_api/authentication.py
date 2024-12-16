from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .utils import decode_jwt
from .models import User

class JWTAuthentication(BaseAuthentication):
    """
    Аутентификация по JWT токену.
    """
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None
        print(f"Authorization Header: {auth_header}")

        try:
            prefix, token = auth_header.split(' ')
            if prefix != 'Bearer':
                raise AuthenticationFailed("Invalid token prefix")
        except ValueError:
            raise AuthenticationFailed("Invalid Authorization header format")

        try:
            payload = decode_jwt(token)
        except Exception as e:
            raise AuthenticationFailed(str(e))

        try:
            user = User.objects.get(id=payload['user_id'])
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found")

        return (user, None)
