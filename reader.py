#Main program to handle persistence for NavUP Users Module
#Author: Drew Langley 11039753 COS 301 Broadsword-Users

import sys
import nsq
import json

uri = "localhost:27017"

from pymongo import MongoClient

client = MongoClient(uri)
db = client.userDB

def requestHandler(message):

        #response = message.body.decode('utf-8')
        #string = response.readall().decode('utf-8')
        print(message.body)
        obj = json.loads(message.body.decode('utf-8'))
        #message.enable_async()
        if obj['dest'] == 'users':

            query = obj['queryType']

            if query == 'insert':
                name = obj['content']['fname']
                lName = obj['content']['sname']
                sNumber = obj['content']['stud_num']
                email = obj['content']['email']
                password = obj['content']['password']
                phone = obj['content']['phone']

                insertOne(name, lName, email, password, sNumber, phone)


            elif query == 'update':
                toUpdate = obj['content']['update']
                name = obj['content']['fname']
                lName = obj['content']['sname']
                sNumber = obj['content']['stud_num']
                email = obj['content']['email']
                password = obj['content']['password']
                phone = obj['content']['phone']
                update(toUpdate, name, lName, email, password, sNumber, phone)

            elif query == 'delete':
                toDelete = obj['content']['to_delete']
                update(toDelete)

            elif query == 'read':
                read()

            elif query == 'get_user':
                toGet = obj['content']['toGet']
                getUser(toGet)

            else:
                print(message.body)

######################################### Function to insert data into mongo db#######################################
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


r = nsq.Reader(message_handler=requestHandler, lookupd_http_addresses=['http://127.0.0.1:4161'], topic='users', channel='navup', lookupd_poll_interval=15)
nsq.run()
