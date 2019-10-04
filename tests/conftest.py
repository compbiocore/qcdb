from sqlalchemy import *
from sqlalchemy.orm import Session
import pytest
import os
from qcdb.db_create import tables, db_create
from qcdb.connection import connection
import oyaml as yaml

@pytest.fixture
def test_yaml():
	dirname = os.path.dirname(__file__)
	with open(os.path.join(dirname, 'test_params.yaml'), 'r') as io:
		d = yaml.load(io, Loader=yaml.FullLoader)
		return(d)

@pytest.fixture
def test_data():
	dirname = os.path.dirname(__file__)
	return(os.path.join(dirname,'data'))

@pytest.fixture(scope='session')
def con(request):
    params = {'user': 'root',
              'password': 'password',
              'host': os.getenv("MYSQL_HOST"),
              'port': 3306,
              'raise_on_warnings': True
              }

    try:
        con = connection(params,db="test")
    except:
        db_create(params,db="test")
        con = connection(params,db="test")

    metadata = tables(MetaData())
    metadata.create_all(con, checkfirst=True)

    # need to work on this as right now the db doesn't get
    # deleted
    def teardown():
         con = connection(params,db="test")
         con.execute("drop database test;")
         con.close()

    request.addfinalizer(teardown)
    return con

@pytest.fixture(scope='session')
def metadata(con):
	m = MetaData()
	m.reflect(bind=con)
	return(m)

@pytest.fixture(scope='session')
def session(con, request):
	transaction = con.begin()
	session = Session(bind=con)

	def teardown():
		session.close()
		transaction.rollback()
		con.close()

	request.addfinalizer(teardown)
	return session