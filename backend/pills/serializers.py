from django import forms
from rest_framework.serializers import ModelSerializer
from rest_framework.pagination import PageNumberPagination
from pills.models import Pill, UploadFile
from users.models import Favorite,SearchHistory
from users.serializers import TinyUserSerializer


class PillListSerializer(ModelSerializer):
    class Meta:
        model = Pill
        exclude = (
            "id",
        )
        pagination_class = PageNumberPagination


class PillDetailSerializer(ModelSerializer):
    class Meta:
        model = Pill
        fields = (
            "item_num",
            "item_name",
            "image",
            "bit",
            "sungbun",
            "efcy_qesitm",
            "use_method_qesitm",
            "se_qesitm",
            "atpn_qesitm",
            "deposit_method_qesitm",
            "intrc_qesitm"
        )


class TinyPillSerializer(ModelSerializer):
    class Meta:
        model = Pill
        fields = (
            "item_num",
        )


class SearchLogSerializer(ModelSerializer):
    # custom serializer
    user = TinyUserSerializer(read_only=True)
    pill = PillDetailSerializer(read_only=True)

    class Meta:
        model = SearchHistory
        fields = "__all__"


class LikedPillSerializer(ModelSerializer):
    # custom serializer
    user = TinyUserSerializer(read_only=True)
    pill = TinyPillSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = "__all__"


class ImageFormSerializer(forms.ModelForm):
    class Meta:
        model = UploadFile
        fields = "__all__"