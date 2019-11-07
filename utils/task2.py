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

def dotask2(val):
    values = val.split(',')
    remove_indices = []
    # first = values[0]
    # last = values[1]
    birth = values[2]
    print('birth:', birth)
    birthArr = birth.split('-')
    remove_indices.append(2)
    phone = values[3]
    phoneArr = phone.split('-')
    if len(phoneArr) >= 3:
        phoneArr.append(phoneArr[-2] + phoneArr[-1]) #Last 6 digits
    remove_indices.append(3)
    street = values[4]
    streetArr = street.split(' ')
    remove_indices.append(4)
    # apt = values[5]
    # city = values[6]
    # state = values[7]
    # zipcode = values[8]
    email = values[9]
    emailArr = email.split('@')[0]
    emailArr = emailArr.split('_')
    remove_indices.append(9)
    values = [i for j, i in enumerate(values) if j not in remove_indices]
    for arr in [birthArr, phoneArr, streetArr, emailArr]:
        values.extend(arr)
    parseReplacementCsv()
    tempArr = []
    for value in values:
        for rep in replacementList:
            tempArr.append(value.replace(rep["original"], rep["modified"]))
            break
    values.extend(tempArr)
    perm_iterator = combinations(values, 2)
    wordList = []
    with open(PASSWORDSLIST2, mode="w") as passwords_list:
        passwords_writer = csv.DictWriter(passwords_list, ["word"])
        passwords_writer.writeheader()
        # wordList = []
        for word in perm_iterator:
            password = word[0] + word[1]
            passwords_writer.writerow({"word": password})
            wordList.append(password)
            password = word[1] + word[0]
            passwords_writer.writerow({"word": password})
            wordList.append(password)
    return wordList