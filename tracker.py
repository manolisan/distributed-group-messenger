
client_list = []

def string():
        return 'sample_string'
def register(ip, port, username):
    client_list.append((ip, port, username))


def proccess_message(message):
    if (message.startswith('!')):
        command = message.split('-')
        cmd = command[0].lstrip('!')
        args_size = len(command) - 1

        print "Command: " + cmd

        ## check for errors
        if (cmd == "r" and args_size != 3):
            return "Invalid arguments", []
        elif (cmd == "lg" and args_size != 0):
            return "Invalid arguments", []

        ## return command with correct arguments
        return cmd, command[1:]
