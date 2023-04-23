from flask import abort, jsonify
from flask_restful import reqparse, abort, Api, Resource

from data import db_session
from data.sports import Sports
from data.reqparse_acc import parser


def abort_if_sport_not_found(sport_id):
    session = db_session.create_session()
    sport = session.query(Sports).get(sport_id)
    if not sport:
        abort(404, message=f"Sports {sport_id} not found")


class SportResource(Resource):
    def get(self, sport_id):
        abort_if_sport_not_found(sport_id)
        session = db_session.create_session()
        sport = session.query(Sports).get(sport_id)
        return jsonify({'sport': sport.to_dict()})

    def delete(self, sport_id):
        abort_if_sport_not_found(sport_id)
        session = db_session.create_session()
        sport = session.query(Sports).get(sport_id)
        session.delete(sport)
        session.commit()
        return jsonify({'success': 'OK'})

class SportListResource(Resource):
    def get(self):
        session = db_session.create_session()
        sport = session.query(Sports).all()
        return jsonify({'sport': [item.to_dict() for item in sport]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        sport = Sports(
            name=args['name'],
            cost=args['cost'],
            picture=args['picture'],
            description=args['description'],
            type=args['type']
        )
        session.add(sport)
        session.commit()
        return jsonify({'success': 'OK'})