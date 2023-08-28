from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from users import views

app_name = "users"

# url: v1/users/

urlpatterns = [
    path("mypill-list", views.MyPillList.as_view()),  # 유저의 즐겨찾기 목록 반환
    path("searchlog-list", views.SearchLogList.as_view()),  # 유저가 검색했던 알약 목록 반환
    path("<int:pnum>/like", views.LikedPill.as_view()),  # 유저가 좋아요 표시하는 라우터
]