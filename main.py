from hashlib import md5

import webbrowser
from web.web_server import start_server

if __name__ == '__main__':
    passwd = input('Пароль базы: ').encode('utf-8')
    if md5(passwd).hexdigest() != 'b703ad2d5ae6b286fb52bd5cb955d02b':
        print('не верный пароль!')
    else:
        webbrowser.open_new_tab('http://127.0.0.1:5000/tovar')
        start_server()
