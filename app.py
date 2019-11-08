from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS, cross_origin
import csv
import json
import os.path
import hashlib
import secrets
from utils.task1 import *
from utils.task2 import *

ACTUALPASSWORDS = "csv_files/savedPasswords.csv"
ACTUALHASHES = "csv_files/savedHashes.csv"
DICTIONARY = "csv_files/dictionary.csv"
REPLACEMENT = "csv_files/replacement.csv"
PASSWORDSLIST = "csv_files/passwords_list.csv"
dictionaryList = []
replacementList = []

app = Flask(__name__)
CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


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


@app.route("/task2/<info>")
def task2List(info):
    words = dotask2(info)
    return jsonify(words=words)


@app.route("/task3")
def task3():
    return send_from_directory(".", "client/task3.html")


# Send using:
# var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
# var theUrl = "/task3/savepass";
# xmlhttp.open("POST", theUrl);
# xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
# xmlhttp.send(JSON.stringify({ "username": "username", "password": "password" }));


@app.route("/task3/savepass")
def savePass():
    try:
        body = json.loads(request.data)
        username = body["username"]
        password = body["password"]
        hashed = secrets.token_hex(8)
        saltedPassword = password + hashed
        password = hashlib.sha224(bytes(saltedPassword, "utf-8")).hexdigest()

        with open(ACTUALPASSWORDS, "a") as csvfile:
            fieldnames = ["username", "password"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({"username": username, "password": password})

        with open(ACTUALHASHES, "a") as csvfile:
            fieldnames = ["username", "hashes"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({"username": username, "hashes": hashed})

        return jsonify({"acknowledged": "true"})
    except:
        print("Saving password to a file failed")
        return jsonify({"acknowledged": "false"})


def initPasswordList():
    if not os.path.exists(ACTUALPASSWORDS):
        with open(ACTUALPASSWORDS, "a") as csvfile:
            fieldnames = ["username", "password"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    if not os.path.exists(ACTUALHASHES):
        with open(ACTUALHASHES, "a") as csvfile:
            fieldnames = ["username", "hashes"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()


def parseDictCsv():
    global dictionaryList
    dictionaryList = []
    with open(DICTIONARY, mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            dictionaryList.append(row["word"])
    print(dictionaryList)


def parseReplacementCsv():
    global replacementList
    replacementList = []
    with open(REPLACEMENT, mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            replacementList.append(
                {"original": row["original"], "modified": row["modified"]}
            )


def createListOfPasswords():
    global dictionaryList
    with open(PASSWORDSLIST, mode="w") as passwords_list:
        passwords_writer = csv.DictWriter(passwords_list, ["word"])
        passwords_writer.writeheader()
        wordList = []
        for word in dictionaryList:
            wordList.extend(generateListDouble(word))
            wordList.extend(generateListTriple(word))
        for word in wordList:
            passwords_writer.writerow({"word": word})


if __name__ == "__main__":
    parseDictCsv()
    parseReplacementCsv()
    initPasswordList()
    createListOfPasswords()
    app.run(debug=True)

