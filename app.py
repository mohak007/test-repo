from flask import Flask, request,render_template
from datetime import datetime
from dotenv import load_dotenv
import os
import pymongo

load_dotenv()
MONGO_URI=os.getenv('MONGO_URI')

client = pymongo.MongoClient(MONGO_URI)
db=client.test

collection = db['flask-tutorial']

app=Flask(__name__)
@app.route('/first')
def home():
	return 'hello guys'

@app.route('/second')
def second():
	return 'welcome to second page'

@app.route('/third')
def third():
	return 'third page'

@app.route('/api')
def name():
	name= request.values.get('name')
	age=request.values.get('age')
	age=int(age)
	if(age>30):
		return {'name':name, 'age':age}
	else:
		return {"message":"sorry"}
@app.route('/')
def signup():
	day_of_week=datetime.today().strftime('%A')
	print(day_of_week)
	return render_template('signup.html', day_of_week=day_of_week)

@app.route('/signup', methods=['POST', 'GET'] )
def submit():
	#name=request.form.get('fullname')
	form_data=dict(request.form)
	collection.insert_one(form_data)
	return "data submited successfully"

@app.route('/view')
def view():
	data=collection.find()
	print(data)
	data = list(data)
	for i in data:
		print (i)
		del i['_id']
	data = {
		'data':data
	}
	return data

if __name__=='__main__':
	app.run()
