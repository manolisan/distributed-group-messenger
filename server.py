import time
import zmq
import tracker

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

tracker = tracker.Tracker()

while True:
    #  Wait for next request from client
    message = socket.recv()
    print("Received message: %s" % message)

    #  Do some 'work'
    time.sleep(1)

    # testing here
    string = tracker.string()
    print string




    #  Send reply back to client
    socket.send(b"World")
