import zmq

host = 'distrib-1'
host = 'localhost'
port = 3000
username = 'ifouros'

context = zmq.Context()

#  Socket to talk to server
print("Connecting to 'distrib-1' server")
socket = context.socket(zmq.REQ)
#socket.connect("tcp://distrib-1:5555")
socket.connect("tcp://" + host  + ":5555")

for request in range(2):
    print("Sending request %s " % request)
    socket.send(b"!r-%s-%s-%s" %(host, port, username))

    #  Get the reply.
    message = socket.recv()
    print("Received reply %s [ %s ]" % (request, message))
