import base64
import datetime
from __init__ import db

class Group(db.Model):
    __tablename__ = 'user_tbl'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.Enum('Owner', 'Member'), nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    image = db.Column(db.Text, nullable=True)
    group_id = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.datetime.utcnow)

    
    
    def __repr__(self):
        return f'<tbl_group {self.title}>'
    
    
    def set_file(self, image_data):
        """Set file data after encoding it to base64."""
        self.image = base64.b64encode(image_data).decode('utf-8')

    def get_file(self):
        """Get file data after decoding it from base64."""
        return base64.b64decode(self.image.encode('utf-8'))
    
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'due_date': self.due_date.strftime('%Y-%m-%d') if self.due_date else None,
            'user_id': self.user_id,
            'image' : self.image,
            'created_at': self.created_at.strftime('%Y-%m-%dT%H:%M:%S') if self.created_at else None
        }
