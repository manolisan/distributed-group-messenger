import zmq
import sys
import socket
import select
import ast
import threading
import time


if (len(sys.argv) != 3):
    print "Usage: python client.py [port] [username]"
    exit()

joined_groups = []
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
    #check if user wants to choose a group
    if user_input.startswith('!w'):
        command = user_input.split(' ')
        #check if user has joined the certain group
        if command[1] in joined_groups:
            current_group = command[1]
            print "Write a message in group  %s" %command[1]
        else:
            print "You haven't joined group %s" %command[1], "in order to send a message"
     #check if user wants to communicate with server
    elif (user_input.startswith('!')):
        print("REQUEST: [ %s ]" % user_input)
        socket_tcp.send(user_input + " " + my_id)
        message = socket_tcp.recv()
        if (message.startswith('*')):
            print "Error: ", message.lstrip('*')
        else:
            #after communication with server user stores the members of the group and the group name
            if user_input.startswith('!j'):
                command = user_input.split(' ')
                groups_members[command[1]] = list(ast.literal_eval(message))
                joined_groups.append(command[1])
                for item in groups_members[command[1]][::-1]:
                    receive_sock.sendto('*' + str(((my_id, host, str(port), username), command[1])), (item[1], int(item[2])))
                print "REPLY: [ %s ]" % message
            # if user exits a certain group remove group from joined groups and the list of users of the group
            elif user_input.startswith('!e'):
                command=user_input.split(' ')
                for item in groups_members[command[1]][::-1]:
                    receive_sock.sendto('&' + str(((my_id, host, str(port), username), command[1])), (item[1], int(item[2])))
                groups_members[command[1]][:] = []
                joined_groups.remove(command[1])
                current_group=None
                print "REPLY: [ %s ]" % message
            #if user quits empty joined groups list and groups_members dictionary
            elif user_input.startswith('!q'):
                for item1 in groups_members:
                    for item in groups_members[item1][::-1]:
                        receive_sock.sendto('&' + str(((my_id, host, str(port), username), item1)), (item[1], int(item[2])))
                groups_members.clear()
                joined_groups[:] = []
                print "REPLY: [ %s ]" % message
                current_group = None
            else:
                print "REPLY: [ %s ]" % message
     #check if user wants to send a message
    else:
        #if user hasn't selected a group to send a message
        if (current_group is None):
            print "Please selece a group in order to sent a message!!!"
        else:
            #check if user is still a member of current group,he may have left
            if current_group in joined_groups:
                print "TODO: Sending user input! "
                for item in groups_members[current_group][::-1]:
                    receive_sock.sendto("in " + current_group + ' ' + username + " says:: " + user_input, (item[1], int(item[2])))
            else:
                current_group=None
                print "Please selece a group in order to sent a message!!!"
    sys.stdout.write("[%s]>" %username); sys.stdout.flush()



def heartbeat():
    while True:
        timer_context = zmq.Context()
        socket_timer = timer_context.socket(zmq.REQ)
        socket_timer.connect("tcp://" + host  + ":5555")
        if current_group is None:
            socket_timer.send(b"!a "+my_id)
        else:
            socket_timer.send(b"!a "+my_id + ' ' + current_group)
        message = socket_timer.recv()
        print "***ALIVE!"

        if message.startswith("*u"):
            message = message[2:]
            groups_members[current_group] = list(ast.literal_eval(message))

        print "Group members", groups_members
        print "***ALIVE!"
        time.sleep(5)



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


## make heartbeat thread
heartbeat_thread = threading.Thread(target = heartbeat)
heartbeat_thread.daemon = True
heartbeat_thread.start()


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
                if data.startswith('*'):
                    data = data[1::]
                    data = eval(data)

                    if groups_members.has_key(data[1]):
                        if not (data[0] in groups_members[data[1]]):
                            groups_members[data[1]].append(data[0])
                            print groups_members[data[1]]
                elif data.startswith('&'):
                    data = data[1::]
                    data = eval(data)

                    if groups_members.has_key(data[1]):
                        if data[0] in groups_members[data[1]]:
                            groups_members[data[1]].remove(data[0])
                            print groups_members[data[1]]

                else:
                    sys.stdout.write('\n')
                    sys.stdout.write(data)
                    sys.stdout.write('\n')
                    sys.stdout.write("[%s]>" %username); sys.stdout.flush()

        else:
            #users writes message
            send_input()
