import qcdb.sra_metadata as sm
import pytest

# sends 4 queries
# if you run too often, it will time out...
# need to implement a solution to this.

@pytest.fixture
def sample_id2(): # library_name, no run_center
	return("SRS5193621_SRX6631077")

@pytest.fixture
def sample_id3(): # library_name, run_center, DRP/DRS
	return("DRS000001_DRX000001")

@pytest.fixture
def xml2(sample_id2):
	xml_tables=sm.sra_query_xml("compbiocore@brown.edu",sample_id2)
	return(xml_tables[0])

@pytest.fixture
def xml3(sample_id3):
	xml_tables=sm.sra_query_xml("compbiocore@brown.edu",sample_id3)
	return(xml_tables[0])

def test_get_metadata2(xml2):
	metadata = sm.get_metadata(xml2)
	assert(metadata['SRS_ID'] == 'SRS5193621')
	assert(metadata['SRX_ID'] == 'SRX6631077')
	assert(metadata['library_name'] == 'NexteraXT')
	assert(metadata['run_center'] == None)

def test_get_metadata3(xml3):
	metadata = sm.get_metadata(xml3)
	assert(metadata['SRS_ID'] == 'DRS000001')
	assert(metadata['SRX_ID'] == 'DRX000001')
	assert('BEST195' in metadata['library_name'])
	assert(metadata['run_center'] == 'NIG')

def test_get_json(xml2):
	json = sm.get_json(xml2)
	assert(isinstance(json,str)==True)

def test_sra_metadata(sample_id2):
	metadata = sm.sra_metadata(sample_id2)
	with pytest.raises(KeyError):
		metadata['SRS_ID']
	with pytest.raises(KeyError):
		metadata['SRX_ID']

def test_bad_sample_id():
	with pytest.raises(Exception):
		sm.sra_metadata("SRS643403_SRX612431")