from django.urls import path

from home.views import MyProjectsAPIView, CreateProjectAPIView, FindJobAPIView

app_name = 'home'

urlpatterns = [
    path('find_job/', FindJobAPIView.as_view()),
    path('create_project/', CreateProjectAPIView.as_view()),
    path('my_projects/', MyProjectsAPIView.as_view()),
]
