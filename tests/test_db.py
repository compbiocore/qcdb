from sqlalchemy import *
from sqlalchemy.orm import Session
import pytest
import os

def test():
	assert 5 == 5

@pytest.fixture(scope='session')
def connection(request, tmpdir_factory):
	#engine = create_engine('mysql+pymysql://root:password@0.0.0.0:3306/qcdb')
	fn = tmpdir_factory.mktemp('db').join('test.db')
	engine = create_engine('sqlite:///'+str(fn))

	metadata = MetaData()

	samplemeta = Table('samplemeta', metadata,
    	Column('sample_id', String(50), primary_key=True),
	    Column('sample_name', String(50), nullable=False),
	    Column('library_read_type', String(50)),
	    Column('experiment', String(50))
	)

	# todo: code for creating the other tables

	metadata.create_all(engine)
	connection = engine.connect()
	#print("ok?")
	#request.addfinalizer(metadata.drop_all(connection))
	return connection

@pytest.fixture(scope='function')
def session(connection, request):
	#connection = engine.connect()
	#print("ok?")
	#connection = db.engine.connect()
	connection.execute("insert into samplemeta values('1','2','3','4')")
	transaction = connection.begin()
	session = Session(bind=connection)

	def teardown():
		session.close()
		transaction.rollback()
		connection.close()

	request.addfinalizer(teardown)
	return session

def test_db_tables(session):
	assert 0 == 0
	#connection.execute("insert into samplemeta values('1','2','3','4')")
#	print(metadata.tables.keys())
#	assert len(metadata.tables.keys()) == 1
	#assert 1 == session.query('show tables;').count()
	assert 1 == session.query('select * from samplemeta')