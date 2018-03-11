import zmq
import sys
import socket
import select
import ast


if (len(sys.argv) != 3):
    print "Usage: python client.py [port] [username]"
    exit()

groups_members = {}
current_group = None
host = "localhost"
port = int(sys.argv[1])
username = sys.argv[2]

my_id = 0
context = zmq.Context()


# client give commands from stdin
def send_input():
    global current_group
    print ("------------------------")
    line = sys.stdin.readline()
    user_input = line.rstrip("\n ")
    user_input = ' '.join(user_input.split())

    # input command
    if user_input.startswith('!w'):
        command = user_input.split(' ')
        current_group = command[1]
    elif (user_input.startswith('!')):
        print("REQUEST: [ %s ]" % user_input)
        socket_tcp.send(user_input + " " + my_id)
        message = socket_tcp.recv()
        if (message.startswith('*')):
            print "Error: ", message.lstrip('*')
        else:
            if user_input.startswith('!j'):
                command = user_input.split(' ')
                groups_members[command[1]] = list(ast.literal_eval(message))
                print "REPLY: [ %s ]" % message
            else:
                print "REPLY: [ %s ]" % message
    else:
        if (current_group is None):
            print "Please join or create a group in order to sent a message!!!"
        else:
            print "TODO: Sending user input! "
            for item in groups_members[current_group][::-1]:
                receive_sock.sendto(user_input, (item[1], int(item[2])))

    sys.stdout.write("[%s]>" %username); sys.stdout.flush()



# # Initialize soccents and connect to tracker
print("Connecting to " + host + " server")
socket_tcp = context.socket(zmq.REQ)
socket_tcp.connect("tcp://" + host  + ":5555")

## REGISTER to thhe service
print ("------------------------")
print("Sending register request [ !r ]")
socket_tcp.send(b"!r %s %s %s" %(host, port, username))

message = socket_tcp.recv()
if (message.startswith('*')):
    print ("Error: ", message.lstrip('*'))
else:
    my_id = message
    print ("REPLY --> ID: %s" %my_id)

## udp sockets.
receive_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_sock.bind((host, port))

sys.stdout.write("[%s]>" %username); sys.stdout.flush()

while True:
    readable, writable, exceptional = select.select([sys.stdin, receive_sock], [], [])
    for s in readable:
        if receive_sock == s:
            # incoming message from peer
            data = receive_sock.recv(1024)
            if not data:
                print "Error receiving data"
                sys.exit()
            else:
                sys.stdout.write('\n')
                sys.stdout.write(data)
                sys.stdout.write('\n')
                sys.stdout.write("[%s]>" %username); sys.stdout.flush()

        else:
            #users writes message
            send_input()
            #sys.stdout.wr
