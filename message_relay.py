"""
This module defines the class MessageRelay which is responsible for distributing messages to each
client other than the sender. One problem with this class is that it must also keep track of which
clients are connected and which have disconnected from the server.
"""

import socket


class MessageRelay(object):
    """
    MessageRelay is responsible for distributing messages to each client other than the sender. One
    problem with this class is that it must also keep track of which clients are connected and
    which have disconnected from the server.
    """
    def __init__(self, server_socket):
        """
        Initializes class member variables.
        params:
            server_socket
        """
        self.server_socket = server_socket
        self.connections = {}

    def new_client(self, client_socket, client_name, ft_listening_port):
        """
        Adds the given client to the list of clients to which messages will be broadcasted.
        params:
            client_socket
            client_name
            ft_listening_port
        """
        self.connections[client_name] = (client_socket, ft_listening_port)
        # print('[ SUCCESS ] Added new client: ' + client_name)

    def send_port(self, owner, client_socket):
        """
        This method writes the file transfer port number of the file's owner from whom
        a file has been requested to the requesting client's messaging socket.
        params:
            owner
            client_socket
        """
        try:
            client_socket.send(self.connections[owner][1])
        except socket.error as err:
            print '[ ERROR ] ' + str(err)

    def relay_message(self, msg_encoded, from_client_name):
        """
        This method writes the encoded message to all clients except for that of the sender.
        params:
            msg_encoded
            from_client_name
        """
        for dest_client_name in list(self.connections):
            if dest_client_name == from_client_name:
                continue
            try:
                self.connections[dest_client_name][0].send(msg_encoded)
            except socket.error as err:
                print '[ ERROR ] Unable to send message to client "' + dest_client_name + '" '
                print str(err)
