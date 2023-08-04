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
    
    SUBJECT = "Welcome to BaymexGPT - Your Gateway to a World of AI-Powered Services!"
    FROM = "s.pratap.4155@gmail.com"
    TO = email
    TEXT = f"Dear {name}, \nWelcome to BaymexGPT! We are thrilled to have you join our family. Thank you for registering with us using the email address {email}.\n\nAt BaymexGPT, we are dedicated to providing you with exceptional AI-powered services. Our platform offers two remarkable features: Chatbot and Image Generation. Whether you need interactive conversational support or stunning image creation, we've got you covered!\n\nWe understand the importance of safeguarding your personal information. Rest assured, we have implemented robust security measures to ensure that your data remains private and protected. Your trust is our top priority.\n\nWith BaymexGPT, you can enjoy a seamless user experience, exploring the vast possibilities of artificial intelligence. We believe in simplicity without compromising on quality, making your journey with us both impressive and effortless.\n\nOnce again, thank you for choosing BaymexGPT. We are excited to embark on this AI-powered adventure with you. Should you have any questions or need assistance, our friendly support team is just a message away.\n\nBest regards,\nBaymexGPT Bot"
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(username, password)
    
    msg = EmailMessage()
    msg['Subject'] = SUBJECT
    msg['From'] = FROM
    msg['To'] = TO
    msg.set_content(TEXT)
    server.send_message(msg)
    server.quit()

    return "Success"


def forgotten_mail(name, email):
    otp = random.randint(100000,999999)
    
    SUBJECT = "Password Reset Confirmation - BaymexGPT"
    FROM = "s.pratap.4155@gmail.com"
    TO = email
    TEXT = f"Dear Surya Pratap,\nWe have received a request to reset your password for your BaymexGPT account. We understand that forgetting passwords happens to the best of us, and we are here to assist you in regaining access to your account.\n\nTo proceed with resetting your password, please click on the following link: [Password Reset Link].\n\nUpon clicking the link, you will be directed to a secure page where you can create a new password for your BaymexGPT account. Please ensure that your new password is unique and easy for you to remember, but difficult for others to guess.\n\nIf you did not initiate this password reset request, kindly ignore this email. Rest assured, your account remains secure, and no changes have been made.\n\nYour privacy and security are of utmost importance to us. If you encounter any issues or require further assistance, please do not hesitate to reach out to our dedicated support team. We are here to help you navigate through any challenges.\n\nThank you for choosing BaymexGPT. We appreciate your patience and understanding as we assist you in restoring access to your account.\n\nBest regards,\nBaymexGPT Bot"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(username, password)
    
    msg = EmailMessage()
    msg['Subject'] = SUBJECT
    msg['From'] = FROM
    msg['To'] = TO
    msg.set_content(TEXT)
    server.send_message(msg)
    server.quit()

    return "Success"

def delete_user_mail(name, email):
    otp = random.randint(100000,999999)
    
    SUBJECT = "Account Deletion Confirmation - BaymexGPT"
    FROM = "s.pratap.4155@gmail.com"
    TO = email
    TEXT = f"Dear {name},\nWe regret to inform you that your account has been successfully deleted from BaymexGPT. We acknowledge your decision and respect your choice.\n\nWe sincerely thank you for being a part of our community and for the trust you placed in us during your time with BaymexGPT. We hope our services were able to meet your expectations, and we apologize for any inconvenience caused.\n\nIf you have any feedback or suggestions regarding your experience with us, we would greatly appreciate your valuable insights. Your input plays a crucial role in helping us improve our services for the benefit of our users.\n\nShould you ever reconsider, remember that you are always welcome back to the BaymexGPT family. We are constantly evolving and introducing new features to enhance your AI-powered journey.If you have any remaining concerns or require further assistance, please don't hesitate to reach out to our support team. We are here to assist you.\n\nOnce again, thank you for being a part of BaymexGPT. We wish you the very best in all your future endeavors.\n\n--\nWarm regards,\nBaymexGPT Bot"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("s.pratap.4155@gmail.com", "rvteiugmcykpqxsr")
    
    msg = EmailMessage()
    msg['Subject'] = SUBJECT
    msg['From'] = FROM
    msg['To'] = TO
    msg.set_content(TEXT)
    server.send_message(msg)
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

        elif username != user or bcrypt.verify(password, user.password):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        
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
        if user_email or user_name:
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

            print(upt_data)
            try:
                db.session.commit()
                db.session.close()
                return redirect(url_for('main.profile'))
            except:
                return redirect(url_for('auth.edit_profile'))
        
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


            
