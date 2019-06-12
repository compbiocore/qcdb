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

@pytest.fixture(scope='session')
def metadata(connection):
	m = MetaData()
	m.reflect(bind=connection)
	return(m)

# Tests that there are only 3 tables
def test_3_tables(metadata):
	tables = metadata.tables.keys()
	assert(len(tables)==3)

# not really in use but works
@pytest.fixture(scope='session')
def session(connection, request):
	transaction = connection.begin()
	session = Session(bind=connection)

	def teardown():
		session.close()
		transaction.rollback()
		connection.close()

	request.addfinalizer(teardown)
	return session

# TEST PARSERS

import glob2
import os
import pytest
from qcdb.parsers.parse import BaseParser
from qcdb.parsers.fastqc_parse import fastqcParser
from qcdb.parsers.qckitfastq_parse import qckitfastqParser
from qcdb.parsers.picardtools_parse import picardtoolsParser

dirname = os.path.dirname(__file__)

def test_library_read_type(session, metadata):
	assert(BaseParser("SRS1_SRX2_1","a", session, metadata.tables['reference'], true).library_read_type=='paired-end forward')
	assert(BaseParser("SRS1_SRX2_2",'b', session, metadata.tables['reference'], true).library_read_type=='paired-end reverse')
	assert(BaseParser("SRS1_SRX2_a",'c', session, metadata.tables['reference'], true).library_read_type=='single ended')
	with pytest.raises(KeyError):
		BaseParser("SRS1_SRX2_3",'d', session, metadata.tables['reference'], true)

def test_fastqcparser(session, metadata):
	results = []
	files = glob2.glob(os.path.join(dirname, 'data', '*_fastqc.zip'))
	for f in files:
		results.append(fastqcParser(f, session, metadata.tables['reference'], true))
	for r in results:
		assert(isinstance(r, fastqcParser))
		assert(r.sample_name.startswith('SRS'))
		assert(r.experiment.startswith('SRX'))
		# don't have paired end test files right now
		assert(r.sample_id.split('_')[2]=='se')
		assert(r.library_read_type=='single ended')
		# FASTQC has 11 modules
		# could do this based off of the tables YAML as an auto check
		assert(len(r.metrics) == 11)

def test_qckitfastqparser(session, metadata):
	results = qckitfastqParser(os.path.join(dirname, 'data', 'SRS643403_SRX612437_overrep_kmer.csv'), session, metadata.tables['reference'], true)
	assert(results.sample_name.startswith('SRS'))
	assert(results.experiment.startswith('SRX'))
	assert(results.sample_id.split('_')[2]=='se')
	assert(results.library_read_type=='single ended')
	assert(len(results.metrics)==9)

def test_picardtoolsparser(session, metadata):
    results = picardtoolsParser(os.path.join(dirname, 'data', 'SRS999999_SRX999999_summary_gcbias_metrics_picard.txt'), session, metadata.tables['reference'], true)
    assert(results.sample_name.startswith('SRS'))
    assert(results.experiment.startswith('SRX'))
    assert(len(results.metrics) == 3)
