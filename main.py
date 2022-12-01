from hashlib import md5

from web.web_server import start_server

if __name__ == '__main__':
    passwd = input('Пароль базы: ').encode('utf-8')
    print(md5('zagfa123'.encode('utf-8')).hexdigest())
    print(type(md5(passwd).hexdigest()))
    if md5(passwd).hexdigest() != 'b703ad2d5ae6b286fb52bd5cb955d02b':
        print('не верный пароль!')
    else:
        start_server()
