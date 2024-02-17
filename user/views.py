from .serializers import UserSerializer
from .models import User

from django.contrib.auth import authenticate
from rest_framework import viewsets, status, mixins, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# 회원가입
class SignUpAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
        
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user" : serializer.data,
                    "message" : "Signup Successs!",
                    "token" : {
                        "access_token" : access_token,
                        "refresh_token" : refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )

            res.set_cookie("access_token", access_token, httponly=True)
            res.set_cookie("refresh_token", refresh_token, httponly=True)

            return res
        return Response({"message" : "이미 가입된 사용자입니다."}, status=status.HTTP_400_BAD_REQUEST)

# 로그인
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = authenticate(
            email = request.data.get('email'),
            password = request.data.get('password')
        )
        
        if user is not None:
            serializer = UserSerializer(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "Login Success!",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        return Response({"message" : "가입되지 않은 사용자 혹은, 이외의 오류"}, status=status.HTTP_400_BAD_REQUEST)

# 유저 전문가 판별
class UserExpertDetermineAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        expert_status = request.data.get('Expert')
        user = request.user

        user.isExpert = expert_status
        user.save()

        return Response({"success": "Expert status Update"}, status=status.HTTP_200_OK)
        
# 유저 프로필 조회
class ProfileViewSet(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]