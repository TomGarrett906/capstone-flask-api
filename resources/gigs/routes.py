from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError
from schemas import GigSchema
from resources.users.models import GigModel
from . import bp
from db import gigs
#-----------------------------------------



@bp.route('/')
class Gigs(MethodView):

# SHOW GIGS

    # @jwt_required()
    @bp.response(200, GigSchema(many=True))
    def get(self):
         return GigModel.query.all()

# ADD GIG   
  
    @bp.arguments(GigSchema)
    @bp.response(201, GigSchema)
    def post(self, gig_data):
        gig = GigModel()
        gig.from_dict(gig_data)
        try:
            gig.save()
            return gig_data
        except IntegrityError:
            abort(400, message="Gig already exists")    



# DELETE GIG

    # @jwt_required()
    # @bp.arguments(AuthUserSchema)
    def delete(self, gig_data, gig_id):    
        gig_id = get_jwt_identity()
        gig = GigModel.query.get(gig_id)
 
        if gig and gig.gig_name == gig_data['gig_name'] and gig.check_password(gig_data['password']):
            gig.delete()
            return {"message": f"{gig_data['gigname']} deleted"}, 202
        abort(400, message="gigname or Password Invalid")
 
#-----------------------------------------




#SHOW GIG

@bp.route('/<user_id>')
class User(MethodView):
    @bp.response(200, GigSchema)
    def get(self, gig_id):
        gig = None
        if gig_id.isdigit():
            gig = GigModel.query.get(gig_id)
        else:
            gig = GigModel.query.filter_by(gig_name=gig_id).first()
        if gig:
            return gig
        abort(400, message='Please enter a valid Gig or ID')



#UPDATE GIG

    # @bp.jwt_required()
    # @bp.arguments(UpdateUserSchema)
    # @bp.response(202, UpdateUserSchema)          
    def put(self,gig_data, gig_id):
        gig = GigModel.query.get_or_404(gig_id, description="gig not found")
        if gig and gig.check_password(gig_data["password"]):
            try:
                gig.from_dict(gig_data)
                gig.save()
                return gig
            except KeyError:
                abort(400, message="Gig already exists")