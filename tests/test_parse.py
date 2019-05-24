import glob2
import os
import pytest
from qcdb.parsers.parse import BaseParser
from qcdb.parsers.fastqc_parse import fastqcParser
from qcdb.parsers.qckitfastq_parse import qckitfastqParser
from qcdb.parsers.picardtools_parse import picardtoolsParser

dirname = os.path.dirname(__file__)

def test_library_read_type():
	assert(BaseParser("SRS1_SRX2_1").library_read_type=='paired-end forward')
	assert(BaseParser("SRS1_SRX2_2").library_read_type=='paired-end reverse')
	assert(BaseParser("SRS1_SRX2_a").library_read_type=='single ended')
	with pytest.raises(KeyError):
		BaseParser("SRS1_SRX2_3")

def test_fastqcparser():
	results = []
	files = glob2.glob(os.path.join(dirname, 'data', '*_fastqc.zip'))
	for f in files:
		results.append(fastqcParser(f))
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

def test_qckitfastqparser():
	results = qckitfastqParser(os.path.join(dirname, 'data', 'SRS643403_SRX612437_overrep_kmer.csv'))
	assert(results.sample_name.startswith('SRS'))
	assert(results.experiment.startswith('SRX'))
	assert(results.sample_id.split('_')[2]=='se')
	assert(results.library_read_type=='single ended')
	assert(len(results.metrics)==9)
    
def test_picardtoolsparser():
    results = picardtoolsParser(os.path.join(dirname, 'data', 'SRS999999_SRX999999_summary_gcbias_metrics_picard.txt'))
    assert(results.sample_name.startswith('SRS'))
    assert(results.experiment.startswith('SRX'))
    assert(len(results.metrics) == 3)
    assert(results.qc_progam == 'picard')
    
    
        