import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import tkinter.font as tkFont
import smtplib

from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

from tkinter import messagebox
import encryption_decryption as AES
import rpc_client
import os
import path_handler
# import client

class App:
    sender = "18P9093@eng.asu.edu.eg"
    password = "kareemamr123"
    tovar=""

    def __init__(self, root):
        self.connected = False
        self.client = rpc_client.RPCClient()
        self.client.login_as_recipient('email_2.dat')
        self.root = root
        # s = ttk.Style()
        # s.theme_use('clam')

        # Configure the style of Heading in Treeview widget
        # s.configure('Treeview.Heading', background="#F0F0F0")
        #setting window size
        width=600
        height=500
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2,(screenheight - height) / 2)

        self.root.geometry(alignstr)
        self.root.resizable(width=True, height=True)
        self.root.config(padx=10, pady=10)
        self.root.columnconfigure(index=0, weight=1)
        self.root.columnconfigure(index=2, weight=1)
        self.root.rowconfigure(index=0, weight=1)
        self.root.title("Secure Mail Decryptor")
        # Bind the close window event to the on_close() function
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.tree = ttk.Treeview(self.root, columns=("sender", "subject"), show='headings', selectmode='browse')
        
        self.tree.heading('sender', text='Sender Email Address', anchor="center")
        self.tree.heading('subject', text='Email Subject')
        self.tree.column('sender', anchor="center")
        self.tree.column('subject', anchor="center")


        self.tree.bind('<<TreeviewSelect>>', self.item_selected)
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        filtr_area = ttk.LabelFrame(self.root, text='Filters')
        filtr_area.grid(row=0, column=2, sticky="new", ipadx=20, ipady=20)



        self.unseen_filter = tk.BooleanVar(value=False)
        unseen_radio_box = tk.Checkbutton(master=filtr_area, variable=self.unseen_filter, text="Unseen Only")
        unseen_radio_box.pack(side="top", anchor='w', padx=10, pady=10)



        from_filter_label = tk.Label(master=filtr_area, text="From")
        from_filter_label.pack(side='top', anchor='w', padx=10)

        self.from_filter_entry = tk.Entry(master=filtr_area, text="From")
        self.from_filter_entry.pack(side='top', anchor='w', padx=10, pady=[0, 10], fill='x')



        subject_filter_label = tk.Label(master=filtr_area, text="Subject")
        subject_filter_label.pack(side='top', anchor='w', padx=10)

        self.subject_filter_entry = tk.Entry(master=filtr_area, text="Subject")
        self.subject_filter_entry.pack(side='top', anchor='w', padx=10, pady=[0, 10], fill='x')



        limit_filter_label = tk.Label(master=filtr_area, text="Limit")
        limit_filter_label.pack(side='top', anchor='w', padx=10)

        self.limit_filter_entry = tk.Entry(master=filtr_area, text="Limit")
        self.limit_filter_entry.pack(side='top', anchor='w', padx=10, fill='x')
        self.limit_filter_entry.config(validate="key")
        self.limit_filter_entry.config(validatecommand=(self.root.register(self.valid_limit), '%P'))



        self.filter_button = tk.Button(master=filtr_area, text="Request Emails", command=self.read_emails)
        self.filter_button.config(relief='groove')
        self.filter_button.pack(side='bottom', fill='x', padx=10, pady=10)
        self.filter_button['state'] = 'disable'


        button_connect=tk.Button(self.root, padx=0, pady=0, command=self.connect)
        button_connect["bg"] = "#f0f0f0"
        button_connect["fg"] = "#000000"
        button_connect["text"] = "Connect to KDS"
        button_connect.grid(row=1, column=2)
        button_connect.config(relief='groove')
        self.connection_status = tk.Label(self.root, text="Not Connected")
        self.connection_status["fg"] = "#FF0000"
        self.connection_status.grid(row=2, column=2)

    def connect(self):
        if(self.connected):
            return

        self.connected = self.client.connect()
        self.update_connection_status()

    def update_connection_status(self):
        if(self.connected):
            self.connection_status["fg"] = "#00FF00"
            self.connection_status["text"] = "Connected"
            self.filter_button['state'] = 'normal'
        else:
            self.connection_status["fg"] = "#FF0000"
            self.connection_status["text"] = "Not Connected"

    def valid_limit(self, text):
        return str.isdigit(text) or text == ""
        
    def item_selected(self, event):
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item).get('values')
            email_id = selected_item
            sender = item[0]
            subject = item[1]
            # return
            # show a message
            # showinfo(title='Information', message=selected_item)
            # Create a new window.
            self.open_email(email_id, sender, subject)


    def open_email(self, email_id, sender, subject):
            new_window = tk.Toplevel(self.root)

            # Set the title of the new window.
            new_window.title("Email " + str(email_id))
            width=600
            height=500
            screenwidth = new_window.winfo_screenwidth()
            screenheight = new_window.winfo_screenheight()
            alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2,(screenheight - height) / 2)

            new_window.geometry(alignstr)
            new_window.resizable(width=True, height=True)
            new_window.config(padx=10, pady=10)
            # new_window.columnconfigure(index=0, weight=1)
            # new_window.columnconfigure(index=2, weight=1)

            
            entries_frame = tk.Frame(new_window)
            entries_frame.rowconfigure(index=3, weight=1)
            entries_frame.rowconfigure(index=5, weight=1)

            label_to=tk.Label(entries_frame)
            # label_to["font"] = font_poppins_bold
            # label_to["fg"] = "#333333"
            # label_to["justify"] = "right"
            label_to["text"] = "To:"
            label_to.grid(row=0, column=0, sticky='e')
            self.email_to=tk.Entry(entries_frame)
            # self.email_to["font"] = font_poppins_light
            self.email_to["fg"] = "#333333"
            # self.email_to["justify"] = "left"
            self.email_to.insert(1, sender)
            self.email_to.grid(row=0, column=1, sticky='ew')
            self.email_to.config(state='disabled')

            label_subject=tk.Label(entries_frame)
            # label_subject["font"] = font_poppins_bold
            label_subject["fg"] = "#333333"
            # label_subject["justify"] = "right"
            label_subject["text"] = "Subject:"
            label_subject.grid(row=1, column=0, sticky='e')
            self.email_subject=tk.Entry(entries_frame)
            # self.email_subject["font"] = font_poppins_light
            self.email_subject["fg"] = "#333333"
            # self.email_subject["justify"] = "left"
            self.email_subject.insert(1, subject)
            self.email_subject.grid(row=1, column=1, sticky='ew')
            self.email_subject.config(state='disabled')
            
            label_encrypted_body=tk.Label(entries_frame)
            # label_encrypted_body["font"] = font_poppins_bold
            label_encrypted_body["fg"] = "#333333"
            # label_encrypted_body["justify"] = "left"
            label_encrypted_body["text"] = "Encrypted Body"
            label_encrypted_body.grid(row=2, column=1, sticky='w')
            self.email_encrypted_body=tk.Text(entries_frame, height=0)
            # self.email_encrypted_body["font"] = font_poppins_light
            self.email_encrypted_body["fg"] = "#333333"
            self.email_encrypted_body.insert('1.0', "Wait please...")
            self.email_encrypted_body.grid(row=3, column=1, sticky='ns')
            
            label_decrypted_body=tk.Label(entries_frame)
            # label_decrypted_body["font"] = font_poppins_bold
            label_decrypted_body["fg"] = "#333333"
            # label_decrypted_body["justify"] = "left"
            label_decrypted_body["text"] = "Decrypted Body"
            label_decrypted_body.grid(row=4, column=1, sticky='w')
            self.email_decrypted_body=tk.Text(entries_frame, height=0)
            # self.email_decrypted_body["font"] = font_poppins_light
            self.email_decrypted_body["fg"] = "#333333"
            self.email_decrypted_body.insert('1.0', "Wait please...")
            self.email_decrypted_body.grid(row=5, column=1, sticky='ns')

            # Pack the new window.
            entries_frame.pack(anchor='nw', fill='both', expand=True)
            new_window.update()

            self.client.decrypt_email(email_id)
            decrypted_message = self.get_decrypted_message(email_id)

            self.email_decrypted_body.delete('1.0', 'end')
            self.email_decrypted_body.insert('1.0', decrypted_message)

            encrypted_message = self.get_encrypted_message(email_id)

            self.email_encrypted_body.delete('1.0', 'end')
            self.email_encrypted_body.insert('1.0', encrypted_message)

            self.email_encrypted_body.config(state='disabled')
            self.email_decrypted_body.config(state='disabled')

            new_window.update()

    def get_decrypted_message(self, email_id):
        with open(os.path.join(path_handler.DECRYPTED_FILES_DIR, "(dec)_email_" + str(email_id)), 'r') as f:
            lines = f.readlines()
            
        return ''.join(lines)

    def get_encrypted_message(self, email_id):
        with open(os.path.join(path_handler.ATTACH_FILES_DIR, "email_" + str(email_id), 'EncryptedMessage.bin'), 'rb') as f:
            lines = f.readlines()
            
        return ''.join([line.decode("latin1") for line in lines])

    def read_emails(self):
        unseen, sender, subject, limit = self.get_filters()
        self.emails = self.client.read_emails(limit=limit, unseen=unseen, sender=sender, subject=subject)
        self.update_emails()

    def update_emails(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for email in self.emails:
            self.tree.insert('', tk.END, values=email[1:], iid=email[0])

    def get_filters(self):
        unseen = self.unseen_filter.get()
        sender = self.from_filter_entry.get()
        subject = self.subject_filter_entry.get()
        limit = self.limit_filter_entry.get()

        if(limit):
            limit = int(limit)
        else:
            limit = None

        return unseen, sender, subject, limit
    
    # Create a close window event handler
    def on_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            # print("BYE BYE")
            self.client.logout_recipient()
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()