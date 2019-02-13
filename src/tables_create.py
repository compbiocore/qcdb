from connection import connection
from sqlalchemy import *
from connection import connection


# Set database name
db = 'qcdb'

# Start connection
conn = connection(db=db)

# Init metadata
metadata = MetaData()

# Sample metadata table
samplemeta = Table('samplemeta', metadata,
    Column('sample_id', Integer, primary_key=True),
    Column('sample_name', String(50), nullable=False),
    Column('file_type', String(50)),
    Column('encoding', String(50)),
    Column('poor_quality', Integer),
    Column('seq_length', Integer),
    Column('percent_gc', Float)
)

# Adapter count
adptcontent = Table('adaptcontent', metadata,
    Column('_id', Integer, primary_key=True),
    Column('sample_id', Integer, ForeignKey('samplemeta.sample_id')),
    Column('adapter', String(100), nullable=False),
    Column('count', Integer, nullable=False)
)

# GC Content table
gccontent = Table('gccontent', metadata,
    Column('_id', Integer, primary_key=True),
    Column('sample_id', Integer, ForeignKey('samplemeta.sample_id')),
    Column('frequency', Integer),
    Column('mean_gc', Integer)
)

#Overrepresented Kmers table
overkmer = Table('overkmer', metadata,
    Column('_id', Integer, primary_key=True),
    Column('sample_id', Integer, ForeignKey('samplemeta.sample_id')),
    Column('row', Integer),
    Column('position', Integer),
    Column('obsexp_ratio', Float),
    Column('kmer', String(20))
)

#Overrepresented Sequences
overseq = Table('overseq', metadata,
    Column('_id', Integer, primary_key=True),
    Column('sample_id', Integer, ForeignKey('samplemeta.sample_id')),
    Column('sequence', String(200), nullable=False),
    Column('count', Integer, nullable=False)
)

# Per base quality
basequal = Table('basequal', metadata,
    Column('_id', Integer, primary_key=True),
    Column('sample_id', Integer, ForeignKey('samplemeta.sample_id')),
    Column('position', Integer, nullable=False),
    Column('q10', Integer),
    Column('q25', Integer),
    Column('median', Integer),
    Column('q75', Integer),
    Column('q90', Integer)
)

# Sequence Content
seqcontent = Table('seqcontent', metadata,
    Column('_id', Integer, primary_key=True),
    Column('sample_id', Integer, ForeignKey('samplemeta.sample_id')),
    Column('position', Integer, nullable=False),
    Column('scA', Integer),
    Column('scT', Integer),
    Column('scC', Integer),
    Column('scG', Integer),
    Column('scN', Integer),
)

metadata.create_all(conn, checkfirst=True)
