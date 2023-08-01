from datetime import timedelta

from django.contrib.auth import authenticate, login, logout
from django.core.mail.message import EmailMessage
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.core.mail import send_mail

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from users.models import Favorite, SearchHistory
from pills.views import CustomPagination
from pills.serializers import PillListSerializer
from users.serializers import FavoritePillListSerializer, SearchHistoryPillListSerializer


class MyPillList(ListAPIView):
    '''
    🔗 url: /users/mypill-list
    ✅ 유저의 즐겨찾기 목록 반환
    ✅ pagination(page=20) 적용
    '''
    permission_classes = [IsAuthenticated]

    serializer_class = FavoritePillListSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        favorite_pill_object = Favorite.objects.filter(user=user)
        
        # print(favorite_pill_object.count())
        if favorite_pill_object.count() == 0:
            raise NotFound(
                detail="즐겨찾기 목록이 없습니다.",
            )

        return favorite_pill_object


class SearchLogList(ListAPIView):
    '''
    🔗 url: /users/searchlog-list
    ✅ 검색 기록 목록 반환(1주일 지난 기록은 db에서 자동 삭제 / order by: 최신 순)
    ✅ pagination(page=20) 적용
    '''
    permissions_classes = [IsAuthenticated]

    serializer_class = SearchHistoryPillListSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        search_log_pill_object = SearchHistory.objects.filter(user=user)

        print(search_log_pill_object.count())
        if search_log_pill_object.count() == 0:
            raise NotFound(
                detail="최근 검색 기록이 없습니다.",
            )

        search_history_max_days = 7  # one week
        max_days_ago = timezone.now() - timedelta(days=search_history_max_days)

        old_history = SearchHistory.objects.filter(
            user=user,
            updated_at__lte=max_days_ago,
        )
        # print(old_history.count())

        # 일주일 지난 기록이 있는 경우: 오래된 기록 삭제하기
        if old_history.count() > 0:
            old_history.delete()

        history_pill_list = SearchHistory.objects.filter(user=user)

        return history_pill_list


class ChangePassword(APIView):
    '''
    🔗 url: /users/change-password
    ✅ 비밀번호 변경
    '''
    permission_classes = [IsAuthenticated]  # 등록된 사용자만 접근 가능 (로그인된 상태)

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not old_password or not new_password:
            raise ParseError
        
        if user.check_password(old_password):  # validate hashed pw
            user.set_password(new_password)  # hashed new_pw
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            raise ParseError


HOST = 'localhost'

class ResetPassword(APIView):
    '''
    🔗 url: /users/reset-password
    TODO: 비밀번호 재발급 (email 사용해서)
    '''
    permission_classes = [IsAuthenticated]  # 등록된 사용자만 접근 가능 (로그인된 상태)

    def post(self, request):
        user = request.user
        user_email = str(user.email)

        email = request.data.get("email")
        print("2")

        if user_email == email:
            print("1")
            # 재설정 토큰 생성
            token = get_random_string(length=16)
            # token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            
            # 토큰과 사용자 이메일을 이용해 비밀번호 재설정 링크 구성
            reset_link = f"http://{HOST}/v1/users/reset-password/{token}/"
            
            # 이메일 보내기 (ver.1: send_mail() 메서드 사용)
            subject = "비밀번호 재설정 링크"
            message = f"비밀번호를 재설정하려면 다음 링크를 클릭하세요: {reset_link}"
            from_email = "ksge1124@gmail.com"  # 보낼 때 표시되는 이메일
            recipient_list = [user_email, ]  # 수신자 목록

            send_mail(subject, message, from_email, recipient_list)

            # # 이메일 보내기 (ver.2: EmailMessage() 메서드 사용)
            # subject = "비밀번호 재설정 링크"
            # message = f"비밀번호를 재설정하려면 다음 링크를 클릭하세요: {reset_link}"
            # from_email = "ksge1124@gmail.com"  # 보낼 때 표시되는 이메일

            # EmailMessage(subject, message, from_email, to=[user_email]).send()
            
            return Response(
                {"message": "이메일이 성공적으로 전송되었습니다."},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": "입력한 이메일에 해당하는 사용자가 존재하지 않습니다."},
                status=status.HTTP_404_NOT_FOUND,
            )




# 비밀번호 변경(초기화): 이메일 보내주는 함수

# def send_email(request):
#     subject = "message"
#     to = ["igmy1108@gmail.com"]
#     from_email = "igmy1108@email.com"
#     message = "메시지 테스트"
#     EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()


