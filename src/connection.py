from sqlalchemy import create_engine
import pymysql

def connection(params={'user':'root',
                       'password':'password',
                       'host':'0.0.0.0',
                       'port': '3306'
                      },
               db=False):

    str = 'mysql+pymysql://{0}:{1}@{2}:{3}'.format(params['user'],
                                           params['password'],
                                           params['host'],
                                           params['port'])
    if db:
        str = '{0}/{1}'.format(str, db)

    engine = create_engine(str)
    return engine.connect()
