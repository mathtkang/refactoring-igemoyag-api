
from rest_framework.serializers import ModelSerializer
from .models import Pill



class PillListSerializer(ModelSerializer):
    class Meta:
        model = Pill
        exclude = (
            "id",
        )


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