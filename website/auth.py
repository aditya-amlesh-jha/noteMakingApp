from flask import Blueprint, render_template, redirect, url_for, request, Response
from .models import User, Note
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

# Blueprint is a way to organize a group of related auth and other code.

auth = Blueprint('auth', __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html", title="Login", user=current_user)

    data = request.json
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        login_user(user, remember=True)
        return Response(status=200)
    else:
        return Response("Invalid Credentials", status=400)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html", title="Register", user=current_user)

    # this function will receive the data from the form which is validated by the js file
    # in the form of json object

    try:

        # checking if the user already exists
        data = request.json
        user = User.query.filter_by(email=data['email']).first()
        phone = User.query.filter_by(phone=data['phone']).first()
        aadhar = User.query.filter_by(aadhar=data['aadhar']).first()


        if aadhar:
            raise Exception("User already exists with this aadhar number")
        if phone:
            raise Exception("User already exists with this phone number")
        if user:
            raise Exception("User already exists with this email")
        
        
        new_user = User(
            name=data['name'],
            phone=data['phone'],
            email=data['email'],
            aadhar=data['aadhar'],
            password=generate_password_hash(data['password'], method='sha256')
        )

        db.session.add(new_user)
        db.session.commit()

    except Exception as e:
        return Response(str(e),status=400)
    
    # return status code 200 if the data is saved successfully
    return Response(status=200)

    # saving the data in database
    # if the data is saved successfully then send a 200 status code else send a 400 status code
