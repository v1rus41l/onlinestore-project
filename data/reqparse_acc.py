from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('name', required=True, nullable=True)
parser.add_argument('cost', required=True, nullable=True)
parser.add_argument('description', required=True, nullable=True)
parser.add_argument('picture', required=True, nullable=True)
parser.add_argument('type', required=True, nullable=True)