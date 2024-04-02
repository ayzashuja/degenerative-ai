from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

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
