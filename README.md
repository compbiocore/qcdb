## Master

[![Build Status](https://travis-ci.org/compbiocore/qcdb.svg?branch=master)](https://travis-ci.org/compbiocore/qcdb)[![codecov](https://codecov.io/gh/compbiocore/qcdb/branch/master/graph/badge.svg)](https://codecov.io/gh/compbiocore/qcdb)

## Devel

[![Build Status](https://travis-ci.org/compbiocore/qcdb.svg?branch=devel)](https://travis-ci.org/compbiocore/qcdb)[![codecov](https://codecov.io/gh/compbiocore/qcdb/branch/devel/graph/badge.svg)](https://codecov.io/gh/compbiocore/qcdb/branch/devel)

# QCDB Development

## Prerequisites

#### Install Docker and docker-compose

[Docker Installation](https://docs.docker.com/docker-for-mac/install/)

#### Install dependencies

Pre-requisite of `pipenv` needed [pipenv](https://docs.pipenv.org/en/latest/)

```
pipenv install
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

## Usage

All commands below need to be run from the top-level directory of this repository. All aspects related to starting and connection to the MySQL server are handled in the file `params.yaml`. The structure of the `params.yaml` file should look like the following:
```yaml
db:
  name: qcdb
  params:
    host: 127.0.0.1
    port: 3306
    user: root
    password: password
files:
  - name: fastqc
    directory: /Users/aguang/CORE/qckit/qcdb/tests/data/
  - name: qckitfastq
    directory: /Users/aguang/CORE/qckit/qcdb/tests/data/
  - name: picardtools
    directory: /Users/aguang/CORE/qckit/qcdb/tests/data/
```

Each module run in the commands below also take a `-f` argument which by default is set to the top-level `params.yaml`. Thus no additional arguments need to be provided. However, if the user wishes to provide a yaml file from a different location, that is possible by providing commands like the following:

**NOTE:** to take advantage of the pipenv installation, enter a `pipenv shell` before running the python commands


```
python -m qcdb.db_create -f path/to/params.yaml
```

Additionally, code will likely only run for Python 3+.

#### Start MySQL Server
```
docker-compose up
```

#### Connect to Server
```
docker-compose exec mysql mysql -p
```
Password: `password`

#### Create database and tables
From another terminal window:
```
python -m qcdb.db_create
```

#### Load Data
If loading for the first time or adding a new metric/file type, run with the `--buildref` flag.

```
python -m qcdb.db_load
```

#### Running tests via Docker Compose

```
docker-compose run test
```

For testing the connection, create a `.env` file in the `tests` folder with `MYSQLUSER` and `MYSQLPASSWORD` used to connect to the datasci mysql server.
