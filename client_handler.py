import socket
import os
import sys
import threading


class ClientHandler( threading.Thread ):
    def __init__(self, server_socket, client_socket, messageRelay):
        threading.Thread.__init__(self)
        self.server_socket = server_socket
        self.client_socket = client_socket
        self.messageRelay = messageRelay

    def run(self):
        try:
            self.client_socket.send('Please enter your name: '.encode())
        except socket.error as err:
            print('[ ERROR ] Unable to send client name request message: ' + str(err))
            sys.exit()
            
        try:
            response_encoded = self.client_socket.recv(1024)
        except socket.error as err:
            print('[ ERROR ] Message recv failed: ' + str(err))
            sys.exit()
        
        response = response_encoded.decode().split(':')
        client_name = response[0]
        ft_listening_port = response[1]
        self.messageRelay.new_client(self.client_socket, client_name, ft_listening_port)
        
        while True:
            try:
                msg_encoded = self.messageRelay.connections[client_name][0].recv(1024)
            except socket.error as err:
                print('[ ERROR ] Message recv from client ' + client_name + ' failed: ' + str(err))
            
            if len(msg_encoded):
                # print('[ OK ] Relaying message ' + msg_encoded.decode())
                self.messageRelay.relay_message(msg_encoded, client_name)
