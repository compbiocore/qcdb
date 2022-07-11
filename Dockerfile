FROM python:3.7

ADD . /usr/src
WORKDIR /usr/src

RUN pip install pipenv
RUN pipenv install --dev

COPY . .
