"""
This module defines the class MessageReceiver which is responsible for 
"""

import threading
import socket
import sys
import time


class MessageReceiver(threading.Thread):
    def __init__(self, server_socket, client_name):
        threading.Thread.__init__(self)
        self.server_socket = server_socket
        self.client_name = client_name

    def send_file(self, message):
        request = message.split(':')
        # print('request[3] = ' + request[3])
        try:
            transfer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # print('Attempting to connect to TM socket at ' + str(time.time()))
            time.sleep(1)
            transfer_socket.connect(('localhost', int(request[3])))
            # print('[ SUCCESS ] Socket bound to port')
        except socket.error as err:
            print '[ ERROR ] Failed to connect to remote host ' + str(err)
        try:
            send_file = open(request[2], 'rb')           # files to be sent kept in same directory
        except IOError as err:
            print '[ ERROR ] Could not open file' + str(err)
            transfer_socket.shutdown(socket.SHUT_WR)
            transfer_socket.close()
            return
        # print('Initiating file transfer...')
        piece = send_file.read(1024)
        while piece:
            # print('[ OK ] File transfer in Progress...')
            try:
                transfer_socket.send(piece)
            except socket.error as err:
                print '[ ERROR ] Unable to send file chunk to remote host: ' + str(err)
                print str(time.time())
                sys.exit()
            piece = send_file.read(1024)
        send_file.close()
        # print('[ SUCCESS ] Finished file transfer.')
        transfer_socket.shutdown(socket.SHUT_WR)
        transfer_socket.close()

    def is_ft_request(self, message):
        request = message.split(':')
        return request[0] == 'FT_REQUEST'

    def ft_request_for_this_client(self, message):
        request = message.split(':')
        return request[1] == self.client_name

    def run(self):
        while True:
            try:
                message = self.server_socket.recv(1024).decode()
            except socket.error as err:
                print '[ ERROR ] Unable to receive messages from server: ' + str(err)
            if message != '':
                if self.is_ft_request(message):
                    if self.ft_request_for_this_client(message):
                        self.send_file(message)
                    else:
                        continue
                else:
                    print message
                print '(\'m\', \'f\', \'x\'):\n   (M)essage (send)\n   (F)ile (request)\n   e(X)it'
            else:
                print '[ ERROR ] Received no bytes, closing socket...'
                self.server_socket.close()
                sys.exit()
