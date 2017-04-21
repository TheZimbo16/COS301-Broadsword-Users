
import nsq
import tornado.ioloop
import time
import json

request="""{
    "src"  : "Access",
    "dest" : "users",
    "msgType" : "request",
    "queryType" : "insert",
    "content" : {
                      "fname" : "Whazzaaaa!",
                      "sname" : "okeey",
                      "stud_num" : "123456",
                      "email" : "wow@gmail.com",
                      "password" : "funny",
                      "phone" : "0820618804"
                }
}""";

def pub_message():
     writer.pub('users', request.encode('utf-8'), finish_pub)

def finish_pub(conn, data):
	print(data)
	tornado.ioloop.IOLoop.current().stop()



writer = nsq.Writer(['127.0.0.1:4150'])
tornado.ioloop.PeriodicCallback(pub_message,1000).start()
nsq.run()
