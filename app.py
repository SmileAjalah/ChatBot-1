from flask import Flask, render_template, request, redirect, url_for, session
# import json
import openai
import os
from dotenv import load_dotenv
from datetime import datetime
# from fastapi import FastAPI
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.sql import text
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

# Set up Flask app
app = Flask(__name__)

app.secret_key = 'xyzsdfg'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mydatabase'

mysql = MySQL(app)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password,))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            mesage = 'Logged in successfully !'
            return render_template('user.html', mesage=mesage)
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage=mesage)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s', (email,))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not userName or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (userName, email, password,))
            mysql.connection.commit()
            mesage = 'You have successfully regist  ered !'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('register.html', mesage=mesage)

@app.route('/chat',methods=['GET','POST'])
def chat():
    msg = ''
    if request.method == 'POST' and 'chat' in request.form:
        chat = request.form['chat']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO chat VALUES (NULL,"1","u",now(), % s)', (chat))
        mysql.connection.commit()
    return render_template('Len.html', msg=msg)

# https://platform.openai.com/account/api-keys
load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

# print(openai.api_key)

# Define the home page route
@app.route("/Homechat.html")
def home():
    return render_template("Homechat.html")
@app.route("/firstchat.html")
def FLen():
    return render_template("firstchat.html")

# Define the chatbot route
@app.route("/chatbot", methods=["POST"])
def chatbot():
    # pass

    # Get the message input from the user
    user_input = request.form["message"]
    # return render_template('Len.html', user_input=user_input)

    date_time = datetime.now()
    date = date_time.strftime("%H:%M")
    # return str(date_time)
    # return render_template('Len.html', date=date)

    # Use the OpenAI API to generate  a response
    prompt = f"User: {user_input}\nChatbot: "
    chat_history = []
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        stop=["\nUser: ", "\nChatbot: "]
    )

    # Extract the response text from the OpenAI API result
    bot_response = response.choices[0].text.strip()

    # Add the user input and bot response to the chat history
    chat_history.append(f"User: {user_input}\nChatbot: {bot_response}")

    # Render the Chatbot template with the response text

    # if request.method == 'POST' and 'chat' in request.form:
    #     chat = request.form['chat']
    #     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #     cursor.execute('INSERT INTO chat VALUES (NULL,"1", % s,"u",now())', (chat))
    #     mysql.connection.commit()

    return render_template(
        "Len.html",
        user_input=user_input,
        bot_response=bot_response,
        date=date
    )

# Start the Flask app
if __name__ == "__main__":
    app.run(debug=True)