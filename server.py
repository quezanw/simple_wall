from flask import Flask, request, render_template, redirect, session, flash
from mysqlconnection import connectToMySQL
import re
from flask_bcrypt import Bcrypt
import datetime

app = Flask(__name__)
app.secret_key = "secret"
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    if not session.get("first_name"):
        session["first_name"] = ""
    if not session.get("last_name"):
        session["last_name"] = ""
    if not session.get("email"):
        session["email"] = ""

    return render_template('index.html')

@app.route('/register', methods=["POST"])
def register():
    data = request.form
    session["first_name"] = data["first_name"]
    session["last_name"] = data["last_name"]
    session["email"] = data["email"]
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
    PASSWORD_REGEX = re.compile(r'(?=.*[A-Z])(?=.*[0-9])^[a-zA-Z0-9]+$')
    print("*"*50, "\n", data, "\n", "*"*50)
    # add sql queries

    def empty_field():
        return "should not be left blank"

    select_query = connectToMySQL("loginDB")
    email_address =  {
        "email": data["email"]
    }
    email_query = select_query.query_db("SELECT email FROM users WHERE email = %(email)s;", email_address)

    if len(data["first_name"]) < 1:
        flash(u"First Name {}".format(empty_field()), "first_name_error")
    elif len(data["first_name"]) < 2:
        flash(u"Must be longer than 2 characters", "first_name_error")
    elif not NAME_REGEX.match(data["first_name"]):
        flash(u"name must not contain numbers", "first_name_error")

    if len(data["last_name"]) < 1:
        flash(u"Last Name {}".format(empty_field()),"last_name_error")
    elif len(data["first_name"]) < 2:
        flash(u"Must be longer than 2 characters", "last_name_error")
    elif not NAME_REGEX.match(data["last_name"]):
        flash(u"name must not contain numbers", "last_name_error")

    if len(data["email"]) < 1:
        flash(u"Email {}".format(empty_field()), "email_error")
    elif not EMAIL_REGEX.match(data["email"]):
        flash(u"Invalid Email", "email_error")
    elif email_query:
        flash(u"Email has been used already", "email_error") 

    if len(data["password"]) < 1:
        flash(u"Password {}".format(empty_field()), "password_error")
    elif len(data["password"]) <= 8:
        flash(u"password must be longer than 8 character", "password_error")

    if len(data["confirm_password"]) < 1:
        flash(u"Confirm Password {}".format(empty_field()),"confirm_password_error")
    elif data["password"] != data["confirm_password"]:
        flash(u"Passwords do not match", "password")
    
    if "_flashes" in session.keys():
        return redirect('/')
    print(session)
    pw_hash = bcrypt.generate_password_hash(data["password"])
    print(pw_hash)
    insert_query = connectToMySQL("loginDB")
    query_data = {
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "email": data["email"],
        "password_hash": pw_hash
    }
    insert_query.query_db("INSERT INTO users (first_name, last_name, email, password_hash, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password_hash)s, now(), now())", query_data)
    session.clear()
    session["registered"] = True
    return redirect('/success')

@app.route('/login', methods=["POST"])
def login():
    session.clear()
    session["registered"] = False
    data = request.form
    select_query = connectToMySQL("loginDB")
    user_data = {
        "email": data["login_email"],
    }
    user_query = select_query.query_db("SELECT * FROM users WHERE email = %(email)s", user_data)
    session["first_name"] = user_query[0]["first_name"]
    session["user_id"] = user_query[0]["id"]
    if user_query:
        if bcrypt.check_password_hash(user_query[0]["password_hash"], data["login_password"]):
            print(user_query)
            return redirect('/success')
    flash(u"The information you provided was wrong", "login_error")
    return redirect('/')

@app.route('/success')
def success():
    print(session)
    success_msg = ""
    if session["registered"]:
        success_msg = "you've been successfully registered!"
    select_query = connectToMySQL("loginDB")
    query_data = {
        "first_name": session["first_name"],
        "id": session["user_id"]
    }
    friends_query = select_query.query_db("SELECT * FROM users JOIN friendships ON users.id = friendships.friend_1_id JOIN users as friends ON friends.id = friendships.friend_2_id WHERE users.id = %(id)s", query_data)
    #print(friends_query[0]["friends.first_name"])

    select_query = connectToMySQL("loginDB")
    message_query = select_query.query_db("SELECT *, TIMESTAMPDIFF(HOUR, messages.created_at, now()) as hours FROM users JOIN messages ON users.id = messages.user_id JOIN users as friends ON friends.id = messages.user2_id WHERE users.id =  %(id)s", query_data)
    select_query = connectToMySQL("loginDB")
    message_count_query = select_query.query_db("SELECT * FROM messages WHERE user2_id =  %(id)s", query_data)
    datetime_query = connectToMySQL("loginDB")
    datetime_query_data = datetime_query.query_db("SELECT TIMESTAMPDIFF(HOUR, messages.created_at, now()) as hours FROM users JOIN messages ON users.id = messages.user_id JOIN users as friends ON friends.id = messages.user2_id WHERE users.id =  %(id)s", query_data) 
    for i in datetime_query_data:
        print(i["hours"])
    return render_template("success.html", msg=success_msg, friends_info=friends_query, messages=message_query, recieved=len(message_query), sent=len(message_count_query))

@app.route('/send', methods=["POST"])
def send_mesage():
    data = request.form
    insert_query = connectToMySQL("loginDB")
    query_data = {
        "friend_id": data["friend_id"],
        "user_id": session["user_id"],
        "message": data["message"]
    }
    insert_query.query_db("INSERT INTO messages (user_id, user2_id, content, created_at, updated_at) VALUES (%(friend_id)s, %(user_id)s, %(message)s, now(), now())", query_data)
    return redirect('/success')

@app.route('/delete', methods=["POST"])
def delete():
    delete = connectToMySQL('loginDB')
    delete_data = {
        "friend_id": request.form["friend_id"]
    }
    delete.query_db("DELETE FROM messages WHERE user2_id = %(friend_id)s", delete_data)

    return redirect('/success')

@app.route('/clear')
def clear():
    session.clear()

    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)