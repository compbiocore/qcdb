from sqlalchemy import *
from sqlalchemy.orm import Session
import glob2
import oyaml as yaml
import os
#import pandas as pd
import argparse
import logging
import sys
from ruamel.yaml import YAML
from ruamel.yaml.constructor import SafeConstructor
from qcdb_modify import QCDB_table
from connection import connection
import logging
from sqlalchemy import *
from sqlalchemy.orm import Session
import glob2
import oyaml as yaml
import os
#import pandas as pd
import argparse


def parse_yaml(yaml_file):
    with open(yaml_file) as f:
        docs = yaml.load(f, Loader=yaml.FullLoader)
    return results


def insert(results, m, session):
    s = m.tables['QCDB_table']
    for i in results:
        q = session.query(s).filter(s.c.db_id==i['db_id'])
        if not session.query(q.exists()).scalar():
            #Might need more condition to flow into the system??
            logging.info("Loading {} into metadata...".format(i['db_id']))
            value = QCDB_table(**i)
            if i['db_id'] is None:  # Give db_id an unique identifier and we have ID_column auto_increment for internal checks
                i['db_id'] = str(i['taxon_id'])+i['instrument_model'] # i['db_id'] == Null
            try:
                session.add(value)
                session.commit()  
            except:
                logging.error("Error of type: ", sys.exc_info()[0], sys.exc_info()[1])
        else:
            logging.error('Data already exists for {}'.format(i['db_id']))


if __name__ == "__main__":
    yaml_file = open('D:\Desktop\metadata_filled.yaml','r')
    params ={'user':'root',
                       'password':'arc_ccv_cbc_2022',
                       'host':'tdatascicit.services.brown.edu',
                       'port': '3306'}
    params['db'] = 'sampledata'
    try:
    	conn = connection(params,db = params['db'])
    except:
    	print('fail')
     #Create the session
    s = Session(bind=conn)
    m = MetaData()
    m.reflect(bind=conn)
    s1 = m.tables['QCDB_table']
    data = parse_yaml(yaml_file)
    qc = m.tables['QCDB_table']
    insert(data, m, s)

    #write to yaml file -TO DO
    