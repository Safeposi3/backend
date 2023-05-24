from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from api.serializers import CustomUserSerializer, RegisterSerializer, UpdateSerializer

class LoginApi(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        if email is None or password is None:
            return Response({'error': 'Please provide both email and password'}, status=HTTP_400_BAD_REQUEST)
        user = authenticate(email=email, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials'}, status=HTTP_400_BAD_REQUEST)
        token = AuthToken.objects.create(user)[1]
        return Response({
            'user_info': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            },
            'token': token,
        }, status=HTTP_200_OK)


class RegisterApi(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        _, token = AuthToken.objects.create(user)

        return Response({
            'user_info': {
                'id': user.id,
                'email': user.email,
            },
            'token': token,
        })


class UserDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response({
            'user_info': serializer.data,
        })

    def put(self, request):
        user = request.user
        serializer = UpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
        return Response(serializer.data)



