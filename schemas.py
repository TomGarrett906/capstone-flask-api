from marshmallow import Schema, fields

class UserSchema(Schema):
    user_id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    password_hash = fields.Str(required=True, load_only=True)
    first_name = fields.Str()
    last_name = fields.Str()
    role = fields.Str(required=True)

class GigSchema(Schema):
    gig_id = fields.Str(dump_only=True)
    gig_name = fields.Str(required=True)
    description = fields.Str(required=True)
    date = fields.Date(required=True)
    location = fields.Str(required=True)
    promoter_id = fields.Str(required=True)
    dj_id = fields.Str(required=True)
    
class UpdateUserSchema(Schema):
    username = fields.Str()
    email = fields.Str()
    password_hash = fields.Str(required = True, load_only = True)
    new_password = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()

class AuthUserSchema(Schema):
    username = fields.Str()
    email = fields.Str()
    password_hash = fields.Str(required = True, load_only = True)