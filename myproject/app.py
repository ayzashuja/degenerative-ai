from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from pymongo import MongoClient
import os
import importlib.util
# from werkzeug.security import generate_password_hash, check_password_hash
from nbconvert import PythonExporter
import nbformat
from IPython.display import display
import traceback


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
'''
notebook_path = 'myproject//models//final_prompts.ipynb'
with open(notebook_path, 'r', encoding='latin-1') as f:
    nb = nbformat.read(f, as_version=4)

py_exporter = PythonExporter()
py_script, _ = py_exporter.from_notebook_node(nb)
spec = importlib.util.spec_from_loader('__main__', loader=None)
module = importlib.util.module_from_spec(spec)
exec(py_script, module.__dict__)
'''
import textwrap
import chromadb
import numpy as np
import pandas as pd
import google.generativeai as genai
import google.ai.generativelanguage as glm
import os
import re
import inflect
from chromadb import Documents, EmbeddingFunction, Embeddings
from IPython.display import Markdown

genai.configure(api_key='AIzaSyC1xnPaYuc0BXq-NOl9cGXKdzwLVRu4w-k')  # Replace with your API key


class GeminiEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        model = 'models/embedding-001'
        title = "Custom query"
        return genai.embed_content(model=model,
                                    content=input,
                                    task_type="retrieval_document",
                                    title=title)["embedding"]


def read_transcripts_to_dataframe(dataset_path):
    data = []

    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            if file.endswith('.txt'):
                video_id = file.replace('.txt', '')
                file_path = os.path.join(root, file)

                with open(file_path, 'r') as file:
                    content = file.read()
                    data.append((video_id, content))

    df = pd.DataFrame(data, columns=['Video_ID', 'Transcript'])
    return df


def clean_text(text):
    p = inflect.engine()

    def number_to_words(number_str):
        try:
            if '.' in number_str:
                parts = number_str.split('.')
                if len(parts) == 2:
                    return p.number_to_words(parts[0]) + ' point ' + ' '.join(p.number_to_words(part) for part in parts[1])

            return p.number_to_words(number_str)
        except:
            return number_str

    if not isinstance(text, str) or not text.strip():
        return "emptytext"

    text = text.lower()
    text = re.sub(r'\d+\.\d+|\d+', lambda x: number_to_words(x.group()), text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'#\w+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text if text.strip() else "defaulttext"

def process_transcripts(base_path):
    data = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                video_id = file.split('.')[0]
                with open(file_path, 'r', encoding='latin-1') as f:
                    content = f.read()
                    cleaned_content = clean_text(content)
                    #cleaned_content=content
                    data.append((video_id, cleaned_content))

    df = pd.DataFrame(data, columns=['Video_ID', 'Cleaned_Transcript'])
    return df

def create_chroma_db(documents, name):
    chroma_client = chromadb.Client()
    db = chroma_client.create_collection(name=name, embedding_function=GeminiEmbeddingFunction())

    for i, d in enumerate(documents):
        db.add(
            documents=d,
            ids=str(i)
        )
    return db

def get_relevant_passages(query, db, num_results=5):
    query_embedding = GeminiEmbeddingFunction()(query)
    query_embedding = np.array(query_embedding)  # Convert to numpy array

    results = db.query(query_texts=[query], n_results=num_results)
    #results = db.query(query_embeddings=query_embedding,include=[ "embeddings" ], n_results=num_results,where={"metadata_field": "is_equal_to_this"}, where_document={"$contains":"search_string"}) #,where_document={"$contains":query}
    #print(results['documents'])
    documents = results['documents'][0] #['documents'][0]
    return documents

def make_prompt(query, relevant_passages):
    combined_passages = ' '.join([passage.replace("'", "").replace('"', "").replace("\n", " ") for passage in relevant_passages])

    prompt = (f"""You are a helpful and informative bot that answers questions using text from the reference passages included below.
    Be sure to respond in a complete sentence, being comprehensive, including all relevant background information.
    However, you are talking to a non-technical audience, so be sure to break down complicated concepts and use analogies where possible.
    If the question is unclear or there are multiple possible interpretations, provide information for all interpretations or ask for clarification.
    Question: {query}
    Reference Passages: {combined_passages}""")

    return prompt


def query_result(query,db):
    try:
        passages = get_relevant_passages(query, db, num_results=2)
        prompt = make_prompt(query, passages)
        model = genai.GenerativeModel('gemini-pro')
        answer = model.generate_content(prompt)
        return answer.text
    except Exception as e:
        # Log the exception traceback for debugging
        traceback.print_exc()
        # Return a generic error message to the client
        return "An error occurred while processing the query"

dataset_path = './myproject//models//transcripts'
df = process_transcripts(dataset_path)
db = create_chroma_db(df['Cleaned_Transcript'], "transcript_new_transcripts")

@app.route('/process_message', methods=['POST'])
def process_message():
    data = request.json
    message = data.get('message') 
    
    #exec(py_script)
    #result,prompt = module.query_result(message)
    #print(prompt)
   
    #print(pd.DataFrame(db.peek(12)))
    result = query_result(message,db)
    #print(result)
    # Process the message here (e.g., send to a model for response generation)
    # For now, let's just acknowledge the message
    return jsonify({"message": result})


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
