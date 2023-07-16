from datetime import timedelta

from django.contrib.auth import authenticate, login, logout
from django.core.mail.message import EmailMessage
from django.utils import timezone

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from users.models import User, Favorite, SearchHistory
from pills.models import Pill
from pills.serializers import PillListSerializer, SearchLogSerializer
from users.serializers import FavoritePillListSerializer, RoughPillSerializer


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
    - url: /users/searchlog-list
    '''
    permissions_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        user_email = str(user.email)

        if "#$%" in user_email:
            user_email = user_email.split("#$%")[1]

        queryset = super().get_queryset()
        queryset = queryset.filter(
            user_email=user_email
        ).values_list(
            "pill_num", flat=True
        ).order_by("id")[:9]
        
        return queryset

    def get(self, request):
        '''
        - 검색 기록 로그 보여주기 (시간에 따라서 최근 것만 보여줌!)
        - order by: 최신 순
        - Post는 pill검색할 때 자동으로 이루어짐 / delete는 시간이 지나면 자동으로 이루어짐

        기록이 적재될 때, 이미 db에 있는 알약내용이라도 다음 id로 적재된다. (서로 다른 것으로 인식)
        1주일이 지난 뒤에는 db에서 자동으로 삭제해줌 <- 이게 가능할지 모르겠당 (샐러리 사용해야하나?)
        '''
        user = request.user
        user_email = str(user.email)

        if "#$%" in user_email:
            user_email = user_email.split("#$%")[1]

        data = SearchHistory.objects.filter(user_email=user_email).count()
        
        search_history_max_days = 7
        max_days_ago = timezone.now() - timedelta(days=search_history_max_days)

        # 검색 기록이 없는 경우
        if data == 0:
            return Response({"message": "최근 검색 기록이 없습니다."})

        old_history = SearchHistory.objects.filter(
            user_email=user_email,
            create_at__lte=max_days_ago
        ).count()

        # 일주일 지난 기록이 없는 경우 (old_history =< 0)
        if old_history == 0:
            history_pill_list = self.get_queryset()
            '''
            history_pill_list = SearchHistory.objects.filter(
                user_email=user_email
            ).all().values_list("pill_num").order_by("id")[:9]
            '''
            pills = Pill.objects.filter(item_num__in=history_pill_list)
            serializer = RoughPillSerializer(pills, many=True)

            return Response(serializer.data)
        
        # 일주일 지난 기록이 있는 경우 (old_history > 0)
        SearchHistory.objects.filter(
            user_email=user_email,
            create_at__lte=max_days_ago
        ).delete()
        history_pill_list = self.get_queryset()
        '''
        history_pill_list = SearchHistory.objects.filter(
            user_email=user_email
        ).all().values_list("pill_num").order_by("id")[:9]
        '''

        # 오래된 기록 삭제 후 최근 기록이 남아있는 경우
        if history_pill_list:
            pills = Pill.objects.filter(item_num__in=history_pill_list)
            serializer = RoughPillSerializer(pills, many=True)
            return Response(serializer.data)
        
        # 오래된 기록 삭제 후 최근 기록이 없는 경우
        return Response(
            {"detail": "최근 검색 기록이 없습니다."},
            status=HTTP_404_NOT_FOUND,
        )


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
            return Response(status=HTTP_200_OK)
        else:
            raise ParseError



# 비밀번호 변경: 이메일 보내주는 함수 (테스트용)

def send_email(request):
    subject = "message"
    to = ["igmy1108@gmail.com"]
    from_email = "igmy1108@email.com"
    message = "메시지 테스트"
    EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()