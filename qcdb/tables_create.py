from sqlalchemy import *
from qcdb.connection import connection
from collections import OrderedDict
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


# assuming our only types will be Integer, Float and String
def sql_types(type_):
    if type_ == 'Integer':
        return Integer
    elif type_ == 'Float':
        return Float
    else:
        return String(int(type_.split('(')[1].strip(')')))

def metadata_tables(metadata):
    # Sample metadata table
    samplemeta = Table('samplemeta', metadata,
        Column('sample_id', String(50), primary_key=True),
        Column('sample_name', String(50), nullable=False),
        Column('library_read_type', String(50)),
        Column('experiment', String(50))
    )

    files = glob2.glob(os.path.join(dirname,'tables/*.yaml'))
    for f in files:
        with open(f, 'r') as io:
            d = yaml.load(io)
        for t in d:
        	Table(t['table'], metadata, 
        		Column('_id', Integer, primary_key=True),
        		Column('sample_id', String(50), ForeignKey('samplemeta.sample_id')),
        		*(Column(name=x['name'],type_=sql_types(x['type'])) for x in t['columns']))

    return metadata

def main():

    # Set database name
    db = 'qcdb'

    # Start connection
    conn = connection(db=db)

    # Init metadata
    log.info("Making tables...")
    metadata = metadata_tables(MetaData())
    metadata.create_all(conn, checkfirst=True)

if __name__ == '__main__':
    main()