from rest_framework.serializers import ModelSerializer
from users.models import Favorite, User
from pills.models import Pill

class FavoritePillListSerializer(ModelSerializer):
    class Meta:
        model = Pill
        fields = (
            "item_num",
            "item_name",
            "image",
            "sungbun",
            "use_method_qesitm",
        )


class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "username",
        )