import os
from qcdb.connection import connection
import sqlalchemy
import pytest
import subprocess
import time

#from dotenv import load_dotenv
#load_dotenv()


@pytest.fixture
def params():
    params_ = {'user': 'root',
              'password': 'password',
              'host': os.getenv("MYSQL_HOST"),
              'port': 3306,
              'raise_on_warnings': True
              }
    return params_

def test_connection(params):
    con = connection(params)

    assert(type(con) == sqlalchemy.engine.base.Connection)
    assert(con.invalidated == False)


def test_datsci_msql_conn(params):
    if os.getenv("MYSQLUSER"):
        params["user"] = os.getenv("MYSQLUSER")
        params["password"] = os.getenv("MYSQLPASSWORD")
        params["host"] = "pdspracticemydbcit.services.brown.edu"

        con = connection(params)

        assert(type(con) == sqlalchemy.engine.base.Connection)
        assert(con.invalidated == False)
