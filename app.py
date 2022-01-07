from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




class Leave(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    detail = db.Column(db.String(500), nullable=True)
    date_request = db.Column(db.String(100), nullable=True)
    date_create = db.Column(db.DateTime, default=datetime.utcnow)
    remark = db.Column(db.String(500), nullable=True)

    def __repr__ (self):
        return '<Leave %r>' % self.id

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
    def __repr__(self):
        return '<User %r>' % self.username
    def verify_password(self, pwd):
        return (self.password, pwd)




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
             return redirect('/login')
    else:
        pass
    return render_template('Leave/login_page.html' )

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)