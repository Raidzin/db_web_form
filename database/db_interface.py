from collections.abc import Iterable

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from constants import CONNECT_STRING, DIALECT, CLIENT_DIR
from database.models import Partners, Tovar, Unit, Head, Summary, create_db

if DIALECT == 'oracle':
    import cx_Oracle
    cx_Oracle.init_oracle_client(CLIENT_DIR)


class DataBase:
    def __init__(self, tables):
        self.tables = tables
        self.engine = create_engine(CONNECT_STRING)
        self.session = Session(self.engine)

    def update_session(self):
        self.session = Session(self.engine)

    def create_tables(self):
        create_db(self.engine)

    @staticmethod
    def get_data(row):
        columns = {}
        for column in row.__table__.columns:
            columns[column.name] = getattr(row, column.name)
        return columns

    def get_table(self, model, model_id=None):
        if model_id is None:
            return [
                self.get_data(row)
                for row
                in self.session.query(model).all()
            ]
        return self.get_data(
            self.session.query(model).filter(model.id == model_id).first()
        )

    def get_raw_table(self, model, model_id=None):
        if model_id is None:
            return self.session.query(model).all()
        return self.session.query(model).filter(model.id == model_id).first()

    def update_table(self, model, model_id, **kwargs):
        if model_id is None:
            raise ValueError
        row = self.get_raw_table(model, model_id)
        for attr_name in kwargs.keys():
            setattr(row, attr_name, kwargs[attr_name])
        self.session.commit()

    def del_table(self, model, model_id):
        if model_id is not Iterable:
            self.session.delete(self.get_raw_table(model, model_id))
            self.session.commit()
            return
        self.session.delete(
            self.session.query(model).filter(model.id in model_id).all())
        self.session.commit()

    def get_selecter(self, model):
        def selecter(model_id=None):
            return self.get_table(model, model_id=model_id)

        return selecter

    def get_updater(self, model):
        def updater(model_id, **kwargs):
            return self.update_table(model, model_id, **kwargs)

        return updater

    def get_deleter(self, model):
        def deleter(model_id):
            return self.del_table(model, model_id=model_id)

        return deleter

    def init_default_api(self):
        crud_operations = (
            ('select_', self.get_selecter),
            ('update_', self.get_updater),
            ('delete_', self.get_deleter),
        )
        for table_name in self.tables:
            func_name = table_name.__name__.lower()
            for prefix, operation in crud_operations:
                setattr(
                    self,
                    f'{prefix}{func_name}',
                    operation(table_name)
                )


hackathon_db = DataBase((Partners, Tovar, Unit, Head, Summary))
hackathon_db.init_default_api()

if __name__ == '__main__':
    hackathon_db.create_tables()
    print(hackathon_db.select_unit(365648))
