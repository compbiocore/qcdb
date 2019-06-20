from sqlalchemy import *
from sqlalchemy.orm import Session
from qcdb.connection import connection
import argparse
import logging
import oyaml as yaml
import os

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
        Column('sample_id', String(50), primary_key=True), # not the same as SRA
        Column('sample_name', String(50), nullable=False), # = sample_id from SRA
        Column('library_read_type', String(50)), # may be = library_layout from SRA
        Column('experiment', String(50)), # = experiment_id from SRA
        Column('run_date', String(50)),
        Column('updated_date', String(50)),
        Column('spots', Integer),
        Column('bases', Integer),
        Column('run_center', String(100)),
        Column('experiment_name', String(100)),
        Column('library_name', String(50)),
        Column('library_strategy', String(50)),
        Column('library_source', String(50)),
        Column('library_selection', String(50)),
        Column('library_layout', String(50)),
        Column('platform', String(50)),
        Column('instrument_model', String(50)),
        Column('instrument_name', String(50)),
        Column('taxon_id', String(50)),
        Column('common_name', String(50)),
        Column('study_type', String(50)),
        Column('center_project_name', String(50)),
        Column('submission_center', String(50)),
        Column('submission_lab', String(50)),
        Column('json', JSON)
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
        Column('sample_id', String(50), ForeignKey('samplemeta.sample_id')),
        Column('qc_program', String(50)),
        Column('qc_metric', String(50)),
        Column('data', JSON),
        ForeignKeyConstraint(['qc_program', 'qc_metric'],
            ['reference.qc_program', 'reference.qc_metric']),
        # sample_id, qc_program, qc_metric combo must be unique
        UniqueConstraint('sample_id', 'qc_program', 'qc_metric'))

    return metadata

<<<<<<< HEAD

def populate(session, metadata, reference_yaml):
    log.info("Populating reference...")
    with open(reference_yaml, 'r') as io:
        r = yaml.load(io, Loader=yaml.FullLoader)
    for ref in r:
        qc_program = ref['qc_program']
        experiment_type = ref['experiment_type']
        inserts = [{'qc_program': qc_program, 'experiment_type': experiment_type,
        'qc_metric': qc_metric} for qc_metric in ref['qc_metric']]
        session.execute(metadata.tables['reference'].insert(), inserts)
        session.commit()


=======
>>>>>>> f9d205626444beb07558b8be3d260c7d5490562e
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

if __name__ == '__main__':
    args = parser.parse_args()
    config = str(args.file)
    main(config)
