import zmq
import sys
import socket
import struct


if (len(sys.argv) != 3):
    print "Usage: python client.py [port] [username]"
    exit()

host = 'localhost'
port = sys.argv[1]
username = sys.argv[2]

my_id = 0
context = zmq.Context()

# # Initialize soccents and connect to tracker
print("Connecting to " + host + " server")
socket = context.socket(zmq.REQ)
socket.connect("tcp://" + host  + ":5555")

## REGISTER to thhe service
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

    # input command
    if (user_input.startswith('!')):
        print("REQUEST: [ %s ]" %user_input)
        socket.send(user_input + " " + my_id)
        message = socket.recv()
        if (message.startswith('*')):
            print "Error: ", message.lstrip('*')
        else:
            print "REPLY: [ %s ]" %message

    else:
        print "TODO: Sending user input! "
        #sender_sock.send(user_input)
