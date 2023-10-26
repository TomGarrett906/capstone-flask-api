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

    @jwt_required()
    @bp.response(200, GigSchema(many=True))
    def get(self):
         return GigModel.query.all()

# ADD GIG   
  
    @jwt_required()
    @bp.arguments(GigSchema)
    @bp.response(200, GigSchema)
    def post(self, gig_data):
        promoter_id = get_jwt_identity()
        print(promoter_id)
        print(gig_data)
        gig = GigModel(**gig_data)
        try:
            gig.save()
            return gig
        except IntegrityError as e:
            print(e)
            abort(400, message="Invalid Gig Id")

 






            
#-----------------------------------------





@bp.route('/<gig_id>')
class Gig(MethodView):  


# SHOW GIG

    @jwt_required()
    @bp.response(200, GigSchema)
    def get(self, gig_id):
        p = GigModel.query.get(gig_id)
        if p:
            return p
        abort(400, message='Invalid Gig ID')



# UPDATE GIG

    @jwt_required()
    @bp.arguments(GigSchema)
    @bp.response(200, GigSchema)
    def put(self, gig_data, gig_id):
        gig = GigModel.query.get(gig_id)
        current_user_id = get_jwt_identity()

        if gig and "gig_name" in gig_data:
            if gig.promoter_id == current_user_id:
                gig.gig_name = gig_data['gig_name']
                gig.save()
                return gig
            else:
                abort(400, message="Unauthorized ID")
        # if gig and gig_data['gig_name']:
        #     username = get_jwt_identity()
        # if gig.username == username:
        #         gig.body = gig_data['gig_name']
        #         gig.save()
        #         return gig
        else:
            
            abort(400, message='Invalid Gig Data')


# DELETE GIG

    @jwt_required()
    def delete(self, gig_id):
        current_user_id = get_jwt_identity()
        gig = GigModel.query.get(gig_id)
        if gig:
            if gig.promoter_id == current_user_id:
                gig.delete()
                return {'message' : 'Gig Deleted'}, 202
            abort(401, message='User doesn\'t have rights')
        abort(400, message='Invalid Gig ID')