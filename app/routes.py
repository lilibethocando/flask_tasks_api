from flask import request, render_template, jsonify
from . import app, db
from tasks import tasks_list
from datetime import datetime, timezone
from .models import Task, User
from .auth import basic_auth, token_auth



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
    accept_header = request.headers.get('Accept', '')
    if 'application/json' in accept_header:
        return jsonify(tasks_list)
    return render_template('tasks.html', tasks=tasks_list)

@app.route("/tasks/<int:id>")
def get_task(id):
    task = db.session.query(Task).filter_by(id=id).first()
    if not task:
        return {'error': f"Task with id {id} does not exist"}, 404
    accept_header = request.headers.get('Accept', '')
    if 'application/json' in accept_header:
        return jsonify(task.to_dict())
    else:
        return render_template('task.html', task=task.to_dict())
    

@app.route("/tasks", methods=['POST'])
@token_auth.login_required
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

    current_user_id = token_auth.current_user()
    new_task = Task(title=title, description=description, completed=completed, user_id=current_user_id.id)
    return new_task.to_dict(), 201


@app.route("/tasks/<int:id>", methods=['PUT'])
@token_auth.login_required
def edit_task(id):
    if not request.is_json:
        return {'error': 'You content-type must be application/json'}, 400
    
    task = db.session.get(Task, id)
    if task is None:
        return {'error': f"Task with ID #{id} does not exist"}, 404
    
    current_user = token_auth.current_user()
    if current_user is not task.user:
        return {'error': "This is not your task. You do not have permission to edit it"}, 403

    data = request.json
    task.update(**data)
    return task.to_dict()


@app.route("/tasks/<int:id>", methods=['DELETE'])
@token_auth.login_required
def delete_task(id):
    if not request.is_json:
        return {'error': 'You content-type must be application/json'}, 400
    
    task = db.session.get(Task, id)
    if task is None:
        return {'error': f"Task with ID #{id} does not exist"}, 404
    
    current_user = token_auth.current_user()
    if current_user is not task.user:
        return {'error': "This is not your task. You do not have permission to edit it"}, 403

    task.delete()
    return {'success': f"{task.title} was successfully deleted"}, 200



    # return render_template('create_task.html', new_task=new_task.to_dict()) 

#User 

@app.route("/users/", methods=['POST'])
def create_user():
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    data = request.json
    required_fields = ['firstName', 'lastName', 'username', 'email', 'password']
    missing_fields = []

    for field in required_fields:
        if field not in data:
            missing_fields.append(field)

    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400
    
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    check_users = db.session.execute(db.select(User).where( (User.username == username) | (User.email == email) )).scalars().all()
    if check_users:
        return {'error': "A user with that username and/or email already exists"}, 400
    
    new_user = User(first_name=first_name, last_name=last_name,  username=username, email=email, password=password)

    return new_user.to_dict(), 201


@app.route('/token')
@basic_auth.login_required()
def get_token():
    user = basic_auth.current_user()
    return user.get_token()


@app.route('/users/<int:user_id>')
def get_user(user_id):
    user = db.session.get(User, user_id)
    if user:
        return user.to_dict()
    else:
        return {'error': f'User with {user_id} does not exist'}, 404
    
@app.route("/users/<int:user_id>", methods=['PUT'])
@token_auth.login_required
def edit_user(user_id):
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    user = User.query.get(user_id)
    print(user)

    if user is None:
        return {'error': f'User with {user_id} does not exist'}, 404
    
    current_user = token_auth.current_user()
    print(current_user)
    
    if user_id != current_user.id:
        return {'error': 'You do not have permission to edit this user'}, 403
    
    data = request.json
    user.update(**data)
    return user.to_dict()

@app.route('/users/<int:user_id>', methods=['DELETE'])
@token_auth.login_required
def delete_user(user_id):
    # Get the user based on the user id
    user = db.session.get(User, user_id)
    # Check if the user exists
    if user is None:
        return {'error': f'User with {user_id} does not exist'}, 404
    # Get the logged in user based on the token
    current_user = token_auth.current_user()
    # Check if the user to edit is the logged in user
    if user_id != current_user.id:
        return {'error': 'You do not have permission to delete this user'}, 403
    # Delete the user
    user.delete()
    return {'success': f"{user.username} has been deleted"}
