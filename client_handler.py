"""
This module defines the class ClientHandler which runs as its own thread and is responsible
for both adding a client to the chat server and forwarding its messages to the MesssageRelay class.
"""

import socket
import sys
import threading


class ClientHandler(threading.Thread):
    """
    ClientHandler runs as its own thread and is responsible for both adding a client to the chat
    server and forwarding its messages to the MesssageRelay class.
    """
    def __init__(self, server_socket, client_socket, message_relay):
        threading.Thread.__init__(self)
        self.server_socket = server_socket
        self.client_socket = client_socket
        self.message_relay = message_relay

    def run(self):
        try:
            self.client_socket.send('Please enter your name: '.encode())
        except socket.error as err:
            print '[ ERROR ] Unable to send client name request message: ' + str(err)
            sys.exit()

        try:
            response_encoded = self.client_socket.recv(1024)
        except socket.error as err:
            print '[ ERROR ] Message recv failed: ' + str(err)
            sys.exit()

        response = response_encoded.decode().split(':')
        client_name = response[0]
        ft_listening_port = response[1]
        self.message_relay.new_client(self.client_socket, client_name, ft_listening_port)

        while True:
            msg_encoded = ''
            try:
                msg_encoded = self.message_relay.connections[client_name][0].recv(1024)
            except socket.error as err:
                print '[ ERROR ] ' + client_name + ' has disconnected.'
                sys.exit()

            if msg_encoded != '':
                # print('[ OK ] Relaying message ' + msg_encoded.decode())
                self.message_relay.relay_message(msg_encoded, client_name)
