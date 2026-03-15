from unittest import result

from flask import Flask, render_template, request
import os
import json
import pymongo
from dotenv import load_dotenv



load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')
client = pymongo.MongoClient(MONGO_URI)
db=client.test
collection=db['flask-tutorial-assignment']
print("Mongo URI:", MONGO_URI)

app = Flask(__name__)
@app.route('/api', methods=['GET'])
def view():
  with open('data.json', 'r') as f:
    data = json.load(f)
  return data

@app.route('/home')
def home():
    return render_template('signup.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    name=request.values.get('fullname')
    form_data=dict(request.form)
    collection.insert_one(form_data)
    return "Data submitted successfully"
@app.route('/todo', methods=['POST', 'GET'])
def todo():
	form_data=dict(request.form)
	return render_template('todo.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	return render_template('login.html')

@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():

    data = request.get_json()
    print("Received data:", data)

    todo_data = {
        "itemName": data.get("itemName"),
        "itemDescription": data.get("itemDescription"),
        "itemID": data.get("itemID"),
        "itemUUID": data.get("itemUUID"),
        "itemHash": data.get("itemHash")
    }

    result = collection.insert_one(todo_data)
    print("Mongo URI:", MONGO_URI) 
    print("Inserted ID:", result.inserted_id)

    return {"message": "Todo stored successfully"}


if __name__ == '__main__':
    app.run(debug=True)
