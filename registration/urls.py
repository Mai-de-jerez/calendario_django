from django.urls import path
from .views import SignUpView, password_reset_username, password_reset_question, password_reset_confirm, profile_update

urlpatterns=[
    path('signup/', SignUpView.as_view(), name='signup'),
    path('reset/', password_reset_username, name='password_reset_username'),
    path('reset/question/', password_reset_question, name='password_reset_question'),
    path('reset/confirm/', password_reset_confirm, name='password_reset_confirm'),
    path('profile/', profile_update, name='profile'),
]