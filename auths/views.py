import jwt
import requests
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from auths.serializers import CreateUserSerializer, ValidationSerializer
from users.models import User

class SignUp(APIView):
    '''
    🔗 url: /auth/signup
    ✅ 회원가입
    '''
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get("email")
        username = request.data.get("username")
        password = request.data.get("password")
        print(request.data)

        if not email or not username or not password:
            raise ParseError(detail="잘못된 요청입니다. email, username, password 모두 존재해야합니다.")
        
        serializer = ValidationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)  # hashed password
            user.save()
            print(CreateUserSerializer(user).data)
            return Response(
                CreateUserSerializer(user).data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_409_CONFLICT
            )


class Login(APIView):
    '''
    🔗 url: /auth/login
    ✅ session 로그인 (장고 기본 지원, 내장 메서드 사용)
    '''
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        # username = request.data.get("username")
        password = request.data.get("password")

        if not email or not username or not password:
            raise ParseError(detail="잘못된 요청입니다. email, username, password 모두 존재해야합니다.")
        
        # validation: email이 맞지 않은 경우, 접근 권한 여부 확인 후 에러발생
        is_email_verified = User.objects.filter(email=email).exists()

        if not is_email_verified:
            return Response(
                {"detail": "해당 email은 존재하지 않습니다."},
                status=status.HTTP_404_NOT_FOUND,
            )

        user = authenticate(
            request,
            email=email,
            # username=username,
            password=password,
        )

        if user:
            login(request, user)
            return Response(
                {"detail": "로그인 되었습니다."},
                status=status.HTTP_200_OK,
            )
        else:
            raise ParseError(detail="The username or password is wrong.")


# class JWTLogin(APIView):
#     '''
#     🔗 url: /auth/jwt-login
#     ✅ JWT 로그인
#     '''
#     permission_classes = [AllowAny]

#     def post(self, request):
#         email = request.data.get("email")
#         password = request.data.get("password")

#         if not email or not password:
#             raise ParseError(detail="잘못된 요청입니다. email, username, password 모두 존재해야합니다.")
        
#         is_email_verified = User.objects.filter(email=email).exists()

#         if not is_email_verified:
#             return Response(
#                 {"detail": "해당 email은 존재하지 않습니다."},
#                 status=status.HTTP_404_NOT_FOUND,
#             )
        
#         user = authenticate(
#             request,
#             email=email,
#             # username=username,
#             password=password,
#         )
#         print(user)
#         if user:
#             token = jwt.encode(
#                 {"id": user.id},
#                 settings.SECRET_KEY,
#                 algorithm="HS256",
#             )
#             return Response(
#                 {"token": token},
#                 status=status.HTTP_200_OK,
#             )
#         else:
#             raise ParseError(detail="The username or password is wrong.")

class JWTLogin(APIView):
    '''
    🔗 url: /auth/jwt-login
    ✅ JWT 로그인
    '''
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            return JsonResponse(
                {"detail": "잘못된 요청입니다. email, password 모두 존재해야합니다."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(
            request, 
            username=email, 
            password=password
        )

        if user is not None:
            refresh = RefreshToken.for_user(user)

            data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "username": user.username,
                "email": user.email,
            }

            return JsonResponse(
                data,
                status=status.HTTP_200_OK
            )
        else:
            return JsonResponse(
                {"detail": "이메일 또는 비밀번호가 잘못되었습니다."}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
    

class Logout(APIView):
    '''
    🔗 url: /auth/logout
    ✅ 로그아웃
    '''
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(
            {"detail": "로그아웃 되었습니다."}, 
            status=status.HTTP_204_NO_CONTENT,
        )


'''OAuth : kakao social login'''
KAKAO_CLIENT_ID = "36bab671cc6d302ae5ccc02a2c1aa707"
REDIRECT_URI = "https://127.0.0.1:3000/social/kakao"  # REACT URI
# URL_BACK = "http://elice-kdt-2nd-team6.koreacentral.cloudapp.azure.com/"

class KakaoLogIn(APIView):
    '''
    🔗 url: /auth/kakao
    ✅ 카카오 소셜로그인
    ref. https://developers.kakao.com/docs/latest/ko/kakaologin/rest-api#request-token-request-body
    '''
    permission_classes = [AllowAny]

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