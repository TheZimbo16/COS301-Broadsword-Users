import csv

uri = "localhost:27017"

from pymongo import MongoClient

client = MongoClient(uri)
db = client.userDB

def insertOne(UserName, UserSurname, Email, Password, StudentNumber, Phone):
    try:

        db.userDB.insert_one(
        {
            "Name":UserName,
            "Surname":UserSurname,
            "Email":Email,
            "Password": Password,
            "StudentNumber":StudentNumber,
            "Phone":Phone,
            "isAuthenticated": False,
            "isAdmin":False
        })
        print('\nInserted data successfully\n')

    except Exception:
        print(Exception)


with open('names.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')

    for row in reader:
        print(row[0], row[1], row[2],row[3], row[4], row[5])
        insertOne(row[0], row[1], row[2],row[3], row[4], row[5])
