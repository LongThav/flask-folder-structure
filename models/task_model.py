# models/task_model.py
import base64
import datetime
from __init__ import db

class Task(db.Model):
    __tablename__ = 'tasks'
     
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    priority = db.Column(db.Enum('High', 'Medium', 'Low'), nullable=True)
    status = db.Column(db.Enum('Open', 'In Progress', 'Completed'), nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    file = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    group_id = db.Column(db.Integer, db.ForeignKey('tbl_group.id'), nullable=True)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.datetime.utcnow)
    
    # Remove redundant tasks relationship
    # tasks = db.relationship('Task', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<Task {self.title}>'

    def set_file(self, file_data):
        """Set file data after encoding it to base64."""
        self.file = base64.b64encode(file_data).decode('utf-8')

    def get_file(self):
        """Get file data after decoding it from base64."""
        return base64.b64decode(self.file.encode('utf-8'))
    
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'due_date': self.due_date.strftime('%Y-%m-%d') if self.due_date else None,
            'user_id': self.user_id,
            'created_at': self.created_at.strftime('%Y-%m-%dT%H:%M:%S') if self.created_at else None
        }