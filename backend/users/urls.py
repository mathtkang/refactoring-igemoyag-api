from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from users import views

app_name = "users"

urlpatterns = [
    # path("", views.Users.as_view()),
    path("mypill-list", views.MyPillList.as_view()),  # 유저의 즐겨찾기 목록 반환
    path("mypill/<int:pnum>", views.MyPill.as_view()),  
    path("search-history", views.SearchHistoryLog.as_view()),

    # path("change-password", views.ChangePassword.as_view()),
    path("send-email/", views.send_email), # 비밀번호 찾기위해서(구글이메일보내는 기능,test) 
]