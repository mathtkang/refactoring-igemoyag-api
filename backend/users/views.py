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
from users.serializers import FavoritePillListSerializer
from pills.serializers import PillListSerializer



class MyPillList(APIView):
    '''
    - url: /users/mypill-list
    '''
    permission_classes = [IsAuthenticated]

    def get(self, request):
        '''
        - 즐겨찾기 한 목록 모두 보여주기
        '''
        user = request.user

        # 아래 부분은 User 모델에서 가져오는 방향?
        if "#$%" in user.email:
            user_email = user.email.split("#$%")[1]
        
        user_pill = Favorite.objects.filter(
            user_email=user_email
        ).values_list("pill_num")
        pill = Pill.objects.filter(item_num__in=user_pill)

        serializer = FavoritePillListSerializer(pill, many=True)

        return Response(serializer.data)


class MyPill(APIView):
    '''
    - url: /users/mypill/?pn={알약num}
    '''
    permission_classes = [IsAuthenticated]

    # def get_object(self, request):
    #     pass
    
    def post(self, request):
        '''
        - 즐겨찾기(db)에 추가하기
        '''
        user = request.user  # 유저 불러오기

        if "#$%" in user.email:
            user_email = user.email.split("#$%")[1]

        # pill_object = Pill.objects.all()  # 약 정보 데이터 베이스 전부 가져오기 (여기서 이걸 가져오면 overhead 일어날듯?)
        pn = request.GET.get("pn", "")  # 약 넘버

        # url 약 넘버 정확하게 일치한다면

        if Pill.objects.filter(item_num=pn).exists():
        # if pn:
        #     pill = pill_object.filter(item_num__exact=pn).distinct()
            # __exact : 정확히 일치하는 데이터를 필터링 -> 굳이 사용 안해도 됨!
            # .distinct() : 중복된 항목을 제거하고 고유한(unique)한 항목들만 반환
            
            pills = Pill.objects.filter(item_num=pn).distinct()
            serializer = PillListSerializer(pills, many=True)
            # print(serializer.data)

            pill_num = Pill.objects.get(item_num=pn)  # 입력한 약 넘버와 일치하는 약 번호 가져오기

            # Favorite 테이블에 user_email과 pill_num를 넣고 저장
            mypillinfo = Favorite(user_email=user_email, pill_num=pill_num)
            mypillinfo.save()  # 저장
            return Response(
                {"detail": f"{serializer.data}를 성공적으로 즐겨찾기에 추가했습니다."},
                status=HTTP_200_OK,
            )
        
        # 정확한 약 넘버가 들어오지 않다면!
        else:
            return Response(
                {"detail": "올바른 요청 값이 아닙니다."},
                status=HTTP_400_BAD_REQUEST
            )
    
    def delete(self, request):
        '''
        - 즐겨찾기(db)에서 삭제하기
        '''
        user = request.user  # 유저 불러오기

        if "#$%" in user.email:
            user_email = user.email.split("#$%")[1]

        pill = Pill.objects.all()  # 약 정보 데이터 베이스 전부 가져오기 (여기서 이걸 가져오면 overhead 일어날듯?)
        pn = request.GET.get("pn", "")  # 약 넘버

        # url 약 넘버 정확하게 일치한다면
        if pn:
            pill = pill.filter(Q(item_num__exact=pn)).distinct()
            serializer = PillListSerializer(pill, many=True)
            pill_num = Pill.objects.get(item_num=pn)  # 입력한 약 넘버와 일치하는 약 번호 가져오기

            Favorite.objects.filter(user_email=user.email, pill_num=pill_num).delete()

            return Response(
                {"detail": "삭제 완료"},
                status=HTTP_204_NO_CONTENT
            )
        else:
            return Response(
                {"detail": "올바른 요청 값이 아닙니다."},
                status=HTTP_400_BAD_REQUEST
            )


class SearchHistoryLog(APIView):
    '''
    - url: /users/search-history
    '''
    permissions_classes = [IsAuthenticated]

    # ??
    def get_queryset(self):
        user_email = str(self.request.user.email)

        if "#$%" in user_email:
            user_email = user_email.split("#$%")[1]

        queryset = super().get_queryset()
        queryset = queryset.filter(user_email=user_email).values_list(
            "pill_num", flat=True).order_by("id")[:9]
        return queryset

    def get(self, request):
        '''
        - 검색 기록 로그 보여주기 (시간에 따라서 최근 것만 보여줌!)
        - order by: 최신 순
        - Post는 pill검색할 때 자동으로 이루어짐 / delete는 시간이 지나면 자동으로 이루어짐
        '''
        user = request.user
        user_email = user.email
        # user_email = str(request.user.email)

        if "#$%" in user_email:
            user_email = user_email.split("#$%")[1]

        data = SearchHistory.objects.filter(user_email=user_email).count()
        search_history_max_days = 7
        max_days_ago = timezone.now() - timedelta(days=search_history_max_days)

        # 검색 기록이 없는 경우
        if data == 0:
            return Response(
                {"detail": "최근 검색 기록이 없습니다."},
                status=HTTP_404_NOT_FOUND
            )
                            

        # old_history = (
        #     SearchHistory.objects.filter(
        #         Q(user_email=user_email)
        #         & Q(create_at__lte=date.today() - timedelta(days=7))
        #     )
        #     .all()
        #     .count()
        # )
        old_history = SearchHistory.objects.filter(
            user_email=user_email,
            create_at__lte=max_days_ago
        ).count()


        # 일주일 지난 기록이 없는 경우
        if old_history == 0:
            history_pill_list = self.get_queryset()
            pills = Pill.objects.filter(item_num__in=history_pill_list)
            serializer = FavoritePillListSerializer(pills, many=True)
            return Response(serializer.data)
        
        # 일주일 지난 기록이 있는 경우
        SearchHistory.objects.filter(
            user_email=user_email,
            create_at__lte=max_days_ago
        ).delete()
        history_pill_list = self.get_queryset()

        # 오래된 기록 삭제 후 최근 기록이 남아있는 경우
        if history_pill_list:
            pills = Pill.objects.filter(item_num__in=history_pill_list)
            serializer = FavoritePillListSerializer(pills, many=True)
            return Response(serializer.data)
        
        # 오래된 기록 삭제 후 최근 기록이 없는 경우
        return Response(
                {"detail": "최근 검색 기록이 없습니다."},
                status=HTTP_404_NOT_FOUND
            )
    
        # [아래는 참고용]
        # # 일주일 지난 기록이 있는 경우
        # if old_history > 0:
        #     SearchHistory.objects.filter(
        #         Q(user_email=user_email)
        #         & Q(create_at__lte=date.today() - timedelta(days=7))
        #     ).all().delete()

        #     history_pill_list = (
        #         SearchHistory.objects.filter(user_email=user_email)
        #         .all()
        #         .values_list("pill_num")
        #         .order_by("id")[:9]
        #     )
        #     pills = Pill.objects.filter(item_num__in=history_pill_list)
        #     serializer = FavoritePillListSerializer(pills, many=True)

        #     return Response(serializer.data)

        # # 일주일이 지난 기록이 없는 경우
        # history_pill_list = (
        #     SearchHistory.objects.filter(user_email=user_email)
        #     .all()
        #     .values_list("pill_num")
        #     .order_by("id")[:9]
        # )
        # pills = Pill.objects.filter(item_num__in=history_pill_list)

        # serializer = FavoritePillListSerializer(pills, many=True)





# 비밀번호 변경: 이메일 보내주는 함수 (테스트용)

def send_email(request):
    subject = "message"
    to = ["igmy1108@gmail.com"]
    from_email = "igmy1108@email.com"
    message = "메시지 테스트"
    EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()