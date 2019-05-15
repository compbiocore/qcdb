import glob2
import os
import pytest
import warnings
from qcdb.parsers.parse import BaseParser
from qcdb.parsers.fastqc_parse import fastqcParser

def test_library_read_type():
	assert(BaseParser("SRS1_SRX2_1").library_read_type=='paired-end forward')
	assert(BaseParser("SRS1_SRX2_2").library_read_type=='paired-end reverse')
	assert(BaseParser("SRS1_SRX2_a").library_read_type=='single ended')
	with pytest.raises(KeyError):
		BaseParser("SRS1_SRX2_3")

def test_metadata(tmpdir):
	with open(os.path.join(tmpdir, "SRS1_SRX2_1"),'w') as f:
		f.write("a")
	with open(os.path.join(tmpdir, "SRS1_SRX2_2"),'w') as f:
		f.write("b")
	with open(os.path.join(tmpdir, "SRS1_SRX2_1"),'w') as f:
		f.write("duplicate")
	with pytest.warns(Warning):
		bp = BaseParser(os.path.join(tmpdir,"SRS1_SRX2_1"))
		bp.metadata(tmpdir)

def test_fastqcparser():
	results = []
	files = glob2.glob(os.path.join('data', '*_fastqc.zip'))
	for f in files:
		results.append(fastqcParser(f))
	for r in results:
		assert(isinstance(results, fastqcParser))
		assert(r.sample_name.startswith('SRS'))
		assert(r.experiment.startswith('SRX'))
		# don't have paired end test files right now
		assert(r.sample_id.split('_')[2]=='se')
		assert(r.library_read_type=='single ended')
		# FASTQC has 12 modules
		# could do this based off of the tables YAML as an auto check
		assert(len(results.tables) == 12)