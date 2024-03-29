from flask import Flask, request, send_from_directory, jsonify, render_template
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
ELCP2 = "csv_files/ELCP2.csv"
dictionaryList = []
replacementList = []

app = Flask(__name__)
CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return send_from_directory(".", "client/404.html"), 404


@app.route("/favicon.ico")
def favicon():
    return send_from_directory("media", "favicon.ico")


@app.route("/")
def home():
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


@app.route("/task2/<info>")
def task2List(info):
    words = dotask2(info)
    return jsonify(words=words)


@app.route("/task3")
def task3():
    return send_from_directory(".", "client/task3.html")


@app.route("/task3/validpass", methods=["POST"])
def validPass():
    body = json.loads(request.data)
    password = body["password"]
    info = body["info"]
    infoString = ",".join(map(str, info))
    infoVars = dotask2(infoString)
    for x in infoVars:
        if password == x:
            return jsonify(
                {"valid": "false", "error": "Password contains personal information"}
            )

    dictVars = []
    with open(PASSWORDSLIST, mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            dictVars.append(row["word"])

    for x in dictVars:
        if password == x:
            return jsonify(
                {
                    "valid": "false",
                    "error": "Password contains a common dictionary word",
                }
            )

    dictVars1 = []
    with open(ELCP2, mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            dictVars1.append(row["word"])

    for x in dictVars1:
        if password == x:
            return jsonify(
                {
                    "valid": "false",
                    "error": "Password contains a common dictionary word",
                }
            )

    return jsonify({"valid": "true"})


@app.route("/task3/login")
def task3Login():
    return send_from_directory(".", "client/task3Login.html")


@app.route("/task3/savepass", methods=["POST"])
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


@app.route("/task3/checkpass", methods=["POST"])
def checkPass():
    body = json.loads(request.data)
    requestUsername = body["username"]
    requestPassword = body["password"]
    username = ""
    password = ""
    salt = ""
    with open(ACTUALPASSWORDS, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["username"] == requestUsername:
                username = requestUsername
                password = row["password"]  # this is the set password
    with open(ACTUALHASHES, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["username"] == requestUsername:
                salt = row["hashes"]
    if salt != "" and password != "" and username != "":
        hashedPass = hashlib.sha224(bytes(requestPassword + salt, "utf-8")).hexdigest()
        if hashedPass == password:
            return jsonify({"acknowledged": "true"})
    return jsonify({"acknowledged": "false", "error": "Incorrect username or password"})


@app.route("/task3/getpass")
def getpass():
    with open(ACTUALPASSWORDS, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        d = {}
        for row in reader:
            d[row["username"]] = row["password"]
    return d


@app.route("/task3/getsigninpass", methods=["POST"])
def getSignInPass():
    try:
        body = json.loads(request.data)
        username = body["username"]
        password = body["password"]

        with open(ACTUALHASHES, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                d[row["username"]] = row["hashed"]
                if row["username"] == username:
                    hashed = row["hashed"]
                    saltedPassword = password + hashed
                    return hashlib.sha224(bytes(saltedPassword, "utf-8")).hexdigest()
    except:
        print("Getting sign in hash failed")
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

