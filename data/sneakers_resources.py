from flask import abort, jsonify
from flask_restful import reqparse, abort, Api, Resource

from data import db_session
from data.sneakers import Sneakers
from data.reqparse_acc import parser


def abort_if_sneakers_not_found(sneakers_id):
    session = db_session.create_session()
    sneakers = session.query(Sneakers).get(sneakers_id)
    if not sneakers:
        abort(404, message=f"Sneakers {sneakers_id} not found")


class SneakersResource(Resource):
    def get(self, sneakers_id):
        abort_if_sneakers_not_found(sneakers_id)
        session = db_session.create_session()
        sneakers = session.query(Sneakers).get(sneakers_id)
        return jsonify({'sneakers': sneakers.to_dict()})

    def delete(self, sneakers_id):
        abort_if_sneakers_not_found(sneakers_id)
        session = db_session.create_session()
        sneakers = session.query(Sneakers).get(sneakers_id)
        session.delete(sneakers)
        session.commit()
        return jsonify({'success': 'OK'})

class SneakersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        sneakers = session.query(Sneakers).all()
        return jsonify({'sneakers': [item.to_dict() for item in sneakers]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        sneakers = Sneakers(
            name=args['name'],
            cost=args['cost'],
            picture=args['picture'],
            description=args['description'],
            sex=args['sex']
        )
        session.add(sneakers)
        session.commit()
        return jsonify({'success': 'OK'})