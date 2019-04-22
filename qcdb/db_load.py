from sqlalchemy import *
from sqlalchemy.orm import Session
from connection import connection
import glob2
import oyaml as yaml
import os
import pandas as pd
import argparse
import logging
import sys
from parsers.qckitfastq_parse import qckitfastqParser
from parsers.fastqc_parse import fastqcParser
from parsers.parse import BaseParser

# Initialize the logger
log = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
handler.setLevel(logging.INFO)
log.addHandler(handler)
log.setLevel(logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('--file', '-f', help='Location of params.yaml')

def insert(results, m, session):
    for k,v in results.tables.items():
        log.info("Loading {} ...".format(k))
        t = m.tables[k]
        print(v[1:5])
        session.execute(t.insert(),v[1:5])
        print("executed")
        session.commit()

def main(config):
    # Load load.yaml file
    with open(config, 'r') as io:
        d = yaml.load(io)

    db = d['db']['name']
    params = d['db']['params']
    # start connection
    conn = connection(params=params, db=db)
    log.info("Connected to {0}:{1}:{2}".format(params['host'],
                                            params['port'],
                                            db))
    session = Session(bind=conn)
    m = MetaData()
    m.reflect(bind=conn)

    # parse and load metadata
    for module in d['files']['module']:
        log.info("Loading metadata for {} ...".format(module['name']))
        directory = module['directory']
        #mdata = metadata(directory)
        #mdata.to_sql(con=conn,
        #    name='samplemeta',
        #    index=False,
        #    if_exists='append')

        try:
            if module['name'] == 'fastqc':
                files = glob2.glob(os.path.join(directory, '*_fastqc.zip'))
                if not files:
                    log.error("No fastqc output found in: {}".format(directory))
                for f in files:
                    results = fastqcParser(f)
                    log.info("results were fine")
                    #or k,v in results.tables.items():
                    #    log.info("Loading {} ...".format(k))
                        #t = m.tables[k]
                        #session.execute(t.insert(),v)
                        #session.commit()
                    insert(results, m, session)
                    t = m.tables['fastqc_basequal']
                    test = [{'base': 1.0, 'mean': 32.0919987170987, 'median': 33.0, 'lower_quartile': 31.0, 'upper_quartile': 34.0, '10th_percentile': 30.0, '90th_percentile': 34.0}, {'base': 2.0, 'mean': 32.329207655386554, 'median': 34.0, 'lower_quartile': 31.0, 'upper_quartile': 34.0, '10th_percentile': 30.0, '90th_percentile': 34.0}]
                    session.execute(t.insert(), test)
                    session.commit()
                   #insert(results, m, session)
            elif module['name'] == 'qckitfastq':
                results = qckitfastqParser(directory)
                insert(results, m, session)
        except:
            log.error("Error in parsing...")

    # parse and load content
#    for entry in d['files']['data']:
 #       print("Loading {} ...".format(entry['name']))
#
 #       cols = False
  #      if 'columns' in entry:
   #         col = entry['columns']
    #    data = parse(directory, entry['name'], cols)
     #   data.to_sql(con=conn,
      #          name=entry['table'],
       #         index=False,
        #        if_exists='append')


if __name__ == '__main__':
    args = parser.parse_args()
    config = str(args.file)
    main(config)
