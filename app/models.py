from . import db
from datetime import datetime, timezone

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean)
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))


# task = Task(title='First task', description='Finish the Flask Homework', completed=True)