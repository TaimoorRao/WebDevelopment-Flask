from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

from pymongo import ReturnDocument
app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://dbFlask:Flask@cluster0-4gro5.mongodb.net/test?retryWrites=true&w=majority'

mongo = PyMongo(app)


@app.route('/')
def index():
    return "Hello"


@app.route('/updateName', methods=["POST"])
def updateName():
    data = request.json
    usersData = mongo.db.usersData
    result = usersData.find_one_and_update({"email": data['email']}, {
                                           "$set": {"userName": data['userName']}}, return_document=ReturnDocument.AFTER)
    print(result)
    return "Done"


@app.route('/daleteName', methods=["POST"])
def deleteName():
    data = request.json
    usersData = mongo.db.usersData
    print(data)
    result = usersData.find_one_and_delete({"email": data['email']})
    print(result)
    return "Done"


app.run(debug=True)
