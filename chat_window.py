"""
This module defines the class ChatWindow, a GUI for the chat client.
"""

import socket
import Tkinter as tk
import ttk

import transfer_manager as tm


class ChatWindow(object):
    """
    This class defines a GUI for the chat client.
    """
    def __init__(self, master, client_name, server_socket, ft_listening_port):
        """
        Initializes class member variables and launches the chat window.

        params:
            master
            client_name
            server_socket
            ft_listening_port
        """
        self.master = master
        self.client_name = client_name
        self.server_socket = server_socket
        self.ft_listening_port = ft_listening_port
        self.prompt_root = None
        self.messages_label = None
        self.name_input = None
        self.fname_input = None
        self.mainframe = tk.Frame(self.master, bg='white')

        self.mainframe.pack(fill='both', expand=True)
        self.master.title('%s - %s' % ('PyChat', self.client_name))
        self.chat_text = tk.StringVar()

        self.build_grid()
        self.build_message_area()
        self.build_input_area()
        self.build_buttons()

    def update_chat_text(self, new_text):
        """
        Will be called by MessageRececiver to pass new messages to the client window.

        params:
            new_text
        """
        updated_text = self.chat_text.get() + new_text + '\n'
        print 'updated_text =', updated_text
        self.chat_text.set(updated_text)

    def send_message(self, message):
        """
        Reads input from client, then writes the message to the server.
        
        params:
            message
        """
        print '"Send" clicked'
        if message:
            message = self.client_name + ': ' + message
            try:
                self.server_socket.send(message.encode())
            except socket.error as err:
                print '[ ERROR ] Could not send message. Code: ' + err[0] + ' Text: ' + err[1]

    def send_pressed(self, *args):
        """
        Callback method for the 'Send' button, initiates sending the typed message to the server.
        """
        message = self.input_area.get('1.0', tk.END).strip()
        self.send_message(message)
        self.input_area.delete('1.0', tk.END)

    def request_file_pressed(self):
        """
        Called when the user clicks 'Request File' to request a file transfer from another user.
        Prompts the user for the file owner's username, and the name of the file (including
        extension). Then sends the request to the server and spins up an instance of
        TransferManager locally in its own thread.
        """
        # Launch a mini-window to prompt user for file owner and filename
        self.prompt_root = tk.Tk()
        prompt_mainframe = tk.Frame(self.prompt_root, bg='white')
        prompt_mainframe.pack(fill='both')
        prompt_mainframe.columnconfigure(0, weight=1)
        prompt_mainframe.rowconfigure(0, weight=1)
        prompt_mainframe.rowconfigure(1, weight=0)
        prompt_mainframe.rowconfigure(2, weight=0)
        name_frame = tk.Frame(prompt_mainframe, bg='white')
        name_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        tk.Label(name_frame, bg='white', text='User name:').pack()
        self.name_input = tk.Entry(name_frame)
        self.name_input.pack()
        fname_frame = tk.Frame(prompt_mainframe, bg='white')
        fname_frame.grid(row=1, column=0, sticky='ew', padx=10, pady=10)
        tk.Label(fname_frame, bg='white', text='File name:').pack()
        self.fname_input = tk.Entry(fname_frame)
        self.fname_input.bind('<Return>', self.ok_pressed)
        self.fname_input.pack()
        ok_button = tk.Button(
            prompt_mainframe,
            text='OK',
            width=4,
            command=self.ok_pressed
        )
        ok_button.grid(row=2, column=0, sticky='ew', padx=10, pady=10)

    def ok_pressed(self, *args):
        """
        Called when user clicks "OK" button after filling in the user name and file name.
        this causes the TransferManager to run and kills the File Request dialog box.
        """
        owner = self.name_input.get().strip()
        file_name = self.fname_input.get().strip()
        if not file_name or not owner:
            print '[ ERROR ] Filename or username could not be read from stdin.'
        else:
            request = 'FT_REQUEST:' + owner + ':' + file_name + ':' + self.ft_listening_port
            try:
                # print('request sent at: ' + str(time.time()))
                self.server_socket.send(request.encode())
            except socket.error as err:
                print '[ ERROR ] Could not connect to server: ' + str(err) + ' Exiting...'

            tm.TransferManager(self.ft_listening_port, file_name, owner).start()

        self.prompt_root.destroy()

    def build_grid(self):
        """
        This method defines the grid for arranging the chat client window.
        """
        self.mainframe.columnconfigure(0, weight=1)
        # A row for the chat room message area, for the user's message entry area,
        # and for the send button.
        self.mainframe.rowconfigure(0, weight=1)
        self.mainframe.rowconfigure(1, weight=0)
        self.mainframe.rowconfigure(2, weight=0)

    def current_msg_text(self):
        """
        This method returns the appropriate content for the message area

        returns:
            string
        """
        chat_text = self.chat_text.get()
        if not chat_text:
            return 'Sample label text'
        return chat_text

    def build_message_label(self, *args):
        """
        Creates and packs the message label into the messag area frame.
        """
        self.messages_label = tk.Label(
            self.message_frame,
            height=8,
            justify=tk.LEFT,
            textvariable=self.chat_text
        )
        self.messages_label.pack(side='left')

    def build_message_area(self):
        """
        This method defines the message viewing area of the chat window.
        """
        # ttk.Style().configure('Messages.TFrame',
            # bg='white',
            # width=200,
            # height=80
        # )
        # message_frame = ttk.Frame(self.mainframe, style='Messages.TFrame')
        self.message_frame = tk.Frame(self.mainframe, height=80, width=20)
        self.message_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        self.message_frame.columnconfigure(0, weight=1)

        self.build_message_label()

    def build_input_area(self):
        """
        This method defines the message input area of the chat window.
        """
        self.input_area = tk.Text(
            self.mainframe,
            width=60,
            height=6
        )
        self.input_area.bind('<Return>', self.send_pressed)
        self.input_area.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

    def build_buttons(self):
        """
        This method builds the send button inside a frame for the chat window.
        """
        buttons_frame = tk.Frame(self.mainframe)
        buttons_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=10)
        buttons_frame.columnconfigure(0, weight=1)

        self.send_button = ttk.Button(
            buttons_frame,
            text='Send',
            command=self.send_pressed
        )
        self.request_ft_button = ttk.Button(
            buttons_frame,
            text='Request File',
            command=self.request_file_pressed
        )
        self.send_button.pack(side='right')
        self.request_ft_button.pack(side='right')


if __name__ == '__main__':
    ROOT = tk.Tk()
    ChatWindow(ROOT, 'TestClient', '6000', '6001')
    ROOT.mainloop()
