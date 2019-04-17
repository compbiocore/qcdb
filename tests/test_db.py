from sqlalchemy import *
from sqlalchemy.orm import Session
import pytest
import os
from qcdb.modules.qckitfastq.tables_create import qckitfastq_create
from qcdb.modules.fastqc.tables_create import fastqc_create
#from qcdb.db_load import main

@pytest.fixture(scope='session')
def metadata():
	metadata = MetaData()

	samplemeta = Table('samplemeta', metadata,
    	Column('sample_id', String(50), primary_key=True),
	    Column('sample_name', String(50), nullable=False),
	    Column('library_read_type', String(50)),
	    Column('experiment', String(50))
	)

	qckitfastq_create(metadata)
	fastqc_create(metadata)

	return metadata

@pytest.fixture(scope='session')
def connection(request, tmpdir_factory, metadata):
	#engine = create_engine('mysql+pymysql://root:password@0.0.0.0:3306/qcdb')
	fn = tmpdir_factory.mktemp('db').join('test.db')
	engine = create_engine('sqlite:///'+str(fn))

	metadata.create_all(engine)
	connection = engine.connect()
	# this finalizer for dropping the tables isn't working, not sure why
	#request.addfinalizer(metadata.drop_all(engine))
	return connection

# Tests that the start of each table name should either be
# samplemeta, qckitfastq, or fastqc
def test_tables_all_prepended(metadata):
	tables = metadata.tables.keys()
	modules = set()
	for t in tables:
		modules.add(t.split('_')[0])
	assert(len(modules)==3)

@pytest.fixture(scope='function')
def session(connection, request):
	#connection = engine.connect()
	#print("ok?")
	#connection = db.engine.connect()
	transaction = connection.begin()
	session = Session(bind=connection)

	def teardown():
		session.close()
		transaction.rollback()
		connection.close()

	request.addfinalizer(teardown)
	return session

def test_fastqc_parse():
	#run fastqc parse
	#make sure data is in correct format

def test_db_load(session):
	#main("testdata/test.yaml")
	#tests using session.query to see that the data is actually in there
	assert 0 == 0
	#connection.execute("insert into samplemeta values('1','2','3','4')")
#	print(metadata.tables.keys())
#	assert len(metadata.tables.keys()) == 1
	#assert 1 == session.query('show tables;').count()
	#assert 1 == session.query('select * from samplemeta')