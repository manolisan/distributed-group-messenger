import zmq
import sys
import socket
import select
import ast
import threading
import time

#
if (len(sys.argv) != 4 and len(sys.argv) != 3):
    print "Usage: python client.py [port] [username] or client.py [port] [username] [textfile]"
    exit()

#list of joined groups
joined_groups = []
#list for every group the clients is in for multicast sending
groups_members = {}
#for fifo
sequence_vector = {}
#variavle for the group the client has chosen to write with !w
current_group = None

#initializations
host = "localhost"
port = int(sys.argv[1])
username = sys.argv[2]
my_id = 0
context = zmq.Context()


# client give commands from stdin
def send_input(line):
    global current_group
    #print ("------------------------")
    user_input = line.rstrip("\n ")
    user_input = ' '.join(user_input.split())

    # check if user wants to choose a group
    if user_input.startswith('!w'):
        command = user_input.split(' ')
        args_size = len(command) - 1
        if args_size==1:
            # check if user has joined the certain group
            if command[1] in joined_groups:
                current_group = command[1]
                print "Write a message in group  %s" % command[1]
            else:
                print "You haven't joined group %s" % command[1], "in order to send a message"
        else:
            print "Invalid arguments"

    # check if user wants to communicate with server
    elif (user_input.startswith('!')):
        socket_tcp.send(user_input + " " + my_id)
        message = socket_tcp.recv()
        if (message.startswith('*')):
            print "Error: ", message.lstrip('*')
        else:
            # after communication with server user stores the members of the group and the group name
            if user_input.startswith('!j'):
                command = user_input.split(' ')
                groups_members[command[1]] = list(ast.literal_eval(message))
                joined_groups.append(command[1])
                sequence_vector[command[1]] = {}
                for item in groups_members[command[1]][::-1]:
                    # initialize counter of all clients of group for fifo
                    sequence_vector[command[1]][item[3]] = 0
                    #let the clients of group know that you joined
                    if int(item[2]) != port:
                        receive_sock.sendto('*' + str(((my_id, host, str(port), username), command[1])),
                                            (item[1], int(item[2])))
                print "You succesfully joined group %s" %command[1]

            # if user exits a certain group remove group from joined groups and the list of users of the group
            elif user_input.startswith('!e'):
                command = user_input.split(' ')
                for item in groups_members[command[1]][::-1]:
                    # let the clients of group know that you exited
                    if int(item[2]) != port:
                        receive_sock.sendto('&' + str(((my_id, host, str(port), username), command[1])),
                                        (item[1], int(item[2])))
                groups_members[command[1]][:] = []
                joined_groups.remove(command[1])
                current_group = None
                print "REPLY: [ %s ]" % message
            # if user quits empty joined groups list and groups_members dictionary
            elif user_input.startswith('!q'):
                for item1 in groups_members:
                    for item in groups_members[item1][::-1]:
                        # let the clients of all groups know that you exited
                        if int(item[2]) != port:
                            receive_sock.sendto('&' + str(((my_id, host, str(port), username), item1)),
                                                (item[1], int(item[2])))
                groups_members.clear()
                joined_groups[:] = []
                print "REPLY: [ %s ]" % message
                current_group = None
                sys.exit()
            else:
                print "REPLY: [ %s ]" % message
    # check if user wants to send a message
    else:
        # if user hasn't selected a group to send a message
        if (current_group is None):
            print "Please selece a group in order to sent a message!!!"
        else:
            # check if user is still a member of current group,he may have left
            if current_group in joined_groups:
                #for every multicats in a group increase counter
                sequence_vector[current_group][username] += 1
                for item in groups_members[current_group][::-1]:
                    receive_sock.sendto( (str(sequence_vector[current_group][username]) + "&&" + "in " + current_group + ' ' + username + " says:: " + user_input),
                                        (item[1], int(item[2])))
            else:
                current_group = None
                print "Please selece a group in order to sent a message!!!"
    sys.stdout.write("[%s]>" % username);
    sys.stdout.flush()


def heartbeat():
    while True:
        timer_context = zmq.Context()
        socket_timer = timer_context.socket(zmq.REQ)
        socket_timer.connect("tcp://" + host + ":5555")
        if current_group is None:
            socket_timer.send(b"!a " + my_id)
        else:
            socket_timer.send(b"!a " + my_id + ' ' + current_group)
        message = socket_timer.recv()
        #print "***ALIVE!"

        if message.startswith("*u"):
            message = message[2:]
            groups_members[current_group] = list(ast.literal_eval(message))

        #print "Group members", groups_members
        #print "***ALIVE!"
        time.sleep(5)


# # Initialize soccents and connect to tracker
print("Connecting to " + host + " server")
socket_tcp = context.socket(zmq.REQ)
socket_tcp.connect("tcp://" + host + ":5555")

## REGISTER to thhe service
print ("------------------------")
print("Sending register request [ !r ]")
socket_tcp.send(b"!r %s %s %s" % (host, port, username))

message = socket_tcp.recv()
if (message.startswith('*')):
    print ("Error: ", message.lstrip('*'))
else:
    my_id = message
    print ("REPLY --> ID: %s" % my_id)

## udp sockets.
receive_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_sock.bind((host, port))

sys.stdout.write("[%s]>" % username);
sys.stdout.flush()

## make heartbeat thread
heartbeat_thread = threading.Thread(target=heartbeat)
heartbeat_thread.daemon = True
heartbeat_thread.start()

#open file if it is given and join a group
if len(sys.argv) == 4:
    textfile = sys.argv[3]
    fds = open(textfile, "r")
    send_input("!j slack")
    send_input("!w slack")
    inputs = [sys.stdin, receive_sock, fds]
else:
    inputs = [sys.stdin, receive_sock]
    fds = None
outputs = []

while True:
    time.sleep(0.5)
    readable, writable, exceptional = select.select(inputs, outputs, [])
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
                    #for refreshing group members dictionary
                    if groups_members.has_key(data[1]):
                        if not (data[0] in groups_members[data[1]]):
                            groups_members[data[1]].append(data[0])
                    #adding counters for new clients of a group
                    if sequence_vector.has_key(data[1]):
                        if not (sequence_vector[data[1]].has_key(data[0][3])):
                            sequence_vector[data[1]][data[0][3]] = 0

                elif data.startswith('&'):
                    data = data[1::]
                    data = eval(data)
                    #for refreshing group members dicrionary
                    if groups_members.has_key(data[1]):
                        if data[0] in groups_members[data[1]]:
                            groups_members[data[1]].remove(data[0])
                    if sequence_vector.has_key(data[1]):
                        if sequence_vector[data[1]].has_key(data[0][3]):
                            del sequence_vector[data[1]][data[0][3]]
                #fifooooooo
                else:
                    data = data.split('&&')
                    check_counter = int(data[0])
                    check_username = (data[1].split(' '))[2]
                    check_group = (data[1].split(' '))[1]
                    check_counter2 = sequence_vector[check_group][check_username]
                    if check_counter >= check_counter2:
                        sequence_vector[check_group][check_username] = check_counter
                        sys.stdout.write('\n')
                        sys.stdout.write(data[1])
                        sys.stdout.write('\n')
                        sys.stdout.write("[%s]>" % username);
                        sys.stdout.flush()
                    else:
                        sequence_vector[check_group][check_username] = check_counter

        elif fds == s:
            for line in fds:
                if line.startswith("10"):
                    line = line[4::]
                    fds.close()
                    inputs.remove(fds)
                else:
                    line = line[3::]
                line = line.replace('\r', '')
                send_input(line)
                break
        else:
            #print "Send input from stdin"
            # users writes message
            line = sys.stdin.readline()
            send_input(line)
