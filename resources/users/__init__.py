from flask_smorest import Blueprint

bp = Blueprint("users", __name__, url_prefix="/user", description="Ops On Users")

from . import routes 


