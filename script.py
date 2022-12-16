from flask import Flask, render_template, request

import pymongo
import mongoUrl

import certifi
import random

app = Flask(__name__)      # initializing the Flask

myclient = pymongo.MongoClient(mongoUrl.Url, tlsCAFile=certifi.where())
mydb = myclient['Feedback']
mycollection = mydb['feedback']

# @app.route('/',  methods=[ 'GET', 'POST' ])     # creating routes
# def home():
#     if request.method == 'POST':
#         new_feedback = request.form['feedback']
#         return render_template('index.html', feedback = new_feedback)
#     return render_template('index.html')


@app.route('/',  methods=[ 'GET', 'POST' ])     # creating routes
def home():
    if request.method == 'POST':
        if request.form['feedback'] == '':
            return render_template('index.html', feedback = show_random_feedback())
        else:
            create_new_feedback(request.form['feedback'])
            return render_template('index.html', feedback = show_random_feedback())
    else:
        return render_template('index.html', feedback = show_random_feedback())

def show_random_feedback():
    collection_list = (list(mycollection.find()))
    random_feedback = random.choice(collection_list)['feedback']
    return random_feedback


def create_new_feedback(feedback):
    # insert
    new_feedback = {
        # '_id': 1,
        'feedback': feedback
    }
    mycollection.insert_one(new_feedback)
    # for inserting many at a same time 
    # mycollection.insert_many([new_feedback1, new_feedback2])

# def update_feedback():
#     mycollection.update_one({'id': 3}, {'$set':{'feedback': 'New Feedback'}})


def read_feedback():
    # read
    for i in mycollection.find():
        print(i['feedback'])
    # print(mycollection.find_one())    #for returning only first item in collection


if __name__ == '__main__':
    app.run(debug=True, port=5000)

