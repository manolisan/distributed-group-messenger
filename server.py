import time
import zmq
import tracker

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    message = socket.recv()
    print("Received message: %s" % message)

    #  Do some 'work'
    time.sleep(1)

    cmd, args = tracker.proccess_message(message)
    if (cmd == "r"):
        print "Cmd: " + cmd + " args_size: " + str(len(args))
        tracker.register(args[0], args[1], args[2])
        print tracker.client_list
        
        print "Register Succesfull"
        reply = "Register Succesfull"
    else:
        print "Invalid arguments"
        reply = "Invalid arguments"



    socket.send(reply)


    #  Send reply back to client
    #socket.send(b"Register Succesfull")
