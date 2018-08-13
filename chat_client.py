import sys
import socket
import getopt

import transfer_manager as TM
import message_receiver as MR


def handle_send_message(client_name, server_socket):
    print 'Enter your message:'
    message = sys.stdin.readline().strip()
    if not message:
        if message == '':
            pass
        print '[ ERROR ] Message could not be read from stdin. exiting.'
        sys.exit()
    if len(message):
        message = client_name + ': ' + message
        try:
            server_socket.send(message.encode())
        except socket.error as err:
            print '[ ERROR ] Could not send message. Code: ' + err[0] + ' Text: ' + err[1]
            sys.exit()

def handle_request_ft(client_name, server_socket, ft_listening_port):
    print 'Who owns the file?'
    owner = sys.stdin.readline().strip()
    print 'Which file do you want?'
    filename = sys.stdin.readline().strip()
    if not filename:
        print '[ ERROR ] Filename could not be read from stdin. exiting.'
        sys.exit()

    if len(filename):
        request = 'FT_REQUEST:' + owner + ':' + filename + ':' + ft_listening_port
        try:
            # print('request sent at: ' + str(time.time()))
            server_socket.send(request.encode())
        except socket.error as err:
            print '[ ERROR ] Could not connect to server: ' + str(err) + ' Exiting...'
            sys.exit()

        TM.TransferManager(ft_listening_port, filename, owner).start()


def handle_option(user_input, client_name, server_socket, ft_listening_port):
    if user_input in ('M', 'm'):
        handle_send_message(client_name, server_socket)
    if user_input in ('F', 'f'):
        handle_request_ft(client_name, server_socket, ft_listening_port)
    if user_input in ('X', 'x'):
        print '[ OK ] Exiting chat'
        try:
            server_socket.shutdown(socket.SHUT_RDWR)
            server_socket.close()
        except socket.error as err:
            print '[ ERROR ] Could not close server socket. Code: ' + err[0] + ' Text: ' + err[1]
        sys.exit()

def usage(script_name):
    print '[ ERROR ] Usage: python3 ' + script_name + ' -l <listening port number> \
												-p <connect server port>'

def main():
    argc = len(sys.argv)
    if argc < 5 or argc > 5:
        usage(sys.argv[0])
        sys.exit()

    opts, _ = getopt.getopt(sys.argv[1:], 'l:p:')
    ft_listening_port = opts[0][1]
    server_port = opts[1][1]

    # Establish connection with server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # print('[ OK ] Connecting to localhost on port ' + server_port + '...')
    server_socket.connect(('localhost', int(server_port)))
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

    MR.MessageReceiver(server_socket, client_name).start()

    while True:
        print 'Enter an option (\'m\', \'f\', \'x\'):\n   (M)essage (send)\n   \
											(F)ile (request)\n   e(X)it'
        user_input = sys.stdin.readline().strip()
        if not user_input:
            print '[ ERROR ] user_input could not be read from stdin. exiting.'
            sys.exit()
        handle_option(user_input, client_name, server_socket, ft_listening_port)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print 'Exiting on keyboard interrupt'
