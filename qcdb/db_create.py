from connection import connection

conn = connection()

try:
    conn.execute('create database qcdb;')
except:
    print('db exists')
