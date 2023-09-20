FROM python:3.11-slim

# python 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1

# poetry 환경 변수 설정
ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_NO_INTERACTION=1

# poetry 명령을 컨테이너에서 사용 가능하도록 poetry 바이너리 경로를 환경 변수 path에 추가
ENV PATH="$POETRY_HOME/bin:$PATH"

# 작업 디렉토리 설정
RUN mkdir /app

WORKDIR /app
RUN pwd

# curl, poetry 설치
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && curl -sSL https://install.python-poetry.org | python3 -

# 애플리케이션 종속성 설치
COPY pyproject.toml ./
RUN poetry install --no-root --no-ansi --no-dev
# RUN pwd
# RUN cd /app python3 manage.py migrate

# 애플리케이션 코드 복사
COPY . /app