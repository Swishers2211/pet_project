from django.urls import path

from users.views import RegisterAPIView, LoginAPIView, UserAPIView, LogoutAPIView, PortfolioAPIView

urlpatterns = [
    path("portfolio/", PortfolioAPIView.as_view()),
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('<int:pk>/', UserAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
]
