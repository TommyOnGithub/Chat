"""
This module defines the class MessageReceiver which runs in it's own thread and is responsible for
handling messages to the client from the server. One problem with this class is that it has too many
responsiblities. File sending funcationalities should be separated out into their own class.
"""

import threading
import socket
import sys
import time


class MessageReceiver(threading.Thread):
    """
    MessageReceiver runs in it's own thread and is responsible for handling messages to the client
    from the server. One problem with this class is that it has too many responsiblities. File
    sending funcationalities should be separated out into their own class.
    """
    def __init__(self, server_socket, client_name, chat_window):
        """
        Initializes class member variables.
        """
        threading.Thread.__init__(self)
        self.server_socket = server_socket
        self.client_name = client_name
        self.chat_window = chat_window

    def send_file(self, message):
        """
        Sends requested file to the requesting party.
        """
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
            return
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
                return
            piece = send_file.read(1024)
        send_file.close()
        # print('[ SUCCESS ] Finished file transfer.')
        transfer_socket.shutdown(socket.SHUT_WR)
        transfer_socket.close()

    def is_ft_request(self, message):
        """
        Quick check to determine if a message from the server should initialize a file transfer.
        """
        request = message.split(':')
        return request[0] == 'FT_REQUEST'

    def ft_request_for_this_client(self, message):
        """
        Determines if the file stransfer request is meant for this client.
        """
        request = message.split(':')
        return request[1] == self.client_name

    def run(self):
        """
        Core thread funcations - loop on receiving messages from the server and either carry out
        a file transfer or display the message to the user.
        """
        while True:
            try:
                message = self.server_socket.recv(1024).decode()
            except socket.error as err:
                print '[ ERROR ] Unable to receive messages from server: ' + str(err)
                self.server_socket.close()
                sys.exit
            if message != '':
                if self.is_ft_request(message):
                    if self.ft_request_for_this_client(message):
                        self.send_file(message)
                    else:
                        continue
                else:
                    self.chat_window.update_chat_text(message)
            else:
                print '[ ERROR ] Received no bytes, closing socket...'
                self.server_socket.close()
                sys.exit()
