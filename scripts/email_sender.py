import tkinter as tk
import tkinter.font as tkFont
import smtplib

from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

import encryption_decryption as cryption
import path_handler

import os
import re
from tabulate import tabulate

class EmailSender:
    def __init__(self):
        pass

    def read_credentials(self, file_name):
        credentials_file_path = os.path.join(path_handler.STORAGE_FILES_DIR, file_name)

        with open(credentials_file_path, "r") as f:
            self.sender = f.readline().strip()
            self.password = f.readline().strip()
    
    def set_credentials(self, email, password):
        self.sender = email
        self.password = password

    def send_email_preset(self, verbose=True):
        self.send_email(self.recipient, self.subject, self.body, self.att, verbose)

    def send_email(self, recipient, subject, body, key, verbose=True):
        msg = MIMEMultipart()

        msg['From'] = self.sender
        msg['To'] = recipient

        msg['Subject'] = subject
        if(subject == "auto"):
            msg['Subject'] = self.get_new_subject()

        msg.attach(MIMEText("Body is encrypted in 'EncryptedMessage.bin' attachment"))


        with open(os.path.join(path_handler.ENCRYPTED_FILES_DIR, body), 'rb') as f:
            part = MIMEApplication(f.read(), Name="EncryptedMessage.bin")

        # part=MIMEApplication(attachment,Name="RealMessageBody.txt")
        part['Content-Disposition']='attachment; filename=EncryptedMessage.bin'

        msg.attach(part)
        
        with open(os.path.join(path_handler.PLAIN_FILES_DIR, key), 'rb') as f:
            part = MIMEApplication(f.read(), Name="EncryptedKey.bin")

        # part=MIMEApplication(key,Name="wrappedkey.txt")
        part['Content-Disposition']='attachment; filename=EncryptedKey.bin'

        msg.attach(part)

        # smtp_server = smtplib.SMTP("smtp-mail.outlook.com", port=587)
        # if(verbose): print("Connected")

        # smtp_server.starttls()
        # if(verbose): print("TLS SUCCESSFUL")

        # smtp_server.login(self.sender, self.password)
        # if(verbose): print("login SUCCESSFUL")
        # w
        # smtp_server.sendmail(self.sender, recipient, msg.as_string())
        # if(verbose): print("mail sent SUCCESSFUL")

        # smtp_server.quit()

        # self.print_mail()
    
        # print("WAITING")
        self.smtp_server.sendmail(self.sender, recipient, msg.as_string())
        if(verbose): print("mail sent SUCCESSFUL")

    def login(self, verbose=True):
        self.smtp_server = smtplib.SMTP("smtp-mail.outlook.com", port=587)
        if(verbose): print("Connected")

        self.smtp_server.starttls()
        if(verbose): print("TLS SUCCESSFUL")

        self.smtp_server.login(self.sender, self.password)
        if(verbose): print("login SUCCESSFUL")
        
    def logout(self):
        self.smtp_server.quit()

    def valid_email(self, email):
        email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        return re.fullmatch(email_regex, email)

    def set_sender(self, email):
        if(self.valid_email, email):
            self.sender = email

    def set_password(self, password):
        self.password = password

    def set_recipient(self, email):
        if(self.valid_email, email):
            self.recipient= email

    def set_subject(self, subject_text):
        self.subject = subject_text

    def set_body(self,  body_text):
        self.body_text = body_text

    def set_attachement(self, att_text):
        self.att = att_text

    def get_new_subject(self, base = "Encrypted Email Test #"):
        return base + str(self.get_new_test_id())

    def get_new_test_id(self, file_name="test_id_counter.dat"):

        file_path = os.path.join(path_handler.STORAGE_FILES_DIR, file_name)
        with open(file_path, "a+") as f:
            f.seek(0)
            val = int(f.read() or 0) + 1
            f.seek(0)
            f.truncate()
            f.write(str(val))
            return val

    def print_mail(self):
        pass
        # print(
        #     tabulate(
        #         [["From:", self.sender],
        #         ["To:", self.recipient],
        #         ["Subject:", self.subject],
        #         ["Body:", self.body]]
        #         ))

if __name__ == "__main__":
    email = ''
    password = ''

    with open("Support Code\credentials\email_1.dat", "r") as f:
        email = f.readline().strip()
        password = f.readline().strip()

    print(email)
    email_sender = EmailSender(email, password)
    email_sender.send_email_preset(True)