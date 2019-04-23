from qcdb.connection import connection
import argparse
import logging
import oyaml as yaml

# Initialize the logger
log = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
handler.setLevel(logging.INFO)
log.addHandler(handler)
log.setLevel(logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('--file', '-f', help='Location of params.yaml', default='params.yaml')

def main(config):
    # Load load.yaml file
    with open(config, 'r') as io:
        d = yaml.load(io)

    db = d['db']['name']
    params = d['db']['params']
    # start connection
    conn = connection(params=params)
    log.info("Connected to {0}:{1}:{2}".format(params['host'],
                                            params['port'],
                                            db))
    try:
    	conn.execute('create database {};'.format(db))
    	logging.info("Created database {}".format(db))
    except:
    	logging.info("DB {} exists".format(db))

if __name__ == '__main__':
    args = parser.parse_args()
    config = str(args.file)
    main(config)