#Main program to handle persistence for NavUP Users Module
#Author: Drew Langley 11039753 COS 301 Broadsword-Users

import sys
import functions

import nsq
import json

main()

def main():
    while(1):
        r = nsq.Reader(message_handler=handler, lookupd_http_addresses=['http://127.0.0.1:4150'], topic='users', channel='navup', lookupd_poll_interval=15)
        nsq.run()
        print("NSQ RUNNING>??????" + r)

def requestHandler(message):
    try:
        obj = json.loads(message.body)

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
                print("")

    except Exception:
        print(Exception);
