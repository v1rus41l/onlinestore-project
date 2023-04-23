from flask import abort, jsonify
from flask_restful import reqparse, abort, Api, Resource

from data import db_session
from data.accessory import Accessory
from data.reqparse_acc import parser


def abort_if_accessory_not_found(accessory_id):
    session = db_session.create_session()
    accessory = session.query(Accessory).get(accessory_id)
    if not accessory:
        abort(404, message=f"Accessory {accessory_id} not found")


class AccessoryResource(Resource):
    def get(self, accessory_id):
        abort_if_accessory_not_found(accessory_id)
        session = db_session.create_session()
        accessory = session.query(Accessory).get(accessory_id)
        return jsonify({'accessory': accessory.to_dict()})

    def delete(self, accessory_id):
        abort_if_accessory_not_found(accessory_id)
        session = db_session.create_session()
        accessory = session.query(Accessory).get(accessory_id)
        session.delete(accessory)
        session.commit()
        return jsonify({'success': 'OK'})

class AccessoryListResource(Resource):
    def get(self):
        session = db_session.create_session()
        accessory = session.query(Accessory).all()
        return jsonify({'accessory': [item.to_dict() for item in accessory]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        accessory = Accessory(
            name=args['name'],
            cost=args['cost'],
            picture=args['picture'],
            description=args['description'],
            type=args['type']
        )
        session.add(accessory)
        session.commit()
        return jsonify({'success': 'OK'})