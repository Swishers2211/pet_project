from django.urls import path

from home.views import MyProjectsAPIView, CreateProjectAPIView, FindJobAPIView, DetailProjectAPIView, MyRespondAPIView, ResponseToMyProjectAPIView

app_name = 'home'

urlpatterns = [
    path('view_project/<int:pk>/responses/', ResponseToMyProjectAPIView.as_view()),
    path('my_responses/', MyRespondAPIView.as_view()),
    path('view_project/<int:pk>/', DetailProjectAPIView.as_view()),
    path('find_job/', FindJobAPIView.as_view()),
    path('create_project/', CreateProjectAPIView.as_view()),
    path('my_projects/', MyProjectsAPIView.as_view()),
]
