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

if __name__ == '__main__':
    app.run(debug=True)
