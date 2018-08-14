import socket


class MessageRelay(object):
    def __init__(self, server_socket):
        self.server_socket = server_socket
        self.connections = {}

    def new_client(self, client_socket, client_name, ft_listening_port):
        self.connections[client_name] = (client_socket, ft_listening_port)
        # print('[ SUCCESS ] Added new client: ' + client_name)

    def send_port(self, owner, client_socket):
        try:
            client_socket.send(self.connections[owner][1])
        except socket.error as err:
            print '[ ERROR ] ' + str(err)

    def relay_message(self, msg_encoded, from_client_name):
        for dest_client_name in list(self.connections):
            if dest_client_name == from_client_name:
                continue
            try:
                self.connections[dest_client_name][0].send(msg_encoded)
            except socket.error as err:
                print '[ ERROR ] Unable to send message to client "' + dest_client_name + '" '
                print str(err)
