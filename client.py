import zmq

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
    print ("------------------------")
    print("Sending request !r %s " % request)
    socket.send(b"!r %s %s %s" %(host, port, username))

    #  Get the reply.
    message = socket.recv()
    state, reply = message.split('_')
    if (state == "SUCESS"):
        my_id = reply
        print ("Request succeeded with id: %s" %my_id)
    elif (state == "FAIL"):
        print ("Request failed")
    else:
        print("Received unknown reply %s [ %s ]" % (request, message))

print "MY_ID is: ", my_id

print ("------------------------")
print("Sending request !j")
socket.send(b"!j slack2" + " " + my_id)

message = socket.recv()
print("Received reply FOR J [ %s ]" %message)


if (1==1):
    print("Sending request !lg")
    socket.send(b"!lg")

    message = socket.recv()
    print("Received reply FOR LG [ %s ]" %message)
