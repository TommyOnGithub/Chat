import threading
import socket
import getopt
import sys

import ClientHandler as CH
import MessageRelay as MR


def handle_new_client(server_socket, client_socket, messageRelay):
    clientHandler = CH.ClientHandler(server_socket, client_socket, messageRelay)
    clientHandler.start()

def usage(script_name):
    print('Usage: ' + script_name + ' <port number> ')    

def main():
    # Get command line args and check for user error
    argc = len(sys.argv)
    if argc < 2 or argc > 2:
        usage(sys.argv[0])
        sys.exit()
    
    opts, args = getopt.getopt(sys.argv[1:], '')
    listening_port = args[0]
    
    # Initialize socket
    try:
        listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print('[ ERROR ] Could not create socket. Code: ' + str(err[0]) + ' Description: ' + err[1])
        sys.exit()
    # print('[ SUCCESS ] Created socket')
    listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        listening_socket.bind(('localhost', int(listening_port)))
        # print('[ SUCCESS ] Socket bound to port ' + listening_port)
    except socket.error as err:
        print('[ ERROR ] Unable to bind socket: ' + str(err))
        sys.exit()
    
    # start up the Message Relay which will handle message distribution
    # before we start listening for clients.
    messageRelay = MR.MessageRelay(listening_socket)

    listening_socket.listen(5)
    # print('[ OK ] Listening on port ' + listening_port)
    
    while True:
        client_socket, addr = listening_socket.accept()
        # print('[ OK ] New connection ' + addr[0] + ':' + str(addr[1]))
        handle_new_client(listening_socket, client_socket, messageRelay)

if __name__ == "__main__":
    main()