import sqlite3
from flask_restful import Resource, reqparse
from models.user import User

class UserRegister(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('email',
        type=str,
        required=True,
        help='This field cannot be left blank'
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help='This field cannot be left blank'
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'INSERT INTO users VALUES (NULL, ?, ?)'
        cursor.execute(query, (data['email'], data['password']))

        connection.commit()
        connection.close()

        return { 'message': 'user created successfully' }, 201