from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient



app = Flask(__name__)

try:
    # Connect to MongoDB
    client = MongoClient("mongodb+srv://talhatariq:<Helloabc123>@mycluster.tkqpdpz.mongodb.net/")
    db = client.test
    users_collection = db.users
    print("Connected to MongoDB")
except Exception as e:
    print("Error connecting to MongoDB:", e)

@app.route('/users', methods=['GET'])
def get_users():
    users = users_collection.find()
    return jsonify(list(users)), 200

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add():
    data = request.json
    numbers = data.get('numbers')
    if not numbers:
        return jsonify({"error": "Numbers are required"}), 400
    result = sum(numbers)
    return jsonify({"result": result}), 200

@app.route('/hello')
def hello():
    name = request.args.get('name')
    return f'Hello, {name}!'

@app.route('/static/<path:path>')
def static_file(path):
    return app.send_static_file(path)

if __name__ == '__main__':
    app.run(debug=True)
