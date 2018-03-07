import time
import zmq
import tracker

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    message = socket.recv()
    print ("------------------------")
    print ("-->Received message: %s" %message)

    cmd, args = tracker.proccess_message(message)
    reply = tracker.execute(cmd, args)
    
    #  Send reply back to client
    socket.send(reply)
