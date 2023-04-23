import sqlalchemy
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class Basket(SqlAlchemyBase, UserMixin):
    __tablename__ = 'basket'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    cost = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    picture = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    by_who = sqlalchemy.Column(sqlalchemy.String)
    tovar_id = sqlalchemy.Column(sqlalchemy.String)