from datetime import timedelta

from django.core.mail.message import EmailMessage
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from users.models import User


class ChangePassword(APIView):
    '''
    🔗 url: /accounts/change-password
    ✅ 비밀번호 변경
    '''
    permission_classes = [IsAuthenticated]  # 등록된 사용자만 접근 가능 (로그인된 상태)

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not old_password or not new_password:
            raise ParseError
        
        if user.check_password(old_password):  # validation of hashed pw
            user.set_password(new_password)  # hashed new_pw
            user.save()
            return Response(
                {"detail": "비밀번호 변경이 완료되었습니다."},
                status=status.HTTP_200_OK
            )
        else:
            raise ParseError(
                detail="old_password이 맞지 않습니다."
            )


class ResetPassword(APIView):
    '''
    🔗 url: /accounts/reset-password
    ✅ 비밀번호 재발급 링크를 email로 보내주기
    '''
    permission_classes = [IsAuthenticated]  # 등록된 사용자만 접근 가능 (로그인된 상태)

    def post(self, request):
        HOST = 'http://127.0.0.1:8000/v1/accounts/reset-password'

        user = request.user
        user_email = str(user.email)

        email = request.data.get("email")

        if user_email == email:
            # 재설정 토큰 생성
            token = get_random_string(length=16)
            # token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            uid = urlsafe_base64_encode(force_bytes(user.id))
            
            # 토큰과 사용자 이메일을 이용해 비밀번호 재설정 링크 구성
            reset_link = f"{HOST}/{uid}/{token}/"
            
            # 이메일 보내기 (ver.1: send_mail() 메서드 사용)
            subject = "비밀번호 재설정 링크"
            message = f"비밀번호를 재설정하려면 다음 링크를 클릭하세요: {reset_link}"
            from_email = "refactoringforigmy@gmail.com"  # 보낼 때 표시되는 이메일
            recipient_list = [user_email, ]  # 수신자 목록

            send_mail(subject, message, from_email, recipient_list)

            # 이메일 보내기 (ver.2: EmailMessage() 메서드 사용)
            # subject = "비밀번호 재설정 링크"
            # message = f"비밀번호를 재설정하려면 다음 링크를 클릭하세요: {reset_link}"
            # from_email = "ksge1124@gmail.com"  # 보낼 때 표시되는 이메일

            # EmailMessage(subject, message, from_email, to=[user_email]).send()
            
            return Response(
                {
                    "detail": "이메일이 성공적으로 전송되었습니다.",
                    "uid": uid,
                    "token": token,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "입력한 이메일에 해당하는 사용자가 존재하지 않습니다."},
                status=status.HTTP_404_NOT_FOUND,
            )


class ResetPasswordLink(APIView):
    '''
    🔗 url: /users/reset-password/<int:uidb64>/<int:token>
    '''
    def put(self, request, uidb64, token):
        '''
        uidb64: base 64로 인코딩된 사용자의 기본 키입니다.
        token: 재설정 링크가 유효한지 확인하는 토큰입니다.
        '''
        # uid를 디코딩하여 사용자를 가져옵니다.
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
            
            if user != request.user:
                return Response(
                    {"detail": "비밀번호를 변경할 수 있는 권한이 없습니다."},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except User.DoesNotExist:
            return Response(
                {"detail": "유효하지 않은 사용자입니다."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # token이 유효한지 확인합니다.
        if not default_token_generator.check_token(user, token):
            return Response(
                {"detail": "유효하지 않은 토큰입니다."}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        # 새로운 비밀번호를 받아서 기존 비밀번호를 변경합니다.
        new_password = request.data.get('new_password')
        if not new_password:
            return Response(
                {"detail": "새로운 비밀번호를 입력해주세요."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # 비밀번호 유효성 검사: 최소 길이 등을 추가하여 유효성을 검사합니다.
        if len(new_password) < 8:
            return Response(
                {"detail": "비밀번호는 최소 8자 이상이어야 합니다."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return Response(
            {"detail": "비밀번호가 성공적으로 변경되었습니다."}, 
            status=status.HTTP_200_OK
        )