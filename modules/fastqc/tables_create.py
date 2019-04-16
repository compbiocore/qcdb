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
    Column('sample_id', String(50), primary_key=True),
    Column('sample_name', String(50), nullable=False),
    Column('library_read_type', String(50)),
    Column('experiment', String(50))
)

# Per base sequence quality
fastqc_basequal = Table('fastqc_basequal', metadata,
    Column('_id', Integer, primary_key=True),
    Column('sample_id', String(50), ForeignKey('samplemeta.sample_id')),
    Column('base', String(50)),
    Column('mean', Float),
    Column('median', Float),
    Column('lower_quartile', Float),
    Column('upper_quartile', Float),
    Column('10th_percentile', Float),
    Column('90th_percentile', Float)
)

# Per tile sequence quality
fastqc_tilequal = Table('fastqc_tilequal', metadata,
    Column('_id', Integer, primary_key=True),
    Column('sample_id', String(50), ForeignKey('samplemeta.sample_id')),
    Column('tile', Integer),
    Column('base', String(50)),
    Column('mean', Float)
)

# Per sequence quality (equivalent to qckitfastq readqual)
fastqc_seqqual = Table('seqqual', metadata,
    Column('_id', Integer, primary_key=True),
    Column('sample_id', String(50), ForeignKey('samplemeta.sample_id')),
    Column('quality', Integer),
    Column('count', Integer)
)

# Per base sequence content
fastqc_perbaseseqcontent = Table('fastqc_perbaseseqcontent', metadata,
    Column('_id', Integer, primary_key=True),
    Column('sample_id', String(50), ForeignKey('samplemeta.sample_id')),
    Column('base', String(50), nullable=False),
    Column('g', Integer),
    Column('a', Integer),
    Column('t', Integer),
    Column('c', Integer)
)

# GC Content table
fastqc_gccontent = Table('fastqc_gccontent', metadata,
    Column('_id', Integer, primary_key=True),
    Column('sample_id', String(50), ForeignKey('samplemeta.sample_id')),
    Column('gc_content', Integer),
    Column('count', Integer)
)

# per base N content
fastqc_perbaseNcontent = Table('fastqc_perbaseNcontent', metadata,
    Column('_id', Integer, primary_key=True),
    Column('sample_id', String(50), ForeignKey('samplemeta.sample_id')),
    Column('base', String(50), nullable=False),
    Column('n', Integer)
)

# per sequence length distribution
fastqc_seqlength = Table('fastqc_seqlength', metadata,
    Column('_id', Integer, primary_key=True),
    Column('sample_id', String(50), ForeignKey('samplemeta.sample_id')),
    Column('length', Integer),
    Column('count', Integer)
)

# Sequence duplication levels
fastqc_seqdup = Table('fastqc_seqdup', metadata,
    Column('_id', Integer, primary_key=True),
    Column('sample_id', String(50), ForeignKey('samplemeta.sample_id')),
    Column('duplevel', String(50)),
    Column('percentdedup', Float),
    Column('percenttotal', Float)
)

#Overrepresented sequences
fastqc_overseqs = Table('fastqc_overseqs', metadata,
    Column('_id', Integer, primary_key=True),
    Column('sample_id', String(50), ForeignKey('samplemeta.sample_id')),
    Column('sequence', String(200)),
    Column('count', Integer),
    Column('percentage', Float),
    Column('possiblesource', String(50))
)

# Adapter content
fastqc_adaptercontent = Table('fastqc_adaptercontent', metadata,
    Column('_id', Integer, primary_key=True),
    Column('sample_id', String(50), ForeignKey('samplemeta.sample_id')),
    Column('position', String(50)),
    Column('illumina_universal', Float),
    Column('illumina_smallRNA3', Float),
    Column('illumina_smallRNA5', Float),
    Column('nextera_transposase', Float),
    Column('solid_smallRNA', Float)
)

# kmer count table
fastqc_kmercount = Table('fastqc_kmercount', metadata,
    Column('_id', Integer, primary_key=True),
    Column('sample_id', String(50), ForeignKey('samplemeta.sample_id')),
    Column('sequence', String(100)),
    Column('count', Integer),
    Column('pvalue', Float),
    Column('obsexp_max', Float),
    Column('position', String(50))
)

metadata.create_all(conn, checkfirst=True)
