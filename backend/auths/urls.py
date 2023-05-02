from django.urls import path
from auths import views

app_name = "auths"

# url: v1/auth/
urlpatterns = [
    path("signup", views.Signup.as_view()),
    path("login", views.Login.as_view()),
    path("logout", views.Logout.as_view()),
    # path("token-login", obtain_auth_token),
    # path("jwt-login", views.JWTLogin.as_view()),
]