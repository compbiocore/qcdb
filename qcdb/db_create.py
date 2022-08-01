from sqlalchemy import *
from sqlalchemy.orm import Session
from qcdb.connection import connection
import argparse
import logging
import oyaml as yaml
import os
import sys
import sqlalchemy

# Initialize the logger
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


# columns are organized by how they are found in sra_metadata.py
def tables(metadata):
    samplemeta = Table('samplemeta', metadata,
        Column('_id', Integer, primary_key=True, autoincrement=True),
        Column('db_id', String(50), primary_key=True, unique=True), # formerly sample_id for db
        Column('sample_id', String(50), nullable=False), # = sample_id from SRA
        Column('experiment_id', String(50)), # = experiment_id from SRA
        Column('library_name', String(50)), #
        Column('library_strategy', String(50)),
        Column('library_source', String(50)),
        Column('library_selection', String(50)),
        Column('library_layout', String(50)), #
        Column('platform', String(50)), #
        Column('instrument_model', String(50)), #
        Column('sra_ids', String(50)), #
        Column('run_ids', String(50)), # = SRR, ERR, DRR
        Column('run_center', String(100)), #
        Column('project_id', String(50)), # = SRP, ERP, DRP
        Column('taxon_id', String(50)), #
        Column('scientific_name', String(50)), #
        Column('published', String(50)), #
        Column('spots', Integer), #
        Column('bases', BigInteger), #
        Column('experiment_name', String(100)), # maybe TITLE?
        Column('study_type', String(50)), #
        Column('center_project_name', String(50)), #
        Column('submission_center', String(50)), #
        Column('submission_lab', String(50)), #
        Column('json', JSON) #
        )

    reference = Table('reference', metadata,
        Column('qc_program', String(50), primary_key=True),
        Column('qc_metric', String(50), primary_key=True),
        Column('field_name', String(50), primary_key=True),
        Column('field_code', String(5)),
        Column('display_name', String(50))
        )

    metrics = Table('metrics', metadata,
        Column('_id', Integer, primary_key=True),
        Column('samplemeta_id', Integer),
        Column('db_id', String(50)),
        Column('qc_program', String(50)),
        Column('qc_metric', String(50)),
        Column('read_type', Integer),
        Column('data', JSON),
        ForeignKeyConstraint(['qc_program', 'qc_metric'],
            ['reference.qc_program', 'reference.qc_metric']),
        # db_id, qc_program, qc_metric, read_type combo must be unique
        UniqueConstraint('db_id', 'qc_program', 'qc_metric', 'read_type'))

    return metadata


def db_create(params, db):
    # start connection
    conn = connection(params=params)

    log.info("Connected to {0}:{1}:{2}".format(params['host'],
                                            params['port'],
                                            db))

#    try:
    conn.execute("create database {};".format(db))
    logging.info("Created database {}".format(db))
    # appears to never get called...
    #except sqlalchemy.exc.DatabaseError:
    #    logging.info("Database {} already exists".format(db))

def main(config):

    with open(config, 'r') as io:
        d = yaml.load(io, Loader=yaml.FullLoader)

    # Set database name
    db = d['db']['name']
    params = d['db']['params']

    try:
        # Start connection
        conn = connection(params=params,db=db)
        log.info("Connected to {0}:{1}:{2}".format(params['host'],
                                            params['port'],
                                            db))
    except:
        db_create(params,db)
        conn = connection(params=params,db=db)

    # Init metadata
    log.info("Making tables...")
    metadata = tables(MetaData())
    metadata.create_all(conn, checkfirst=True)

if __name__ == '__main__':
    args = parser.parse_args()
    config = str(args.file)
    main(config)
