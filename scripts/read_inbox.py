import email
import imaplib
from email.header import decode_header
import os
import re
import path_handler

class InboxReader():
    def __init__(self):
        # Your email address and password
        # self.EMAIL_ADDRESS = "test.mail.test.v1@gmail.com"
        # self.EMAIL_PASSWORD = "srxzlddmhxruzipa"
        self.connected = False
        self.search_filter = 'ALL'
        # self.connect()

    def read_credentials(self, file_name):
        credentials_file_path = os.path.join(path_handler.STORAGE_FILES_DIR, file_name)

        with open(credentials_file_path, "r") as f:
            self.sender = f.readline().strip()
            self.password = f.readline().strip()
    
    def set_credentials(self, email, password):
        self.sender = email
        self.password = password

    def login(self):
        # Connect to the IMAP server
        imap_server = "imap.gmail.com"
        port = 993

        # Create an IMAP client
        self.imap_client = imaplib.IMAP4_SSL(imap_server, port)

        # Login to your email account
        self.imap_client.login(self.sender, self.password)
        self.connected = True

    def valid_email(self, email):
        email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        return re.fullmatch(email_regex, email)

    def set_search_filter(self, unseen_only = False, from_filter = "", subject_filter = ''):
        search_filter = ''

        if(unseen_only):
            search_filter = "UNSEEN"
        else:
            search_filter = "ALL"

        if(self.valid_email(from_filter)):
            from_filter = '"' + from_filter + '"'
            search_filter = " ".join([search_filter, "FROM", from_filter])

        if(len(subject_filter) > 0 and not subject_filter.isspace()):
            subject_filter = '"' + subject_filter + '"'
            search_filter = " ".join([search_filter, "SUBJECT", subject_filter])

        search_filter = "(" + search_filter + ")"
        self.search_filter = search_filter

    def get_messages_UIDs(self, limit = None):
        status, message_ids = self.imap_client.select("INBOX")
        status, message_ids = self.imap_client.search(None, self.search_filter)
        message_ids = bytes.decode(message_ids[0], 'utf-8').split()[::-1]

        if(limit is None or limit > 50):
            limit = 50
            
        return message_ids[0:limit]

    def read_inbox(self, messages_ids):
        emails = []

        for message_id in messages_ids:
            res, msg = self.imap_client.fetch(str(message_id), "(RFC822)") 
            email_items = []
        
            for response in msg:
                # print(f"{response=}")
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    
                    # for header in [ 'subject', 'to', 'from' ]:
                    #     print('%-8s: %s' % (header.upper(), msg[header]))

                    subject, sender = self.obtain_header(msg)
                    
                    email_items.append(message_id)
                    email_items.append(sender)
                    email_items.append(subject)

                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))


                        body = part.get_payload(decode=True)

                        if(body):
                            try:
                                body = body.decode()
                            except:
                                body = body.decode('latin1')
                            
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            pass
                        elif "attachment" in content_disposition:
                            pass
                            self.download_attachment(part.get_filename(), "email_" + str(message_id), part.get_payload(decode=True))
                            # email_items.append(part.get_filename())
            
            emails.append(email_items)

        return emails
        
    def logout(self):
        self.close_connection()

    def clean(self, text):
        # clean text for creating a folder
        return "".join(c if c.isalnum() else "_" for c in text)
    
    def obtain_header(self, msg):
        # decode the email subject
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding)
    
        # decode email sender
        sender, encoding = decode_header(msg.get("From"))[0]
        if isinstance(sender, bytes):
            sender = sender.decode(encoding)
    
        # print("Subject:", subject)
        # print("sender:", sender)
        return subject, sender
    
    def download_attachment(self, file_name, folder_name, file):
        folder_path = os.path.join(path_handler.ATTACH_FILES_DIR, folder_name)
        filepath = os.path.join(folder_path, file_name)

        if(os.path.exists(filepath)):
            return

        if(not os.path.exists(folder_path)):
            os.makedirs(folder_path)

        # download attachment and save it
        with open(filepath, "wb") as f:
            f.write(file)

    def close_connection(self):
        try:
            self.imap_client.close()
        except:
            pass

    def fetch_last_email(self):
        self.connect()
        message_ids = self.get_messages_UIDs(0, 1)
        self.read_inbox(message_ids)
        return int(message_ids[0])

if __name__ == "__main__":
    email_reader = InboxReader()

