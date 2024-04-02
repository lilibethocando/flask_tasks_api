from flask import request, render_template, jsonify, redirect, url_for
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

    

@app.route("/task", methods=['GET', 'POST'])
def get_task():    
    if request.method == 'GET':
        default_task = {'id': 1, 'title': 'Default Task', 'description': 'This is a default task'}
        return render_template('task.html', task=default_task)
    
    if request.method == 'POST':
        id = request.form.get('id')
        task = db.session.query(Task).filter_by(id=id).first()

        if not task:
            return {'error': f"Task with id {id} does not exist"}, 404
        
        accept_header = request.headers.get('Accept', '')
        if request.is_json:
            id = request.args.get('id')
            print(id)
            return jsonify(task.to_dict())
        return render_template('task.html', task=task.to_dict(), task_id=id)



@app.route("/create/tasks", methods=['GET','POST'])
@token_auth.login_required
def create_task():
    current_user = token_auth.current_user()
    if id == current_user.id:

        if request.method == 'GET':
            new_task = None
            return render_template('create_task.html', new_task=new_task)
        if request.method == 'POST':

            required_fields = ['title','description']
            missing_fields = []

            title = request.form.get('title')
            description = request.form.get('description')
            completed = request.form.get('completed', False)

            data = [title, description, completed]

            for field in required_fields:
                if field not in data:
                    missing_fields.append(field)
            if missing_fields:
                return {'error': f"{','.join(missing_fields)} must be in the request body"}, 400
            
            createdAt = datetime.now(timezone.utc)

            current_user_id = token_auth.current_user()
            new_task = Task(title=title, description=description, completed=completed, user_id=current_user_id.id)
            return render_template('create_task.html', new_task=new_task.to_dict())


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

@app.route("/create/users", methods=['GET','POST'])
def create_user():
    if request.method == 'GET':
        new_user = None
        return render_template('create_user.html', new_user=new_user)
    
    if request.method == 'POST':
        # if not request.is_json:
        #     return {'error': 'Your content-type must be application/json'}, 400
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check for missing fields
        required_fields = ['firstName', 'lastName', 'username', 'email', 'password']
        missing_fields = [field for field in required_fields if not request.form.get(field)]
        

        if missing_fields:
            return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400
        
        # Check if the username or email already exists
        check_users = db.session.execute(db.select(User).where((User.username == username) | (User.email == email))).scalars().all()
        if check_users:
            return {'error': "A user with that username and/or email already exists"}, 400
        
        # Create a new user object
        new_user = User(first_name=first_name, last_name=last_name,  username=username, email=email, password=password)

        return render_template('create_user.html', new_user=new_user.to_dict())
    



@app.route('/token')
@basic_auth.login_required()
def get_token():
    user = basic_auth.current_user()
    return render_template('token.html', user=user.get_token())   


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
