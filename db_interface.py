from collections.abc import Iterable

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from constants import CONNECT_STRING, DIALECT, CLIENT_DIR
import models

if DIALECT == 'oracle':
    import cx_Oracle

    cx_Oracle.init_oracle_client(CLIENT_DIR)


class DataBase:
    engine = create_engine(CONNECT_STRING)
    session = Session(engine)
    tables = [
        models.Partners,
        models.Tovar,
        models.Unit,
        models.Head,
        models.Summary
    ]

    @classmethod
    def create_tables(cls):
        models.create_db(cls.engine)

    @staticmethod
    def get_data(row):
        columns = {}
        for column in row.__table__.columns:
            columns[column.name] = getattr(row, column.name)
        return columns

    @classmethod
    def get_table(cls, model, model_id=None):
        if model_id is None:
            return [
                cls.get_data(row)
                for row
                in cls.session.query(model).all()
            ]
        return cls.get_data(
            cls.session.query(model).filter(model.id == model_id).first()
        )

    @classmethod
    def get_raw_table(cls, model, model_id=None):
        if model_id is None:
            return cls.session.query(model).all()
        return cls.session.query(model).filter(model.id == model_id).first()

    @classmethod
    def update_table(cls, model, model_id, **kwargs):
        if model_id is None:
            raise ValueError
        row = cls.get_raw_table(model, model_id)
        for attr_name in kwargs.keys():
            setattr(row, attr_name, kwargs[attr_name])
        cls.session.commit()

    @classmethod
    def del_table(cls, model, model_id):
        if model_id is not Iterable:
            cls.session.delete(cls.get_raw_table(model, model_id))
            cls.session.commit()
            return
        cls.session.delete(
            cls.session.query(model).filter(model.id in model_id).all())
        cls.session.commit()

    @classmethod
    def get_getter(cls, model):
        def getter(model_id=None):
            return cls.get_table(model, model_id=model_id)

        return getter

    @classmethod
    def get_updater(cls, model):
        def updater(model_id, **kwargs):
            return cls.update_table(model, model_id, **kwargs)

        return updater

    @classmethod
    def get_deleter(cls, model):
        def deleter(model_id):
            return cls.del_table(model, model_id=model_id)

        return deleter

    @classmethod
    def init_default_api(cls):
        default_functions = (
            ('select_', cls.get_getter),
            ('update_', cls.get_updater),
            ('delete_', cls.get_deleter),
        )
        for table_name in cls.tables:
            func_name = table_name.__name__.lower()
            for prefix, func in default_functions:
                setattr(
                    cls,
                    f'{prefix}{func_name}',
                    func(table_name)
                )


DataBase.init_default_api()

if __name__ == '__main__':
    DataBase.create_tables()
    print(DataBase.select_unit(2))
