from datetime import timedelta

from django.contrib.auth import authenticate, login, logout
from django.core.mail.message import EmailMessage
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.core.mail import send_mail

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from users.models import User, Favorite, SearchHistory
from pills.models import Pill
from pills.serializers import PillListSerializer, SearchLogSerializer
from users.serializers import FavoritePillListSerializer, RoughPillSerializer, SearchHistoryPillListSerializer


class MyPillList(APIView):
    '''
    - url: /users/mypill-list
    '''
    permission_classes = [IsAuthenticated]

    def get(self, request):
        '''
        ✅ 유저의 즐겨찾기 목록 반환
        '''
        user = request.user
        user_pill = Favorite.objects.filter(user=user)
        serializer = FavoritePillListSerializer(user_pill, many=True)
        return Response(serializer.data)
        


class SearchLogList(APIView):
    '''
    검색 기록 목록 반환
    - url: /users/searchlog-list
    '''
    permissions_classes = [IsAuthenticated]

    def get(self, request):
        '''
        ✅ 검색 기록 로그 보여주기 (일주일 안의 기록만 보여줌!)
        - order by: 최신 순
        - delete는 자동으로 이루어짐

        1주일이 지난 뒤에는 db에서 자동으로 삭제해줌 <- 샐러리 사용해야하나?
        페이지네이션 해주는거?
        '''

        user = request.user
        cnt = SearchHistory.objects.filter(user=user).count()
        print(cnt)  # 2

        # 검색 기록이 없는 경우
        if cnt == 0:
            return Response(
                {"detail": "최근 검색 기록이 없습니다."},
                status=status.HTTP_404_NOT_FOUND,
            )

        search_history_max_days = 7  # one week
        max_days_ago = timezone.now() - timedelta(days=search_history_max_days)

        old_history = SearchHistory.objects.filter(
            user=user,
            created_at__lte=max_days_ago,
        )
        print(old_history.count())  # 0

        # 일주일 지난 기록이 있는 경우: 오래된 기록 삭제하기
        if old_history.count() > 0:
            old_history.delete()

        history_pill_list = SearchHistory.objects.filter(user=user)
        serializer = SearchHistoryPillListSerializer(history_pill_list, many=True)

        return Response(serializer.data)


class ChangePassword(APIView):
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


