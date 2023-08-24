from datetime import timedelta

from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from users.models import Favorite, SearchHistory
from pills.views import CustomPagination
from pills.models import Pill
from pills.serializers import LikedPillSerializer
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


class LikedPill(APIView):
    '''
    🔗 url: /users/<int:pnum>/like
    유저가 좋아요 표시하는/취소하는 라우터
    '''
    permissions_classes = [IsAuthenticated]

    def get_pill_object(self, pnum):
        try:
            return Pill.objects.get(item_num=pnum)
        except Pill.DoesNotExist:
            raise NotFound(
                detail="This Pill item_num Not Found."
            )
    
    def post(self, request, pnum):
        '''
        ✅ 즐겨찾기(db)에 추가하기
        '''
        user = request.user
        pill_object = self.get_pill_object(pnum)

        if Favorite.objects.filter(user=user, pill=pill_object).exists():
            return Response(
                {"detail": "This pill has already been liked."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            serializer = LikedPillSerializer(
                data=request.data,
            )
            if serializer.is_valid():
                like = serializer.save(
                    user=user,
                    pill=pill_object,
                )
                return Response(LikedPillSerializer(like).data)
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )

    def delete(self, request, pnum):
        '''
        ✅ 즐겨찾기(db)에서 삭제하기
        '''
        user = request.user
        pill_object = self.get_pill_object(pnum)

        like_object = Favorite.objects.filter(user=user, pill=pill_object)

        if like_object.exists():
            like_object.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            return Response(
                {"detail": "This pill has already been marked as unliked."},
                status=status.HTTP_400_BAD_REQUEST,
            )



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