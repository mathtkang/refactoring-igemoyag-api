from django.db import models


class Pill(models.Model):
    """Pill Model Definition"""
    item_num = models.PositiveIntegerField(
        unique=True,
    )  # 품목일련번호
    item_name = models.CharField(
        max_length=200,
    )  # 품목명
    company_name = models.CharField(
        max_length=100,
    )  # 업소명
    image = models.URLField(blank=True)  # 사진 링크
    shape = models.CharField(
        max_length=100,
    )  # 제형
    color_front = models.CharField(
        max_length=30,
    )  # 색상앞
    color_back = models.CharField(
        max_length=30,
    )  # 색상뒤
    bit = models.CharField(
        max_length=100,
    )  # 분류명
    prescription = models.CharField(
        max_length=30,
    )  # 전문일반구분
    sungbun = models.TextField(
        null=True, blank=True
    )  # 성분/함량/단위
    efcy_qesitm = models.TextField()  # 효능/효과
    use_method_qesitm = models.TextField()  # 용법/용량(하루 복용량)
    atpn_warn_qesitm = models.TextField()  # 알레르기 반응 일으킬  수 있는 질환군(warn)
    atpn_qesitm = models.TextField()  # 사용 시 주의사항(알레르기 반응 일으킬  수 있는 질환군)
    intrc_qesitm = models.TextField()  # 다른 약들과의 상호작용
    se_qesitm = models.TextField()  # 부작용(이상반응의 부분집합)
    deposit_method_qesitm = models.TextField()  # 보관 방법

    def __str__(self):
        return f"Pill number is {self.item_num}, Pill name is {self.item_name}."


class UploadFile(models.Model):
    files = models.FileField(upload_to="images", null=True)
    upload_at = models.DateTimeField(auto_now=True)