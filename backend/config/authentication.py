from multiprocessing import AuthenticationError
import jwt
from django.conf import settings

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from users.models import User


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("Authorization")
        if not token:
            return None  # token이 없다면 none을 반환하고, 연결은 계속 유지 (api view는 호출하지만 유저는 인증하지 않는 상태)
        decoded = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"],
        )
        id = decoded.get("id")
        if not id:
            raise AuthenticationFailed("Invalid Token")
        try:
            user = User.objects.get(id=id)
            return (user, None)
        except User.DoesNotExist:
            raise AuthenticationFailed("User Not Found")