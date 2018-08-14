#! /usr/bin/env python

"""
This module defines a CLI chat server which accepts up to five
simultaneous connected users. Users may send messages which are
then posted to the other users' client windows.

In addition to broadcasting messages to the chat users, this
server facilitates P2P file transfers. The client sends the
name of the desired file (including extention) and the name of
the file's owner, and the server writes the file to the
client's dedicated file transfer port.
"""

import socket
import getopt
import sys

import client_handler as CH
import message_relay as MR


def handle_new_client(server_socket, client_socket, message_relay):
    """
    Kicks off a new instance of ClientHandler in its own separate thread.
    params:
        server_socket
        client_socket
        message_relay
    """
    client_handler = CH.ClientHandler(server_socket, client_socket, message_relay)
    client_handler.start()

def usage(script_name):
    """
    Called when the user tries to start with extra or missing parameters.
    params:
        script_name
    """
    print 'Usage: ' + script_name + ' <port number> '

def main():
    """
    Opens a socket on the specified port number, and listens for up to 5 connecting clients.
    """
    # Get command line args and check for user error
    argc = len(sys.argv)
    if not argc == 2:
        usage(sys.argv[0])
        sys.exit()

    _, args = getopt.getopt(sys.argv[1:], '')
    listening_port = args[0]

    # Initialize socket
    try:
        listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print '[ ERROR ] Could not create socket. Code: ' + str(err[0]) + ' Description: ' + err[1]
        sys.exit()
    # print('[ SUCCESS ] Created socket')
    listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        listening_socket.bind(('localhost', int(listening_port)))
        # print('[ SUCCESS ] Socket bound to port ' + listening_port)
    except socket.error as err:
        print '[ ERROR ] Unable to bind socket: ' + str(err)
        sys.exit()

    # start up the Message Relay which will handle message distribution
    # before we start listening for clients.
    message_relay = MR.MessageRelay(listening_socket)

    listening_socket.listen(5)
    # print('[ OK ] Listening on port ' + listening_port)

    while True:
        client_socket, _ = listening_socket.accept()
        # print('[ OK ] New connection ' + addr[0] + ':' + str(addr[1]))
        handle_new_client(listening_socket, client_socket, message_relay)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print 'Exiting on keyboard interrupt'
        sys.exit()
