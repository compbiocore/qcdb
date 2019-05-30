import mysql.connector

def connection(params = {
              'user': '',
              'password': '',
              'host': '',
              'raise_on_warnings': True,
            },
            db = False):
    if db:
        params['db'] = db

    params_cleartext = params.copy()
    params_cleartext['auth_plugin'] = 'mysql_clear_password'

    try:
        con = mysql.connector.connect(**params)
    except:
        con = mysql.connector.connect(**params_cleartext)

    return con
