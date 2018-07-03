from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def reset_database():
    from pets_api.database.models import Pet, Category
    db.drop_all()
    db.create_all()
