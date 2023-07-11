from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from users import views

app_name = "users"

urlpatterns = [
    path("mypill-list", views.MyPillList.as_view()),  # 유저의 즐겨찾기 목록 반환
    path("searchlog-list", views.SearchLogList.as_view()),  # 유저가 검색했던 알약 목록 반환
    path("change-password", views.ChangePassword.as_view()),
    path("find-password", views.send_email), # 비밀번호 찾기위해서(구글이메일보내는 기능,test) 
]