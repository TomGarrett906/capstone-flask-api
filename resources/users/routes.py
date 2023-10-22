from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError


from schemas import UserSchema, UpdateUserSchema, AuthUserSchema
from . import bp
from resources.users.models import UserModel
from db import users


@bp.route('/')
class Users(MethodView):

#SHOW USERS
    @bp.response(200, UserSchema(many=True))
    def get(self):
         return UserModel.query.all()
    
#POST USER    
    @bp.arguments(UserSchema)
    @bp.response(201, UserSchema)
    def post(self, user_data):
        user = UserModel()
        user.from_dict(user_data)
        try:
            user.save()
            return user_data
        except IntegrityError:
            abort(400, message="Username or Email already taken")


#Delete User
    @jwt_required()
    @bp.arguments(AuthUserSchema)
    def delete(self, user_data):    
        user_id = get_jwt_identity()
        user = UserModel.query.get(user_id)
 
        if user and user.username == user_data['user_name'] and user.check_password(user_data['password_hash']):
            user.delete()
            return {"message": f"{user_data['username']} deleted"}, 202
        abort(400, message="Username or Password Invalid")
 











#Show User
@bp.route('/<user_id>')
class User(MethodView):
    @bp.response(200, UserSchema)
    def get(self, user_id):
        user = None
        if user_id.isdigit():
            user = UserModel.query.get(user_id)
        else:
            user = UserModel.query.filter_by(username=user_id).first()
        if user:
            return user
        abort(400, message='Please enter valid username or id')

#Update User
    # @bp.jwt_required()
    @bp.arguments(UpdateUserSchema)
    @bp.response(202, UpdateUserSchema)          
    def put(self,user_data, user_id):
        user = UserModel.query.get_or_404(user_id, description="user not found")
        if user and user.check_password(user_data["password_hash"]):
            try:
                user.from_dict(user_data)
                user.save()
                return user
            except KeyError:
                abort(400, message="Username or Email already taken")






#SHOW user's gig  
# @bp.get('/<user_id>/gig')
# @bp.response(200, UserSchema(many=True)) 
# def get_users_gig(user_id):
#     if user_id not in users:
#         abort(404, message="user not found")
#     users_gig = [gig for gig in gigs.values() if gig['user_id'] == user_id]
#     return users_gig