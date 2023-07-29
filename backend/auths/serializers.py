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