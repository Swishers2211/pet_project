from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
import jwt, datetime

from home.serializer import ProjectSerializer

from users.models import User
from home.models import Project

class MyProjectsAPIView(APIView):
    def get(self, request):
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Вы не авторизованы!")

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Вы не авторизованы!")
        # конец получения токена
        
        user = User.objects.get(email=payload['id']) 
        if user.active_role == 'C':
            project = Project.objects.filter(user=user)
        else:
            raise AuthenticationFailed("Вы не клиент")
        
        serializer = ProjectSerializer(project, many=True)
        return Response(serializer.data)
