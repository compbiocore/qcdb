import logging
import os
import json
from Bio import Entrez
from collections import OrderedDict
#from xml.etree.ElementTree import fromstring
#from xml.etree.ElementTree import ElementTree
import time
import xml.etree.ElementTree as ET
from xmljson import Abdera  

log = logging.getLogger(__name__)
dirname = os.path.dirname(__file__)

def sra_metadata(sample_id):
    xmls = sra_query_xml("compbiocore@brown.edu", sample_id)
    for xml in xmls:
        metadata = get_metadata(xml)
        if metadata['SRS_ID'] == sample_id.split("_")[0]:
            json = get_json(xml)
            metadata["json"] = json
            assert(metadata.pop('SRS_ID', None) == sample_id.split("_")[0])
            assert(metadata.pop('SRX_ID', None) == sample_id.split("_")[1])
            return(metadata)
    log.error("No metadata found in SRA for {0}".format(sample_id))
    raise Exception

def sra_query_xml(email, sample_id):
    Entrez.email = email
    # this is SRX ID
    sra_results = Entrez.read(Entrez.esearch(db='sra', term=(sample_id.split("_")[1]))) 
    # todo: intersection of Entrez IdLists for srx and srs would be faster than
    # parsing metadata for each xml one would think
    xml_tables=[]
    for sra_id in sra_results['IdList']:
        time.sleep(1)
        sra_fetch = Entrez.efetch(db='sra', id=sra_id, rettype='text', retmode='xml')
        xml_tables.append(sra_fetch.read())
    return(xml_tables)


def get_json(xml):
    ab = Abdera(dict_type=OrderedDict)
    json_table = json.dumps(ab.data(ET.fromstring(xml)))
    return(json_table)


def find_ids(tag,text,key,m):
    assert(tag.isupper()) # all tags must be uppercase since we convert them to lower
    u=[tag,'D'+tag[1:],'E'+tag[1:]]
    tags=[s.lower() for s in u] + u
    # if no tags are in text then list(filter) will be empty
    if list(filter(lambda x: x in text,tags)) != []:
        m[key] = text

# do we need to include something if the tags don't exist?
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
        for child in node:#instrument model
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

    # published in run_center
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
