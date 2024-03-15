from django.shortcuts import get_object_or_404
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
import jwt, datetime

from users.serializers import RegisterSerializer, ProfileSerializer, PortfolioSerializer
from users.models import User, Portfolio

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

        user_cache_name = 'user_cache'
        user_cache = cache.get(user_cache_name)
        if user_cache:
            user = user_cache
        else:
            user = get_object_or_404(User, pk=pk)
            cache.set(user_cache, user, 20)
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

class PortfolioAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            data = Portfolio.objects.get(pk=request.user.id)
            images = data.img.all()
            data.delete("photos")
            data.update(images)
            serializer = PortfolioSerializer(data)
            return Response(serializer.data)
        else:
            return {}
