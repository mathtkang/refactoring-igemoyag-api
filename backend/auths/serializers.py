from rest_framework.serializers import ModelSerializer, ValidationError
from users.models import User


class CreateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "username",
            # password를 입력하면 hashed된 pw가 db에 저장된다.
        )


class ValidationSerializer(ModelSerializer):
    # password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError("비밀번호는 최소 8자 이상이어야 합니다.")
        return value
    
    class Meta:
        model = User
        fields = ("email", "username", "password",)