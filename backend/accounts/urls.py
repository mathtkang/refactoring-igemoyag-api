from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
    path("change-password", views.ChangePassword.as_view()),
    path("reset-password", views.ResetPassword.as_view()),
    path("reset-password/<int:uidb64>/<int:token>", views.ResetPasswordLink.as_view()),

    # django 내장
    path("password-reset", auth_views.PasswordResetView.as_view(), name='password_reset'),
    path(
        route='reset/<uidb64>/<token>/', 
        view=auth_views.PasswordResetConfirmView.as_view(), 
        name='password_reset_confirm',
    ),


    # path("password_reset/done", auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html')),
    # path("password_reset_confirm/<int:uidb64>/<int:token>/", auth_views.PasswordResetConfirmView.as_view(template_name='templates/accounts/password_reset_confirm.html')),
    # path("reset/done", auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html')),
]



'''
accounts/password_change/ [name='password_change']
accounts/password_change/done/ [name='password_change_done']
accounts/password_reset/ [name='password_reset']
accounts/password_reset/done/ [name='password_reset_done']
accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/reset/done/ [name='password_reset_complete']
'''