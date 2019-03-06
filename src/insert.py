from sqlalchemy import *
from connection import connection

db = 'qcdb'
conn = connection(db=db)


def get_tables(connection):
    # Create a MetaData instance
    metadata = MetaData()
    # reflect db schema to MetaData
    metadata.reflect(bind=conn)
    tables = metadata.tables
    return tables


def insert_(connection, table, values):
    # Get table
    t = get_tables(connection)[table]
    # Create insert statement
    ins = t.insert().values(values)
    # Execute query to insert data
    conn.execute(ins)


insert_(conn, 'samplemeta', {'sample_id': 1, 'sample_name': "test", 'file_type': 'test', 'encoding': 'Illumina1.8'})
insert_(conn, 'gccontent', {'sample_id': 1, 'frequency': 10, 'mean_gc': 100})

# insert_(conn, 'samplemeta', {'sample_name': 'testsample1',
#                             'file_type': 'base call',
#                             'encoding': 'sanger',
#                             'poor_quality': 10,
#                             'seq_length': 200,
#                             'percent_gc': 0.5
#                             })
