from flask import Flask, render_template, request, jsonify
import os
import pymongo
from dotenv import load_dotenv

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')

if not MONGO_URI:
    raise Exception("MONGO_URI not set in .env")

# -----------------------------
# MongoDB setup
# -----------------------------
client = pymongo.MongoClient(MONGO_URI)
db = client.test
collection = db['flask-tutorial-assignment']

# -----------------------------
# Flask app
# -----------------------------
app = Flask(__name__)

# -----------------------------
# Routes
# -----------------------------
@app.route('/')
@app.route('/home')
def home():
    return render_template('signup.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form_data = dict(request.form)
    collection.insert_one(form_data)
    return "Data submitted successfully"

@app.route('/todo', methods=['GET'])
def todo():
    return render_template('todo.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    data = request.get_json()
    todo_data = {
        "itemName": data.get("itemName"),
        "itemDescription": data.get("itemDescription"),
        "itemID": data.get("itemID"),
        "itemUUID": data.get("itemUUID"),
        "itemHash": data.get("itemHash")
    }
    collection.insert_one(todo_data)
    return jsonify({"message": "Todo stored successfully"})

@app.route('/api', methods=['GET'])
def view():
    todos = list(collection.find({}, {"_id": 0}))
    return jsonify(todos)

# -----------------------------
# Run Flask
# -----------------------------
if __name__ == '__main__':
    print(f"Mongo URI: {os.getenv('MONGO_URI')}")
    app.run(host='0.0.0.0', port=5000, debug=True)
