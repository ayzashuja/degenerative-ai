# from flask import Flask, jsonify, request, render_template, redirect, url_for, session
# from pymongo import MongoClient
# import os
# import importlib.util
# # from werkzeug.security import generate_password_hash, check_password_hash
# from nbconvert import PythonExporter
# import nbformat
# from IPython.display import display
# import traceback


# app = Flask(__name__)

# try:
#     # Connect to MongoDB
#     client = MongoClient("mongodb+srv://talhatariq:Helloabc123@mycluster.tkqpdpz.mongodb.net/?retryWrites=true&w=majority&appName=MyCluster")
#                         #  mongodb+srv://23100300:0123456789@cluster0.snltxmz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
#                         #  mongodb+srv://talhatariq:<Helloabc123>@mycluster.tkqpdpz.mongodb.net/")
#     db = client.test
#     users_collection = db.users
#     print("Connected to MongoDB")
#     print("Mongo: ", client)
#     print("DB: ", db)
#     print("users_collection: ", users_collection)
# except Exception as e:
#     print("Error connecting to MongoDB:", e)

# app = Flask(__name__)

# app.secret_key = 'your_secret_key'

# # @app.route('/')
# # def index():
# #     return render_template('index.html')

# @app.route('/')
# def login_page():
#     return render_template('login.html')

# @app.route('/signup_page')
# def signup_page():
#     return render_template('signup.html')

# @app.route('/signup', methods=['POST'])
# def signup():
#     data = request.json
#     username = data.get('username')
#     password = data.get('password')
#     print(username)
#     print(password)

#     # Check if username already exists
#     if users_collection.find_one({"username": username}):
#         return jsonify({"message": "Username already exists"}), 400

#     # Insert user into the database
#     users_collection.insert_one({"username": username, "password": password})
#     session['logged_in'] = True
#     print("Redirecting to channels page after signup")
#     return redirect(url_for('channels'))
#     # return jsonify({"message": "Signup successful"}), 200

# @app.route('/', methods=['POST'])
# def login():
#     data = request.json
#     username = data.get('username')
#     password = data.get('password')
#     print(username)
#     print(password)
#     # Retrieve user from the database
#     user = users_collection.find_one({"username": username})

#     if not user:
#         return jsonify({"message": "User not found"}), 404

#     # Check if the provided password matches the password in the database
#     if password == user['password']:
#         session['logged_in'] = True
#         print("Redirecting to channels page after signup")
#         return redirect(url_for('channels'))
#         # return redirect('/channels')
#         # return jsonify({"message": "Login successful"}), 200
#     else:
#         return jsonify({"message": "Incorrect password"}), 401

# @app.route('/channels')
# def channels():
#     if not session.get('logged_in'):
#         return redirect(url_for('login_page'))
#     return render_template('channels.html')

# # Route for channel videos
# @app.route('/channel/<int:channel_id>')
# def channel_videos(channel_id):
#     return render_template(f'channel{channel_id}.html')

# # Redirect after successful login/signup
# @app.route('/redirect_to_channels')
# def redirect_to_channels():
#     return redirect(url_for('channels'))

# @app.route('/logout', methods=['POST'])
# def logout():
#     # Clear session variables
#     session.pop('logged_in', None)
#     return redirect(url_for('login_page'))
# '''
# notebook_path = 'myproject//models//final_prompts.ipynb'
# with open(notebook_path, 'r', encoding='latin-1') as f:
#     nb = nbformat.read(f, as_version=4)

# py_exporter = PythonExporter()
# py_script, _ = py_exporter.from_notebook_node(nb)
# spec = importlib.util.spec_from_loader('__main__', loader=None)
# module = importlib.util.module_from_spec(spec)
# exec(py_script, module.__dict__)
# '''
# import textwrap
# import chromadb
# import numpy as np
# import pandas as pd
# import google.generativeai as genai
# import google.ai.generativelanguage as glm
# import os
# import re
# import inflect
# from chromadb import Documents, EmbeddingFunction, Embeddings
# from IPython.display import Markdown

# genai.configure(api_key='AIzaSyC1xnPaYuc0BXq-NOl9cGXKdzwLVRu4w-k')  # Replace with your API key


# class GeminiEmbeddingFunction(EmbeddingFunction):
#     def __call__(self, input: Documents) -> Embeddings:
#         model = 'models/embedding-001'
#         title = "Custom query"
#         return genai.embed_content(model=model,
#                                     content=input,
#                                     task_type="retrieval_document",
#                                     title=title)["embedding"]


# def read_transcripts_to_dataframe(dataset_path):
#     data = []

#     for root, dirs, files in os.walk(dataset_path):
#         for file in files:
#             if file.endswith('.txt'):
#                 video_id = file.replace('.txt', '')
#                 file_path = os.path.join(root, file)

#                 with open(file_path, 'r') as file:
#                     content = file.read()
#                     data.append((video_id, content))

#     df = pd.DataFrame(data, columns=['Video_ID', 'Transcript'])
#     return df


# def clean_text(text):
#     p = inflect.engine()

#     def number_to_words(number_str):
#         try:
#             if '.' in number_str:
#                 parts = number_str.split('.')
#                 if len(parts) == 2:
#                     return p.number_to_words(parts[0]) + ' point ' + ' '.join(p.number_to_words(part) for part in parts[1])

#             return p.number_to_words(number_str)
#         except:
#             return number_str

#     if not isinstance(text, str) or not text.strip():
#         return "emptytext"

#     text = text.lower()
#     text = re.sub(r'\d+\.\d+|\d+', lambda x: number_to_words(x.group()), text)
#     text = re.sub(r'http\S+', '', text)
#     text = re.sub(r'#\w+', '', text)
#     text = re.sub(r'@\w+', '', text)
#     text = re.sub(r'[^\w\s]', '', text)
#     return text if text.strip() else "defaulttext"

# def process_transcripts(base_path):
#     data = []
#     for root, dirs, files in os.walk(base_path):
#         for file in files:
#             if file.endswith('.txt'):
#                 file_path = os.path.join(root, file)
#                 video_id = file.split('.')[0]
#                 with open(file_path, 'r', encoding='latin-1') as f:
#                     content = f.read()
#                     cleaned_content = clean_text(content)
#                     #cleaned_content=content
#                     data.append((video_id, cleaned_content))

#     df = pd.DataFrame(data, columns=['Video_ID', 'Cleaned_Transcript'])
#     return df

# def create_chroma_db(documents, name):
#     chroma_client = chromadb.Client()
#     db = chroma_client.create_collection(name=name, embedding_function=GeminiEmbeddingFunction())

#     for i, d in enumerate(documents):
#         db.add(
#             documents=d,
#             ids=str(i)
#         )
#     return db

# def get_relevant_passages(query, db, num_results=5):
#     query_embedding = GeminiEmbeddingFunction()(query)
#     query_embedding = np.array(query_embedding)  # Convert to numpy array

#     results = db.query(query_texts=[query], n_results=num_results)
#     #results = db.query(query_embeddings=query_embedding,include=[ "embeddings" ], n_results=num_results,where={"metadata_field": "is_equal_to_this"}, where_document={"$contains":"search_string"}) #,where_document={"$contains":query}
#     #print(results['documents'])
#     documents = results['documents'][0] #['documents'][0]
#     return documents

# def make_prompt(query, relevant_passages):
#     combined_passages = ' '.join([passage.replace("'", "").replace('"', "").replace("\n", " ") for passage in relevant_passages])

#     prompt = (f"""You are a helpful and informative bot that answers questions using text from the reference passages included below.
#     Be sure to respond in a complete sentence, being comprehensive, including all relevant background information.
#     However, you are talking to a non-technical audience, so be sure to break down complicated concepts and use analogies where possible.
#     If the question is unclear or there are multiple possible interpretations, provide information for all interpretations or ask for clarification.
#     Question: {query}
#     Reference Passages: {combined_passages}""")

#     return prompt


# def query_result(query,db):
#     try:
#         passages = get_relevant_passages(query, db, num_results=2)
#         prompt = make_prompt(query, passages)
#         model = genai.GenerativeModel('gemini-pro')
#         answer = model.generate_content(prompt)
#         return answer.text
#     except Exception as e:
#         # Log the exception traceback for debugging
#         traceback.print_exc()
#         # Return a generic error message to the client
#         return "An error occurred while processing the query"

# dataset_path = './myproject//models//transcripts'
# df = process_transcripts(dataset_path)
# db = create_chroma_db(df['Cleaned_Transcript'], "transcript_new_transcripts")

# @app.route('/process_message', methods=['POST'])
# def process_message():
#     data = request.json
#     message = data.get('message') 
    
#     #exec(py_script)
#     #result,prompt = module.query_result(message)
#     #print(prompt)
   
#     #print(pd.DataFrame(db.peek(12)))
#     result = query_result(message,db)
#     #print(result)
#     # Process the message here (e.g., send to a model for response generation)
#     # For now, let's just acknowledge the message
#     return jsonify({"message": result})


# # @app.route('/users', methods=['GET'])
# # def get_users():
# #     users = users_collection.find()
# #     return jsonify(list(users)), 200

# # @app.route('/add', methods=['POST'])
# # def add():
# #     data = request.json
# #     numbers = data.get('numbers')
# #     if not numbers:
# #         return jsonify({"error": "Numbers are required"}), 400
# #     result = sum(numbers)
# #     return jsonify({"result": result}), 200

# # @app.route('/hello')
# # def hello():
# #     name = request.args.get('name')
# #     return f'Hello, {name}!'

# # @app.route('/static/<path:path>')
# # def static_file(path):
# #     return app.send_static_file(path)

# if __name__ == '__main__':
#     app.run(debug=True)


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

# app = Flask(_name_)

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
spec = importlib.util.spec_from_loader('_main_', loader=None)
module = importlib.util.module_from_spec(spec)
exec(py_script, module._dict_)
'''
import textwrap
import chromadb
import numpy as np
import pandas as pd

import google.generativeai as genai
import google.ai.generativelanguage as glm

import os
from IPython.display import Markdown
from chromadb import Documents, EmbeddingFunction, Embeddings
from openai import OpenAI
import logging



client = OpenAI(api_key="api_key")

def generate_embedding(text):
    try:
        response = client.embeddings.create(
            input=text,
            model="text-embedding-ada-002"
        )
        # Extracting the embedding from the response
        embedding = response.data[0].embedding
        return embedding
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def initialize_chroma_db_connection():
    client = chromadb.Client()
    return client

def chunk_text(text, max_tokens=1000):
    """
    Splits text into chunks where each chunk has a maximum number of tokens.
    """
    words = text.split()
    chunks = []
    current_chunk = []
    current_token_count = 0
    
    for word in words:
        word_token_count = 1 
        if current_token_count + word_token_count > max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_token_count = word_token_count
        else:
            current_chunk.append(word)
            current_token_count += word_token_count
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def add_document_to_chroma_db(document_text, embedding, db, collection_name="documents"):
    try:
        if collection_name not in db.list_collections():
            db.create_collection(name=collection_name)
    except:
    # except UniqueConstraintError:
        # If the collection already exists, we ignore the error and proceed
        pass

    collection = db.get_collection(collection_name)
    
    # Generate a unique ID for the document
    document_id = generate_unique_id_for_document(document_text)
    
    # Add the document to the collection with the correct parameters
    collection.add(
        ids=[document_id],  # list of unique identifiers
        embeddings=[embedding],  # list of embeddings
        documents=[document_text]  # list of document texts
    )

def generate_unique_id_for_document(document_text):
    return str(hash(document_text))

def retrieve_relevant_passages(query, db, num_results=4, collection_name="documents"):
    collection = db.get_collection(collection_name)
    # using same embedding generator as we did for the transcripts
    query_embedding = generate_embedding(query) 
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=num_results
    )
    
    return [result for result in results['documents']]

def process_and_store_documents(base_path, db):
    file_count = 1
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='latin-1') as f:
                    print(f"Processing file {file_count}")
                    # console.log("Processing file {file_count}")
                    content = f.read()
                    chunks = chunk_text(content)
                    for chunk in chunks:
                        embedding = generate_embedding(chunk)
                        add_document_to_chroma_db(chunk, embedding, db)
                    file_count += 1

def query_with_gpt4(query, context_chunks):
    # prompt = f"Answer the following question based on the provided context: {query}\n\nContext: {' '.join(context_chunks)}"
    prompt_instructions = """
    You are a helpful and informative bot that answers questions primarily using information from the reference passages provided. 
    Please note that the reference passages might have some typos and incorrect grammar. 
    Focus on the information provided in the reference passages, but when needed, you can use your own knowledge too. 
    Your audience may be non-technical, so try to break down complicated concepts and use analogies where possible. 
    In your answer, do not mention referring to any passages or a database.
    If the question is unclear or there are multiple possible interpretations, ask the user for clarification.
    """

    context_chunks = [str(chunk) for chunk in context_chunks]
    context_chunks_string = ' '.join(context_chunks)

    completion = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": prompt_instructions},
        {"role": "user", "content": f"Query: {query}\n\nReference Passages: {context_chunks_string}"}
    ]
    )
    return completion.choices[0].message.content




# dataset_path = './myproject//models//transcripts'
# df = process_transcripts(dataset_path)
# db = create_chroma_db(df['Cleaned_Transcript'], "transcript_new_transcripts")

dataset_path = './/models//transcripts'

db = initialize_chroma_db_connection()

# setting logging level to WARNING only to not be bombarded with informational messages
logging.basicConfig(level=logging.WARNING)

process_and_store_documents(dataset_path, db)


@app.route('/process_message', methods=['POST'])
def process_message():
    data = request.json
    message = data.get('message') 
    
    #exec(py_script)
    #result,prompt = module.query_result(message)
    #print(prompt)
   
    #print(pd.DataFrame(db.peek(12)))
    relevant_passages = retrieve_relevant_passages(message, db, num_results=4)
    result = query_with_gpt4(message, relevant_passages)
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