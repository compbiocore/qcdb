FROM python:3.7

#RUN  unset -v PYTHONPATH

ADD . /usr/src
WORKDIR /usr/src

RUN pip install pipenv
RUN pipenv install --dev

COPY . .
