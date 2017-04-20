#Main program to handle persistence for NavUP Users Module
#Author: Drew Langley 11039753 COS 301 Broadsword-Users

import sys
import nsq
import json
import tornado.ioloop

URI = "localhost:27017"

from pymongo import MongoClient

client = MongoClient(URI)
db = client.userDB

def requestHandler(message):

        obj = json.loads(message.body.decode('utf-8'))
        message.enable_async()
        if obj['dest'] == 'users':

            query = obj['queryType']

            if query == 'insert':
                insertOne(obj['content']['fname'], obj['content']['sname'], obj['content']['email'], obj['content']['password'], obj['content']['stud_num'], obj['content']['phone'])
                request="""{
                        "src"  : "users",
                        "dest" : "notification",
                        "msgType" : "request",
                        "queryType" : "insert",
                        "content" : {
                                        "email" : "obj['content']['email']",
                                    }
                }""";

                def pub_message():
                     writer.pub('notifications',request.encode('utf-8'), finish_pub)

                def finish_pub(conn, data):
                    #print(data)
                    tornado.ioloop.IOLoop.current().stop()


                writer = nsq.Writer(['127.0.0.1:4150'])
                tornado.ioloop.PeriodicCallback(pub_message,1000).start()
                nsq.run()

            elif query == 'update':
                update(obj['content']['update'], obj['content']['fname'], obj['content']['sname'], obj['content']['email'], obj['content']['password'], obj['content']['stud_num'], obj['content']['phone'])

            elif query == 'delete':
                delete(obj['content']['to_delete'])

            elif query == 'read':
                read()

            elif query == 'make_admin':
                makeAdmin(obj['content']['makeAdmin'])

            elif query == 'get_user':
                getUser(obj['content']['toGet'])

            elif query == 'log_in':
                log_in(obj['content']['log_in'], obj['content']['password'])


######################################### Function to insert data into mongo db#######################################
def insertOne(UserName, UserSurname, Email, Password, StudentNumber, Phone):
        if getUser(StudentNumber):
            print('StudentNumber already exists!')

        else:
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


##################################### Function to update record to mongo db #############################################
def update(toUpdate, Username, UserSurname, Email, Password, StudentNumber, Phone):
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


############################################ function to read records from mongo db###################################################
def read():
        numCols = db.userDB.find()
        print('\n ************* All data from users Database ****************\n')
        for nums in numCols:
            print(nums)


################################################ Function to delete record from mongo db##############################################
def delete(toDelete):
        db.userDB.delete_many({"StudentNumber":toDelete})
        print('\nDeletion successful\n')


############################################### Function for getUser from mongo db ######################################################
def getUser(toGet):
        if(db.userDB.find_one({"StudentNumber":toGet})):
            print(db.userDB.find_one({"StudentNumber":toGet}))
            return True

        else:
            #print("User does not exist")
            return False

############################################ Function to set user as an Admin ###############################################################
def makeAdmin(UserName):
        user = db.userDB.find_one({"StudentNumber":UserName})
        if(user["StudentNumber"] == UserName):
            print('User does not exist')

        else:
            db.userDB.update_one(
                {"StudentNumber": UserName},
                {
                    "$set": {
                        "isAdmin":True
                            }
                }
                )
            print("\nRecords updated successfully\n")

def log_in(UserName, Password):
        user = db.userDB.find_one({"StudentNumber":UserName})
        if(user["StudentNumber"] == UserName):
            if(user["Password"] == Password):
                db.userDB.update_one(
                    {"StudentNumber": UserName},
                    {
                        "$set": {
                            "isAuthenticated":True
                                }
                    }
                    )
            else:
                print('Log In failed')

########################################################################################################

r = nsq.Reader(message_handler=requestHandler, lookupd_http_addresses=['http://127.0.0.1:4161'], topic='users', channel='navup', lookupd_poll_interval=5)
nsq.run()
