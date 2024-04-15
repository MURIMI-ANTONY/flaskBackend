from flask import Blueprint,make_response, render_template , request, jsonify, flash, redirect, url_for
from flask_restful import Api, Resource
from .models import User,db
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)
api = Api(auth)

class Login(Resource):
    def get(self):
        return make_response(render_template("login.html", user=current_user))
    
    def post(self):
        data = request.form.to_dict()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash('Logged in successfully', category='success')
                
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect email or password' , category="error")
        else:
            flash('Email does not exist', category="error")
        

class Logout(Resource):
    @login_required
    def post(self):
        logout_user()
        return redirect(url_for('auth.login'))
    
    
    
class SignUp(Resource):
    def get(self):
        return make_response(render_template('signup.html',user= current_user))
    
    def post(self):
        data = request.form.to_dict()
        firstName = data.get("firstName")
        secondName =  data.get("secondName")
        email = data.get("email")
        password = data.get("password")
        password2 = data.get("password2")

        user = User.query.filter_by(email=email).first()
        if user:
            flash('User already exists', category='error')
        elif len(email)<4:
            flash("Email must be greater than 3 characters", category="error")
        elif len(firstName)<2:
            flash("Name must be greater than 3 characters", category="error")
        elif password!=password2:
            flash("Invalid password", category="error")
        elif len(password)<7:
            flash("password must be greater than 7 characters", category="error")
        else:
            new_user = User(email=email, first_name=firstName,second_name=secondName,password=generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash("Account created successfully", category="success")
            return redirect(url_for('views.home'))



    
    
api.add_resource(Login,"/login")
api.add_resource(Logout,"/logout")
api.add_resource(SignUp,"/signup")

 