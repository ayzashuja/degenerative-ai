from flask import Flask, jsonify, request
# from pymongo import MongoClient
import re
from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
from pymongo import MongoClient

# app = Flask(__name__)
# app.config["MONGO_URI"] = "mongodb+srv://23100300:0123456789@genaicluster.qemlnnb.mongodb.net/?retryWrites=true&w=majority&appName=GenAiCluster"
# mongo = PyMongo(app)
# db = mongo.db
# users_collection = db.users

# password_regex = re.compile(
#     r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$'
# )

# @app.route('/signup', methods=['POST'])
# def signup():
#     data = request.json
#     username = data.get('username')
#     password = data.get('password')

#     # Check if username already exists
#     if users_collection.find_one({'username': username}):
#         return jsonify({"message": "Username already exists"}), 400

#     # Validate password
#     if not password_regex.match(password):
#         return jsonify({"message": "Password must contain at least one uppercase letter, one lowercase letter, one numeric character, and have a minimum length of 8 characters"}), 400

#     # Hash password
#     hashed_password = generate_password_hash(password)

#     # Insert user into database
#     users_collection.insert_one({'username': username, 'password': hashed_password})
#     return jsonify({"message": "User created successfully"}), 201

# @app.route('/login', methods=['POST'])
# def login():
#     data = request.json
#     username = data.get('username')
#     password = data.get('password')

#     # Find user by username
#     user = users_collection.find_one({'username': username})

#     if not user:
#         return jsonify({"message": "User not found"}), 404

#     # Check password
#     if not check_password_hash(user['password'], password):
#         return jsonify({"message": "Incorrect password"}), 401

#     return jsonify({"message": "Signin successful"}), 200

# if __name__ == '__main__':
#     app.run(debug=True)


app = Flask(__name__)
client = MongoClient("mongodb+srv://23100300:0123456789@genaicluster.qemlnnb.mongodb.net/?retryWrites=true&w=majority&appName=GenAiCluster")
db = client.get_database("genaicluster")  # Get the database
users_collection = db.users  # Collection for storing user data

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Check if username already exists
    if users_collection.find_one({'username': username}):
        return jsonify({"message": "Username already exists"}), 400

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

    return jsonify({"message": "Login successful"}), 200

if __name__ == '__main__':
    app.run(debug=True)
    