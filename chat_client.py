#! /usr/bin/env python

"""
This script defines a CLI chat client capable of sharing messages to a chat server and sending
and receiving files P2P with other connected clients.
"""

import sys
import socket
import getopt
import Tkinter as tk

import transfer_manager as TM
import message_receiver as MR
import chat_window as cw


def handle_send_message(client_name, server_socket):
    """
    Called when the user types 'M' to send a message. Prompts user, reads input, and formats
    message for the chat server. Then writes the message to the server's socket.
    params:
        client_name
        server_socket
    """
    print 'Enter your message:'
    message = sys.stdin.readline().strip()
    if not message:
        print '[ ERROR ] Message could not be read from stdin. exiting.'
        sys.exit()
    else:
        message = client_name + ': ' + message
        try:
            server_socket.send(message.encode())
        except socket.error as err:
            print '[ ERROR ] Could not send message. Code: ' + err[0] + ' Text: ' + err[1]
            sys.exit()

def handle_request_ft(server_socket, ft_listening_port):
    """
    Called when the user types 'F' to request a file transfer from another user. Prompts the
    user for the file owner's username, and the name of the file (including extension).
    Then sends the request to the server and spins up an instance of TransferManager locally
    in its own thread.
    params:
        client_name
        server_socket
        ft_listening_port
    """
    print 'Who owns the file?'
    owner = sys.stdin.readline().strip()
    print 'Which file do you want?'
    filename = sys.stdin.readline().strip()

    if not filename or not owner:
        print '[ ERROR ] Filename or username could not be read from stdin.'
    else:
        request = 'FT_REQUEST:' + owner + ':' + filename + ':' + ft_listening_port
        try:
            # print('request sent at: ' + str(time.time()))
            server_socket.send(request.encode())
        except socket.error as err:
            print '[ ERROR ] Could not connect to server: ' + str(err) + ' Exiting...'
            sys.exit()

        TM.TransferManager(ft_listening_port, filename, owner).start()


def handle_option(user_input, client_name, server_socket, ft_listening_port):
    """
    Determines the action requested by the user and executes it.
    params:
        user_input
        client_name
        server_socket
        ft_listening_port
    """
    user_input = user_input.upper()
    if user_input == 'M':
        handle_send_message(client_name, server_socket)
    if user_input == 'F':
        handle_request_ft(server_socket, ft_listening_port)
    if user_input == 'X':
        print '[ OK ] Exiting chat'
        try:
            server_socket.shutdown(socket.SHUT_RDWR)
            server_socket.close()
        except socket.error as err:
            print '[ ERROR ] Could not close server socket. Code: ' + err[0] + ' Text: ' + err[1]
        sys.exit()

def usage(script_name):
    """
    Called when the user attempts to run the script with extra or missing parameters.
    params:
        script_name
    """
    print '[ ERROR ] Usage: python3 ' + script_name + ' -l <listening port number> ' \
	'-p <connect server port>'

def main():
    """
    Reads in the parameters specified by the user, while error-checking, then connects to the
    specified server. Spins up an instance of MessageReceiver in its own separate thread. Then
    loops indefinitely on user input.
    """
    # argc = len(sys.argv)
    # if not argc == 5:
        # usage(sys.argv[0])
        # sys.exit()

    # opts, _ = getopt.getopt(sys.argv[1:], 'l:p:')
    # ft_listening_port = opts[0][1]
    # server_port = opts[1][1]
    server_addr = None
    server_port = None
    ft_listening_port = None
    config = open('config.ini', 'rU').readlines()    # 'U' for cross-platform newline support
    for line in config:
        line = line.split('=')
        if line[0] == 'server':
            server_addr = line[1].strip()
        elif line[0] == 'port':
            server_port = line[1].strip()
        elif line[0] == 'recv_file_port':
            ft_listening_port = line[1].strip()
    print 'addr = %s, port = %s, xfer port = %s' % (server_addr, server_port, ft_listening_port)

    # Establish connection with server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_socket.connect(('localhost', int(server_port)))
    server_socket.connect((server_addr, int(server_port)))
    # print('[ SUCCESS ] Connection established with the server')

    # Exchange information about this client with the server
    try:
        print server_socket.recv(1024).decode()
    except socket.error as err:
        print '[ ERROR ] Unable to receive prompt from server: ' + str(err)
    client_name = sys.stdin.readline().strip()
    response = client_name + ':' + str(ft_listening_port)
    try:
        server_socket.send(response.encode())
    except socket.error as err:
        print '[ ERROR ] Unable to send response to server: ' + str(err)

    root = tk.Tk()
    chat_window = cw.ChatWindow(root, client_name, server_socket, ft_listening_port)
    MR.MessageReceiver(server_socket, client_name, chat_window).start()
    
    root.mainloop()

    # while True:
        # print 'Enter an option (\'m\', \'f\', \'x\'):\n   (M)essage (send)\n' \
		# '   (F)ile (request)\n   e(X)it'
        # user_input = sys.stdin.readline().strip()
        # if not user_input:
            # pass
        # handle_option(user_input, client_name, server_socket, ft_listening_port)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print 'Exiting on keyboard interrupt'
