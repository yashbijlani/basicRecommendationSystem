from flask import Flask, jsonify
from flask_cors import CORS
import csv
from math import sqrt

app = Flask(__name__)
CORS(app)

def similarity(points):
    dist = 0
    for i in range(len(points[0])):
        dist += (points[0][i] - points[1][i]) ** 2
    return sqrt(dist)

def controversy(vote):
    return 12 * abs(vote[0] - vote[1]) / (vote[0] + vote[1])

with open('all_unique.csv', mode='r') as file:
    csvFile = csv.reader(file)
    data = list(csvFile)

data = data[1:1201]
votes = [(int(val[1]), int(val[3])) for val in data]

y = [controversy(vote) for vote in votes]
x = [item for sublist in ([i] * 6 for i in range(int(len(data) / 6))) for item in sublist]

Ques = 356

def nextQuestion(currX, currY, userRating):
    global Ques
    currVote = votes[currY]
    distances = []
    loc = currX
    for v in range(loc - 6, loc + 13):
        if votes[v] != currVote:
            distances.append(similarity((currVote, votes[v])))
    if userRating:
        nextQuestion = loc - 6 + distances.index(min(distances))
    else:
        nextQuestion = loc - 6 + distances.index(max(distances))
    votes.pop(loc)
    data.pop(loc)
    x.pop(loc)
    y.pop(loc)
    Ques = nextQuestion
    return Ques

def wouldYouRather():
    global Ques
    #question = f"Would you rather {data[Ques][0]} or {data[Ques][2]}?"
    Ques = nextQuestion(Ques, Ques, 0)
    return str(data[Ques][0]),  str(data[Ques][2])

@app.route('/get_string', methods=['GET'])
def get_string():
    ques1, ques2 = wouldYouRather()
    return jsonify({"ques1": ques1, "ques2": ques2})

if __name__ == '__main__':
    app.run(debug=True)
