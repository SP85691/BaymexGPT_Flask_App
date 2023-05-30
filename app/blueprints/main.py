from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user, login_remembered
from app.models import User, Chat
from app import db
import smtplib
from email.message import EmailMessage
from app.blueprints.openai import openai_prompt, text_to_image_converter
import pyttsx3
import os

main = Blueprint('main', __name__)

def query_mail(name, email, text):
    
    SUBJECT = "Request for the Query!"
    FROM = email
    TO = "s.pratap.4155@gmail.com"
    TEXT = text
    

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("s.pratap.4155@gmail.com", "rvteiugmcykpqxsr")
    
    # to the owner
    msg = EmailMessage()
    msg['Subject'] = SUBJECT
    msg['From'] = FROM
    msg['To'] = TO
    msg.set_content(TEXT)
    server.send_message(msg)

    # to the user
    cust_msg = EmailMessage()
    cust_msg['Subject'] = "Thank you for contacting us!"
    cust_msg['From'] = TO
    cust_msg['To'] = FROM
    cust_msg.set_content(f"Dear {name},\nThank you for contacting us.\nWe will get back to you soon.\n\nRegards,\nBayMexGPT Team")
    server.send_message(cust_msg)
    server.quit()

    return "Success"

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/contact')
def contact():
    return render_template('contact_page.html')

@main.route('/chat')
@login_required
def chat():
    return render_template("components/chat.html")

@main.route('/chat', methods=['GET', 'POST'])
@login_required
def chat_response():
    if request.method == 'POST':
        msg = request.form['msg']
        
        # find the same question in DB
        chat = Chat.query.filter_by(question=msg).first()
        if chat:
            return chat.answer, convert_text_to_speech(chat.answer, voice='en-us', speed=150)
        
        else:
            input = msg
            response = openai_prompt(input)
            new_chat = Chat(username=current_user.username, question=input, answer=response, user_id = current_user.id)
            db.session.add(new_chat)
            db.session.commit()
            answer = response
            convert_text_to_speech(answer, voice='en-us', speed=150)
            return openai_prompt(input)
        
@main.route('/text_to_image')
@login_required
def text_to_image():
    return render_template('text_to_image.html')

@main.route('/text_to_image', methods=['GET', 'POST'])
@login_required
def text_to_image_response():
    if request.method == "POST":
        text = request.form["text"]
    try:
        text_to_image_converter(text)
    except Exception as e:
        # Handle the error or display an error message
        error_message = str(e)
        error = 'Wrong Prompt Attempted'
        return render_template('error.html', error=error)
    return redirect(url_for("main.text_to_image"))

@main.route('/error')
def error():
    return render_template('error.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name,
                           image = current_user.profile_picture,
                           state = current_user.state,
                           city = current_user.city,
                           profession = current_user.profession,
                           company = current_user.company_or_school,
                           about = current_user.bio,
                           address = current_user.address
                           )


@main.route('/contact', methods=['POST', 'GET'])
def index_post():
    if request.method == 'POST':
        contactDet = request.json
        name = contactDet['name']
        email = contactDet['email']
        message = contactDet['message']
        print(name, email, message)
        query_mail(name, email, message)
    
    return render_template('index.html', username=current_user.username)



@main.route('/playground')
@login_required
def playground():
    return render_template('playground.html', name=current_user.name,
                                        username=current_user.username,
                                        email=current_user.email
                            )


def convert_text_to_speech(text, voice='en-us', speed=150):
    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()
    
    # Set voice
    voices = engine.getProperty('voices')
    for v in voices:
        if voice.lower() in v.name.lower():
            engine.setProperty('voice', v.id)
            break
    
    # Set speed
    engine.setProperty('rate', speed)
    
    # Convert the text to speech
    engine.say(text)
    engine.runAndWait()