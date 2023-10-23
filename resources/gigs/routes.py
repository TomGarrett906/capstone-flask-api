from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError
from schemas import AuthUserSchema, GigSchema, UpdateUserSchema
from resources.users.models import GigModel
from . import bp
from db import gigs
#-----------------------------------------



@bp.route('/')
class Gigs(MethodView):

# SHOW ALL GIGS

    # @jwt_required()
    @bp.response(200, GigSchema(many=True))
    def get(self):
         return GigModel.query.all()

# ADD GIG   
  
    # @jwt_required()
    @bp.arguments(GigSchema)
    @bp.response(200, GigSchema)
    def post(self, post_data):
        user_id = get_jwt_identity()
        gig = GigModel(**post_data, user_id = user_id)
        try:
            gig.save()
            return gig
        except IntegrityError:
            abort(400, message="Invalid User Id")
#-----------------------------------------





@bp.route('/<user_id>')
class Gig(MethodView):  


# SHOW GIG

#   @jwt_required()
    @bp.response(200, GigSchema)
    def get(self, gig_id):
        p = GigModel.query.get(gig_id)
        if p:
            return p
        abort(400, message='Invalid Gig ID')



# UPDATE GIG

    # @jwt_required()
    @bp.arguments(GigSchema)
    @bp.response(200, GigSchema)
    def put(self, gig_data, gig_id):
        gig = GigModel.query.get(gig_id)
        if gig and gig_data['body']:
            user_id = get_jwt_identity()
        if gig.user_id == user_id:
            gig.body = gig_data['body']
            gig.save()
            return gig
        else:
            abort(401, message='Unauthorized')
        abort(400, message='Invalid Gig Data')


# DELETE GIG

    #   @jwt_required()
    def delete(self, gig_id):
        user_id = get_jwt_identity()
        gig = GigModel.query.get(gig_id)
        if gig:
            if gig.user_id == user_id:
                gig.delete()
                return {'message' : 'Gig Deleted'}, 202
            abort(401, message='User doesn\'t have rights')
        abort(400, message='Invalid Gig ID')