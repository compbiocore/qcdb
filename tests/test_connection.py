import os
import subprocess
import time
import mysql.connector
from dotenv import load_dotenv
from qcdb.connection import connection
import pytest

load_dotenv()

@pytest.fixture
def params():
    params = {'user': 'root',
              'password': 'password',
              'host': '0.0.0.0',
              'raise_on_warnings': True,
              }
    return params

def test_connection_local(params):
    # start mysql server on docker
    subprocess.run(['docker-compose', '-f', 'tests/data/docker-compose.yml', 'up', '-d'])
    time.sleep(10)

    con = connection(params)

    assert(type(con) == mysql.connector.connection_cext.CMySQLConnection)
    assert(con.is_connected() == True)

def test_datsci_msql_conn(params):
    params["user"] = os.getenv("MYSQLUSER")
    params["password"] = os.getenv("MYSQLPASSWORD")
    params["host"] = "pdspracticemydbcit.services.brown.edu"

    con = connection(params)

    assert(type(con) == mysql.connector.connection_cext.CMySQLConnection)
    assert(con.is_connected() == True)
