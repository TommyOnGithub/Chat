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


def main():
    """
    Reads in the parameters specified by the user, while error-checking, then connects to the
    specified server. Spins up an instance of MessageReceiver in its own separate thread. Then
    loops indefinitely on user input.
    """
    # Get initialization information from "config.ini" file.
    server_addr = None
    server_port = None
    ft_listening_port = None
    config = open('config.ini', 'rU').readlines()    # 'U' for cross-platform newline support
    for line in config:
        line = line.strip().split('=')
        if line[0] == 'server':
            server_addr = line[1]
        elif line[0] == 'port':
            server_port = line[1]
        elif line[0] == 'recv_file_port':
            ft_listening_port = line[1]

    # Establish connection with server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.connect((server_addr, int(server_port)))
    except socket.gaierror as gaierror:
        server_socket.connect((server_addr+'.local', int(server_port)))

    # Server prompts for client name, this will read from stdin and respond.
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

    # Start listening for messages from server and open the client window.
    root = tk.Tk()
    chat_window = cw.ChatWindow(root, client_name, server_socket, ft_listening_port)
    MR.MessageReceiver(server_socket, client_name, chat_window).start()
    
    root.mainloop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print 'Exiting on keyboard interrupt'
