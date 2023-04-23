from flask import abort, jsonify
from flask_restful import reqparse, abort, Api, Resource

from data import db_session
from data.clothes import Clothes
from data.reqparse_acc import parser


def abort_if_clothes_not_found(clothes_id):
    session = db_session.create_session()
    clothes = session.query(Clothes).get(clothes_id)
    if not clothes:
        abort(404, message=f"Clothes {clothes_id} not found")


class ClothesResource(Resource):
    def get(self, clothes_id):
        abort_if_clothes_not_found(clothes_id)
        session = db_session.create_session()
        clothes = session.query(Clothes).get(clothes_id)
        return jsonify({'clothes': clothes.to_dict()})

    def delete(self, clothes_id):
        abort_if_clothes_not_found(clothes_id)
        session = db_session.create_session()
        clothes = session.query(Clothes).get(clothes_id)
        session.delete(clothes)
        session.commit()
        return jsonify({'success': 'OK'})

class ClothesListResource(Resource):
    def get(self):
        session = db_session.create_session()
        clothes = session.query(Clothes).all()
        return jsonify({'clothes': [item.to_dict() for item in clothes]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        clothes = Clothes(
            name=args['name'],
            cost=args['cost'],
            picture=args['picture'],
            description=args['description'],
            sex=args['sex']
        )
        session.add(clothes)
        session.commit()
        return jsonify({'success': 'OK'})