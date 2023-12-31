from app import db
from werkzeug.security import generate_password_hash, check_password_hash




#-----------------------------------------


roles = db.Table('roles',
         db.Column('promoter_id', db.Integer, db.ForeignKey('users.user_id')),        
         db.Column('dj_id', db.Integer, db.ForeignKey('users.user_id'))                     
)

#-----------------------------------------



class UserModel(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)   
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)   
    role = db.Column(db.String, nullable=False)

    # promoter_gigs = db.relationship('GigModel', foreign_keys='GigModel.promoter_id', backref='promoter_user')
    # dj_gigs = db.relationship('GigModel', foreign_keys='GigModel.dj_id', backref='dj_user')
    
#     role_type = db.relationship('UserModel', 
#         secondary=roles, 
#         primaryjoin = roles.c.promoter_id == user_id,
#         secondaryjoin = roles.c.dj_id == user_id,
#         backref = db.backref('roles', lazy='dynamic'),
#         lazy='dynamic' 
#   )




    def __repr__(self):
        return f"<User: {self.username}>"
    
    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def from_dict(self, dict):
        password = dict.pop("password_hash")
        self.hash_password(password)
        for k,v in dict.items():
            setattr(self, k, v)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

#-----------------------------------------





class GigModel(db.Model):
    __tablename__ = "gigs"
    gig_id = db.Column(db.Integer, primary_key=True)   
    gig_name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String, nullable=False)
    pay = db.Column(db.DECIMAL(10, 2), nullable=True)
    promoter_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    dj_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)

    # promoter_id = db.relationship('UserModel', foreign_keys='users.user_id', backref='promoter_id')
    # dj_id = db.relationship('UserModel', foreign_keys='users.user_id', backref='dj_id')

    # user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)

    def __repr__(self):
        return f"<Gig: {self.username}>"
    
    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def from_dict(self, dict):
        password = dict.pop("password")
        self.hash_password(password)
        for k,v in dict.items():
            setattr(self, k, v)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()