
from rest_framework.serializers import ModelSerializer
from rest_framework.pagination import PageNumberPagination
from pills.models import Pill
from users.models import SearchHistory



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


class PillSearchLogSerializer(ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = (
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