import sqlite3
from flask_restful import Resource, reqparse
from models.crib import CribModel
from flask_jwt import jwt_required, current_identity

class Cribs(Resource):
    @jwt_required()
    def get(self):
        user_id = current_identity.id
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM cribs WHERE id=?'
        results = cursor.execute(query, (user_id,))
        crib_list = list(results)
        formatted_cribs = []

        for c in crib_list:
            formatted_crib = {
                'id': c[0],
                'url': c[1],
                'name': c[2],
                'price': c[3],
                'pictures': c[4].split('|'),
                'user': c[5]
            }
            formatted_cribs.append(formatted_crib)

        return { 'cribs': formatted_cribs }, 200


class Crib(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('url',
        type=str,
        required=True,
        help='This field cannot be left blank'
    )

    @jwt_required()
    def post(self):
        user_id = current_identity.id
        data = Crib.parser.parse_args()
        try:
            crib = CribModel(data['url'], user_id, None)
            crib.save_to_db()
            return { 'crib': crib.json() }, 201
        except Exception as err:
            print(err)
            return { 'message': 'an error occured' }, 500

    @jwt_required()
    def delete(self, _id):
        try:
            user_id = current_identity.id
            crib = CribModel.get_by_id(_id)
            if crib.user != user_id:
                return { 
                    'message': 'you do not have authorization to delete this crib'
                    }, 401

            crib.delete_from_db()
            return { 'message': 'crib successfully deleted' }, 200
        except Exception as err:
            print(err)
            return { 'message': 'an error occured' }, 500
