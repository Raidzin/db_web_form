from os import getenv

from dotenv import load_dotenv

load_dotenv()

DIALECT = getenv('DIALECT')

if DIALECT == 'oracle':
    SQL_DRIVER = getenv('SQL_DRIVER')
    USERNAME = getenv('USER')
    PASSWORD = getenv('PASSWORD')
    HOST = getenv('HOST')
    PORT = getenv('PORT')
    SERVICE = getenv('HOST')
    CLIENT_DIR = getenv('CLIENT_DIR')
    CONNECT_STRING = f'{DIALECT}+{SQL_DRIVER}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/?service_name={SERVICE}'
else:
    DB_FILE = getenv('DB_FILE')
    CLIENT_DIR = None
    CONNECT_STRING = f"sqlite:///{DB_FILE}"

"""
CLIENT_DIR должен указывать на папки с клиентом для oracle
Скачать можно тут https://www.oracle.com/database/technologies/instant-client.html

ХЗ кто такой этот ваш SERVICE_NAME, будет равен хосту. Способ работает 
"""
