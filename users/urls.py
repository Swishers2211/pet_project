from django.urls import path

from users.views import RegisterAPIView, LoginAPIView, UserAPIView, LogoutAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('profile/<int:pk>/', UserAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
]
