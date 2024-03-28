from . import db
from datetime import datetime, timezone

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))



    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.save()

    def __repr__(self) -> str:
        return f"<Task {self.id}|{self.title}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "dateCreated": self.date_created
            
        }

# task = Task(title='First task', description='Finish the Flask Homework', completed=True)
    


