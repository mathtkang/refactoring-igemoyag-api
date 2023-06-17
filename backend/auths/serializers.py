from rest_framework.serializers import ModelSerializer
# from rest_framework_simplejwt.serializers import TokenRefreshSerializer, TokenObtainPairSerializer
# from rest_framework_simplejwt.state import token_backend

from users.models import User

class CreateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "username",
            # password를 입력하면 hashed된 pw가 db에 저장된다.
        )


# # 토큰 obtain 커스터마이징
# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     # 페이로드 확장
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         token['email'] = user.email  # 확장
#         token['username'] = user.username  # 확장
#         return token

#     def validate(self, attrs):
#         data = super().validate(attrs)

#         refresh = self.get_token(self.user)

#         data['refresh'] = str(refresh)
#         data['access'] = str(refresh.access_token)
#         data['username'] = str(self.user.username)

#         return data


# # 토큰 refresh 커스터마이징
# class MyTokenRefreshSerializer(TokenRefreshSerializer):
#     def validate(self, attrs):
#         data = super(MyTokenRefreshSerializer, self).validate(attrs)
#         decoded_payload = token_backend.decode(data['access'], verify=True)
#         user_uid = decoded_payload['user_id']
#         email = decoded_payload['email']
#         username = decoded_payload['username']
#         # add filter query
#         data.update({
#             'email': email,
#             'username': username,
#         })
#         return data