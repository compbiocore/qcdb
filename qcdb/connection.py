from sqlalchemy import create_engine
import pymysql

def connection(params={'user':'root',
                       'password':'password',
                       'host':'0.0.0.0',
                       'port': '3306'
                      },
               db=False):

    str_ = 'mysql+pymysql://{0}:{1}@{2}:{3}'.format(params['user'],
                                           params['password'],
                                           params['host'],
                                           params['port'])
    if db:
        str_ = '{0}/{1}'.format(str_, db)

    engine = create_engine(str_)
    return engine.connect()
