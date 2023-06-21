from django.urls import path
from pills import views

app_name = "pills"

# url: v1/auth/

urlpatterns = [
    path("", views.PillList.as_view()),
    path("search_direct", views.DirectSearchPillList.as_view()),  # ?name={알약이름}&color_front={앞면색상}&shape={알약모양}&page={페이지}
    path("<int:pnum>", views.PillDetails.as_view()),
]