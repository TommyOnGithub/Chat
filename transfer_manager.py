import socket
import threading
import time


class TransferManager(threading.Thread):
    def __init__(self, ft_listening_port, filename, owner):
        threading.Thread.__init__(self)
        self.ft_listening_port = ft_listening_port
        self.filename = filename
        self.owner = owner

    def recv_file(self, file_host):
        piece = None

        # Save the received file in the local directory
        recv_file = open(self.filename, 'wb')
        # print('[ OK ] Initiating file transfer...')
        try:
            piece = file_host.recv(1024)
        except socket.error as err:
            print '[ ERROR ] Unable to receive file chunk from remote host ' + str(err)
            print str(time.time())
        while piece:
            # print('[ OK ] Receiving file...')
            recv_file.write(piece)
            piece = file_host.recv(1024)
        recv_file.close()
        # print('[ SUCCESS ] Finished file transfer.')
        file_host.shutdown(socket.SHUT_WR)
        file_host.close()

    def run(self):
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
