import csv
from itertools import combinations 

DICTIONARY = "csv_files/dictionary.csv"
REPLACEMENT = "csv_files/replacement.csv"
PASSWORDSLIST2 = "csv_files/ELCP2.csv"
dictionaryList = []
replacementList = []
SYMBOLS = [
    "!",
    "@",
    "#",
    "$",
    "%",
    "^",
    "&",
    "*",
    "(",
    ")",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
]


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


def double(string):
    return string + string


def triple(string):
    return string + string + string


def reverseWord(string):
    return string[::-1]


def capitalize(string):
    return string.capitalize()


def secondToLast(string, char):
    return string[: len(string) - 1] + char + string[-1:]


def addToLast(string, char):
    return string + char


def generateListDouble(word):
    words = [word]
    words.append(double(word))

    tempArr = []
    for word in words:
        tempArr.append(reverseWord(word))
    words.extend(tempArr)

    tempArr = []
    for word in words:
        tempArr.append(capitalize(word))
    words.extend(tempArr)

    tempArr = []
    for word in words:
        for rep in replacementList:
            tempArr.append(word.replace(rep["original"], rep["modified"]))
            break
    words.extend(tempArr)

    tempArr = []
    for word in words:
        for symbol in SYMBOLS:
            tempArr.append(secondToLast(word, symbol))
            tempArr.append(addToLast(word, symbol))
    words.extend(tempArr)

    return words


def generateListTriple(word):
    words = [word]
    words.append(triple(word))

    tempArr = []
    for word in words:
        tempArr.append(reverseWord(word))
    words.extend(tempArr)

    tempArr = []
    for word in words:
        tempArr.append(capitalize(word))
    words.extend(tempArr)

    tempArr = []
    for word in words:
        for rep in replacementList:
            tempArr.append(word.replace(rep["original"], rep["modified"]))
            break
    words.extend(tempArr)

    tempArr = []
    for word in words:
        for symbol in SYMBOLS:
            tempArr.append(secondToLast(word, symbol))
            tempArr.append(addToLast(word, symbol))
    words.extend(tempArr)

    return words


def createListOfPasswords():
    global dictionaryList
    with open(PASSWORDSLIST2, mode="w") as passwords_list:
        passwords_writer = csv.DictWriter(passwords_list, ["word"])
        passwords_writer.writeheader()
        wordList = []
        for word in dictionaryList:
            wordList.extend(generateListDouble(word))
            wordList.extend(generateListTriple(word))
        for word in wordList:
            passwords_writer.writerow({"word": word})

def test(val):
    values = val.split(',')
    # first = values[0]
    # last = values[1]
    # birth = values[2]
    # phone = values[3]
    # street = values[4]
    # apt = values[5]
    # city = values[6]
    # state = values[7]
    # zipcode = values[8]
    parseReplacementCsv()
    tempArr = []
    for value in values:
        for rep in replacementList:
            tempArr.append(value.replace(rep["original"], rep["modified"]))
            break
    values.extend(tempArr)
    perm_iterator = combinations(values, 2)
    with open(PASSWORDSLIST2, mode="w") as passwords_list:
        passwords_writer = csv.DictWriter(passwords_list, ["word"])
        passwords_writer.writeheader()
        # wordList = []
        for word in perm_iterator:
            password = word[0] + word[1]
            passwords_writer.writerow({"word": password})
    return 