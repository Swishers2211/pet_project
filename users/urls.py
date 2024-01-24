from django.urls import path
from users.views import create_auth, LoginAPIView, UserAPIView, LogoutAPIView

urlpatterns = [
    path('register/', create_auth),
    path('login/', LoginAPIView.as_view()),
    path('user/', UserAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
]
