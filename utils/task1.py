import csv

DICTIONARY = "csv_files/dictionary.csv"
REPLACEMENT = "csv_files/replacement.csv"
PASSWORDSLIST = "csv_files/passwords_list.csv"
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

