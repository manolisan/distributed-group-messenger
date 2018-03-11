import time
import zmq
import tracker
import threading

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

def clean_dead():
    while True:
        print "***********************************Clean DEAD"
        dead_clients = []
        with tracker.alive_lock:
            for client_id in tracker.alive_clients:
                print tracker.alive_clients[client_id], time.clock()
                if  (tracker.alive_clients[client_id] < time.clock() - 0.05):
                    dead_clients.append(client_id)

            for client_id in dead_clients:
                del tracker.alive_clients[client_id]
            print "**********************************Clean DEAD,", dead_clients
        time.sleep(20)

## make clean_dead thread
clean_thread = threading.Thread(target = clean_dead)
clean_thread.daemon = True
clean_thread.start()

while True:
    #  Wait for next request from client
    message = socket.recv()
    print ("------------------------")
    print ("-->Received message: %s" %message)

    cmd, args = tracker.proccess_message(message)
    reply = tracker.execute(cmd, args)

    #if ( not cmd == 'a'):
        #  Send reply back to client only if it's not an alive message
    socket.send(reply)
