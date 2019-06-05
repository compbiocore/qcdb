import os
import mysql.connector
from qcdb.connection import connection
import pytest
import subprocess
import time

from dotenv import load_dotenv
load_dotenv()


@pytest.fixture
def params():
    params_ = {'user': 'root',
              'password': 'password',
              'host': os.getenv("MYSQL_HOST"),
              'raise_on_warnings': True,
              }
    return params_

def test_connection(params):
    con = connection(params)

    assert(type(con) == mysql.connector.connection_cext.CMySQLConnection)
    assert(con.is_connected() == True)


def test_datsci_msql_conn(params):
    if os.getenv("MYSQLUSER"):
        params["user"] = os.getenv("MYSQLUSER")
        params["password"] = os.getenv("MYSQLPASSWORD")
        params["host"] = "pdspracticemydbcit.services.brown.edu"

        con = connection(params)

        assert(type(con) == mysql.connector.connection_cext.CMySQLConnection)
        assert(con.is_connected() == True)
