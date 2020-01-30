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
from qcdb.parsers.picardtools_parse import picardtoolsParser

def test_insert_singleend(test_data,metadata,session):
	db_id='SRS643404_SRX612438'
	results = fastqcParser(os.path.join(test_data,'SRS643404_SRX612438_fastqc.zip'), session, metadata.tables['reference'], True)
	dbl.insert(results,metadata,session)
	s = metadata.tables['samplemeta']
	q = session.query(s).filter(s.c.db_id==db_id, s.c.library_layout=='SINGLE')
	assert(session.query(q.exists()).scalar())
	m = metadata.tables['metrics']
	# test that there is 0
	qm = session.query(m).filter(m.c.db_id==db_id, m.c.qc_program=='fastqc', m.c.read_type==0)
	assert(session.query(qm.exists()).scalar())

	# test that double insert will raise exception
	with pytest.raises(Exception):
		dbl.insert(results,metadata,session)

def test_insert_pairedend(test_data,metadata,session):
	db_id='SRS4814656_SRX5892975'
	fastqc_results_1 = fastqcParser(os.path.join(test_data,'SRS4814656_SRX5892975_1_fastqc.zip'), session, metadata.tables['reference'], True)
	fastqc_results_2 = fastqcParser(os.path.join(test_data,'SRS4814656_SRX5892975_2_fastqc.zip'), session, metadata.tables['reference'], True)
	picard_results = picardtoolsParser(os.path.join(test_data, 'SRS4814656_SRX5892975_alignment_summary_metrics_picard.txt'), session, metadata.tables['reference'], True)
	dbl.insert(fastqc_results_1,metadata,session)
	dbl.insert(fastqc_results_2,metadata,session)
	dbl.insert(picard_results,metadata,session)
	s = metadata.tables['samplemeta']
	q = session.query(s).filter(s.c.db_id==db_id, s.c.library_layout=='PAIRED')
	assert(session.query(q.exists()).scalar())
	m = metadata.tables['metrics']
	# check that there is read1 and read2 but also that picardtools is NULL
	qm1 = session.query(m).filter(m.c.db_id==db_id, m.c.qc_program=='fastqc', m.c.read_type==1)
	qm2 = session.query(m).filter(m.c.db_id==db_id, m.c.qc_program=='fastqc', m.c.read_type==2)
	qm_picard = session.query(m).filter(m.c.db_id==db_id, m.c.qc_program=='picard', m.c.read_type==-1)
	assert(session.query(qm1.exists()).scalar())
	assert(session.query(qm2.exists()).scalar())
	assert(session.query(qm_picard.exists()).scalar())

def test_parse(metadata,session,test_yaml):
	dbl.parse(test_yaml,metadata,session,True)
