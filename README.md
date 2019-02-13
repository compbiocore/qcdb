# QCDB Development

## Prerequisites

#### Install Docker and docker-compose

[Docker Installation](https://docs.docker.com/docker-for-mac/install/)

#### Install dependencies
```
pip install sqlalchemy
pip install pymysql
```

## Development

#### Start MySQL Server
```
docker-compose up
```

#### Connect to Server
```
docker-compose exec db mysql -p
```
Password: `password`

#### Create database
From another terminal window:
```
python src/db_create.py
```

#### Create tables
```
python src/tables_create.py
```

#### Insert Data
```
python src/insert.py
```
