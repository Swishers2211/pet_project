from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
import jwt, datetime

from users.serializers import RegisterSerializer, ProfileSerializer
from users.models import User

'''Регистрация аккаунта'''
class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

'''Вход в аккаунт по почте'''
class LoginAPIView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('Пользователь не найден!')

        if not user.check_password(password):
            raise AuthenticationFailed('Не коректный пароль!')

        payload = {
            'id': user.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')#.decode('utf-8')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response
    
class UserAPIView(APIView):
    """Просмотр профиля"""
    def get(self, request, pk):
        # получение токена может ли пользователь изменять данную страницу
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Вы не авторизованы!")

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Вы не авторизованы!")

        # конец получения токена

        user = get_object_or_404(User, pk=pk)
        if payload["id"] == user.email:
            res = {"is_my": 1}
        else:
            res = {"is_my": 0}

        serializer = ProfileSerializer(user)

        res.update(serializer.data)
        return Response(res)

'''Выход из аккаунта'''
class LogoutAPIView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Вы вышли из аккаунта'
        }
        return response

