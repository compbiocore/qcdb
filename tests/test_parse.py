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
	assert(BaseParser("SRS1_SRX2_1","a", session, metadata.tables['reference'], True).library_read_type=='paired-end forward')
	assert(BaseParser("SRS1_SRX2_2",'b', session, metadata.tables['reference'], True).library_read_type=='paired-end reverse')
	assert(BaseParser("SRS1_SRX2_a",'c', session, metadata.tables['reference'], True).library_read_type=='single ended')
	with pytest.raises(KeyError):
		BaseParser("SRS1_SRX2_3",'d', session, metadata.tables['reference'], True)

def test_fastqcparser(session, metadata):
	r = fastqcParser(os.path.join(dirname, 'data', 'SRS643403_SRX612437_fastqc.zip'), session, metadata.tables['reference'], True)
	assert(isinstance(r, fastqcParser))
	assert(r.sample_id.startswith('SRS'))
	assert(r.experiment.startswith('SRX'))
	assert(r.library_read_type=='single ended')
	assert(len(r.metrics)==11)

	# test that the reference table updated with minified values
	count = 0
	for row in session.execute(metadata.tables['reference'].select()):
		if count == 0:
			assert(len(row['field_name']) > len(row['field_code']))
		count +=1
	assert(count > 0)

def test_fastqcparser_notilequal(session, metadata):
	r = fastqcParser(os.path.join(dirname, 'data', 'SRS4807080_SRX5884550_1_fastqc.zip'), session, metadata.tables['reference'], True)
	assert(isinstance(r, fastqcParser))
	assert(r.sample_id.startswith('SRS'))
	assert(r.experiment.startswith('SRX'))
	assert(r.library_read_type=='paired-end forward')
	assert(len(r.metrics)==10)

def test_fastqcparser_notile_nooverrep(session, metadata):
	r = fastqcParser(os.path.join(dirname, 'data', 'SRS4807083_SRX5884553_2_fastqc.zip'), session, metadata.tables['reference'], True)
	assert(isinstance(r, fastqcParser))
	assert(r.sample_id.startswith('SRS'))
	assert(r.experiment.startswith('SRX'))
	assert(r.library_read_type=='paired-end reverse')
	assert(len(r.metrics)==9)	

def test_qckitfastqparser(session, metadata):
	results = qckitfastqParser(os.path.join(dirname, 'data', 'SRS643403_SRX612437_overrep_kmer.csv'), session, metadata.tables['reference'], True)
	assert(results.sample_id.startswith('SRS'))
	assert(results.experiment.startswith('SRX'))
	assert(results.db_id.split('_')[2]=='se')
	assert(results.library_read_type=='single ended')
	assert(len(results.metrics)==1)

def test_picardtoolsparser(session, metadata):
    results = picardtoolsParser(os.path.join(dirname, 'data', 'SRS999999_SRX999999_summary_gcbias_metrics_picard.txt'), session, metadata.tables['reference'], True)
    assert(results.sample_id.startswith('SRS'))
    assert(results.experiment.startswith('SRX'))
    assert(len(results.metrics) == 1)