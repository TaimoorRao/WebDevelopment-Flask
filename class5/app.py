
from flask_pymongo import PyMongo
import bcrypt
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


app.config['MONGO_URI'] = 'mongodb+srv://dbFlask:Flask@cluster0-4gro5.mongodb.net/test?retryWrites=true&w=majority'

mongo = PyMongo(app)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/home')
def home():
    return "Hello from Home Page"


@app.route('/signupAuth', methods=["POST"])
def signupAuth():
    data = dict(request.form)
    print(data)
    usersData = mongo.db.usersData
    result = usersData.find_one({"email": data['email'][0]})
    print(result)
    if(result):
        return redirect('/signup')
    # for i in result:
    #     print(i)

    bcrypt_password = bcrypt.hashpw(
        data['password'][0].encode('utf8'), bcrypt.gensalt(12))
    data['password'] = bcrypt_password
    data['email'] = data['email'][0]
    data['userName'] = data['userName'][0]
    usersData.insert_one(data)
    return redirect('/login')


@app.route('/loginAuth', methods=["POST"])
def loginAuth():
    data = dict(request.form)

    usersData = mongo.db.usersData

    findEmail = usersData.find_one({"email": data["email"]})

    print(findEmail)
    if(findEmail):

        check_password = bcrypt.checkpw(
            data['password'].encode('utf8'), findEmail['password'])

        if(check_password):

            return redirect('/home')

        return redirect('/login')

    return redirect('/login')


@app.route('/auth', methods=["POST"])
def auth():
    data = request.form
    for i, v in enumerate(users):
        if(data['userName'] == v['name'] and data['password'] == v['password']):
            print(i)
            return redirect('/home')
    return redirect('/login')


if __name__ == "__main__":
    app.run(debug=True, port=5000)
