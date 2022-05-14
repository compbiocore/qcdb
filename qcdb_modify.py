from numpy import genfromtxt
from time import time
from datetime import datetime
from sqlalchemy import Column, Integer, Float, Date,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd 
from connection import connection
from sqlalchemy import *
import logging
import numpy as np
import csv

def Load_Data(file_name):
    file_name = "D:/Desktop/qcviz_shiny/samplemeta.csv"
    file = open(file_name)
    csv_data = csv.reader(file)
    return csv_data

Base = declarative_base()

class QCDB_table(Base):
    #Tell SQLAlchemy what the table name is and if there's any table-specific arguments it should know about
    __tablename__ = 'QCDB_table'
    #tell SQLAlchemy the name of column and its attributes:
    id = Column(Integer,primary_key = True, nullable = False, autoincrement=True)
    db_id = Column(String(50)) # formerly sample_id for db
    sample_id = Column( String(50), nullable=False) # = sample_id from SRA
    experiment_id = Column( String(50)) # = experiment_id from SRA
    library_name = Column(String(50)) #
    library_strategy = Column( String(50))
    library_source = Column( String(50))
    library_selection = Column( String(50))
    library_layout = Column(String(50)) #
    platform = Column( String(50)) #
    instrument_model = Column(String(50)) #
    sra_ids = Column(String(50)) #
    run_ids = Column(String(50)) # = SRR, ERR, DRR
    run_center = Column(String(100)) #
    project_id = Column(String(50)) # = SRP, ERP, DRP
    taxon_id = Column(String(50)) #
    scientific_name = Column(String(50)) #
    published = Column( String(50)) #
    spots = Column( String(50))#
    bases = Column(BigInteger) #
    experiment_name = Column( String(100)) # maybe TITLE?
    study_type = Column(String(50)) #
    center_project_name = Column( String(50)) #
    submission_center = Column(String(50)) #
    submission_lab = Column(String(50)) #
    json = Column(JSON) 

def db_create(params, db):
    # start connection
    conn = connection(params=params)

    logging.info("Connected to {0}:{1}:{2}".format(params['host'],
                                            params['port'],
                                            db))
#    try:
    conn.execute("create database {};".format(db))
    logging.info("Created database {}".format(db))

if __name__ == "__main__":
    t = time()

    db = 'sampledata'
    params ={'user':'root',
                       'password':'arc_ccv_cbc_2022',
                       'host':'tdatascicit.services.brown.edu',
                       'port': '3306'}

    try:
        # Start connection
        engine= connection(params=params,db=db)
        log.info("Connected to {0}:{1}:{2}".format(params['host'],
                                            params['port'],
                                            db))
    except:
        db_create(params,db)
        engine = connection(params=params,db=db)

    Base.metadata.create_all(engine)

    #Create the session
    session = sessionmaker()
    session.configure(bind=engine)

    s = session()
    file_name = "D:/Desktop/qcviz_shiny/samplemeta.csv"
    temp = 0 
    csv_data = (Load_Data(file_name))
    skipHeader = True
    for row in csv_data:
        if skipHeader:
            skipHeader = False
            continue
        i_record = QCDB_table(db_id = row[0],
                            sample_id = row[1],
                            experiment_id = row[2],
                            library_name = row[3], #
                            library_strategy = row[4],
                            library_source = row[5],
                            library_selection = row[6],
                            library_layout = row[7], #
                            platform = row[8], #
                            instrument_model = row[9], #
                            sra_ids = row[10], #
                            run_ids = row[11], # = SRR, ERR, DRR
                            run_center = row[12], #
                            project_id = row[13], # = SRP, ERP, DRP
                            taxon_id = row[14],#
                            scientific_name = row[15], #
                            published = row[16], #
                            spots = row[17],#
                            bases = row[18],#
                            experiment_name = row[19], # maybe TITLE?
                            study_type = row[20], #
                            center_project_name = row[21], #
                            submission_center = row[22], #
                            submission_lab = row[23], #
                            json = row[24])
        s.add(i_record) #Add all the records

    s.commit() #Attempt to scommit all the records
    tnow = time()
    print('it takes ',tnow-t)




'''
rs = s.query(QCDB_table).all()
for r in rs:
    print(r.id,r.db_id,r.sample_id,r.experiment_id)

print('innitally the sample excel is 57, now the table len is:',len(rs))

# Assert some value
new_point = QCDB_table(**{'db_id':'qcdb_test_point1'})
s.add(new_point)
s.commit()
new_table = s.query(QCDB_table).all()
assert len(rs)+1 == len(new_table),'Index not match'
'''