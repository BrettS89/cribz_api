from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from resources.user import UserRegister
from resources.crib import Crib, Cribs

app = Flask(__name__)
app.secret_key = 'darthvader21'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(UserRegister, '/register')
api.add_resource(Crib, '/crib')
api.add_resource(Cribs, '/cribs')

@app.route('/')
def home():
    return 'Hello world!'

app.run(port = 5000)
