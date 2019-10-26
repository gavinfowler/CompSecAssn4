from flask import Flask,request,send_from_directory
import itertools
from flask_cors import CORS, cross_origin
import csv
import copy

DICTIONARY = 'dictionary.csv'
dictionaryList = []
REPLACEMENT = 'replacement.csv'
replacementList = []
SYMBOLS = ['!','@','#','$','%','^','&','*','(',')']

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def home():
    parseDictCsv()
    return send_from_directory('.', 'client/index.html')

@app.route("/task1")
def task1():
    return send_from_directory('.', 'client/task1.html')

@app.route("/task1/<word>")
def task1List(word):
    return word

@app.route("/task2")
def task2():
    return send_from_directory('.', 'client/task2.html')

@app.route("/task3")
def task3():
    return send_from_directory('.', 'client/task3.html')

def parseDictCsv():
    global dictionaryList
    dictionaryList = []
    with open(DICTIONARY, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            dictionaryList.append(row["word"])

def parseReplacementCsv():
    global replacementList
    replacementList = []
    with open(REPLACEMENT, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            replacementList.append({
                'original': row['original'],
                'modified': row['modified'],
            })

# reverse list: 'this is a test'[::-1]
# double: 'cat' + 'cat'
# triple: 'cat' + 'cat' + 'cat'
# capitalize: 'this'.capitalize()
def double(string):
    return string + string

def triple(string):
    return string + string + string

def capitalize(string):
    return string.capitalize()

def secondToLast(string, char):
    return string[:len(string)-1] + char + string[-1:]

def addToLast(string,char):
    return string + char

if __name__ == "__main__":
    parseDictCsv()
    parseReplacementCsv()
    app.run(debug=True)