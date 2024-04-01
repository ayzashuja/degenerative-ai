from flask import Flask, jsonify, request
from pymongo import MongoClient
import re
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
client = MongoClient("mongodb+srv://23100300:0123456789@genaicluster.qemlnnb.mongodb.net/")
db = client.genaicluster
users_collection = db.users

password_regex = re.compile(
    r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$'
)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Check if username already exists
    if users_collection.find_one({'username': username}):
        return jsonify({"message": "Username already exists"}), 400

    # Validate password
    if not password_regex.match(password):
        return jsonify({"message": "Password must contain at least one uppercase letter, one lowercase letter, one numeric character, and have a minimum length of 8 characters"}), 400

    # Hash password
    hashed_password = generate_password_hash(password)

    # Insert user into database
    users_collection.insert_one({'username': username, 'password': hashed_password})
    return jsonify({"message": "User created successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Find user by username
    user = users_collection.find_one({'username': username})

    if not user:
        return jsonify({"message": "User not found"}), 404

    # Check password
    if not check_password_hash(user['password'], password):
        return jsonify({"message": "Incorrect password"}), 401

    return jsonify({"message": "Signin successful"}), 200


# @app.route('/')
# def hello():
#     return 'Hello, World!'

# @app.route('/api/data', methods=['GET'])
# def get_data():
#     data = list(db.collection.find())
#     return jsonify(data), 200

# @app.route('/api/data', methods=['POST'])
# def add_data():
#     new_data = request.json
#     db.collection.insert_one(new_data)
#     return jsonify({"message": "Data added successfully"}), 201

# Add routes for other CRUD operations (PUT, DELETE) as needed

if __name__ == '__main__':
    app.run(debug=True)
