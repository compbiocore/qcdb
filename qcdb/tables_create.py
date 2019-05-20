from sqlalchemy import *
from sqlalchemy.orm import Session
from qcdb.connection import connection
from collections import OrderedDict
import argparse
import logging
import oyaml as yaml
import os
import glob2

dirname = os.path.dirname(__file__)
log = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
handler.setLevel(logging.INFO)
log.addHandler(handler)
log.setLevel(logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('--file', '-f', help='Location of params.yaml', default='params.yaml')

def tables(metadata):
    samplemeta = Table('samplemeta', metadata,
        Column('sample_id', String(50), primary_key=True),
        Column('sample_name', String(50), nullable=False),
        Column('library_read_type', String(50)),
        Column('experiment', String(50)))

    reference = Table('reference', metadata,
        Column('qc_program', String(50), primary_key=True),
        Column('qc_metric', String(50), primary_key=True),
        Column('experiment_type', String(50), nullable=False)
        )

    metrics = Table('metrics', metadata,
        Column('_id', Integer, primary_key=True),
        Column('sample_id', String(50), ForeignKey('samplemeta.sample_id')),
        Column('qc_program', String(50)),
        Column('qc_metric', String(50)),
        Column('data', JSON),
        ForeignKeyConstraint(['qc_program', 'qc_metric'],
            ['reference.qc_program','reference.qc_metric']),
        # sample_id, qc_program, qc_metric combo must be unique
        UniqueConstraint('sample_id','qc_program','qc_metric')
        )

    return metadata

def populate(conn, metadata):
    session = Session(bind=conn)
    log.info("Populating reference...")
    with open(os.path.join(dirname,"reference.yaml"), 'r') as io:
        r = yaml.load(io, Loader=yaml.FullLoader)
    for ref in r:
        qc_program = ref['qc_program']
        experiment_type = ref['experiment_type']
        inserts = [{'qc_program': qc_program, 'experiment_type': experiment_type,
        'qc_metric': qc_metric} for qc_metric in ref['qc_metrics']]
        session.execute(metadata.tables['reference'].insert(), inserts)
        session.commit()

def main(config):

    with open(config, 'r') as io:
        d = yaml.load(io, Loader=yaml.FullLoader)

    # Set database name
    db = d['db']['name']
    params = d['db']['params']

    # Start connection
    conn = connection(params=params,db=db)
    log.info("Connected to {0}:{1}:{2}".format(params['host'],
                                            params['port'],
                                            db))
    # Init metadata
    log.info("Making tables...")
    metadata = tables(MetaData())
    metadata.create_all(conn, checkfirst=True)

    populate(conn, metadata)

if __name__ == '__main__':
    args = parser.parse_args()
    config = str(args.file)
    main(config)