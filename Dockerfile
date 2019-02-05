FROM python:3.6.7-alpine

#ENV PIPENV_VERSION=2018.7.1

#RUN pip install "pipenv==$PIPENV_VERSION"

RUN apk --no-cache add \
     bash \
     build-base \
     curl \
     gcc \
     gettext \
     git \
     libffi-dev \
     linux-headers \
     musl-dev \
     postgresql-dev \
     tini

ADD . /code
WORKDIR /code

RUN pip install pipenv
RUN pipenv install --system --deploy
CMD ["python", "entry.py"]