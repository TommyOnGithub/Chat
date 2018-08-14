"""
This module defines the TransferManager class, which is responsible for receiving and
writing requested files to the local host.
"""

import socket
import threading


class TransferManager(threading.Thread):
    """
    This class is responsible for receiving and writing requested files to the local host.
    """
    def __init__(self, ft_listening_port, filename, owner):
        """
        Initializes class member variables.
        params:
            ft_listening_port
            filename
            owner
        """
        threading.Thread.__init__(self)
        self.ft_listening_port = ft_listening_port
        self.filename = filename
        self.owner = owner

    def recv_file(self, file_host):
        """
        This method is responsible for reading the requested file from the owner's File
        Transfer Socket and writing to this client's local directory. This could be improved
        by giving the user a chance to "Save As" under a different file name or directory.
        params:
            file_host
        """
        piece = None

        # Save the received file in the local directory
        recv_file = open(self.filename, 'wb')
        # print('[ OK ] Initiating file transfer...')
        try:
            piece = file_host.recv(1024)
            while piece:
                # print('[ OK ] Receiving file...')
                recv_file.write(piece)
                piece = file_host.recv(1024)
            recv_file.close()
            # print('[ SUCCESS ] Finished file transfer.')
            file_host.shutdown(socket.SHUT_WR)
            file_host.close()
        except socket.error as err:
            print str(err)

    def run(self):
        """
        This method implements the core function of the class, to handle file transfers.
        Initializes the client's Listening File Transfer Socket, and indefinitely loops to
        accept up to five connections and receive those files.
        """
        ft_listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ft_listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            ft_listening_socket.bind(('localhost', int(self.ft_listening_port)))
        except socket.error as err:
            print '[ ERROR ] Unable to bind to given socket'
            print str(err)
        ft_listening_socket.listen(5)
        # print('TM socket is listening at ' + str(time.time()))
        while True:
            file_host, _ = ft_listening_socket.accept()
            self.recv_file(file_host)
