from flask import Flask, render_template

from db_interface import DataBase

app = Flask(__name__)


@app.route('/partners')
def partners():
    DataBase.update_session()
    return render_template('partners.html', partners=DataBase.select_partners())


@app.route('/tovar')
def tovar():
    DataBase.update_session()
    return render_template('tovar.html', tovars=DataBase.select_tovar())


@app.route('/unit')
def unit():
    DataBase.update_session()
    return render_template('unit.html', units=DataBase.select_unit())


def start_server(debug=False):
    app.run(debug=debug, host="0.0.0.0")


if __name__ == '__main__':
    start_server()
