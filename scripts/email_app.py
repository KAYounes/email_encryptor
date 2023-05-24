import tkinter as tk
import tkinter.font as tkFont
import smtplib

from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

import encryption_decryption as AES
import rpc_client
import path_handler
import os
import re

from tkinter import messagebox
# import client

class App:
    sender = "18P9093@eng.asu.edu.eg"
    password = "kareemamr123"
    tovar=""

    def __init__(self, root):
        self.connected = False

        self.client = rpc_client.RPCClient()
        self.client.login_as_sender('email_1.dat')

        self.load_default_text()

        self.root = root
        
        #setting window size
        width=600
        height=500
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2,(screenheight - height) / 2)

        self.root.geometry(alignstr)
        self.root.resizable(width=True, height=True)
        self.root.config(padx=10, pady=10)
        self.root.title("Secure Mail Composer")
        
        # Bind the close window event to the on_close() function
        root.protocol("WM_DELETE_WINDOW", self.on_close)

        # self.root.bind("<Return>", lambda event: self.button_send_command())

        entries_frame = tk.Frame(self.root)
        entries_frame.columnconfigure(1, weight=1)
        entries_frame.rowconfigure(3, weight=1)
        action_frame = tk.Frame(entries_frame)

        font_poppins_bold = tkFont.Font(family='Poppins Bold',size=12)
        font_poppins_bold_sm = tkFont.Font(family='Poppins Bold',size=8)
        font_poppins_light = tkFont.Font(family='Poppins Light',size=12)
        font_poppins_light_sm = tkFont.Font(family='Poppins Light',size=8)

        label_to=tk.Label(entries_frame)
        label_to["font"] = font_poppins_bold
        label_to["fg"] = "#333333"
        label_to["justify"] = "right"
        label_to["text"] = "To:"
        label_to.grid(row=0, column=0, sticky='e')
        self.email_to=tk.Entry(entries_frame)
        self.email_to["font"] = font_poppins_light
        self.email_to["fg"] = "#333333"
        self.email_to["justify"] = "left"
        self.email_to.insert(1, self.default_recipient)
        self.email_to.grid(row=0, column=1, sticky='ew')

        label_subject=tk.Label(entries_frame)
        label_subject["font"] = font_poppins_bold
        label_subject["fg"] = "#333333"
        label_subject["justify"] = "right"
        label_subject["text"] = "Subject:"
        label_subject.grid(row=1, column=0, sticky='e')
        self.email_subject=tk.Entry(entries_frame)
        self.email_subject["font"] = font_poppins_light
        self.email_subject["fg"] = "#333333"
        self.email_subject["justify"] = "left"
        self.email_subject.insert(1, self.default_subject)
        self.email_subject.grid(row=1, column=1, sticky='ew')
        
        label_body=tk.Label(entries_frame)
        label_body["font"] = font_poppins_bold
        label_body["fg"] = "#333333"
        label_body["justify"] = "left"
        label_body["text"] = "Body"
        label_body.grid(row=2, column=1, sticky='w')
        self.email_body=tk.Text(entries_frame, height=0)
        self.email_body["font"] = font_poppins_light
        self.email_body["fg"] = "#333333"
        self.email_body.insert('1.0', self.default_message)
        self.email_body.grid(row=3, column=1, sticky='ns')

        button_connect=tk.Button(action_frame, padx=0, pady=0, command=self.connect)
        button_connect["bg"] = "#f0f0f0"
        button_connect["fg"] = "#000000"
        button_connect["font"] = font_poppins_light_sm
        button_connect["text"] = "Connect to KDS"
        button_connect.pack(side='left', ipadx=10)
        button_connect.config(relief='groove')
        self.connection_status = tk.Label(action_frame, text="Not Connected")
        self.connection_status["fg"] = "#FF0000"
        self.connection_status.pack(side='left')
        
        self.button_send=tk.Button(action_frame, padx=0, pady=0, command=self.button_send_command)
        self.button_send["bg"] = "#f0f0f0"
        self.button_send["font"] = font_poppins_light_sm
        self.button_send["fg"] = "#000000"
        self.button_send["text"] = "Send"
        self.button_send["state"] = "disabled"
        self.button_send.pack(side='right', ipadx=10)
        self.button_send.config(relief='groove')
        
        button_clear=tk.Button(action_frame, padx=0, pady=0, command=self.button_clear_command)
        button_clear["bg"] = "#f0f0f0"
        button_clear["font"] = font_poppins_light_sm
        button_clear["fg"] = "#000000"
        button_clear["text"] = "Clear"
        button_clear.pack(side='right', ipadx=10)
        button_clear.config(relief='groove')

        action_frame.grid(row=4, column=1, sticky='ew', pady=10)
        entries_frame.pack(fill='both', expand=True, anchor='nw')
    
    def connect(self):
        # print("2")
        if(self.connected):
            return

        self.connected = self.client.connect()
        # print("3")
        self.update_connection_status()
        # print("7")


    def update_connection_status(self):
        # print("4")
        if(self.connected):
            # print("5B")
            self.connection_status["fg"] = "#00FF00"
            self.connection_status["text"] = "Connected"
            self.button_send['state'] = 'normal'
        else:
            # print("5A")
            self.connection_status["fg"] = "#FF0000"
            self.connection_status["text"] = "Not Connected"
        
        # print("6")


    def button_send_command(self):
        # print(f"{self.button_send['state']=}")
        # if(self.button_send['state'] == 'disable'):
        #     return

        if(not self.connected):
            # print("1")
            self.connect()

        # print("8")
        recipient = self.email_to.get()
        subject = self.email_subject.get()
        message = self.email_body.get("1.0", "end-1c")

        # print(f"{recipient=} \n {subject=} \n {message=}")

        if(not self.valid_email(recipient, subject, message)):
            return

        self.client.send_email('email_1.dat', recipient, subject, message)
        # self.root.update()
        # self.button_send.config(state="normal")


    def valid_email_address(self, email):
        email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        return re.fullmatch(email_regex, email)

    def valid_email(self, recipient, subject, message):
        try:
            if(not self.valid_email_address(recipient)):
                raise Exception("Invalid Sender Email")
                # return False

            if(len(subject) == 0 or subject.isspace()):
                raise Exception("Invalid Subject")
                # return False

            if(len(message) == 0 or message.isspace()):
                raise Exception("Invalid Message")
                # return False

            return True
        except Exception as e:
            print("\n", "="*20, f"[ERROR {e}] [script: email_app.py] [function: validate_email] [solution: check input]", "="*20, "\n", sep='', end='')
            return False

    def button_clear_command(self):
        self.email_to.delete(0, 'end')
        self.email_subject.delete(0, 'end')
        self.email_body.delete('1.0', 'end')

    def connect_to_server(self):
        self.connection_status = self.client.connect_to_server()

    def load_default_text(self):
        with open(os.path.join(path_handler.STORAGE_FILES_DIR, 'default_email.txt'), 'r') as f:
            self.default_recipient = f.readline().strip()
            self.default_subject = f.readline().strip()
            self.default_message = ''.join(f.readlines()).strip()

        # Create a close window event handler
    def on_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            print("BYE BYE")
            self.client.logout_sender()
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()