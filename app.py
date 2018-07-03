import os
from flask import Flask, Blueprint
from pets_api.endpoints.categories import ns as categories_namespace
from pets_api.endpoints.pets import ns as pets_namespace
from flask_restplus import Api
from pets_api.database import db, ma

app = Flask(__name__)
api = Api(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'pet_store.db')


def initialize_app(flask_app):

    blueprint = Blueprint('api', __name__, url_prefix='/petstore')
    api.init_app(blueprint)
    api.add_namespace(categories_namespace)
    api.add_namespace(pets_namespace)
    flask_app.register_blueprint(blueprint)

    db.init_app(flask_app)
    ma.init_app(flask_app)


def main():
    initialize_app(app)
    app.run(debug=settings.FLASK_DEBUG)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
