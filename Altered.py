#Persistence to user database - mockup 
#Author: Drew Langley 11039753 COS 301 Broadsword-Users 
#Assumes mongo instance running at the specified URI 
#and uses the Database name userDB, with the collection name userDB. 
import sys 
uri = "localhost:27017" 


from pymongo import MongoClient 

 
client = MongoClient(uri) 
db = client.userDB 

######################################### Function to insert data into mongo db####################################### 
def insert(Username, UserSurname, StudentNumber, Email, PhoneNumber): 
    try: 
        #_id = input('Enter Employee id :') 
        #UserName = input('Enter Name :') 
        #UserSurname = input('Enter Surname :') 
        #StudentNumber = input('Enter Student Number :') 

 
        db.userDB.insert_one( 
        { 
            #"_id": _id, 
            "Name":UserName, 
            "Surname":UserSurname, 
            "StudentNumber":StudentNumber,
            #"Email":Email,
            #"PhoneNumber":PhoneNumber,
            "isAuthenticated": False, 
            "isAdmin":False 
        }) 
        print('\nInserted data successfully\n') 

    except Exception: 
        print(Exception) 

##################################### Function to update record to mongo db ############################################# 
def update(Username, UserSurname, StudentNumber, Email, PhoneNumber): 
    try: 
        #criteria = input('\nEnter a student number to update\n') 
        #name = input('\nEnter name to update\n') 
        #surname = input('\nEnter Surname to update\n') 
        #StuNumber = input('\nEnter Student Number to update\n') 


        db.userDB.update_one( 
            {"StudentNumber": criteria}, 
            { 
                "$set": { 
                            "Name":UserName, 
                            "Surname":UserSurname, 
                            "StudentNumber":StudentNumber,
                            #"Email":Email,
                            #"PhoneNumber":PhoneNumber,
                            "isAuthenticated": False, 
                            "isAdmin":False 
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
def delete(StudentNumber): 
    try: 
        #criteria = input('\nEnter a student number to delete\n') 
        db.userDB.delete_many({"StudentNumber":StudentNumber}) 
        print('\nDeletion successful\n') 

    except Exception: 
        print(Exception) 
 
 
main() 
sys(exit) 
