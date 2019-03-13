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
  directory: data/qcdb_test_files
  data:
    - name: adapter_content # this is the suffix of the file that qckitfastq outputs, without .csv
      table: adaptcontent # this is the name of the table in the database
    - name: gc_content
      table: gccontent
      columns: # columns from the file you want to keep on the table in database.
        - read
        - mean_GC
```

```
python src/db_load.py -f path/to/params.yaml
```
