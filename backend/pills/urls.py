from django.urls import path
from pills import views

app_name = "pills"

# url: v1/auth/

urlpatterns = [
    path("", views.Pills.as_view()),
    path("<int:pid>", views.PillDetails.as_view()),
]