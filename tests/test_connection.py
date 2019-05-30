import os
import subprocess
import time
import mysql.connector
from qcdb.connection import connection
import pytest

if not os.getenv('TRAVIS'):
    from dotenv import load_dotenv
    load_dotenv()

@pytest.fixture
def params():
    params_ = {'user': 'root',
              'password': 'password',
              'host': '0.0.0.0',
              'raise_on_warnings': True,
              }
    return params_

def test_connection(params):
    if os.getenv('TRAVIS'):
        params["password"] = ""
        params["host"] = "127.0.0.1"
    else:
        subprocess.run(['docker-compose', '-f', 'tests/data/docker-compose.yml', 'up', '-d'])
        time.sleep(10)

    con = connection(params)

    assert(type(con) == mysql.connector.connection_cext.CMySQLConnection)
    assert(con.is_connected() == True)


# def test_datsci_msql_conn(params):
#     if os.getenv('TRAVIS'):
#         print('Skipping Datasci Server Test')
#     else:
#         params["user"] = os.getenv("MYSQLUSER")
#         params["password"] = os.getenv("MYSQLPASSWORD")
#         params["host"] = "pdspracticemydbcit.services.brown.edu"
#
#         con = connection(params)
#
#         assert(type(con) == mysql.connector.connection_cext.CMySQLConnection)
#         assert(con.is_connected() == True)
