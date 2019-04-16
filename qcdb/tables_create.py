from sqlalchemy import *
from connection import connection
import os
from modules.qckitfastq.tables_create import qckitfastq_create
from modules.fastqc.tables_create import fastqc_create

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

qckitfastq_create(metadata)
fastqc_create(metadata)

metadata.create_all(conn, checkfirst=True)