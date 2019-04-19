from sqlalchemy import *
from connection import connection
from collections import OrderedDict
import oyaml as yaml
import os
import glob2
from modules.qckitfastq.tables_create import qckitfastq_create


# stub for turning table creation into a class
#class TableCreate:
#	"""
#	A class for creating tables in qcdb
#	"""
#	def __init__(self):
#		self.name = None
#		self.metadata = None
#		return

# Set database name
db = 'qcdb'

# Start connection
conn = connection(db=db)

# Init metadata
metadata = MetaData()

#for root, dirs, files in os.walk('modules'):
#	if not dirs:
#		assert('tables_create.py' in files)
#		from root import tables_create

# Sample metadata table
samplemeta = Table('samplemeta', metadata,
    Column('sample_id', String(50), primary_key=True),
    Column('sample_name', String(50), nullable=False),
    Column('library_read_type', String(50)),
    Column('experiment', String(50))
)

# assuming our only types will be Integer, Float and String
def sql_types(type_):
    if type_ == 'Integer':
        return Integer
    elif type_ == 'Float':
        return Float
    else:
        return String(int(type_.split('(')[1].strip(')')))


files = glob2.glob('tables/*.yaml')
for f in files:
    with open(f, 'r') as io:
        d = yaml.load(io)
    for t in d:
    	Table(t['table'], metadata, 
    		Column('_id', Integer, primary_key=True),
    		Column('sample_id', String(50), ForeignKey('samplemeta.sample_id')),
    		*(Column(name=x['name'],type_=sql_types(x['type'])) for x in t['columns']))

qckitfastqc_create(metadata)

metadata.create_all(conn, checkfirst=True)