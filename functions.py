#Persistence to user database - functions for NavUP Users Module
#Author: Drew Langley 11039753 COS 301 Broadsword-Users
#Assumes mongo instance running at the specified URI
#and uses the Database name userDB, with the collection name userDB.
import sys
uri = "localhost:27017"

from pymongo import MongoClient

client = MongoClient(uri)
db = client.userDB

######################################### Function to insert data into mongo db#######################################
def insertOne(Username, UserSurname, Email, Password, StudentNumber, Phone):
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

##################################### Function to update record to mongo db #############################################
def update(toUpdate, Username, UserSurname, Email, Password, StudentNumber, Phone):
    try:
        db.userDB.update_one(
            {"StudentNumber": toUpdate},
            {
                "$set": {
                    "Name":Username,
                    "Surname":UserSurname,
                    "Email":Email,
                    "Password":Password,
                    "StudentNumber":StudentNumber,
                    "Phone":Phone
                        }
            }
            )
        print("\nRecords updated successfully\n")

    except Exception:
        print(Exception)

############################################ function to read records from mongo db###################################################
def read():
    try:
        numCols = db.userDB.find()
        print('\n All data from users Database \n')
        for nums in numCols:
            print(nums)

    except Exception:
        print(Exception)

################################################ Function to delete record from mongo db##############################################
def delete(toDelete):
    try:
        criteria = toDelete
        db.userDB.delete_many({"StudentNumber":criteria})
        print('\nDeletion successful\n')

    except Exception:
        print(Exception)

############################################### Function for getUser frtom mongo db ######################################################
def getUser(toGet):
    try:
        criteria = toGet
        user = db.userDB.find_one({"StudentNumber": criteria})
        print(user)

    except Exception:
        print(Exception)
