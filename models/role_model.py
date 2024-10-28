import datetime
from __init__ import db

class Role(db.Model):
    __tablename__ = 'tbl_role'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    role_id = db.Column(db.Integer, nullable=True)
    rule = db.Column(db.Integer, nullable=True,  default=0)

    def __repr__(self):
        return '<Role %r>' % self.title

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.strftime('%Y-%m-%dT%H:%M:%S') if self.created_at else None,
            'role_id': self.role_id,
            'rule': self.rule 
        }
