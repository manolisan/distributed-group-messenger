import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to 'distrib-1' server")
socket = context.socket(zmq.REQ)
socket.connect("tcp://distrib-1:5555")

for request in range(10):
    print("Sending request %s " % request)
    socket.send(b"Hey: " + str(request) )

    #  Get the reply.
    message = socket.recv()
    print("Received reply %s [ %s ]" % (request, message))



