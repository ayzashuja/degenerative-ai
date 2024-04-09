from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

try:
    # Connect to MongoDB
    client = MongoClient("mongodb+srv://talhatariq:<Helloabc123>@mycluster.tkqpdpz.mongodb.net/")
    db = client.test
    users_collection = db.users
    print("Connected to MongoDB")
except Exception as e:
    print("Error connecting to MongoDB:", e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup_page')
def signup_page():
    return render_template('signup.html')

@app.route('/login_page')
def login_page():
    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Check if username already exists
    if users_collection.find_one({"username": username}):
        return jsonify({"message": "Username already exists"}), 400

    # Hash the password before storing
    hashed_password = generate_password_hash(password)

    # Insert user into the database
    users_collection.insert_one({"username": username, "password": hashed_password})
    return jsonify({"message": "Signup successful"}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Retrieve user from the database
    user = users_collection.find_one({"username": username})

    if not user:
        return jsonify({"message": "User not found"}), 404

    # Check if the provided password matches the hashed password in the database
    if check_password_hash(user['password'], password):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Incorrect password"}), 401

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
