from doctest import script_from_examples
import logging
import os
from Bio import Entrez
#from xml.etree.ElementTree import fromstring
#from xml.etree.ElementTree import ElementTree
import time
import xml.etree.ElementTree as ET
import yaml
import argparse
import sys

# Summary: The script parses data folder and queries SRA based on files in data folder to return a single sheet called 
# metadata.yaml that contains important sample information. 

log = logging.getLogger(__name__)
dirname = os.path.dirname(__file__)

def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        print("One of your arguments is NOT a valid directory")
        sys.exit() 
    
parser = argparse.ArgumentParser()
parser.add_argument('-in', '--input_directory', required=True, type=dir_path, help='Location of your input files')
parser.add_argument('-out', '--output_directory', required=True, type=dir_path, help='Location where you want to save metadat.yaml')
args = parser.parse_args()

# Create classes for different file types 

# Overarching class to deal with different file types 
class determine_file_type: 
    def __new__(cls, naming):
        if naming.startswith("SRS"):
            return bioflows(naming) 
        else: 
            return sra_dump(naming) 

# Bioflows class 
class bioflows(object):
    def __new__(self, input):
        base_name = os.path.basename(input)
        self.filename = base_name
        self.db_id = base_name.split('_')[0] + '_' + base_name.split('_')[1]
        id_for_query = base_name.split('_')[0]
        query = sra_query_xml("compbiocore@brown.edu", id_for_query)
        if query:
            result = get_metadata(query[0])
            result['sample_id'] = result.pop('SRS_ID')
            result['experiment_id'] = result.pop('SRX_ID')
            result['db_id'] = self.db_id
            result_update = {self.db_id: result}
        else: 
            result = empty_metadata()
            result['db_id'] = self.db_id
            result_update = {self.db_id: result}
        return result_update 

# SRA class 
class sra_dump(object):
    def __new__(self, input):
        base_name = os.path.basename(input)
        self.filename = base_name
        check = "_"
        if check in base_name:
            self.db_id = base_name.split('_')[0] 
        else: 
            self.db_id = base_name.split(".")[0]
        query = sra_query_xml("compbiocore@brown.edu", self.db_id)
        if query:
            result = get_metadata(query[0])
            result['sample_id'] = result.pop('SRS_ID')
            result['experiment_id'] = result.pop('SRX_ID')
            result['db_id'] = self.db_id
            result_update = {self.db_id: result}
        else: 
            result = empty_metadata()
            result['db_id'] = self.db_id
            result_update = {self.db_id: result}
        return result_update

# Function for parsing data folder and querying SRA 
def create_metadata(input_path, output_path): 
    # Step 1: First get all folder elements and make them unique 
    folder_ids = os.listdir(input_path) # get list of all elements in folder - make sure to only get .zip files later 
    woduplicates = set(folder_ids) # remove duplicates
    folder_ids = list(woduplicates) # turn back into list 
    # Now we use classes we previously created to run on elements in list 
    dict_results = map(determine_file_type, folder_ids) 
    dict_results_new = {}
    for i in dict_results:
        dict_results_new.update(i)
    os.chdir(output_path)
    # Add try and exception here in near future iteration 
    with open('metadata.yml', 'w') as outfile:
        yaml.dump(dict_results_new, outfile, default_flow_style=False)

# Helper functions 

# Query SRA and get info
def sra_query_xml(email, sample_id):
    Entrez.email = email
    # this is SRX ID
    sra_results = Entrez.read(Entrez.esearch(db='sra', term=(sample_id))) 
    # todo: intersection of Entrez IdLists for srx and srs would be faster than
    # parsing metadata for each xml one would think
    xml_tables=[]
    for sra_id in sra_results['IdList']:
        time.sleep(1)
        sra_fetch = Entrez.efetch(db='sra', id=sra_id, rettype='text', retmode='xml')
        xml_tables.append(sra_fetch.read())
    return(xml_tables)

# Function to help get_meta data function get various ID's 
def find_ids(tag,text,key,m):
    assert(tag.isupper()) # all tags must be uppercase since we convert them to lower
    u=[tag,'D'+tag[1:],'E'+tag[1:]]
    tags=[s.lower() for s in u] + u
    # if no tags are in text then list(filter) will be empty
    if list(filter(lambda x: x in text,tags)) != []:
        m[key] = text

# Extracts metadata we need from SRA query 
def get_metadata(xml):
    tree = ET.fromstring(xml)
    m = dict.fromkeys(['library_name','library_strategy','library_source','library_selection',
    'library_layout','platform','instrument_model','sra_ids','run_ids','run_center',
    'project_id','taxon_id','scientific_name','published','spots','bases','experiment_name',
    'study_type','center_project_name','submission_center','submission_lab'])
    # experiment_name = TITLE
    m['experiment_name'] = tree.find('.//TITLE').text
    for node in tree.find('.//LIBRARY_DESCRIPTOR'):
        if node.tag == 'LIBRARY_NAME':
            m['library_name'] = node.text
        if node.tag == 'LIBRARY_STRATEGY':
            m['library_strategy'] = node.text         
        if node.tag == 'LIBRARY_SOURCE':
            m['library_source'] = node.text
        if node.tag == 'LIBRARY_SELECTION':
            m['library_selection'] = node.text
        if node.tag == 'LIBRARY_LAYOUT': 
            for child in node:
                m['library_layout'] = child.tag
    for node in tree.find('.//PLATFORM'):
        m['platform'] = node.tag
        for child in node: # instrument model
            m['instrument_model'] = child.text
    for node in tree.findall('.//PRIMARY_ID'):
        #print(node.tag, node.text)
        for i in zip(['SRA','SRR','SRP','SRX','SRS'],
            ['sra_ids','run_ids','project_id','SRX_ID','SRS_ID']):
            find_ids(i[0],node.text,i[1],m) 
    # TAXON_ID and SCIENTIFIC_NAME
    for node in tree.findall('.//SAMPLE_NAME'):
        for child in node:
            if child.tag == 'TAXON_ID':
                m['taxon_id'] = child.text
            if child.tag == 'SCIENTIFIC_NAME':
                m['scientific_name'] = child.text
    # RUN
    run_attrib = tree.find('.//RUN').attrib
    m['published'] = run_attrib.get('published')
    m['run_center'] = run_attrib.get('run_center')
    m['study_type'] = tree.find('.//STUDY_TYPE').attrib.get('existing_study_type')
    # for node in tree.findall('.//STUDY_TYPE'):
    #     #try get(keys) or whatever
    #     for k in node.attrib.keys():
    #         keys.append(k)
    #     for v in node.attrib.values():
    #         values.append(v)
    for node in tree.findall('.//CENTER_PROJECT_NAME'):
        m['center_project_name'] = node.text
    for node in tree.findall('.//SUBMISSION'):
        m['submission_center'] = node.attrib.get('center_name')
        m['submission_lab'] = node.attrib.get('lab_name')
        # keys.append('submission_center')
        # keys.append('submission_lab')
        # values.append((node.attrib).get('center_name'))
        # values.append((node.attrib).get('lab_name'))
    for node in tree.findall('.//Statistics'):
        m['spots'] = node.attrib.get('nspots')
    for node in tree.findall('.//Bases'):
        m['bases'] = node.attrib.get('count')
    return(m) 

# Creates empty metadata in case of empty query results 
def empty_metadata():
    m = dict.fromkeys(['library_name','library_strategy','library_source','library_selection',
    'library_layout','platform','instrument_model','sra_ids','run_ids','run_center',
    'project_id','taxon_id','scientific_name','published','spots','bases','experiment_name',
    'study_type','center_project_name','submission_center','submission_lab', "sample_id", "experiment_id"])
    return(m) 

# Testing the function that creates metadata.yaml file 
create_metadata(args.input_directory, args.output_directory)
# Example use from command line: python3 new_metadata.py -in /Users/jordan/Desktop/Projects/qcdb/test_data -out /Users/jordan/Desktop    
