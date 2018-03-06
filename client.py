import zmq
import uuid

#host = 'distrib-1'
host = 'localhost'
port = 3000
username = 'ifouros'

my_id = 0
context = zmq.Context()

#  Socket to talk to server
print("Connecting to " + host + " server")
socket = context.socket(zmq.REQ)
socket.connect("tcp://" + host  + ":5555")

for request in range(1):
    print("Sending request !r %s " % request)
    socket.send(b"!r %s %s %s" %(host, port, username))

    #  Get the reply.
    message = socket.recv()
    state, reply = message.split('_')
    if (state == "SUCESS"):
        my_id = uuid.UUID(reply)
        print ("Request succeeded with id: %s" %str(my_id))
    elif (state == "FAIL"):
        print ("Request failed")
    else:
        print("Received unknown reply %s [ %s ]" % (request, message))



print "MY_ID is: ", my_id

print("Sending request !lg")
socket.send(b"!lg")

message = socket.recv()
print("Received reply FOR LG [ %s ]" %message)
