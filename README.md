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

#### Contributing

Please, make sure to use commitizen to commit your messages.
If you don't have commitizen installed:
```
pip install commitizen
```
To commit, instead of `git commit -m` use `cz commit`.
For more information, [read here.](https://compbiocore.github.io/cbc-documentation-templates/semantic_release/)


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
