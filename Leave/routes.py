from Leave import app
from datetime import datetime, date
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from Leave.models import*
from Leave.forms import*



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/add', methods=['POST', 'GET'])
@login_required
def leave_request():
    if request.method == 'POST':
        name = request.form['name']
        detail = request.form['detail']
        requestdate = request.form['date']
        add_leave = Leave(name=name, detail=detail, date_request=requestdate)


        try:
            db.session.add(add_leave)
            db.session.commit()
            return redirect('/add')
        except:
            return  'There was an issue adding your task'

    else:
        leaves = Leave.query.order_by(Leave.id).all()
        return render_template('Leave/add_update.html', leaves=leaves  )


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Leave.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/add')
    except:
        return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Leave.query.get_or_404(id)

    if request.method == 'POST':
        task.detail = request.form['detail']
        task.date_request = request.form['date']

        try:
            db.session.commit()
            return redirect('/add')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('Leave/update_page.html', task=task)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['user_name']
        password = request.form['pass_word']
        mail = request.form['mail']
        newuser = User(username=username, password=password, email=mail)
        try:
            db.session.add(newuser)
            db.session.commit()
            return redirect('/register')
        except:
            return  'Username is already use'

    return render_template('Leave/add_user.html')


@app.route('/login',methods=['POST', 'GET'])
def login():
     # Create an object called "form" to use LoginForm class
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user and user.verify_password(password):
            login_user(user)
            return redirect('/add')
        else:
             flash("Invalid Login please try again")
    else:
        pass
    return render_template('Leave/login_page.html' )

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/addwork', methods=['GET', 'POST'])
@login_required
def register_page():
    form = Addworkform()
    work = Woringlist.query.order_by(Woringlist.id).all()
    if form.validate_on_submit():
        work_to_create = Woringlist(workname=form.workname.data,
                              workdetail=form.workdetail.data,
                              workplace=form.workplace.data,
                              workdate=form.workdate.data,)
        db.session.add(work_to_create)
        db.session.commit()
        return redirect('/addwork')
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            print(f'There was an error with creating a user: {err_msg}')
    return render_template('Leave/workadd.html', form=form, work=work)

