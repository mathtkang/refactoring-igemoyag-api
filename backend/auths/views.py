import jwt
import requests
from django.contrib.auth import authenticate, login, logout
from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from auths.serializers import CreateUserSerializer
from users.models import User


# from auths.serializers import MyTokenRefreshSerializer
# from rest_framework_simplejwt.views import TokenViewBase

class SignUp(APIView):
    '''
    ✅ 회원가입
    '''
    def post(self, request):
        email = request.data.get("email")
        username = request.data.get("username")
        password = request.data.get("password")

        if not email or not username or not password:
            raise ParseError

        serializer = CreateUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = CreateUserSerializer(user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class Login(APIView):
    '''
    ✅ 로그인
    '''
    def post(self, request):
        email = request.data.get("email")
        username = request.data.get("username")
        password = request.data.get("password")

        if not email or not username or not password:
            raise ParseError
        
        # validation: email이 맞지 않은 경우, 접근 권한 여부 확인 후 에러발생
        user = authenticate(
            request,
            email=email,
            username=username,
            password=password,
        )

        if user:
            login(request, user)
            return Response(
                {"detail": "로그인 되었습니다."},
                status=status.HTTP_200_OK,
            )
        else:
            raise ParseError(detail="The password is wrong.")


class Logout(APIView):
    '''
    ✅ 로그아웃
    '''
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(
            {"detail": "로그아웃 되었습니다."}, 
            status=status.HTTP_200_OK,
        )


class JWTLogin(APIView):
    def post(self, request):
        email = request.data.get("email")
        username = request.data.get("username")
        password = request.data.get("password")

        if not email or not username or not password:
            raise ParseError
        
        user = authenticate(
            request,
            email=email,
            username=username,
            password=password,
        )
        
        if user:
            token = jwt.encode(
                {"id": user.id},
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            return Response(
                {"token": token}
            )
        else:
            raise ParseError(detail="wrong password")


'''OAuth : kakao social login'''
KAKAO_CLIENT_ID = "36bab671cc6d302ae5ccc02a2c1aa707"
REDIRECT_URI = "https://127.0.0.1:3000/social/kakao"  # REACT URI
# URL_BACK = "http://elice-kdt-2nd-team6.koreacentral.cloudapp.azure.com/"

class KakaoLogIn(APIView):
    '''
    ref. https://developers.kakao.com/docs/latest/ko/kakaologin/rest-api#request-token-request-body
    '''
    def post(self, request):
        code = request.data.get('code')
        # 카카오에 요청해서 access_token(data) 가져오기
        access_token = request.post(
            "https://kauth.kakao.com/oauth/token",
            headers={
                'Content-Type': "application/x-www-form-urlencoded"
            },
            data={
                "grant_type": "authorization_code",
                "client_id": KAKAO_CLIENT_ID,
                "redirect_uri": REDIRECT_URI,
                "code": code,
            },
        )
        access_token = access_token.json().get("access_token")
        # print(access_token)
        
        user_data = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
            }
        )
        user_data = user_data.json()
        # print(user_data)

        kakao_account = user_data.get("kakao_account")
        is_email_verified = kakao_account.get('is_email_verified')

        if is_email_verified == False:
            return Response(
                {"detail": "이메일 수집 동의가 필요합니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=kakao_account.get("email"))
            login(request, user)
            return Response(
                {"detail": "kakao로 소셜로그인 완료"},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            profile = kakao_account.get("profile")
            user = User.objects.create(
                email=kakao_account.get("email"),
                username=profile.get("nickname"),
            )
            user.set_unusable_password()
            user.save()
            login(request, user)
            return Response(
                {"detail": "kakao로 소셜로그인 완료"},
                status=status.HTTP_200_OK
            )