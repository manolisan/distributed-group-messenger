import time
import zmq
import tracker

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    message = socket.recv()
    print ("------------------------")
    print ("-->Received message: %s" %message)

    cmd, args = tracker.proccess_message(message)
    print "-->EXECUTE CMD"

    if (cmd == "r"):
        id = tracker.register(args[0], args[1], args[2])
        reply = "SUCESS_" + id
        print "ID: ", id
        print "TRACKER_CLIENT_DATA: ", tracker.clients_data

    elif (cmd == "lg"):
        active_groups = tracker.list_groups()
        print "ACTIVE GROUPS: ", active_groups
        reply = str(active_groups)
    elif (cmd == "lm"):
        usernames_group = tracker.list_members(args[0])
        print "MEMBERS in GROUP: " + args[0] + "LIST: ", str(usernames_group)
        reply = str(usernames_group)
    elif (cmd == "j"):
        members_list = tracker.join_groups(args[0], args[1])
        print "Join groups return: ", members_list
        reply = str(members_list)
    elif (cmd == "e"):
        exit = tracker.exit_group(args[0], args[1])
        reply = "SUCESS_EXIT GROUP" if exit else "FAIL_EXIT GROUP"
    elif (cmd == "q"):
        tracker.quit(args[0])
        reply = "SUCESS_QUIT"


        ## check for errors
    elif (cmd == "Invalid arguments"):
        print "Invalid arguments"
        reply = "FAIL_Invalid argumentss"
    else:
        print "Invalid command"
        reply = "FAIL_Invalid command"

    print "-->END CMD"
    #  Send reply back to client
    socket.send(reply)
