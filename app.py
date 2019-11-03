from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS, cross_origin
import csv
from utils.task1 import *


app = Flask(__name__)
CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@app.route("/")
def home():
    parseDictCsv()
    return send_from_directory(".", "client/index.html")


@app.route("/task1")
def task1():
    return send_from_directory(".", "client/task1.html")


@app.route("/task1/<word>")
def task1List(word):
    wordList = []
    wordList.extend(generateListDouble(word))
    wordList.extend(generateListTriple(word))
    return jsonify(words=wordList)


@app.route("/task2")
def task2():
    return send_from_directory(".", "client/task2.html")


@app.route("/task3")
def task3():
    return send_from_directory(".", "client/task3.html")


if __name__ == "__main__":
    parseDictCsv()
    parseReplacementCsv()
    createListOfPasswords()
    app.run(debug=True)
