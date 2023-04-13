import sqlalchemy
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class Accessory(SqlAlchemyBase, UserMixin):
    __tablename__ = 'accessory'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    cost = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    picture = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=True)