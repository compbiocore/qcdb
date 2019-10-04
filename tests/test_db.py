import pytest
import os

from dotenv import load_dotenv
load_dotenv()

# Tests that there are only 3 tables
def test_3_tables(metadata):
	tables = metadata.tables.keys()
	assert(len(tables)==3)

# # TEST DB_LOAD

import qcdb.db_load as dbl

def test_parse_nobuildref(metadata,session,test_yaml):
	with pytest.raises(Exception):
		session.execute("DELETE from references;")
		dbl.parse(test_yaml,metadata,session,False)

from qcdb.parsers.fastqc_parse import fastqcParser
dirname = os.path.dirname(__file__)

def test_insert(metadata,session):
	results = fastqcParser(os.path.join(dirname,'data','SRS643404_SRX612438_fastqc.zip'), session, metadata.tables['reference'], True)
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