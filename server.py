import time
import zmq
import tracker

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    message = socket.recv()
    #socket.fileno()
    print "SOCKET: " + str(socket.fileno())
    print("Received message: %s" %message)



    cmd, args = tracker.proccess_message(message)
    if (cmd == "r"):
        print "Cmd: " + cmd + " args_size: " + str(len(args))
        id = tracker.register(args[0], args[1], args[2])
        print "Id: ", id
        print tracker.clients_data

        print "Register Succesfull"
        reply = "SUCESS_" + id
    elif (cmd == "lg"):
        reply = "LG test reply"
    else:
        print "Invalid arguments"
        reply = "FAIL_Invalid arguments"


    #  Send reply back to client
    socket.send(reply)
