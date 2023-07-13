# import pandas as pd
# from sklearn.cluster import KMeans
# from .photo_key import photo_key
# import tensorflow as tf
# import cv2
# import numpy as np
import os
import requests
import json
from django.core.paginator import Paginator, EmptyPage

from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Q

from pills.models import Pill
from pills.serializers import PillListSerializer, PillDetailSerializer, SearchLogSerializer, LikedPillSerializer
from users.models import Favorite, SearchHistory


class CustomPagination(PageNumberPagination):
    page_size = 20  # 한 페이지당 표시할 항목 수
    page_size_query_param = 'page_size'  # URL에서 페이지 크기를 설정하기 위한 쿼리 파라미터
    max_page_size = 1000  # 최대 페이지 사이즈


class PillList(ListAPIView):
    '''
    ✅ 모든 알약 목록 반환
        url: /pills/?page=n
    '''
    permissions_classes = [AllowAny]

    queryset = Pill.objects.all()
    if not queryset.exists():
        raise NotFound
    serializer_class = PillListSerializer
    pagination_class = CustomPagination


class DirectSearchPillList(ListAPIView):
    '''
    ✅ 알약 직접 검색
        url: /pills/search_direct?name=알약이름&color_front=앞면색상&shape=알약모양&page=페이지
        해당 조건 만족하는 여러 개의 알약 리스트, pagination(page=20)으로 반환 완료!
    '''
    permissions_classes = [AllowAny]

    serializer_class = PillListSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        # queryset = super().get_queryset()

        name = self.request.query_params.get("name", "")  # 약 이름
        color_front = self.request.query_params.get("color_front", "")  # 약 앞면 색상
        shape = self.request.query_params.get("shape", "")  # 약 모양

        queryset = Pill.objects.filter(
            Q(item_name__contains=name) 
            & Q(color_front__contains=color_front) 
            | Q(shape__exact=shape)
        ).distinct()

        if queryset.count() == 0:
            raise NotFound(
                detail="Not found any pill matching your request."
            )

        return queryset


class PillDetails(APIView):
    '''
    - url: /pills/<int:pnum>
    '''
    permissions_classes = [IsAuthenticatedOrReadOnly]

    def get_pill_object(self, pnum):
        try:
            return Pill.objects.get(item_num=pnum)
        except Pill.DoesNotExist:
            raise NotFound(
                detail=f"This Pill Not Found."
            )

    def post(self, request, pnum):
        '''
        ✅ pnum에 맞는 알약 한 개의 상세 정보 반환 (caching 적용 완료!)
        - TODO: 검색기록은 1주일 뒤에 삭제한다. (celery 이용하기)
        [로직 설명]
        1. user.auth가 있는 경우
            최근 검색한 내용 중 pnum에 맞는 객체 있는지 확인
                있으면 해당 searchhistory에서 꺼내줌 (전체 pill을 탐색하지 않아도 되니 부하 줄임)
                없으면 searchhistory에 저장해줌
        2. user.auth가 없는 경우
            전체 pill에서 찾아서 반환
        '''
        user = request.user
        pill_object = self.get_pill_object(pnum)

        if user.is_authenticated:
            # 같은 알약 찾은 기록이 이미 있는 경우 => caching: 기록 db에서 불러옴
            if SearchHistory.objects.filter(
                user=user, pill=pill_object
            ).exists():
                # pill_object = SearchHistory.objects.get(pill=pill_object)
                pill_object = SearchHistory.objects.filter(pill=pill_object).first()
                serializer = SearchLogSerializer(pill_object)
                # print("1")
                return Response(serializer.data)
            else:
                # print("2")
                serializer = SearchLogSerializer(
                    data=request.data,  # 여기서 data=request.data를 쓰기 위해서 HTTP method=POST로 설정
                )
                if serializer.is_valid():
                    # print("3")
                    pill = serializer.save(
                        user=user,
                        pill=pill_object,
                    )
                    return Response(SearchLogSerializer(pill).data)
                else:
                    return Response(
                        serializer.errors,
                        status=HTTP_400_BAD_REQUEST,
                    )
        # print("4")
        return Response(PillDetailSerializer(pill_object).data)


class LikedPill(APIView):
    '''
    - url: /pills/<int:pnum>/like
    '''
    permissions_classes = [IsAuthenticated]

    def get_pill_object(self, pnum):
        try:
            return Pill.objects.get(item_num=pnum)
        except Pill.DoesNotExist:
            raise NotFound(
                detail=f"This Pill Not Found."
            )
    
    def post(self, request, pnum):
        '''
        ✅ 즐겨찾기(db)에 추가하기
        '''
        user = request.user

        pill_object = self.get_pill_object(pnum)

        if Favorite.objects.filter(
            user=user, pill=pill_object
        ).exists():
            return Response(
                {"detail": "This pill has already been liked."},
                status=HTTP_400_BAD_REQUEST,
            )
        else:
            serializer = LikedPillSerializer(
                data=request.data,
            )
            if serializer.is_valid():
                like = serializer.save(
                    user=user,
                    pill=pill_object,
                )
                return Response(LikedPillSerializer(like).data)
            else:
                return Response(
                    serializer.errors,
                    status=HTTP_400_BAD_REQUEST,
                )

    def delete(self, request, pnum):
        '''
        ✅ 즐겨찾기(db)에서 삭제하기
        '''
        user = request.user
        pill_object = self.get_pill_object(pnum)
        like_object = Favorite.objects.filter(user=user, pill=pill_object)

        if like_object.exists():
            like_object.delete()
            return Response(
                status=HTTP_204_NO_CONTENT
            )
        else:
            return Response(
                {"detail": "This pill has already been marked as unliked."},
                status=HTTP_400_BAD_REQUEST,
            )


'''사진 검색 API'''
# with open('./AI/pill_90.json', 'r') as f:
#     pill_dict = json.load(f)

# df = pd.read_excel('./AI/ai_medicine.xlsx')
# model = tf.keras.models.load_model('model')


# def color_distance(r1, g1, b1, r2, g2, b2):
#     red_mean = int(round((r1 + r2) / 2))
#     r = int(r1 - r2)
#     g = int(g1 - g2)
#     b = int(b1 - b2)
#     return (((512 + red_mean) * r * r) >> 8) + 4 * g * g + (((767 - red_mean) * b * b) >> 8)


# @method_decorator(csrf_exempt, name='dispatch')
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def result_photo(request):
#     form = ImageForm(request.POST, request.FILES)
#     if form.is_valid():
#         image_name = form.save()
#         image_path = f'{image_name.files}'
#         try:
#             response = requests.post(
#                 'https://sdk.photoroom.com/v1/segment',
#                 data={'bg_color': '#000000'},
#                 headers={'x-api-key': f'{photo_key}'},
#                 files={'image_file': open(f'{image_path}', 'rb')},
#             )

#             response.raise_for_status()
#             with open(f'{image_path}', 'wb') as f:
#                 f.write(response.content)
#         except:
#             return Response("이미지 형식의 파일을 올려주세요.")

#         try:
#             img_array = np.fromfile(f"{image_path}", np.uint8)
#             image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
#             image_gray = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)
#             number = np.ones_like(image_gray) * 255
#             mul = cv2.multiply(image_gray, number)
#             contours, _ = cv2.findContours(
#                 mul, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#             contours_xy = np.array(contours)
#             for i in range(len(contours_xy)):
#                 if len(contours_xy[i]) < 10:
#                     continue
#                 x_min, x_max = 0, 0
#                 value = list()
#                 for j in range(len(contours_xy[i])):
#                     value.append(contours_xy[i][j][0][0])
#                     x_min = min(value)
#                     x_max = max(value)

#                 y_min, y_max = 0, 0
#                 value = list()
#                 for j in range(len(contours_xy[i])):
#                     value.append(contours_xy[i][j][0][1])
#                     y_min = min(value)
#                     y_max = max(value)

#                 x = x_min
#                 y = y_min
#                 w = x_max-x_min
#                 h = y_max-y_min

#                 img_trim = image[y:y+h, x:x+w]
#                 cv2.imwrite(f"{image_path}", img_trim)
#         except:
#             return Response("알약이 중앙에 위치하도록 사진을 다시 촬영하여주세요.")

#         image = cv2.imread(f'{image_path}')
#         image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#         x, y, _ = image.shape

#         big, small = max(x, y), min(x, y)
#         shape = 1 if ((3*big) // 4) > small else 0

#         image = image.reshape((image.shape[0] * image.shape[1], 3))

#         k = 2
#         clt = KMeans(n_clusters=k)
#         clt.fit(image)

#         color_list = []

#         for center in clt.cluster_centers_:
#             color_list.append(list(center))
#         color_list.sort()
#         color_list = color_list[-1]

#         # 흰색, 갈색, 노랑, 초록
#         color_ck = [[224, 224, 224], [150, 100, 80],
#                     [180, 150, 80], [80, 180, 140]]

#         color_distance_list = []

#         for i in range(len(color_ck)):
#             color_diff = color_distance(
#                 color_list[0], color_list[1], color_list[2], color_ck[i][0], color_ck[i][1], color_ck[i][2])
#             color_distance_list.append((color_diff, i))
#         color_distance_list.sort()
#         color_distance_list
#         color = color_distance_list[0][1]
#         color_distance_list

#         try:
#             predict_list = []
#             predict_img = cv2.imread(f'{image_path}')

#             height, width, _ = predict_img.shape
#             mask = np.zeros([224, 224, 3], np.uint8)

#             if width >= height:
#                 predict_img = cv2.resize(predict_img, (224, int(
#                     224*(height/width))), interpolation=cv2.INTER_LINEAR)
#                 h = (224 - predict_img.shape[0]) // 2
#                 mask[h:h+predict_img.shape[0], :] = predict_img
#                 predict_img = mask / 255
#             else:
#                 predict_img = cv2.resize(
#                     predict_img, (int(224*(width/height)), 224), interpolation=cv2.INTER_LINEAR)
#                 h = (224 - predict_img.shape[1]) // 2
#                 mask[:, h:h+predict_img.shape[1]] = predict_img
#                 predict_img = mask / 255

#             predict_list.append(predict_img)
#             predict_list = np.array(predict_list)

#             predict = model.predict(predict_list)

#             predict_list = []

#             for idx, percent in enumerate(predict[0].tolist()):
#                 predict_list.append((percent, idx))

#             predict_list.sort(reverse=True)

#             result_num = []
#             percent_list = []
#             for i in range(len(predict_list)):
#                 num = predict_list[i][1]
#                 if df.iloc[num]['의약품제형'] == shape and df.iloc[num]['색상앞'] == color:
#                     result_num.append(num)
#                 if i < 5:
#                     percent_list.append(predict_list[i][0])

#             content = {
#                 'message': '알약 인식 성공'
#             }
#             for i in range(len(result_num)):
#                 if i > 4:
#                     break
#                 pill = InfoPill.objects.all()
#                 pill = pill.filter(
#                     Q(item_num__exact=pill_dict[str(result_num[i])])).distinct()
#                 serializer = InfoPillSerializer(pill, many=True)
#                 content[f'{i+1}.알약'] = serializer.data
#                 content[f'{i+1}.확률'] = '{:.2f}%'.format(percent_list[i]*100, 2)

#             return Response(content)

#         except:
#             return Response("인공지능 모델을 불러오지 못했습니다.")

#     else:
#         return Response("파일을 선택해주세요.")
