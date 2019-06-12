FROM python:3

WORKDIR /usr/src/

RUN pip install -I pytest==3.6
RUN pip install codecov \
                pytest-cov \
                sqlalchemy \
                glob2 \
                oyaml \
                pandas \
                mysql-connector-python \
                python-dotenv \
                pymysql

COPY . .
