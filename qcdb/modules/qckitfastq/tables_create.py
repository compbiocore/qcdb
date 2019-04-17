from sqlalchemy import *

#stub
#class Module(TableCreate):
#    """FASTQC module"""

#    def __init__(self):
# alternatively can set it up as a YAML

def qckitfastq_create(metadata):

    # Adapter count
    adptcontent = Table('qckitfastq_adaptcontent', metadata,
        Column('_id', Integer, primary_key=True),
        Column('sample_id', String(50), ForeignKey('samplemeta.sample_id')),
        Column('adapter', String(100)),
        Column('count', Integer)
    )

    # GC Content table
    gccontent = Table('qckitfastq_gccontent', metadata,
        Column('_id', Integer, primary_key=True),
        Column('sample_id', String(50), ForeignKey('samplemeta.sample_id')),
        Column('read', Integer),
        Column('mean_GC', Integer)
    )

    # kmer count table
    kmercount = Table('qckitfastq_kmercount', metadata,
        Column('_id', Integer, primary_key=True),
        Column('sample_id', String(50), ForeignKey('samplemeta.sample_id')),
        Column('kmer', String(100)),
        Column('position', Integer),
        Column('count', Integer)
    )

    #Overrepresented Kmers table
    overkmer = Table('qckitfastq_overkmer', metadata,
        Column('_id', Integer, primary_key=True),
        Column('sample_id', String(50), ForeignKey('samplemeta.sample_id')),
        Column('row', Integer),
        Column('position', Integer),
        Column('obsexp_ratio', Float),
        Column('kmer', String(20))
    )

    #Overrepresented reads
    overreads = Table('qckitfastq_overreads', metadata,
        Column('_id', Integer, primary_key=True),
        Column('sample_id', String(50), ForeignKey('samplemeta.sample_id')),
        Column('read_sequence', String(200)),
        Column('count', Integer)
    )

    # Per base quality
    basequal = Table('qckitfastq_basequal', metadata,
        Column('_id', Integer, primary_key=True),
        Column('sample_id', String(50), ForeignKey('samplemeta.sample_id')),
        Column('position', Integer, nullable=False),
        Column('q10', Float),
        Column('q25', Float),
        Column('median', Float),
        Column('q75', Float),
        Column('q90', Float)
    )

    # Per read quality
    readqual = Table('qckitfastq_readqual', metadata,
        Column('_id', Integer, primary_key=True),
        Column('sample_id', String(50), ForeignKey('samplemeta.sample_id')),
        Column('read', Integer),
        Column('sequence_mean', Float)
    )

    # Read Content
    readcontent = Table('qckitfastq_readcontent', metadata,
        Column('_id', Integer, primary_key=True),
        Column('sample_id', String(50), ForeignKey('samplemeta.sample_id')),
        Column('position', Integer, nullable=False),
        Column('a', Integer),
        Column('c', Integer),
        Column('t', Integer),
        Column('g', Integer),
        Column('n', Integer),
    )

    # Read length
    readlength = Table('qckitfastq_readlength', metadata,
        Column('_id', Integer, primary_key=True),
        Column('sample_id', String(50), ForeignKey('samplemeta.sample_id')),
        Column('read_length', Integer),
        Column('num_reads', Integer)
    )