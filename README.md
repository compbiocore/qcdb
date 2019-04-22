# QCDB Development

## Prerequisites

#### Install Docker and docker-compose

[Docker Installation](https://docs.docker.com/docker-for-mac/install/)

#### Install dependencies
```
pip install sqlalchemy pymysql glob2 oyaml pandas
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
Code will likely only run for Python 3+. From another terminal window:
```
python qcdb/db_create.py
```

#### Create tables
```
python qcdb/tables_create.py
```

#### Load Data
Create a `params.yaml` file like the example below:
```yaml
db:
  name: qcdb
  params:
    host: 0.0.0.0
    port: 3306
    user: root
    password: password
files:
  module:
    - name: fastqc
    - directory: /Users/aguang/CORE/qckit/qcdb/tests/data
```

```
python -m qcdb.db_load -f path/to/params.yaml
```

#### Running tests

From the top level of the `qcdb` directory, run:
```
python -m pytest
```
