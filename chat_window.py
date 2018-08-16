"""
This module defines the class ChatWindow, a GUI for the chat client.
"""

import threading
import Tkinter
import ttk

import transfer_manager as tm

class ChatWindow:
    """
    This class defines a GUI for the chat client.
    """
    def __init__(self, master, client_name, server_socket, ft_listening_port):
        """
        Initializes class member variables and launches the chat window.
        
        params:
            master
        """
        self.master = master
        self.client_name = client_name
        self.server_socket = server_socket
        self.prompt_root = None
        self.ft_listening_port = ft_listening_port
        self.mainframe = Tkinter.Frame(self.master, bg='white')
        self.mainframe.pack(fill='both', expand=True)
        
        self.chat_text = Tkinter.StringVar()
        self.chat_text.trace('w', self.build_message_label)
        
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
        self.chat_text.set(self.chat_text.get() + new_text + '\n')
    
    def send_message(self):
        """
        Reads input from client, then writes the message to the server.
        """
        print '"Send" clicked'
        message = self.input_area.get('1.0',Tkinter.END)
        if message:
            message = self.client_name + ': ' + message
            try:
                self.server_socket.send(message.encode())
            except socket.error as err:
                print '[ ERROR ] Could not send message. Code: ' + err[0] + ' Text: ' + err[1]

    def request_file_pressed(self):
        """
        Called when the user clicks 'Request File' to request a file transfer from another user.
        Prompts the user for the file owner's username, and the name of the file (including
        extension). Then sends the request to the server and spins up an instance of
        TransferManager locally in its own thread.
        params:
        """
        # Launch a mini-window to prompt user for file owner and filename
        self.prompt_root = Tkinter.Tk()
        prompt_mainframe = Tkinter.Frame(prompt_root, bg='white')
        prompt_mainframe.pack(fill='both')
        prompt_mainframe.columnconfigure(0, weight=1)
        prompt_mainframe.rowconfigure(0, weight=0)
        prompt_mainframe.rowconfigure(1, weight=0)
        prompt_mainframe.rowconfigure(2, weight=0)
        prompt_mainframe.rowconfigure(3, weight=0)
        prompt_mainframe.rowconfigure(4, weight=0)
        name_label = Tkinter.Label(prompt_mainframe, text='User name:')
        name_label.pack()
        self.name_input = Tkinter.Entry(prompt_mainframe)
        self.name_input.pack()
        fname_label = Tkinter.Label(prompt_mainframe, text='File name:')
        fname_label.pack()
        self.fname_input = Tkinter.Entry(prompt_mainframe)
        self.fname_input.pack()
        ok_button = Tkinter.Button(
            prompt_mainframe,
            text='OK',
            command=ok_pressed
        )

    def ok_pressed(self):
        """
        Called when user clicks "OK" button after filling in the user name and file name.
        """
        owner = self.name_input.get()
        file_name = self.fname_input.get()
        if not file_name or not owner:
            print '[ ERROR ] Filename or username could not be read from stdin.'
        else:
            request = 'FT_REQUEST:' + owner + ':' + filename + ':' + ft_listening_port
            try:
                # print('request sent at: ' + str(time.time()))
                self.server_socket.send(request.encode())
            except socket.error as err:
                print '[ ERROR ] Could not connect to server: ' + str(err) + ' Exiting...'

            tm.TransferManager(ft_listening_port, filename, owner).start()

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
        else:
            return chat_text
    
    def build_message_label(self, *args):
        self.messages_label = Tkinter.Label(
            self.message_frame,
            text=self.current_msg_text()
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
        self.message_frame = Tkinter.Frame(self.mainframe, height=80, width=20)
        self.message_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        self.message_frame.columnconfigure(0, weight=1)
    
        self.build_message_label()

    def build_input_area(self):
        """
        This method defines the message input area of the chat window.
        """
        self.input_area = Tkinter.Text(
            self.mainframe,
            width=60,
            height=6
        )
        self.input_area.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
    
    def build_buttons(self):
        """
        This method builds the send button inside a frame for the chat window.
        """
        buttons_frame = Tkinter.Frame(self.mainframe)
        buttons_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=10)
        buttons_frame.columnconfigure(0, weight=1)
        
        self.send_button = Tkinter.Button(
            buttons_frame,
            text='Send',
            command=self.send_message
        )
        self.request_ft_button = Tkinter.Button(
            buttons_frame,
            text='Request File',
            command=self.request_file_pressed
        )
        self.send_button.pack(side='right')
        self.request_ft_button.pack(side='right')


if __name__ == '__main__':
    root = Tkinter.Tk()
    ChatWindow(root)
    root.mainloop()
