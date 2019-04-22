import glob2
import os
from qcdb.parsers.fastqc_parse import fastqcParser

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
		assert(r.library_read_type=='single ended')
		# FASTQC has 12 modules
		# could do this based off of the tables YAML as an auto check
		assert(len(results.tables) == 12)