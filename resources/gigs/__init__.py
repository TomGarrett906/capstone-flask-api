from flask_smorest import Blueprint

bp = Blueprint("gigs", __name__, url_prefix="/gig", description="Ops On Gigs")

from . import routes 