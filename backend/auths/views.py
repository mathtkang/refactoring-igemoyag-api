import requests

from django.contrib.auth import authenticate, login, logout
from django.conf import settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.middleware.csrf import InvalidToken
# from rest_framework import status, permissions, generics
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from django.core.exceptions import TokenError

from allauth.socialaccount.models import SocialAccount

from auths.serializers import CreateUserSerializer, MyTokenObtainPairSerializer, MyTokenRefreshSerializer
from users.models import User


# from auths.serializers import MyTokenRefreshSerializer
# from rest_framework_simplejwt.views import TokenViewBase

class SignUp(APIView):
    '''
    ✅ 회원가입
    '''
    permission_classes = [AllowAny]

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
                status=HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST
            )



# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer
# class MyTokenRefreshView(TokenViewBase):
#     serializer_class = MyTokenRefreshSerializer



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
                status=HTTP_200_OK,
            )
        else:
            raise ParseError(detail="The password is wrong.")


class LogOut(APIView):
    '''
    ✅ 로그아웃
    '''
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(
            {"detail": "로그아웃 되었습니다."}, 
            status=HTTP_200_OK,
        )



'''OAuth : kakao social login'''
URL_FRONT = "http://elice-kdt-2nd-team6.koreacentral.cloudapp.azure.com/"
URL_BACK = "http://elice-kdt-2nd-team6.koreacentral.cloudapp.azure.com/"


@api_view(["POST"])
@permission_classes([AllowAny])
def kakao_login(request):
    code = request.GET.get("code", '')  # 파라미터
    KAKAO_CLIENT_ID = getattr(settings, "KAKAO_REST_API_KEY")
    REDIRECT_URI = f"{URL_FRONT}oauth/callback/kakao"
    # 카카오에 요청해서 token data 가져오기
    request_uri = f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={KAKAO_CLIENT_ID}&code={code}&redirect_uri={REDIRECT_URI}"
    token_data = requests.get(request_uri).json()

    access_token = token_data.get('access_token')
    # Authorization(인가코드) : header로 꼭 설정해야함 (카카오는 인가코드 기반으로 토큰을 요청, 받음)
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    # 사용자 정보 json 형식으로 가져오기
    get_user_info_url = 'https://kapi.kakao.com/v2/user/me'
    user_info_json = requests.get(get_user_info_url, headers=headers).json()

    uid = user_info_json.get("id")
    email = user_info_json.get('kakao_account').get('email')
    username = user_info_json.get('properties').get('nickname')
    password = f"password{uid}"
    provider = "kakao"

    # email 수집에 동의하지 않아서 값이 비어있는 경우
    if email == "" or email == None:
        email = f"{uid}@socialemail.com"

    # db에 이메일이 존재하는 경우
    if User.objects.filter(email=email).exists():
        # 소셜 로그인 (토큰 발급)
        if SocialAccount.objects.filter(uid=uid).exists():
            data = {
                'email': email,
                'password': password,
            }

            try:
                serializer = MyTokenObtainPairSerializer(data=data)
                serializer.is_valid(raise_exception=True)
            except:
                email = str(uid) + "#$%" + email
                data = {
                    'email': email,
                    'password': password,
                }
                serializer = MyTokenObtainPairSerializer(data=data)
                serializer.is_valid(raise_exception=True)

            return Response(serializer.validated_data, status=HTTP_200_OK)

        # 해당 이메일로 자체 로그인한 경우 (email+uid로 새로운 email만들어서 회원가입)
        else:
            email = f"{uid}#$%{email}"
            URL = f"{URL_BACK}api/sign-up/"
            data = {
                'email': email,
                'username': username,
                'password': password,
            }
            requests.post(url=URL, data=data)

            user_info = User.objects.filter(email=email).first()
            social_user = SocialAccount(
                user=user_info,
                uid=uid,
                provider=provider
            )
            social_user.save()

            # 토큰 발급
            data = {
                'email': email,
                'password': password,
            }
            serializer = MyTokenObtainPairSerializer(data=data)
            try:
                serializer.is_valid(raise_exception=True)
            except TokenError as e:
                raise InvalidToken(e.args[0])

            return Response(serializer.validated_data, status=status.HTTP_200_OK)

    # db에 이메일이 존재하지 않는 경우 (소셜로그인으로 처음 로그인, db에 저장)
    else:
        URL = f"{URL_BACK}api/sign-up/"
        data = {
            'email': email,
            'username': username,
            'password': password,
        }
        requests.post(url=URL, data=data)

        user_info = User.objects.filter(email=email).first()
        # user_info = User.objects.get(email=email)
        social_user = SocialAccount(
            user=user_info,
            uid=uid,
            provider=provider
        )
        social_user.save()

        # 로그인 시 토큰 발급
        data = {
            'email': email,
            'password': password,
        }
        serializer = MyTokenObtainPairSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=HTTP_200_OK)


# @api_view(["GET"])
# def google_login(request):
#     GOOGLE_CLIENT_ID = getattr(settings, "GOOGLE_CLIENT_ID")
#     REDIRECT_URI = GOOGLE_CALLBACK_URI
#     scope = "https://www.googleapis.com/auth/userinfo.email"

#     return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={GOOGLE_CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={scope}")


# def google_callback(request):
#     GOOGLE_CLIENT_ID = getattr(settings, "GOOGLE_CLIENT_ID")
#     GOOGLE_SECRET = getattr(settings, "GOOGLE_SECRET")
#     REDIRECT_URI = GOOGLE_CALLBACK_URI
#     state = request.GET.get('state')
#     code = request.GET.get('code')

#     # 구글에 요청해서 token data 가져오기
#     token_data = requests.post(
#         f"https://oauth2.googleapis.com/token?client_id={GOOGLE_CLIENT_ID}&client_secret={GOOGLE_SECRET}&code={code}&grant_type=authorization_code&redirect_uri={REDIRECT_URI}&state={state}").json()

#     error = token_data.get("error", None)
#     if error is not None:
#         raise JSONDecodeError(error)

#     access_token = token_data.get("access_token")
#     # 발급된 Access Token을 이용해서 사용자 정보 가져오기
#     get_user_info = requests.get(
#         f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")

#     status_code = get_user_info.status_code  # 제대로 들어가면 200 반환

#     if status_code != 200:
#         return JsonResponse(
#             {'err_msg': 'failed to get email'},
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     user_info_json = get_user_info.json()  # json형태로 프로필 값 가져오기
#     return Response(user_info_json)
#     '''
#     {
#         "issued_to": "775963563051-uv8t5d689e6eerchgedpdu2f36bthj45.apps.googleusercontent.com",
#         "audience": "775963563051-uv8t5d689e6eerchgedpdu2f36bthj45.apps.googleusercontent.com",
#         "user_id": "112901936700065846512",
#         "scope": "https://www.googleapis.com/auth/userinfo.email openid",
#         "expires_in": 3598,
#         "email": "ksge1124@gmail.com",
#         "verified_email": true,
#         "access_type": "online"
#     }
#     '''

#     # 이메일과 이름 데이터 가져옴
#     # (구글에는 이름 데이터가 없다. 로그인 시 닉네임 작성하는 화면 반환 : 프론트)

#     email = user_info_json.get('email')
#     # return HttpResponse(email)  # test : 확인

#     '''db에 이미 저장되어있는 회원인지 확인'''
#     try:
#         user = User.objects.get(email=email)
#         social_user = SocialAccount.objects.get(
#             user=user)  # 소셜로그인으로 회원가입 했는지 여부 확인

#         # 이메일은 있지만 social user가 아님
#         if social_user is None:
#             return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)

#         # google에서 찾을 수 없음
#         if social_user.provider != 'google':
#             return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)

#         # 기존에 Google로 가입된 유저
#         data = {'access_token': access_token, 'code': code}
#         accept = requests.post(
#             f"{BASE_URL}api/login/google/finish/", data=data)

#         accept_status = accept.status_code

#         if accept_status != 200:
#             return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)

#         accept_json = accept.json()
#         accept_json.pop('user', None)

#         # return JsonResponse(accept_json)
#         # jwt토큰 프론트엔드에 전달
#         return JsonResponse(
#             {
#                 "access_token": access_token,
#                 "user_email": email,
#             },
#             status=200,
#         )

#     except User.DoesNotExist:
#         data = {'access_token': access_token, 'code': code}
#         accept = requests.post(
#             f"{BASE_URL}api/login/google/finish/", data=data)
#         accept_status = accept.status_code

#         if accept_status != 200:
#             return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)

#         accept_json = accept.json()
#         accept_json.pop('user', None)

#         # return JsonResponse(accept_json)
#         # jwt토큰 프론트엔드에 전달
#         return JsonResponse(
#             {
#                 "access_token": access_token,
#                 "user_email": email,
#             },
#             status=200,
#         )


# class GoogleLogin(SocialLoginView):
#     adapter_class = google_view.GoogleOAuth2Adapter
#     callback_url = GOOGLE_CALLBACK_URI
#     client_class = OAuth2Client
