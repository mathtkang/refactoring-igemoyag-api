from multiprocessing import AuthenticationError
import jwt
from django.conf import settings

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from users.models import User



# class JWTAuthentication(BaseAuthentication):
#     def authenticate(self, request):
#         token = request.headers.get("Authorization")

#         # token이 없다면 none을 반환하고, 연결은 계속 유지 (api view는 호출하지만 유저는 인증하지 않는 상태)
#         if not token:
#             return None
        
#         try:
#             decoded_token = jwt.decode(
#                 token,
#                 settings.SECRET_KEY,
#                 algorithms=["HS256"],
#             )

#             # 만료된 경우: 재인증 요청
#             if 'exp' in decoded_token and decoded_token['exp'] < settings.TIME_ZONE.now().timestamp():
#                 raise AuthenticationFailed('JWT 토큰이 만료되었습니다. 재인증이 필요합니다.')

#             user_id = decoded_token.get("id")
#             if not user_id:
#                 raise AuthenticationFailed("Invalid Token")
#             user = User.objects.get(id=user_id)

#             # 토큰 갱신: 만료 시간이 얼마 남지 않았을 때 새로운 토큰 발급
#             time_until_expiration = decoded_token['exp'] - settings.TIME_ZONE.now().timestamp()

#             if time_until_expiration < settings.JWT_REFRESH_THRESHOLD:
#                 new_token = self.generate_new_token(user)
#                 return (user, new_token)
            
#             return (user, None)
        
#         # 만료된 경우
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed("JWT expired please try reauthenticate.")
#         # 유효하지 않은 경우
#         except jwt.InvalidTokenError:
#             raise AuthenticationFailed("Invalid Token")
#         # 유저가 존재하지 않는 경우
#         except User.DoesNotExist:
#             raise AuthenticationFailed("User Not Found")
        

#     # 토큰 갱신: 새로운 토큰 생성
#     def generate_new_token(self, user):
        
#         payload = {'user_id': user.id}
#         token = jwt.encode(
#             payload,
#             settings.SECRET_KEY,
#             algorithm='HS256'
#         )
#         return token


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