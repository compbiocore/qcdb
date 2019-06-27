#!/usr/bin/env python
#
# Taken from bioflows

# query SRA and insert relevant metadata + JSON into db

import json
from Bio import Entrez
from collections import OrderedDict
#from xml.etree.ElementTree import fromstring
#from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as ET
from xmljson import Abdera  

##########


#xml_results = sra_query_xml('joselynn_wallace@brown.edu', 'SRS643408_SRX612442')
#json_results = get_json(xml_results)
#metadata_results = get_metadata(xml_results)

#still to do: 
#make sra_load.py import the SRS_SRX id from qcdb tables
#write some tests for sra_load.py

##########

ab = Abdera(dict_type=OrderedDict)

def sra_query_xml(email, sample_id):
    Entrez.email = email
    sra_results = Entrez.read(Entrez.esearch(db='sra', term=(sample_id.split("_")[0]))) 
    sra_id = sra_results['IdList'][0]
    sra_fetch = Entrez.efetch(db='sra', id=sra_id, rettype='text', retmode='xml')
    xml_table = sra_fetch.read()
    return(xml_table)

def get_json(xml):
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
        if 'SRA' in node.text:
            keys.append('SRA_ID')
            values.append(node.text)
        if 'SRR' in node.text:
            keys.append('SRR_ID')
            values.append(node.text)
        if 'SRP' in node.text:
            keys.append('SRP_ID')
            values.append(node.text)
        if 'SRX' in node.text:
            keys.append('SRX_ID')
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
