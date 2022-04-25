from sqlalchemy import *
from sqlalchemy.orm import Session
from qcdb.connection import connection
import glob2
import oyaml as yaml
import os
#import pandas as pd
import argparse
import logging
#import sys
#import json
from qcdb.sra_metadata import sra_metadata
from qcdb.parsers.qckitfastq_parse import qckitfastqParser
from qcdb.parsers.fastqc_parse import fastqcParser
from qcdb.parsers.picardtools_parse import picardtoolsParser

# Initialize the logger
log = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
handler.setLevel(logging.INFO)
log.addHandler(handler)
log.setLevel(logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('--file', '-f', help='Location of params.yaml', default='params.yaml')
parser.add_argument('--buildref', '-r', help='Flag to build reference table from this session', action='store_true')

def insert(results, m, session, metadata):
    s = m.tables['samplemeta']
    # check if db_id is in table already
    q = session.query(s).filter(s.c.db_id==results.db_id)
    if not session.query(q.exists()).scalar():
        log.info("Loading {} into metadata...".format(results.db_id))
        metadata = metadata(results.db_id)

        #sra_m = sra_metadata(results.db_id)
        #sra_m['db_id'] = results.db_id
        #sra_m['sample_id'] = results.sample_id
        #sra_m['experiment_id'] = results.experiment
        try:
            session.execute(s.insert().values(sra_m))
            session.commit()
        except:
            log.error("Error of type: ", sys.exc_info()[0], sys.exc_info()[1])

    metrics = m.tables['metrics']
    log.info("Loading {} results for db_id {} into metrics...".format(
        results.qc_program,results.db_id))
    try:
        session.execute(metrics.insert(), results.metrics)
        session.commit()
    except:
        log.error('Data already exists for {}'.format(results.db_id))
        raise Exception("Data already exists")

def dispatch_parse(directory, module_name, module_glob, module_fn, session, m, refs, build_ref, all_metadata):
    files = glob2.glob(os.path.join(directory, module_glob))
    if not files:
        log.error("No {0} output found in: {1}".format(module_name, directory))
    for f in files:
        try:
            results = module_fn(f, session, refs, build_ref)
        except:
            log.error("Error in parsing {}...".format(f))
        try:
            metadata = all_metadata[results.filename]
        except:
            log.error("No metadata for {}".format(results.filename))
        try:
            insert(results, m, session, metadata)
        except:
            pass
            #seems like uninformative error message
            #log.error("Error in insert for {}...".format(f))

# parse and load metrics & metadata
def parse(d, m, session, build_ref):
    # parse and load metadata
    for module in d['files']:
        directory = module['directory']
        with open(module['metadata'], 'r') as io:
            all_metadata = yaml.load(io, Loader=yaml.FullLoader)

        refs = m.tables['reference']

        if module['name'] == 'fastqc':
            dispatch_parse(directory, 'fastqc', '*_fastqc.zip', fastqcParser, session, m, refs, build_ref, all_metadata)
        elif module['name'] == 'qckitfastq':
            dispatch_parse(directory, 'qckitfastq', '*.csv', qckitfastqParser, session, m, refs, build_ref, all_metadata)
        elif module['name'] == 'picardtools':
            dispatch_parse(directory, 'picardtools', '*.txt', picardtoolsParser, session, m, refs, build_ref, all_metadata)

def main(config, build_ref):
    # Load load.yaml file
    with open(config, 'r') as io:
        d = yaml.load(io, Loader=yaml.FullLoader)

    db = d['db']['name']
    params = d['db']['params']
    # start connection
    conn = connection(params=params, db=db)
    log.info("Connected to {0}:{1}:{2}".format(params['host'],
                                            params['port'],
                                            db))
    session = Session(bind=conn)
    m = MetaData()
    m.reflect(bind=conn)

    parse(d, m, session, build_ref)

if __name__ == '__main__':
    args = parser.parse_args()
    config = str(args.file)
    build_ref = args.buildref
    main(config, build_ref)
