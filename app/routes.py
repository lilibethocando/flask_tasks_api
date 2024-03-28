from flask import request, render_template
from . import app, db
from tasks import tasks_list
from datetime import datetime, timezone
from .models import Task


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/tasks")
def get_tasks():
    select_stmt = db.select(Task)
    search = request.args.get('search')
    print("Search parameter:", search)
    if search:
        select_stmt = select_stmt.where(Task.completed==search)
        print("Generated SQL query:", str(select_stmt))
    tasks = db.session.execute(select_stmt).scalars().all()
    tasks_list = [task.to_dict() for task in tasks]
    return render_template('tasks.html', tasks=tasks_list)

@app.route("/tasks/<int:id>")
def get_task(id):
    tasks = db.session.execute(db.select(Task)).scalars().all()
    for task in tasks:
        if task.id == id:
            return render_template('task.html', task=task)
    return {'error': f"Task with id {id} does not exist"}, 404

@app.route("/tasks", methods=['POST'])
def create_task():
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    required_fields = ['title','description']
    missing_fields = []
    data = request.json
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{','.join(missing_fields)} must be in the request body"}, 400
    
    title = data.get('title')
    description = data.get('description')
    completed = data.get('completed', False)
    createdAt = datetime.now(timezone.utc)

    new_task = Task(title=title, description=description, completed=completed)
    return new_task.to_dict(), 201
