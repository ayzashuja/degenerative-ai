from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from pymongo import MongoClient

# from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

try:
    # Connect to MongoDB
    client = MongoClient("mongodb+srv://talhatariq:Helloabc123@mycluster.tkqpdpz.mongodb.net/?retryWrites=true&w=majority&appName=MyCluster")
                        #  mongodb+srv://23100300:0123456789@cluster0.snltxmz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
                        #  mongodb+srv://talhatariq:<Helloabc123>@mycluster.tkqpdpz.mongodb.net/")
    db = client.test
    users_collection = db.users
    print("Connected to MongoDB")
    print("Mongo: ", client)
    print("DB: ", db)
    print("users_collection: ", users_collection)
except Exception as e:
    print("Error connecting to MongoDB:", e)

app = Flask(__name__)

app.secret_key = 'your_secret_key'

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/signup_page')
def signup_page():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    print(username)
    print(password)

    # Check if username already exists
    if users_collection.find_one({"username": username}):
        return jsonify({"message": "Username already exists"}), 400

    # Insert user into the database
    users_collection.insert_one({"username": username, "password": password})
    session['logged_in'] = True
    print("Redirecting to channels page after signup")
    return redirect(url_for('channels'))
    # return jsonify({"message": "Signup successful"}), 200

@app.route('/', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    print(username)
    print(password)
    # Retrieve user from the database
    user = users_collection.find_one({"username": username})

    if not user:
        return jsonify({"message": "User not found"}), 404

    # Check if the provided password matches the password in the database
    if password == user['password']:
        session['logged_in'] = True
        print("Redirecting to channels page after signup")
        return redirect(url_for('channels'))
        # return redirect('/channels')
        # return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Incorrect password"}), 401

@app.route('/channels')
def channels():
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))
    return render_template('channels.html')

# Route for channel videos
@app.route('/channel/<int:channel_id>')
def channel_videos(channel_id):
    return render_template(f'channel{channel_id}.html')

# Redirect after successful login/signup
@app.route('/redirect_to_channels')
def redirect_to_channels():
    return redirect(url_for('channels'))

@app.route('/logout', methods=['POST'])
def logout():
    # Clear session variables
    session.pop('logged_in', None)
    return redirect(url_for('login_page'))

@app.route('/process_message', methods=['POST'])
def process_message():
    data = request.json
    message = data.get('message')
    # Process the message here (e.g., send to a model for response generation)
    # For now, let's just acknowledge the message
    return jsonify({"message": "Message acknowledged"})


# @app.route('/users', methods=['GET'])
# def get_users():
#     users = users_collection.find()
#     return jsonify(list(users)), 200

# @app.route('/add', methods=['POST'])
# def add():
#     data = request.json
#     numbers = data.get('numbers')
#     if not numbers:
#         return jsonify({"error": "Numbers are required"}), 400
#     result = sum(numbers)
#     return jsonify({"result": result}), 200

# @app.route('/hello')
# def hello():
#     name = request.args.get('name')
#     return f'Hello, {name}!'

# @app.route('/static/<path:path>')
# def static_file(path):
#     return app.send_static_file(path)

if __name__ == '__main__':
    app.run(debug=True)
