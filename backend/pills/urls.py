from django.urls import path
from pills import views

app_name = "pills"

# url: v1/auth/

urlpatterns = [
    path("", views.PillList.as_view()),
    path("search_direct", views.DirectSearchPillList.as_view()),
    path("<int:pid>", views.PillDetails.as_view()),
]