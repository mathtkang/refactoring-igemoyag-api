from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User, Favorite
from pills.models import Pill


DEFAULT_EMAIL="test@email.com"
DEFAULT_USERNAME="test_username"
DEFAULT_PASSWORD="test_password"

BASE_URL="/v1/users"

class TestMyPillList(APITestCase):
    def setUp(self):
        # 테스트에 필요한 초기 데이터 등을 설정합니다.
        user = User.objects.create(
            email=DEFAULT_EMAIL,
            username=DEFAULT_USERNAME,
        )
        user.set_password(DEFAULT_PASSWORD)
        self.client.force_authenticate(user=self.user)

        self.user = user

    def test_my_pill_list_api_view_with_empty_favorite_list(self):
        # 테스트 시 특정 사용자로 로그인된 상태를 시뮬레이션합니다.
        self.client.force_authenticate(user=self.user)

        # 즐겨찾기 목록이 비어있는 경우에 대한 테스트

        # API의 URL을 reverse 함수를 사용하여 가져옵니다.
        url = '/users/mypill-list/'

        # API를 호출하여 응답을 받습니다.
        response = self.client.get(url)

        # 응답의 status code가 404 (Not Found)인지 확인합니다.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # 응답의 JSON 데이터를 확인하여 예상하는 결과를 검사합니다.
        self.assertEqual(response.data['detail'], '즐겨찾기 목록이 없습니다.')

    def test_my_pill_list_api_view_with_favorite_list(self):
        # 즐겨찾기 목록이 있는 경우에 대한 테스트
        # 즐겨찾기 목록을 생성합니다.
        favorite_pill1 = Pill.objects.create(name='알약1', description='알약1에 대한 설명')
        favorite_pill2 = Pill.objects.create(name='알약2', description='알약2에 대한 설명')
        Favorite.objects.create(user=self.user, pill=favorite_pill1)
        Favorite.objects.create(user=self.user, pill=favorite_pill2)

        # API의 URL을 reverse 함수를 사용하여 가져옵니다.
        url = '/users/mypill-list/'

        # API를 호출하여 응답을 받습니다.
        response = self.client.get(url)

        # 응답의 status code가 200 (OK)인지 확인합니다.
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 응답의 JSON 데이터를 확인하여 예상하는 결과를 검사합니다.
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['name'], '알약1')
        self.assertEqual(response.data['results'][1]['name'], '알약2')
