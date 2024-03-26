from flask import request, render_template
from . import app
from tasks import tasks_list


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
