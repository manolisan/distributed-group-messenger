import zmq
import sys

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

while True:
    print ("------------------------")
    line = sys.stdin.readline()
    user_input = line.rstrip("\n ")
    user_input = ' '.join(user_input.split())
    print("Sending request [ %s ]" %user_input)
    socket.send(user_input + " " + my_id)
    #socket.send(user_input)

    message = socket.recv()
    print("Received reply [ %s ]" %message)
