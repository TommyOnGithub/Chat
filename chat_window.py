"""
This module defines the class ChatWindow, a GUI for the chat client.
"""

import Tkinter
import ttk


class ChatWindow:
    """
    This class defines a GUI for the chat client.
    """
    def __init__(self, master):
        """
        Initializes class member vars.
        params:
            master
        """
        self.master = master
        self.mainframe = Tkinter.Frame(self.master, bg='white')
        self.mainframe.pack(fill='both', expand=True)
        
        self.chat_text = Tkinter.StringVar()
        self.chat_text.trace('w', self.display_msg_text)
        
        self.build_grid()
        self.build_message_area()
        self.build_input_area()
        self.build_buttons()

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
        
    def display_msg_text(self):
        return 'Sample label text'

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
        message_frame = Tkinter.Frame(self.mainframe, height=80, width=20)
        message_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        message_frame.columnconfigure(0, weight=1)
        
        self.messages_label = Tkinter.Label(
            message_frame,
            text=self.display_msg_text()
        )
        self.messages_label.pack(side='left')
    
    def build_input_area(self):
        """
        This method defines the message input area of the chat window.
        """
        input_area = Tkinter.Text(
            self.mainframe,
            width=60,
            height=6
        )
        input_area.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
    
    def build_buttons(self):
        """
        This method builds the send button inside a frame for the chat window.
        """
        buttons_frame = Tkinter.Frame(self.mainframe)
        buttons_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=10)
        buttons_frame.columnconfigure(0, weight=1)
        
        self.send_button = Tkinter.Button(
            buttons_frame,
            text='Send'
        )
        self.request_ft_button = Tkinter.Button(
            buttons_frame,
            text='Request File'
        )
        self.send_button.pack(side='right')


if __name__ == '__main__':
    root = Tkinter.Tk()
    ChatWindow(root)
    root.mainloop()
