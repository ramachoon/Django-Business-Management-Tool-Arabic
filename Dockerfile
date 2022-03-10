FROM python:3.9-slim-buster

ENV PYTHONDONTWRITECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SUPERUSER_PASSWORD 12345678Ab

RUN mkdir /src
WORKDIR /src
COPY ./src /src

RUN pip install --upgrade pip
ADD /requirements/requirements.txt /src
RUN pip install -r requirements.txt

CMD while ! python3 manage.py sqlflush > /dev/null 2>&1 ; do sleep 2 ; done && \
    python3 manage.py makemigrations --noinput && \
    python3 manage.py migrate --noinput && \
    python3 manage.py collectstatic --noinput && \
    python3 manage.py createsuperuser --user admin --email admin@gmail.com --noinput; \
    gunicorn -b 0.0.0.0:8000 config.wsgi
