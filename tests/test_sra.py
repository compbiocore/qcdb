import qcdb.sra_metadata as sm
import pytest

@pytest.fixture
def sample_id1(): # no library_name, no run_center
	return("SRS643403_SRX612437")

@pytest.fixture
def sample_id2(): # library_name, no run_center
	return("SRS5193621_SRX6631077")

@pytest.fixture
def sample_id3(): # library_name, run_center, DRP/DRS
	return("DRS000001_DRX000001")

def test_sra_query_xml_1record(sample_id1):
	xml_tables = sm.sra_query_xml("compbiocore@brown.edu",sample_id1)
	assert(len(xml_tables)==1)

@pytest.fixture
def xml1(sample_id1):
	xml_tables=sm.sra_query_xml("compbiocore@brown.edu",sample_id1)
	return(xml_tables[0])

@pytest.fixture
def xml2(sample_id2):
	xml_tables=sm.sra_query_xml("compbiocore@brown.edu",sample_id2)
	return(xml_tables[0])

@pytest.fixture
def xml3(sample_id3):
	xml_tables=sm.sra_query_xml("compbiocore@brown.edu",sample_id3)
	return(xml_tables[0])

def test_get_metadata(xml1):
	metadata = sm.get_metadata(xml1)
	assert(metadata['SRS_ID'] == 'SRS643403')
	assert(metadata['SRX_ID'] == 'SRX612437')
	assert(metadata['library_name'] == '')
	assert(metadata['run_center'] == '')

def test_get_metadata2(xml2):
	metadata = sm.get_metadata(xml2)
	assert(metadata['SRS_ID'] == 'SRS5193621')
	assert(metadata['SRX_ID'] == 'SRX6631077')
	assert(metadata['library_name'] == 'NexteraXT')
	assert(metadata['run_center'] == '')

def test_get_metadata3(xml3):
	metadata = sm.get_metadata(xml3)
	assert(metadata['SRS_ID'] == 'DRS000001')
	assert(metadata['SRX_ID'] == 'DRX000001')
	assert('BEST195' in metadata['library_name'])
	assert(metadata['run_center'] == 'NIG')

def test_get_json(xml1):
	json = sm.get_json(xml)
	assert(isinstance(json,str)==True)

def test_sra_metadata(sample_id):
	metadata = sm.sra_metadata(sample_id)
	with pytest.raises(KeyError):
		metadata['SRS_ID']
	with pytest.raises(KeyError):
		metadata['SRX_ID']

def test_bad_sample_id(sample_id):
	with pytest.raises(Exception):
		sm.sra_metadata("SRS643403_SRX612431")