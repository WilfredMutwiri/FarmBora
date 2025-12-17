from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from ..serializers import RegistrationSerializer, LoginSerializer, CustomUserSerializer
from shared.responses import (
    handle_success,
    handle_error,
    handle_validation_error,
    handle_not_found,
)


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=['Authentication'],
        request_body=RegistrationSerializer,
        responses={
            201: CustomUserSerializer,
            400: 'Bad Request'
        }
    )
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_serializer = CustomUserSerializer(user)
            return handle_success(
                data=user_serializer.data,
                message="User registered successfully.",
                status_code=status.HTTP_201_CREATED
            )
        return handle_validation_error(
            errors=serializer.errors,
            message="Validation failed.",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=['Authentication'],
        request_body=LoginSerializer,
        responses={
            200: 'Login Successful',
            400: 'Bad Request',
            401: 'Unauthorized'
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return handle_success(
                data={
                    'refresh_token': str(refresh),
                    'access_token': str(refresh.access_token),
                },
                message="Login successful.",
                status_code=status.HTTP_200_OK
            )
        return handle_validation_error(
            errors=serializer.errors,
            message="Validation failed.",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

class LogoutView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=['Authentication'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Refresh token to blacklist'
                ),
            },
            required=['refresh_token'],
        ),
        responses={
            200: 'Logout Successful',
            400: 'Bad Request'
        }
    )
    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return handle_success(
                message="Logout successful.",
                status_code=status.HTTP_200_OK
            )
        except TokenError:
            return handle_error(
                message="Invalid or expired token.",
                status_code=status.HTTP_400_BAD_REQUEST
            )