import uuid

## ---------------------------- tracker functionality ----------------------------

clients_data = {}
groups_members = {}
groups = []

def register(ip, port, username):
    generated_id = uuid.uuid4()
    id = str(generated_id)
    clients_data[id] = (ip, port, username)
    print "ID: ", id
    return id

def list_groups():
    print "ACTIVE GROUPS: ", groups
    return groups

def list_members(group_name):
    if (not groups_members.has_key(group_name)):
        return []
    members_ids = groups_members[group_name]
    members_names = []
    for member_id in members_ids:
        _, _, name = clients_data[member_id]
        members_names.append(name)
    print "MEMBERS in GROUP: " + group_name + "LIST: ", str(members_names)
    return members_names

def join_groups(group_name, id):
    # if the group doesn't exist create it & add user to group
    if (not groups_members.has_key(group_name)):
        groups_members[group_name] = []
        groups.append(group_name)

    # now the group exists, (even if it's a null group)
    # first check if the user is ALREADY in the group
    # then add the user to the group only once!
    if id not in groups_members[group_name]:
        groups_members[group_name].append(id)
    else:
        # alredy a member, just return a null list
        return []

    # and then return the full list of members
    members_data = []
    for client_id in groups_members[group_name]:
        members_data.append((client_id, ) + clients_data[client_id])

    print "JOIN GROUPS return: ", members_data
    return  members_data

def exit_group(group_name, id):
    if (not groups_members.has_key(group_name)):
        return False

    # try to delete the user from a pre-specified group
    try:
        groups_members[group_name].remove(id)
    except ValueError:
        print "EXIT_GROUP: User, not member of requested group"
        return False

    # if the group is empty delete it andn remove the corresponding group
    if (groups_members[group_name] == []):
        del groups_members[group_name]
        try:
            groups.remove(group_name)
        except ValueError:
            print "EXIT_GROUP: Group, not found"
            return False

    # Client to exit the group found, everything ok
    print "EXIT_GROUP-FOUND"
    return True


def quit(id):
    # removing user from all groups
    for group_name in groups:
        exit_group(group_name, id)

    print "QUIT_COMPLETED"
    return True



## ---------------------------- Check validity of received message ----------------------------

def proccess_message(message):
    if (message.startswith('!')):
        # message IS a command
        command = message.split(' ')
        cmd = command[0].lstrip('!')
        args_size = len(command) - 1
        print "FULL COMMAND: " + str(command)
        print "ARGS SIZE: " + str(args_size)
        print "CMD: " + cmd

        ## check for errors in arguments
        ##
        ## all the arguments lists (apart from register cmd),
        ## incldue one extra argument, client id.
        if (cmd == "r" and args_size != 3):
            return "Invalid arguments", []
        elif (cmd == "lg" and args_size != 1):
            return "Invalid arguments", []
        elif (cmd == "lm" and args_size != 2):
            return "Invalid arguments", []
        elif (cmd == "j" and args_size != 2):
            return "Invalid arguments", []
        elif (cmd == "e" and args_size != 2):
            return "Invalid arguments", []
        elif (cmd == "q " and args_size != 1):
            return "Invalid arguments", []

        ## return command ensuring that it has correct arguments
        return cmd, command[1:]

    else:
        # message is NOT a command
        # return just null list for now
        return [],[]

## ---------------------------- Execute command ----------------------------

def execute(cmd, args):
    print "-->EXECUTE CMD"

    if (cmd == "r"):
        id = register(args[0], args[1], args[2])
        out = "SUCESS_" + id
    elif (cmd == "lg"):
        active_groups = list_groups()
        out = "SUCESS_" + str(active_groups)
    elif (cmd == "lm"):
        usernames_group = list_members(args[0])
        out = ("SUCESS_" + str(usernames_group) ) if usernames_group else "FAIL_LIST MEMBERS"
    elif (cmd == "j"):
        members_list = join_groups(args[0], args[1])
        out = ("SUCESS_" + str(members_list) ) if members_list else "FAIL_JOIN alredy member"
    elif (cmd == "e"):
        exit = exit_group(args[0], args[1])
        out = "SUCESS_EXIT GROUP" if exit else "FAIL_EXIT GROUP"
    elif (cmd == "q"):
        quit(args[0])
        out = "SUCESS_QUIT"

        ## check for errors
    elif (cmd == "Invalid arguments"):
        print "Invalid arguments"
        out = "FAIL_Invalid arguments"
    else:
        print "Invalid command"
        out = "FAIL_Invalid command"


    print "-->END CMD"
    return out
