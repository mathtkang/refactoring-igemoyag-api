# Refactoring 💫 ⬅️ 이게모약💊

⚠️ 해당 repository는 기존 프로젝트의 Backend part만 refactoring한 repository입니다.

**따라서 backend 관련 기술 위주로 작성되었습니다.**

<br>

## 🔗 [이게모약(기존 프로젝트)의 Repository](https://github.com/mathtkang/meosum-learning)

👆 더 구체적인 "**서비스 소개 및 화면 구성**"이 궁금하시다면 위의 링크를 참고해주세요!


<br>
<br>

## 💫 Refactoring한/할 내용
- 개발환경을 `pyenv`+`poetry`로 변경했습니다. [본인 블로그 글](https://kkangsg.tistory.com/108)
- 하나의 app에서 common, auths, users, pills app으로 확장했습니다.
- 함수형으로 구현된 뷰를 클래스형으로 바꿨습니다.(FBV to CBV)
- API를 RESTful하게 변경했습니다.
- OAuth2를 사용하여 소셜로그인(Kakao, Naver, Google)을 구현할 예정입니다.
- Test Code를 작성할 예정입니다.
<!-- - Swagger를 적용하여 더 직관적인 API spec을 볼 수 있습니다. -->
- AWS EC2를 이용하여 배포할 예정입니다.

<br>

## 🚀 [Refactoring한 서비스 접속하기]()
❗️ 현재 비용의 문제로 서버 접속은 불가능합니다.


<br>
<br>
<br>

---
## 💊 이게모약 로고
<img width="200" alt="이게모약 logo" src="https://user-images.githubusercontent.com/51039577/234815308-25f289a3-b0ec-4e04-8b78-86945e5847ee.png">

<br>

## 📃 프로젝트 개요

- 간편하고 쉽게, 내 손 안의 작은 알약 사전
- AI 이미지 처리 기능을 활용해 알약 사진을 스캔하여, 알약을 구별하고 알약의 정보를 알려주는 서비스

<br>

## ⚙️ 개발 환경 of Refactoring
- ![macosm1 badge](https://img.shields.io/badge/MacOS%20M1-000000.svg?style=flat&logo=macOS&logoColor=white)
- ![Visual Studio Code badge](https://img.shields.io/badge/Visual%20Studio%20Code-007ACC.svg?style=flat&logo=Visual-Studio-Code&logoColor=white)
- ![github badge](https://img.shields.io/badge/GitHub-181717.svg?style=flat&logo=GitHub&logoColor=white)
- ![docker badge](https://img.shields.io/badge/Docker-2496ED.svg?style=flate&logo=Docker&logoColor=white)
- ![postman badge](https://img.shields.io/badge/postman-FF6C37?style=flat&logo=Postman&logoColor=white)
- ![swagger badge](https://img.shields.io/badge/Swagger-85EA2D.svg?style=flat&logo=Swagger&logoColor=black)

<br>

## 🛠 기술 스택 for Refactoring

**Backend**
- ![python badge](https://img.shields.io/badge/Python-3.10-3776AB?style=flat&logo=Python&logoColor=white)
- ![django badge](https://img.shields.io/badge/Django-3.2.9-%23092E20?&logo=Django&logoColor=white)

**Database**
- ![Postgres badge](https://img.shields.io/badge/postgres-%23316192.svg?&logo=postgresql&logoColor=white)

**Deploy**
- ![aws ec2 badge](https://img.shields.io/badge/AWS-EC2-%23FF9900?&logo=Amazon%20EC2&logoColor=white)
- ![docker badge](https://img.shields.io/badge/Docker-20.10.17-%232496ED?&logo=Docker&logoColor=white)
- ![nginx badge](https://img.shields.io/badge/Nginx-1.23.0-%23009639?logo=NGINX&locoColor=white)
- ![Gunicorn badge](https://img.shields.io/badge/Gunicorn-499848.svg?style=flat&logo=Gunicorn&logoColor=white)

<br>

## 📙 API 명세서 (thru Swagger)
### 📑 [API Specification](https://sprinkle-piccolo-9fc.notion.site/API-Specification-gbzr-c287814a50c5452da4d9c2234c2adf75)

<br>

## 📋 E-R Diagram
<img width="1000" alt="ERD" src="https://user-images.githubusercontent.com/51039577/234810851-2de392fb-d9f9-451d-a8d0-62d66f9b1880.png">

<br>

## ✅ Test Case (⭐️NEW!!)

<br>

## 🕸 System Architecture

<img width="1000" alt="System Architecture" src="https://user-images.githubusercontent.com/51039577/234815256-3921b4ba-8f00-4a28-9c63-db5d086c198e.png">
<!-- 수정 필요! AWS EC2로 배포! -->

<br>

## 📂 Directory Structure of Refactoring

<img width="200" alt="Directory Structure" src="">

<br>

## 🌍 배포

Docker, NginX, Gunicorn을 사용하여 AWS EC2 서버에 배포하였습니다.

➡️ [서비스 주소]()

❗️ 현재 비용의 문제로 서버 접속은 불가능합니다.

<br>
<br>
<br>
<br>

# 💊 이게모약 서비스 소개

## 🥅 프로젝트 목표

- **사진 한장으로 알약 정보** **검색이 가능**하도록 합니다.
- 알약 정보 직접 검색을 통해 알약의 이름, 색상, 모양으로 알약 정보를 검색할 수 있습니다.
- **알약 즐겨찾기 기능**을 통해 서비스 내 기능인 '내 알약 상자' 페이지에서 **복용 중인 알약을 쉽게 관리**하도록 합니다.
- 알약 즐겨찾기 기능 페이지에 있는 **알약들을 한 장의 사진으로 리스트업** 할 수 있습니다.

<br>

## 💫 서비스 이용 시 기대효과
1. 의료진들의 자가 복용약 검색 시간 단축
2. 병원 방문이 잦은 사람들에게 약 정보 관리의 편리함 제공
3. 폐의약품 수거 방법을 모르는 일반인들에게 정보 제공
4. 일반 의약품에 대한 정보 제공 및 오남용 사례 제공으로 경각심 제공

<br>

## 🎯 Project Targets

1. Main Targets
    - 병동에서 입원 환자 복용약을 조사하는 의료진들
2. Sub Targets
    - 복용하는 약의 가짓 수가 많은 만성질환 환자 + 보호자들

<br>

## 💻 프로젝트 화면 구성

| ![메인 페이지](https://user-images.githubusercontent.com/51039577/235062849-3d977a4e-6c91-4c70-8c06-a71601dec4aa.png) | ![메인 페이지(햄버거메뉴)](https://user-images.githubusercontent.com/51039577/235062839-093e27b1-9e4f-4758-bfdd-31d87d2a2924.png) | ![회원가입](https://user-images.githubusercontent.com/51039577/235062852-3c6ee161-f8d1-40ea-a2f8-2b41fc340e48.png) | ![로그인](https://user-images.githubusercontent.com/51039577/235062854-651a10a6-6a88-48dd-997e-037673ad9195.png) | ![메인 페이지(로그인 이후)](https://user-images.githubusercontent.com/51039577/235062858-f4b2c249-c07e-46f1-bebc-13a34125cf39.png) |
| :--------: | :--------: | :--------: | :---------: | :---------: |
| 메인 페이지 | 메인 페이지(햄버거메뉴) | 회원가입 | 로그인 | 메인 페이지(로그인 이후) |

<br>

| ![사진으로 검색 1](https://user-images.githubusercontent.com/51039577/235062860-ef54443c-ad49-405c-9c58-d68a15899362.png) | ![사진으로 검색 2](https://user-images.githubusercontent.com/51039577/235062863-4cc38068-a80e-4f79-828f-80860c8e589c.png) | ![사진으로 검색 로딩 중](https://user-images.githubusercontent.com/51039577/235062866-3dd363e4-bb42-485f-82a1-60a5ee81dc2c.png) | ![사진 검색 결과](https://user-images.githubusercontent.com/51039577/235062869-55ae87ab-389d-48b4-bc0d-9569ef41b2c1.png) | ![알약 상세 페이지](https://user-images.githubusercontent.com/51039577/235062870-4302b62c-446c-41d7-8b2a-6a853e0bd82a.png) | 
| :--------: | :--------: | :--------: | :---------: | :---------: |
| 사진으로 검색 페이지 1 | 사진으로 검색 2 | 사진으로 검색 로딩 중 | 사진 검색 결과 | 알약 상세 페이지 |

<br>

| ![직접 검색 페이지](https://user-images.githubusercontent.com/51039577/235062873-b79a64d6-5e68-4a1c-8e70-8abebdfd08c8.png) | ![직접 검색 결과](https://user-images.githubusercontent.com/51039577/235062876-76a90de0-4471-4fdd-90b3-20d79972c91a.png) | ![알약 상세 페이지](https://user-images.githubusercontent.com/51039577/235064613-42e04f7e-2ac2-4180-a8f9-ef36bda3f8ef.png) | ![알약 상세 페이지(더보기)](https://user-images.githubusercontent.com/51039577/235064620-1f4a2b70-9406-4179-a405-2d835c3b5608.png) | ![내 알약 상자(최근 검색 기록)](https://user-images.githubusercontent.com/51039577/235062879-ce3eb4a4-d612-4b59-ae44-9e41b1581756.png) | ![내 알약 상자(즐겨찾기)](https://user-images.githubusercontent.com/51039577/235062882-299af43f-3426-49d4-9b82-c5f7c642e904.png) | 
| :--------: | :--------: | :--------: | :---------: | :---------: | :---------: |
| 직접 검색 페이지 | 직접 검색 결과 | 알약 상세 페이지 | 알약 상세 페이지(더보기) | 내 알약 상자(최근 검색 기록) | 내 알약 상자(즐겨찾기) |

<br>
<br>

## ⭐️ 프로젝트 핵심 기능 (Main & Sub Features)

### Main Feature: 1️⃣ 약 검색
  1. 이미지로 약 검색하기
      - 유저에게 어떤 사진을 올려야하는지 가이드라인을 제시한다.
      - 유저가 사진을 올리면 인공지능 모델을 통해 검색한다.
      - 검색된 약에 관한 정보를 유저에게 제공한다.
      - 유저에게 제공되는 정보는 모두 동일 (약 종류, 성분, 함량, BIT 분류, 용법, 용량 , 효능, 효과, 부작용) 
  2. 약 이름으로 검색하기
      - 검색된 약에 관한 정보를 유저에게 제공한다.
  3. 모양, 색상별로 약 검색하기
      - 검색된 약에 관한 정보를 유저에게 제공한다.
### Main Feature: 2️⃣ 로그인
  1. Oauth 기능: 카카오, 네이버, 구글
### Main Feature: 3️⃣ 내 알약 상자(로그인 시 이용 가능)
  1. 최근 검색한 알약 리스트
      - 로그인 후 알약을 검색할 시 최근 검색한 알약 기록이 남는다.
  2. 알약 즐겨찾기
      - 내 알약 상자에 담을 알약들을 즐겨찾기 기능으로 추가할 수 있다.
  3. 즐겨찾기 해놓은 알약 한장의 사진으로 정리해주기
      - 병원에 갈 일이 있을 경우, 즐겨찾기 해뒀던 알약들을 한 장의 이미지로 리스트업해서 정리해준다.

### Sub Feature : 1️⃣ 검색 알약 랭킹
  - 다른 유저들은 어떤 알약을 많이 검색했는지 알려준다.
### Sub Feature : 2️⃣ 폐의약품 수거 콘텐츠
  - 기간이 지나거나 복용할 수 없게 된 약들의 처리 방법을 알려준다.
  - 페이지를 나누어 콘텐츠로 제작 예정
### Sub Feature : 3️⃣ 일반 의약품 정보
  - 의사의 복용없이도 구매가 가능한 일반 의약품들의 정보를 알려준다.
