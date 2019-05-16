from sqlalchemy import *
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

# assuming our only types will be Integer, Float and String
def sql_types(type_):
    if type_ == 'Integer':
        return Integer
    elif type_ == 'Float':
        return Float
    else:
        return String(int(type_.split('(')[1].strip(')')))

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
        Column('qc_program', String(50), ForeignKey('reference.qc_program')),
        Column('qc_metric', String(50), ForeignKey('reference.qc_metric')),
        Column('data', JSON, nullable=False))

    return metadata

def main(config):

    with open(config, 'r') as io:
        d = yaml.load(io, Loader=yaml.FullLoader)

    # Set database name
    db = d['db']['name']
    params = d['db']['params']

    # Start connection
    conn = connection(params=params,db=db)

    # Init metadata
    log.info("Making tables...")
    metadata = tables(MetaData())
    metadata.create_all(conn, checkfirst=True)

if __name__ == '__main__':
    args = parser.parse_args()
    config = str(args.file)
    main(config)