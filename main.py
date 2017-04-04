#Main program to handle persistence for NavUP Users Module
#Author: Drew Langley 11039753 COS 301 Broadsword-Users

import sys
import functions

import pysqn
import json

def requestHandler(message):
    try:
        obj = json.loads(message.body)

        if obj['dest'] == 'users':

            query = obj['queryType']

            if query == 'insert':
                name = obj['content']['fname']
                lName = obj['content']['fname']
                sNumber = obj['content']['stud_num']
                insertOne(name, lName, sNumber)

            # elif query == 'update':
            #     name = obj['content']['fname']
            #     lName = obj['content']['fname']
            #     sNumber = obj['content']['stud_num']
            #     update(name, lName, sNumber)


    except Exception:
        print(Exception);
