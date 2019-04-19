from sqlalchemy import *
from sqlalchemy.orm import Session
from connection import connection
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

def main(config):
    print(sys.path)
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

    # parse and load metadata
    for module in d['files']['module']:
        log.info("Loading metadata for {} ...".format(module['name']))
        directory = module['directory']
        #mdata = metadata(directory)
        #mdata.to_sql(con=conn,
        #    name='samplemeta',
        #    index=False,
        #    if_exists='append')

        results = ''
        try:
            if module['name'] == 'fastqc':
                results = fastqcParser(directory)
            elif module['name'] == 'qckitfastq':
                results = qckitfastqParser(directory)
        except:
            log.error("Error in parsing...")

        for k, v in results.tables.items():
            log.info("Loading {} ...".format(k))
            session.bulk_insert_mappings(k, v)

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
