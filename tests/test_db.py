from sqlalchemy import *
from sqlalchemy.orm import Session
import oyaml as yaml
import pytest
import os
from qcdb.db_create import tables, db_create
from qcdb.connection import connection

from dotenv import load_dotenv
load_dotenv()

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


# Tests that there are only 3 tables
def test_3_tables(metadata):
	tables = metadata.tables.keys()
	assert(len(tables)==3)

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

# # TEST PARSERS

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
		assert(r.sample_id.startswith('SRS'))
		assert(r.experiment.startswith('SRX'))
		# don't have paired end test files right now
		assert(r.db_id.split('_')[2]=='se')
		assert(r.library_read_type=='single ended')
		# FASTQC has 11 modules
		# could do this based off of the tables YAML as an auto check
		assert(len(r.metrics) == 11)

	# test that the reference table updated with minified values
	count = 0
	for row in session.execute(metadata.tables['reference'].select()):
		if count == 0:
			assert(len(row['field_name']) > len(row['field_code']))
		count +=1
	assert(count > 0)

def test_qckitfastqparser(session, metadata):
	results = qckitfastqParser(os.path.join(dirname, 'data', 'SRS643403_SRX612437_overrep_kmer.csv'), session, metadata.tables['reference'], true)
	assert(results.sample_id.startswith('SRS'))
	assert(results.experiment.startswith('SRX'))
	assert(results.db_id.split('_')[2]=='se')
	assert(results.library_read_type=='single ended')
	assert(len(results.metrics)==1)

def test_picardtoolsparser(session, metadata):
    results = picardtoolsParser(os.path.join(dirname, 'data', 'SRS999999_SRX999999_summary_gcbias_metrics_picard.txt'), session, metadata.tables['reference'], true)
    assert(results.sample_id.startswith('SRS'))
    assert(results.experiment.startswith('SRX'))
    assert(len(results.metrics) == 1)

# # TEST DB_LOAD

import qcdb.db_load as dbl

def test_parse_nobuildref(metadata,session,test_yaml):
	with pytest.raises(Exception):
		session.execute("DELETE from references;")
		dbl.parse(test_yaml,metadata,session,False)


def test_insert(metadata,session):
	results = fastqcParser(os.path.join(dirname,'data','SRS643404_SRX612438_fastqc.zip'), session, metadata.tables['reference'], False)
	dbl.insert(results,metadata,session)
	s = metadata.tables['samplemeta']
	print(s.c.db_id)
	q = session.query(s).filter(s.c.db_id=='SRS643404_SRX612438_se')
	assert(session.query(q.exists()).scalar())

	# test that double insert will raise exception
	with pytest.raises(Exception):
		dbl.insert(results,metadata,session)

def test_parse(metadata,session,test_yaml):
	dbl.parse(test_yaml,metadata,session,True)