from __init__ import db

class RevokedToken(db.Model):
    __tablename__ = 'revoked_token'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return '<RevokedToken %r>' % self.jti
