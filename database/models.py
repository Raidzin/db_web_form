import sqlalchemy as db
from sqlalchemy.orm import declarative_base, relationship, declared_attr

TABLE_NAMES = {
    'Partners': 'partners_hktn',
    'Tovar': 'tovar_hktn',
    'Unit': 'unit_hktn',
    'Head': 'head_hktn',
    'Summary': 'summary_hktn',
}


class PreBase:

    @declared_attr
    def __tablename__(cls):
        return TABLE_NAMES[cls.__name__]

    id = db.Column(db.Integer, primary_key=True)


Base = declarative_base(cls=PreBase)


class AuditMixin:
    creation_date = db.Column(db.Date)
    created_by = db.Column(db.String(30))
    last_update_date = db.Column(db.Date)
    last_updated_by = db.Column(db.String(30))


# class Department(Base, AuditMixin):
#     __tablename__ = 'stg_department'
#     name = db.Column(db.String(50))
#     type = db.Column(db.String(50))
#     ref_id = db.Column(db.Integer, db.ForeignKey('stg_department.id'))
#     head_department = relationship(
#         lambda: Department,
#         remote_side=lambda: Department.id,
#         backref='sub_departments')
#
#     def __repr__(self):
#         return f'{self.name}'


class Partners(Base, AuditMixin):
    name = db.Column(db.String(150))
    inn = db.Column(db.String(12))
    kpp = db.Column(db.String(9))
    address = db.Column(db.String(250))


class Tovar(Base, AuditMixin):
    nom_number = db.Column(db.String(20))
    name_tmc = db.Column(db.String(1500))
    name_tmc_kd = db.Column(db.String(37))


class Unit(Base, AuditMixin):
    unit = db.Column(db.String(50))
    name_unit = db.Column(db.String(150))
    okei = db.Column(db.String(4))


class Head(Base, AuditMixin):
    doc_number = db.Column(db.String(50))
    doc_date = db.Column(db.Date)
    polych_id = db.Column(db.Integer, db.ForeignKey(Partners.id))
    postovshik_id = db.Column(db.Integer, db.ForeignKey(Partners.id))


class Summary(Base, AuditMixin):
    quantity = db.Column(db.Float)
    price = db.Column(db.Float)
    head_id = db.Column(db.Integer, db.ForeignKey(Head.id))
    unit_id = db.Column(db.Integer, db.ForeignKey(Unit.id))
    tovar_id = db.Column(db.Integer, db.ForeignKey(Tovar.id))


def create_db(engine):
    Base.metadata.create_all(engine)
