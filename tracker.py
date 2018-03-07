import uuid

clients_data = {}
groups_members = {}
groups = []

def register(ip, port, username):
    generated_id = uuid.uuid4()
    id = str(generated_id)
    clients_data[id] = (ip, port, username)
    return id

def list_groups():
    return groups

def list_members(group_name):
    members_ids = groups_members[group_name]
    members_names = []
    for member_id in members_ids:
        _, _, name = clients_data[member_id]
        members_names.append(name)
    return members_names

def join_groups(group_name, id):
    # if the group doesn't exist create it & add user to group
    if (not groups_members.has_key(group_name)):
        groups_members[group_name] = []
        groups.append(group_name)

    # now the group exists, (even if it's a null group)
    # so add the user to the group
    groups_members[group_name].append(id)

    # and then return the full list of members
    members_data = []
    for client_id in groups_members[group_name]:
        members_data.append((client_id, ) + clients_data[client_id])
    return  members_data

#def exit_groups(group_name):

#def quit(id):




def proccess_message(message):
    if (message.startswith('!')):
        command = message.split(' ')
        cmd = command[0].lstrip('!')
        args_size = len(command) - 1
        print "FULL COMMAND: " + str(command)
        print "ARGS SIZE: " + str(args_size)
        print "CMD: " + cmd

        ## check for errors
        if (cmd == "r" and args_size != 3):
            return "Invalid arguments", []
        elif (cmd == "lg" and args_size != 0):
            return "Invalid arguments", []
        elif (cmd == "lm" and args_size != 1):
            return "Invalid arguments", []
        elif (cmd == "j" and args_size != 2):
            return "Invalid arguments", []
        elif (cmd == "e" and args_size != 2):
            return "Invalid arguments", []
        elif (cmd == "q " and args_size != 1):
            return "Invalid arguments", []

        ## return command with correct arguments
        return cmd, command[1:]
