from rest_framework.test import APITestCase
from rest_framework import status
from pills.models import Pill
from users.models import User


DEFAULT_EMAIL="test@email.com"
DEFAULT_USERNAME="test_username"
DEFAULT_PASSWORD="test_password"

BASE_URL="/v1/pills"




# class PillListAPIViewTest(APITestCase):
#     def setUp(self):
#         # 테스트에 필요한 초기 데이터 등을 설정합니다.
#         Pill.objects.create(name='알약1', description='알약1에 대한 설명')
#         Pill.objects.create(name='알약2', description='알약2에 대한 설명')

#     def test_pill_list_api_view(self):
#         # API의 URL을 reverse 함수를 사용하여 가져옵니다.
#         url = '/pills/'

#         # API를 호출하여 응답을 받습니다.
#         response = self.client.get(url)

#         # 응답의 status code가 200 (OK)인지 확인합니다.
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         # 응답의 JSON 데이터를 확인하여 예상하는 결과를 검사합니다.
#         self.assertEqual(len(response.data['results']), 2)
#         self.assertEqual(response.data['results'][0]['name'], '알약1')
#         self.assertEqual(response.data['results'][1]['name'], '알약2')


class TestPillList(APITestCase):
    def setUp(self):
        # Create User
        user = User.objects.create(
            email=DEFAULT_EMAIL,
            username=DEFAULT_USERNAME,
        )
        user.set_password(DEFAULT_PASSWORD)
        user.save()
        self.user = user

        print(type(self.user))  # <class 'users.models.User'>

        # Create Pill (원래라면 pill을 직접 만들어야 하지만 지금은 db에 이미 적재되어 있기 때문에 안 만들어 되지 않을까?)
        Pill.objects.create(
            item_num=1,
            item_name="for test name",
            create_user=user
        )

    def test_get(self):
        response = self.client.get(f"{BASE_URL}/")
        # [Anyone Readable]
        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200.",
        )
        data = response.json()
        print(data)
        self.assertIsInstance(
            data,
            list,
        )
        # 페이지네이션이 잘 되었는지 확인 (20개)
        # self.assertEqual(
        #     len(data),
        #     1,
        # )
        # self.assertEqual(
        #     data[0]["iten_num"],
        #     200808876,
        # )
        # self.assertEqual(
        #     data[0]["item_name"],
        #     "가스디알정50밀리그램(디메크로틴산마그네슘)",
        # )
        # self.assertEqual(
        #     data[0]["company_name"],
        #     "일동제약(주)",
        # )


class TestLikedPill(APITestCase):
    def setUp(self):
        # Create User and Update team_name
        user = User.objects.create(
            email=DEFAULT_EMAIL,
            username=DEFAULT_USERNAME,
        )
        user.set_password(DEFAULT_PASSWORD)
        user.save()
        self.user = user

        self.client.login(
            email=DEFAULT_EMAIL,
            username=DEFAULT_USERNAME,
            password=DEFAULT_PASSWORD
        )

        # Create Favorite
        Favorite.objects.create(
            item_num=1,
            item_name="for test name",
            create_user=user
        )
    
    # [tid로 찾는 Task가 없는 경우]
    def test_get_task_object(self):
        response = self.client.get(f"{BASE_URL}/2")
        self.assertEqual(
            response.status_code,
            404
        )

    # [tid로 찾는 Task가 있는 경우]
    def test_get(self):
        response = self.client.get(f"{BASE_URL}/1")
        self.assertEqual(
            response.status_code, 
            200
        )
        data = response.json()
        self.assertEqual(
            data["title"],
            DEFAULT_TITLE,
        )
        self.assertEqual(
            data["content"],
            DEFAULT_CONTENT,
        )

    def test_put(self):
        UPDATED_TITLE = "test updated title"
        UPDATED_CONTENT = "test updated content"

        # [GOOD CASE]
        response = self.client.put(
            f"{BASE_URL}/1",
            data={
                "title": UPDATED_TITLE, 
                "content": UPDATED_CONTENT,
            },
        )
        self.assertEqual(
            response.status_code, 
            200,
        )
        data = response.json()
        self.assertEqual(
            data["title"],
            UPDATED_TITLE,
        )
        self.assertEqual(
            data["content"],
            UPDATED_CONTENT,
        )

        # [BAD CASE 1] 
        BAD_CASE_TITLE = "Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다."

        fail_response = self.client.put(
            f"{BASE_URL}/1",
            data={
                "title": BAD_CASE_TITLE,
            },
        )
        self.assertEqual(
            fail_response.status_code, 
            400
        )
        error_message = fail_response.json()
        self.assertIn(
            "title",
            error_message
        )

    def test_delete(self):
        # [GOOD CASE]
        response = self.client.delete(
            f"{BASE_URL}/1",
        )
        self.assertEqual(
            response.status_code, 
            204
        )

        # [이미 완료된 Task의 경우]
        Task.objects.create(
            title=DEFAULT_TITLE,
            content=DEFAULT_CONTENT,
            create_user=self.user,
            is_complete=True,
        )
        response = self.client.delete(
            f"{BASE_URL}/2",
        )
        self.assertEqual(
            response.status_code, 
            403
        )