from rest_framework.serializers import ModelSerializer
from users.models import User, SearchHistory, Favorite
from pills.models import Pill


class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "username",
        )


class RoughPillSerializer(ModelSerializer):
    class Meta:
        model = Pill
        fields = (
            "item_num",
            "item_name",
            "image",
            "sungbun",
            "use_method_qesitm",
        )


class FavoritePillListSerializer(ModelSerializer):
    # custom serializer
    user = TinyUserSerializer(read_only=True)
    pill = RoughPillSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = "__all__"


class SearchHistoryPillListSerializer(ModelSerializer):
    # custom serializer
    user = TinyUserSerializer(read_only=True)
    pill = RoughPillSerializer(read_only=True)

    class Meta:
        model = SearchHistory
        fields = "__all__"