from django.urls import path

from chat.views import ListChatsAPIView, DialogAPIView

urlpatterns = [
    path('', ListChatsAPIView.as_view()),
    path('dialog/<int:pk>/', DialogAPIView.as_view()),
]
