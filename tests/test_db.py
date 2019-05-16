from sqlalchemy import *
from sqlalchemy.orm import Session
import oyaml as yaml
import pytest
import os
from qcdb.tables_create import tables
from qcdb.db_load import parse

@pytest.fixture
def test_yaml():
	dirname = os.path.dirname(__file__)
	return(os.path.join(dirname,'test_params.yaml'))

@pytest.fixture
def test_data():
	dirname = os.path.dirname(__file__)
	return(os.path.join(dirname,'data'))

@pytest.fixture(scope='session')
def connection(request, tmpdir_factory):
	#engine = create_engine('mysql+pymysql://root:password@0.0.0.0:3306/qcdb')
	fn = tmpdir_factory.mktemp('db').join('test.db')
	engine = create_engine('sqlite:///'+str(fn))

	metadata = MetaData()
	metadata = tables(metadata)
	metadata.create_all(engine)

	connection = engine.connect()
	# this finalizer for dropping the tables isn't working, not sure why
	#request.addfinalizer(metadata.drop_all(engine))
	return connection

# Tests that there are only 3 tables
def test_3_tables(connection):
	m = MetaData()
	m.reflect(bind=connection)
	tables = m.tables.keys()
	assert(len(tables)==3)

# not really in use but works
@pytest.fixture(scope='function')
def session(connection, request):
	transaction = connection.begin()
	session = Session(bind=connection)

	def teardown():
		session.close()
		transaction.rollback()
		connection.close()

	request.addfinalizer(teardown)
	return session

# Tests that everything loads
# Test should probably be more fine-grained and make use of
# session fixture
#def test_db_load(connection, session, test_yaml):
#	with open(test_yaml, 'r') as io:
#		d = yaml.load(io)
#	m = MetaData()
#	m.reflect(bind=connection)
#	parse(d,m,session)