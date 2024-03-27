from flask import request, render_template
from . import app
from tasks import tasks_list
from datetime import datetime


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/tasks")
def get_tasks():
    tasks = tasks_list
    return render_template('tasks.html', tasks=tasks)

@app.route("/tasks/<int:id>")
def get_task(id):
    tasks = tasks_list
    for task in tasks:
        if task['id'] == id:
            return render_template('task.html', task=task)
    return {'error': f"Task with id {id} does not exist"}, 400

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
    createdAt = datetime.now()

    new_task = {
        'id': len(tasks_list) + 1,
        'title': title,
        'description': description,
        'completed': completed,
        'createdAt': createdAt
    }

    tasks_list.append(new_task)
    return new_task, 201
