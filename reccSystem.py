import csv
from math import sqrt
import matplotlib.pyplot as plt

def similarity(points):
  dist =0
  for i in range(len(points[0])):
    dist+=(points[0][i]-points[1][i])**2
  return sqrt(dist)
 
def controversy(vote):
    return 12*abs(vote[0]-vote[1])/(vote[0]+vote[1]) #not to microoptimize, but I think (vote[0]+vote[1]) is faster than sum(vote)


with open('all_unique.csv', mode ='r')as file:
  csvFile = csv.reader(file)
  data = list(csvFile)
data = data [1:1201]
votes = [(int(val[1]), int(val[3])) for val in data]

y = [controversy(vote) for vote in votes]
x = [item for sublist in ([i]*6 for i in range(int(len(data)/6))) for item in sublist]

def nextQuestion(currX, currY, userRating): #userRating is boolean
  currVote = votes[currY]
  distances = []
  loc = currX      #we need this a lot so might as well create a variable
  for v in range(loc-6, loc+13):  #I am aware of the edgecases...
      if votes[v]!=currVote:
        distances.append(similarity((currVote, votes[v])))
  if(userRating):
    nextQuestion = loc-6+distances.index(min(distances))
  else:
    nextQuestion = loc-6+distances.index(max(distances))  #if user doesn't like, pick the least similar
  votes.pop(loc)  #removing the last question to not ask it again
  data.pop(loc)
  x.pop(loc)
  y.pop(loc)
  return nextQuestion

Ques = 356
def wouldYouRather():
  print("Would you rather ", data[Ques][0], " or ", data[Ques][2], "?")
  Ques = nextQuestion(Ques, Ques, 0)

