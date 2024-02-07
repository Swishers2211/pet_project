from django.shortcuts import render, get_object_or_404
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
import jwt, datetime

from home.serializer import ProjectSerializer, RespondSerializer, RespondCreateSerializer, ProjectCreateSerializer

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
        
        client = get_object_or_404(User, email=payload['id']) 
        if client.active_role == 'C':
            project = Project.objects.filter(client=user).order_by('-published')# вывод по дате от нового до старого
        else:
            raise AuthenticationFailed("Вы не клиент!")
        
        serializer = ProjectSerializer(project, many=True)
        return Response(serializer.data)

'''Позоляет опубликовать свой проект для клиента'''
class CreateProjectAPIView(APIView):
    def get(self, request):
        token = request.COOKIES.get("jwt")
        if not token:
            raise AuthenticationFailed("Вы не авторизованы!")
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Вы не авторизованы!")

        client = User.objects.get(email=payload['id'])
        if client.active_role == 'C':
            projects = print('Вы клиент')
        else:
            raise AuthenticationFailed("Вы не клиент!")
        
        return Response(projects)
    
    '''Клиент может опубликовать свой проект'''
    def post(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Вы не авторизованы!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Вы не авторизованы!')

        client = User.objects.get(email=payload['id'])

        serializer = ProjectCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(client=client)
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

        master = User.objects.get(email=payload['id']) 
        if master.active_role == 'M':
            projects = Project.objects.all().order_by('-published')
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
        
        master = User.objects.get(email=payload['id'])
        if master.active_role == 'M':
            try:
                project = Project.objects.get(pk=pk)
            except:
                raise Http404('Проект не найден!')
        else:
            try:
                project = Project.objects.get(client=master, pk=pk)
            except:
                raise Http404('Проект не найден!')

        serializer = ProjectSerializer(project)
        return Response(serializer.data)
    
    '''Мастер может откликнуться на проект'''
    def post(self, request, pk):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Вы не авторизованы!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Вы не авторизованы!')
        
        project = Project.objects.get(pk=pk)
        master = User.objects.get(email=payload['id'])
        
        serializer = RespondCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(project=project, master=master)
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
        
        master = User.objects.get(email=payload['id'])
        if master.active_role == 'M':
            try:
                respond = Respond.objects.filter(master=master).order_by('-published')
            except:
                raise Http404('Отклики не найдены!')
        else:
            raise AuthenticationFailed('Вы не мастер!')
        
        serializer = RespondSerializer(respond, many=True)
        return Response(serializer.data)

'''Позволяет клиенту посмотреть отклики на определенном проекте'''
class ResponseToMyProjectAPIView(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Вы не авторизованы!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Вы не авторизованы!')
        
        client = User.objects.get(email=payload['id'])
        if client.active_role == 'C':
            try:
                project = Project.objects.get(pk=pk, client=client)
            except:
                raise Http404('Проект не найден!')
            respond = Respond.objects.filter(project=project).order_by('-published')
        else:
            raise AuthenticationFailed('Вы не клиент!')
            
        serializer = RespondSerializer(respond, many=True)
        return Response(serializer.data)
