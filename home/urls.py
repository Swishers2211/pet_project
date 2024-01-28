from django.urls import path

from home.views import MyProjectsAPIView

app_name = 'home'

urlpatterns = [
    path('my_projects/', MyProjectsAPIView.as_view()),
]
