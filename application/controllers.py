# from flask import current_app as app
# from flask import redirect, render_template, session
# from application.models import db, users, notes
from datetime import datetime
from email import message
from flask import current_app as app, redirect
from flask import request, session, render_template, flash
from application.models import db, users, notes
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt(app)

# @app.route('/')
# def homepage():
#     if "username" not in session:
#         return redirect('/login')
#     elif "username" in session:
#         current_user = users.query.filter_by(username = session["username"]).first()
#         #if the user exists
#         if current_user:
#             user_todo = notes.query.filter_by(user_id = current_user.user_id)
#             #if to-do exists for that user
#             return render_template('home.html', user_todo = user_todo)

@app.route('/', methods = ['GET'])
def home():
    if "username" not in session:
        message = "You are not Logged in, Log In to access awesome features"
        return render_template('home.html', message = message)
    elif "username" in session:
        current_user = users.query.filter_by(username = session["username"]).first()
        #if the user exists
        if current_user:
            user_todo = notes.query.filter_by(user_id = current_user.user_id)
            #if to-do exists for that user
            return render_template('home.html', user_todo = user_todo, logged_in = True)
    # return render_template('home.html', message = message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ""
    if request.method == 'POST':
        username = request.form['username']
        user = users.query.filter_by(username = username).first()
        if user:
            pw_hash = user.password
            if bcrypt.check_password_hash(pw_hash, request.form['password']):
                session['username'] = username
                return redirect('/')
        else:
            message = "Incorrect credentials"
    elif "username" in session:
        return redirect('/')
    
    return render_template('login.html', message = message)

@app.route('/logout')
def logout():
    if "username" in session:
        session.pop("username")
        return redirect('/')

@app.route('/signup', methods = ['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        username = request.form['username']
        userhai = users.query.filter_by(username = username).first()
        if not userhai:
            pw_hash = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
            user = users(username = username, password = pw_hash)
            db.session.add(user)
            db.session.commit()
            return redirect('/login')
        else:
            message = "Create a unique username, this username already exists"
            return render_template('register.html', message = message) 
    elif "username" in session:
        return redirect('/')
    return render_template('register.html')

@app.route('/create', methods = ['POST', 'GET'])
def create_todo():
    if request.method == 'POST':
        user_id =  users.query.filter_by(username = session["username"]).first().user_id
        heading = request.form["heading"]
        description = request.form["description"]
        created_date = datetime.utcnow()
        completed = False
        todo = notes(user_id = user_id, heading = heading, description = description, created_on = created_date, last_updated = created_date, completed = completed)
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    elif "username" in session:
        return render_template('/create_todo.html', username = session['username'], logged_in = True)
    else:
        return redirect('/')
    
@app.route('/todo/<int:todo_id>/edit')
def edit_todo(todo_id):
    if "username" in session:
        user = users.query.filter_by(username = session["username"]).first()
        if user:
            todos = notes.query.filter_by(notes_id = todo_id, user_id = user.user_id).first()
            if todos:
                #Just give a nice alert for deletion and then redirect
                return render_template('edit_todo.html', todo = todos)
                
            else:
                return redirect('/')

        else:
            return redirect('/logout')
    else:
        return redirect('/')
    


@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    if "username" in session:
        user = users.query.filter_by(username = session["username"]).first()
        if user:
            todos = notes.query.filter_by(notes_id = todo_id, user_id = user.user_id).first()
            if todos:
                notes.query.filter_by(notes_id = todo_id, user_id = user.user_id).delete()
                db.session.commit()
                #Just give a nice alert for deletion and then redirect
                return redirect('/')
                
            else:
                return redirect('/')

        else:
            return redirect('/logout')
    else:
        return redirect('/')