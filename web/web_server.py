from flask import Flask, render_template

from database.db_interface import hackathon_db

app = Flask(__name__)


@app.route('/partners')
def partners():
    hackathon_db.update_session()
    return render_template('partners.html', partners=hackathon_db.select_partners())


@app.route('/tovar')
def tovar():
    hackathon_db.update_session()
    return render_template('tovar.html', tovars=hackathon_db.select_tovar())


@app.route('/unit')
def unit():
    hackathon_db.update_session()
    return render_template('unit.html', units=hackathon_db.select_unit())


def start_server(debug=False):
    app.run(debug=debug)


if __name__ == '__main__':
    start_server()
