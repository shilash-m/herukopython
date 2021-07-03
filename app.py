from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resource.user import UserRegister
from resource.item import Item, ItemList
from resource.store import Store, StoreList

application = Flask(__name__)

application.config['DEBUG'] = True

application.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///data.db"
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.secret_key = 'jose'
api = Api(application)

jwt = JWT(application, authenticate, identity)  # /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(application)


    @application.before_first_request
    def create_tables():
        db.create_all()

    application.run(port=5000)
