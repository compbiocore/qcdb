#!/usr/bin/env python
import logging
import os
import json
from Bio import Entrez
from collections import OrderedDict
#from xml.etree.ElementTree import fromstring
#from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as ET
from xmljson import Abdera  

log = logging.getLogger(__name__)
dirname = os.path.dirname(__file__)

def sra_metadata(sample_id):
    print("sample_id: ", sample_id)
    xmls = sra_query_xml("august_guang@brown.edu", sample_id)
    print("xmls")
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
        sra_fetch = Entrez.efetch(db='sra', id=sra_id, rettype='text', retmode='xml')
        xml_tables.append(sra_fetch.read())
    return(xml_tables)


def get_json(xml):
    ab = Abdera(dict_type=OrderedDict)
    json_table = json.dumps(ab.data(ET.fromstring(xml)))
    return(json_table)

def get_metadata(xml):
    tree = ET.fromstring(xml)
    keys = []
    values = []
    for node in tree.find('.//LIBRARY_DESCRIPTOR'):
        
        if node.tag == 'LIBRARY_STRATEGY':
            keys.append(node.tag)
            values.append(node.text)            
            #print(node.tag, node.text)
            
        if node.tag == 'LIBRARY_SOURCE':
            keys.append(node.tag)
            values.append(node.text)
            #print(node.tag, node.text)
            
        if node.tag == 'LIBRARY_SELECTION':
            keys.append(node.tag)
            values.append(node.text)
            #print(node.tag, node.text) 
              
        if node.tag == 'LIBRARY_LAYOUT': 
            for child in node:
                keys.append(node.tag)
                values.append(child.tag)
                #print(node.tag, child.tag)

    for node in tree.find('.//PLATFORM'):
        keys.append('PLATFORM') #seq platform
        values.append(node.tag)
        for child in node:#instrument model
            keys.append(child.tag)
            values.append(child.text)

            
    for node in tree.findall('.//PRIMARY_ID'):
        #print(node.tag, node.text)
        if 'sra' in node.text:
            keys.append('sra_ids')
            values.append(node.text)
        if 'SRR' in node.text:
            keys.append('run_ids')
            values.append(node.text)
        if 'SRP' in node.text:
            keys.append('project_id')
            values.append(node.text)
        if 'SRX' in node.text:
            keys.append('SRX_ID')
            values.append(node.text)              
        if 'SRS' in node.text:
            keys.append('SRS_ID')
            values.append(node.text)
        for child in node:
            print(child.tag, child.text)        
            
    for node in tree.findall('.//SAMPLE_NAME'):
        for child in node:
            keys.append(child.tag)
            values.append(child.text)
            
    for node in tree.findall('.//STUDY_TYPE'):
        #try get(keys) or whatever
        for k in node.attrib.keys():
            keys.append(k)
        for v in node.attrib.values():
            values.append(v)

    for node in tree.findall('.//CENTER_PROJECT_NAME'):
        keys.append(node.tag)
        values.append(node.text)
    
    for node in tree.findall('.//SUBMISSION'):
        keys.append('center_name')
        keys.append('lab_name')
        values.append((node.attrib).get('center_name'))
        values.append((node.attrib).get('lab_name'))
        
    for node in tree.findall('.//Statistics'):
        keys.append('spots')
        values.append((node.attrib).get('nspots'))
        
    for node in tree.findall('.//Bases'):
        values.append((node.attrib).get('count'))
        keys.append('bases')
        
        metadata_row = dict(zip(keys, values)) 
  
    return(metadata_row)    
