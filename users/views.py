from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from users.serializers import UserSerializer, ProfileSerializer
from users.models import User
import jwt, datetime

'''Регистрация аккаунта'''
class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
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
    
'''Профиль пользоателя'''
class UserAPIView(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Не найден!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Не найден!')

        try:
            user = User.objects.get(email=payload['id'], pk=pk)
        except:
            raise AuthenticationFailed('Пользователь не найден!')
        
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

'''Выход из аккаунта'''
class LogoutAPIView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Вы вышли из аккаунта'
        }
        return response
