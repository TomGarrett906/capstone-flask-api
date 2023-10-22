from flask import Flask
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from Config import Config
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
jwt = JWTManager(app)

from resources.users.routes import bp
api.register_blueprint(bp)

from resources.gigs.routes import bp
api.register_blueprint(bp)

from resources.users import routes
from resources.gigs import routes

from resources.users.models import UserModel, GigModel 