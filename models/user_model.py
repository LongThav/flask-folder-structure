# models/user_model.py
from __init__ import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)
    dectivate = db.Column(db.Integer, nullable=True)
    fname = db.Column(db.String(50), nullable=True)
    lname = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), unique=True, nullable=True)
    phone = db.Column(db.String(50), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(50), nullable=True)
    image = db.Column(db.Text, nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('tbl_role.id'), nullable=True)
    dob = db.Column(db.Date)
    
    # Define the relationship with Task model
    tasks = db.relationship('Task', backref='user', lazy=True)
    groups = db.relationship('Group', backref='creator', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            'id': self.id,
            'fname': self.fname,
            'lname': self.lname,
            'user_id': self.user_id,
            'email': self.email,
            'role': self.role,
            'image': self.image,
            'role_id': self.role_id,
            'phone': self.phone,
            'dob': self.dob.strftime('%d-%m-%Y') if self.dob else None
        }

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
