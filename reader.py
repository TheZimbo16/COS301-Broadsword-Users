#Main program to handle persistence for NavUP Users Module
#Author: Drew Langley 11039753 COS 301 Broadsword-Users

import sys


import nsq
import json

uri = "localhost:27017"

from pymongo import MongoClient

client = MongoClient(uri)
db = client.userDB

    
def insertOne(Username, UserSurname, Email, Password, StudentNumber, Phone):
    try:

        db.userDB.insert_one(
        {
            "Name":Username,
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
        print("hi bra")

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

def requestHandler(message):
	
	message.enable_async()	
        obj = json.loads(message.body)
		
        if obj['dest'] == 'user':
			
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
				print ("")
                

    

	
r = nsq.Reader(message_handler=requestHandler, lookupd_http_addresses=['http://127.0.0.1:4161'], topic='user', channel='navup', max_in_flight=9)
nsq.run()
