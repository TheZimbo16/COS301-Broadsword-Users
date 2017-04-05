
import nsq
import tornado.ioloop
import time
import json
 
request="""{
    "src"  : "Access",
    "dest" : "user",
    "msgType" : "request",
    "queryType" : "insert",
    "content" : {
                      "fname" : "John",
                      "sname" : "Doe",
                      "stud_num" : "15043143",
                      "email" : "wow@gmail.com",
                      "password" : "funny",
                      "phone" : "0820618804"
                }
}""";

def pub_message():
     writer.pub('user',request, finish_pub)
 
def finish_pub(conn, data):
     print(data)
 
writer = nsq.Writer(['127.0.0.1:4150'])
tornado.ioloop.PeriodicCallback(pub_message,1000).start()
nsq.run()