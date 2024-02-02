from django.shortcuts import render, get_object_or_404
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
import jwt, datetime

from home.serializer import ProjectSerializer, RespondSerializer

from users.models import User
from home.models import Project, Respond

'''Просмотр всех проектов, которые опубликовал клиент'''
class MyProjectsAPIView(APIView):
    def get(self, request):
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Вы не авторизованы!")

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Вы не авторизованы!")
        
        user = get_object_or_404(User, email=payload['id']) 
        if user.active_role == 'C':
            project = Project.objects.filter(client=user).order_by('-published')# вывод по дате от нового до старого
        else:
            raise AuthenticationFailed("Вы не клиент!")
        
        serializer = ProjectSerializer(project, many=True)
        return Response(serializer.data)

'''Клиент публикует свой проект'''
class CreateProjectAPIView(APIView):
    def get(self, request):
        token = request.COOKIES.get("jwt")
        if not token:
            raise AuthenticationFailed("Вы не авторизованы!")
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Вы не авторизованы!")

        user = User.objects.get(email=payload['id'])
        if user.active_role == 'C':
            projects = print('Вы клиент')
        else:
            raise AuthenticationFailed("Вы не клиент!")
        
        return Response(projects)
    
    def post(self, request): # публикация происходит в этой функции
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)

'''Позволяет Мастеру найти работу (проект, который опубликовал клиент)'''
class FindJobAPIView(APIView):
    def get(self, request):
        token = request.COOKIES.get("jwt")
        if not token:
            raise AuthenticationFailed("Вы не авторизованы!")
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Вы не авторизованы!")

        user = User.objects.get(email=payload['id']) 
        if user.active_role == 'M':
            projects = Project.objects.all().order_by('-published')#.select_related('user', 'main_category', 'category', 'sub_category')
        else:
            raise AuthenticationFailed("Вы не мастер!")
        
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

'''Позволяет мастеру зайти на какой-то проект'''
class DetailProjectAPIView(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get("jwt")
        if not token:
            raise AuthenticationFailed("Вы не авторизованы!")
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Вы не авторизованы!")
        
        user = User.objects.get(email=payload['id'])
        if user.active_role == 'M':
            try:
                project = Project.objects.get(pk=pk)
            except:
                raise Http404('Проект не найден!')
        else:
            try:
                project = Project.objects.get(client=user, pk=pk)
            except:
                raise Http404('Проект не найден!')

        serializer = ProjectSerializer(project)
        return Response(serializer.data)

'''Позволяет мастеру посмотреть свои отклики'''
class MyRespondAPIView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Вы не авторизованы!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Вы не авторизованы!')
        
        user = User.objects.get(email=payload['id'])
        if user.active_role == 'M':
            try:
                respond = Respond.objects.filter(master=user).order_by('-published')
            except:
                raise Http404('Отклики не найдены!')
        else:
            raise AuthenticationFailed('Вы не мастер!')
        
        serializer = RespondSerializer(respond, many=True)
        return Response(serializer.data)
