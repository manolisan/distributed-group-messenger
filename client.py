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
state, reply = message.split('_')
if (state == "SUCESS"):
    my_id = reply
    print ("Request succeeded with ID: %s" %my_id)
elif (state == "FAIL"):
    print ("Request failed")
else:
    print("Received unknown reply [ %s ]" %message)

# client give commands from stdin
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
