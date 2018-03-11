import time
import zmq
import tracker
import threading

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")



#def clean_dead():
#    threading.Timer(20.0, clean_dead).start()
#    print "Clean DEAD"


#    for
#    with lock:
#        del

#    print "ALIVE!"

#clean_dead()

while True:
    #  Wait for next request from client
    message = socket.recv()
    print ("------------------------")
    print ("-->Received message: %s" %message)

    cmd, args = tracker.proccess_message(message)
    reply = tracker.execute(cmd, args)

    #if ( not cmd == 'a'):
        #  Send reply back to client only if it's not an alive message
    socket.send(reply)
