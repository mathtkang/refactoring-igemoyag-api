from django.urls import path
from auths import views
from rest_framework.authtoken.views import obtain_auth_token

app_name = "auths"

# url: v1/auth/
urlpatterns = [
    path("signup", views.SignUp.as_view()),
    path("login", views.Login.as_view()),
    path("logout", views.Logout.as_view()),
    path("token-login", obtain_auth_token),   # HTTP method : POST
    path("jwt-login", views.JWTLogin.as_view()),
    path("kakao", views.KakaoLogIn.as_view())
]