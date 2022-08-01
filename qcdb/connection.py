import sqlalchemy

def connection(params={'user':'root',
                       'password':'password',
                       'host':'0.0.0.0',
                       'port': '3306',
                      },
               db=False):

    if db:
        params['db'] = db
    else:
        params['db'] = None

    try:
        url = sqlalchemy.engine.url.URL('mysql+mysqlconnector', username=params['user'], password=params['password'], host=params['host'], port=params['port'], database=params['db'])
        engine = sqlalchemy.create_engine(url)
        con = engine.connect()
    except:
        try:
            url = sqlalchemy.engine.url.URL('mysql+mysqlconnector', username=params['user'], password=params['password'], host=params['host'], port=params['port'], database=params['db'], query={'auth_plugin': 'mysql_clear_password'})
            engine = sqlalchemy.create_engine(url)
            con = engine.connect()
        except: # for mariadb connection due to mysql docker image not working for M1
            url = sqlalchemy.engine.url.URL('mariadb+mariadbconnector', username=params['user'], password=params['password'], host = params['host'], port=params['port'], database=params['db'])
            engine = sqlalchemy.create_engine(url)
            con = engine.connect()

    return con
