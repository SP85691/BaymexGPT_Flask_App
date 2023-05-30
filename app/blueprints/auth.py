from flask import Blueprint, request, redirect, render_template, url_for, flash, session, jsonify
from flask_login import login_user,logout_user, login_required, current_user
import smtplib
from datetime import timedelta
import random
from app import db
from app.models import User, Chat
from passlib.hash import bcrypt
from email.message import EmailMessage
import cv2 
import os
import dotenv

dotenv.load_dotenv()

username = os.getenv("Email")
password = os.getenv("Password")

auth = Blueprint('auth', __name__)

def mail(name, email):
    otp = random.randint(100000,999999)
    
    SUBJECT = "BaymexGPT Registration"
    FROM = "s.pratap.4155@gmail.com"
    TO = email
    TEXT = f"Dear {name},\nThank you for becoming a part of our family.\nYou have registered by this email id - {email}"
    

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(username, password)
    
    msg = EmailMessage()
    msg['Subject'] = SUBJECT
    msg['From'] = FROM
    msg['To'] = TO
    msg.set_content(TEXT)
    server.send_message(msg)
    # server.sendmail('support@baymexgpt.com', email, f"Dear {name},\nThank you for becoming a part of our family.\nYou have registered by this email id - {email}")
    server.quit()

    return "Success"


def forgotten_mail(name, email):
    otp = random.randint(100000,999999)
    
    SUBJECT = "Verify Email for Regenerate your password!"
    FROM = "s.pratap.4155@gmail.com"
    TO = email
    TEXT = f"Dear {name},\nRecently, You have reset your password.\nKindly Verify youself by click on this link - 'http://127.0.0.1:5000/auth/login'"
    

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(username, password)
    
    msg = EmailMessage()
    msg['Subject'] = SUBJECT
    msg['From'] = FROM
    msg['To'] = TO
    msg.set_content(TEXT)
    server.send_message(msg)
    # server.sendmail('support@baymexgpt.com', email, f"Dear {name},\nThank you for becoming a part of our family.\nYou have registered by this email id - {email}")
    server.quit()

    return "Success"

@auth.route('/setting')
@login_required
def setting():
    return render_template('setting.html', 
                           name = current_user.name, 
                           username = current_user.username, 
                           profession = current_user.profession, 
                           state=current_user.state, 
                           city = current_user.city,
                           company=current_user.company_or_school)

def delete_user_mail(name, email):
    otp = random.randint(100000,999999)
    
    SUBJECT = "BaymexGPT Registration"
    FROM = "s.pratap.4155@gmail.com"
    TO = email
    TEXT = f"Dear {name},\nThank you for using our website and being a part of our family.\nYou have deleted your account!\nPlease send us feedback that why you have deleted your account!\n\n\n--\nThanks & Regards\nSurya Pratap (Owner of BaymexGPT)\ns.pratap.4155@gmail.com"
    

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("s.pratap.4155@gmail.com", "rvteiugmcykpqxsr")
    
    msg = EmailMessage()
    msg['Subject'] = SUBJECT
    msg['From'] = FROM
    msg['To'] = TO
    msg.set_content(TEXT)
    server.send_message(msg)
    # server.sendmail('support@baymexgpt.com', email, f"Dear {name},\nThank you for becoming a part of our family.\nYou have registered by this email id - {email}")
    server.quit()

    return "Success"

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST', 'GET'])
def login_post():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.verify(password, user.password):
            login_user(user)  # Log in the user
            session.permanent = True
            return redirect(url_for('main.index'))
    
    flash('Invalid username or password')
    return redirect(url_for('auth.login'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST', 'GET'])
def signup_post():
    if request.method == 'POST':
        username = request.form.get('username')
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_pass = bcrypt.hash(password)

        user_email = User.query.filter_by(email=email).first()
        user_name = User.query.filter_by(username=username).first()
        if user_email and user_name:
            flash('This User already exists')
            return redirect(url_for('auth.signup'))
        
        else:
            new_user = User(username=username, name=name, email=email, password=hashed_pass)

            db.session.add(new_user)
            db.session.commit()
            db.session.close()

            msg = mail(name, email)
            print(msg)

    return redirect(url_for('auth.login')) 

# forgot_password
@auth.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

# forgot_password post
@auth.route('/forgot_password', methods=['POST', 'GET'])
def forgot_password_post():
    if request.method == 'POST':
        forgData = request.json
        email = forgData['email']
        user = User.query.filter_by(email=email).first()
        if user:
            # update the user's password
            msg = forgotten_mail(user.name, user.email)
            print(msg)
            user.password = bcrypt.hash(forgData['password'])
            db.session.commit()
            db.session.close()
            return redirect(url_for('auth.login'))
   
    return redirect(url_for('auth.forgot_password'))

# edit_profile
@auth.route('/edit_profile')
@login_required
def edit_profile():
    return render_template('edit_profile.html', 
                           image = current_user.profile_picture,
                           username = current_user.username, 
                           name=current_user.name, 
                           email=current_user.email,
                           about=current_user.bio,
                           profession=current_user.profession,
                           company=current_user.company_or_school,
                           country=current_user.country,
                           phone=current_user.phone,
                           address=current_user.address,
                           city=current_user.city,
                           state=current_user.state,
                           pincode=current_user.pincode
                           )

# update data in the User Table
@auth.route('/edit_profile', methods=['POST', 'GET'])
@login_required
def update_profile():
    if request.method == 'POST':
        upt_data = request.json
        username = upt_data['data']['username']
        user = User.query.filter_by(username=username).first()

        if user:
            # update everything from the database such as profile_picture, bio, profession, college, country, phone, address, city and state
            user.profile_picture = upt_data['data']['image']
            user.bio = upt_data['data']['about']
            user.profession = upt_data['data']['profession']
            user.company_or_school = upt_data['data']['company']
            user.country = upt_data['data']['country']
            user.phone = upt_data['data']['phone']
            user.address = upt_data['data']['address']
            user.city = upt_data['data']['city']
            user.state = upt_data['data']['state']
            user.pincode = upt_data['data']['pincode']
            db.session.commit()
            db.session.close()
            return redirect(url_for('main.profile'))
        
        else:
            return redirect(url_for('auth.edit_profile'))
        
# delete_user
@auth.route('/delete_user')
@login_required
def delete_user():
    user = User.query.filter_by(username=current_user.username).first()
    delete_user_mail(current_user.name, current_user.email)
    db.session.delete(user)
    db.session.commit()
    db.session.close()
    return redirect(url_for('auth.logout'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()  # Log out the user
    db.session.close()
    session.clear()
    return redirect(url_for('auth.login'))


            
