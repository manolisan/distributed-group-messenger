import zmq
import sys

#host = 'distrib-1'
host = 'localhost'
port = 3000
username = 'manolis'

my_id = 0
context = zmq.Context()

# # Initialize soccents and connect to tracker
print("Connecting to " + host + " server")
socket = context.socket(zmq.REQ)
socket.connect("tcp://" + host  + ":5555")

## client register to thhe service
print ("------------------------")
print("Sending register request [ !r ]")
socket.send(b"!r %s %s %s" %(host, port, username))

message = socket.recv()
if (message.startswith('*')):
    print ("Error: ", message.lstrip('*'))
else:
    my_id = message
    print ("REPLY --> ID: %s" %my_id)


# client give commands from stdin
while True:
    print ("------------------------")
    line = raw_input("[%s]>" %username)
    user_input = line.rstrip("\n ")
    user_input = ' '.join(user_input.split())
    print("REQUEST: [ %s ]" %user_input)
    socket.send(user_input + " " + my_id)
    #socket.send(user_input)

    message = socket.recv()

    if (message.startswith('*')):
        print "Error: ", message.lstrip('*')
    else:
        print "REPLY: [ %s ]" %message
