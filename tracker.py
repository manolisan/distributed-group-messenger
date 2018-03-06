import uuid

clients_data = {}
groups = {}

def register(ip, port, username):
    id = uuid.uuid4()
    clients_data[id] = (ip, port, username)
    return str(id)

#def list_groups():

#def list_members(group_name):

#def join_groups(group_name):
    #groups[group_name].append()
#def exit_groups(group_name):

#def quit(id):




def proccess_message(message):
    if (message.startswith('!')):
        command = message.split(' ')
        cmd = command[0].lstrip('!')
        args_size = len(command) - 1
        print "Full Command: " + str(command)
        print "ARGS size: " + str(args_size)
        print "CMD: " + cmd

        ## check for errors
        if (cmd == "r" and args_size != 3):
            return "Invalid arguments", []
        elif (cmd == "lg" and args_size != 0):
            return "Invalid arguments", []

        ## return command with correct arguments
        return cmd, command[1:]
