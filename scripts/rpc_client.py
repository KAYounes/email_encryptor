import xmlrpc.client
import Crypto.Cipher.AES
import email_sender
import read_inbox
import encryption_decryption as cryption
import os
import path_handler
# server = xmlrpc.client.ServerProxy("http://localhost:8000")

class RPCClient:
    def __init__(self, host = "http://localhost", port = "8000"):
        self.host = host
        self.port = port
        self.uri = host + ":" + port
        self.connected = False
        self.emailSender = email_sender.EmailSender()
        self.inboxReader = read_inbox.InboxReader()
    
    def connect(self):
        # if(self.connected):
        #     return self.connected
        # print("2-1")
        try:
            # print("2-2")
            self.server = xmlrpc.client.ServerProxy("http://localhost:8000")
            # print("2-3")
            self.server.ping()
            # print("2-4")
            self.connected = True
            # print("2-5")
        except:
            self.connected = False
            # print("2-2B")

        # print("2-6")
        return self.connected
    
    def check_registration(self, email):
        return self.server.check_registration(email)

    def register(self, email):
        return self.server.register(email)

    def request_shared_key(self, sender, recipient):
        sender_key = self.check_registration(sender)

        if(not sender_key):
            sender_key = self.server.register(sender)
        
        sender_key = bytes(sender_key, "utf-8")
        
        recipient_key = self.check_registration(recipient)
        if(not recipient_key):
            recipient_key = self.server.register(recipient)
        
        return_values = self.server.generate_encrypted_shared_key(sender, recipient)

        # unpack
        sender_encrypted_shared_key,\
        recipient_encrypted_shared_key,\
        sender_nonce,\
        recipient_nonce = return_values

        # Convert xmlrpc client.binary to bytes
        sender_encrypted_shared_key = sender_encrypted_shared_key.data
        recipient_encrypted_shared_key = recipient_encrypted_shared_key.data
        sender_nonce = sender_nonce.data
        recipient_nonce  = recipient_nonce .data

        cipher_sender = Crypto.Cipher.AES.new(sender_key, Crypto.Cipher.AES.MODE_GCM, nonce=sender_nonce)
        shared_key_decrypted_by_sender_key = cipher_sender.decrypt(sender_encrypted_shared_key)

        return (shared_key_decrypted_by_sender_key, recipient_encrypted_shared_key, recipient_nonce)
    
    def store_message_encrypted(self, message, file_name, sender_key):
        file_path = os.path.join(path_handler.PLAIN_FILES_DIR, file_name)
        with open(file_path, 'w') as f:
            f.write(message)

        cryption.encrypt_file(sender_key, file_name)

    def store_key(self, key, nonce, file_name):
        file_path = os.path.join(path_handler.PLAIN_FILES_DIR, file_name)
        # print(f"{key + nonce}")
        # print(f"{key}")
        # print(f"{nonce}")   
        with open(file_path, 'wb') as f:
            f.writelines([key, nonce])

    def send_email(self, sender_credentials, recipient, subject, message):
        plain_body_file = "body.dat"
        encrypted_body_file = "(enc)_body.dat"
        plain_key_file = "key.dat"

        shared_key,\
        recipient_encrypted_shared_key,\
        recipient_nonce = self.request_shared_key(self.emailSender.sender, recipient)

        self.store_key(recipient_encrypted_shared_key, recipient_nonce, plain_key_file)
        self.store_message_encrypted(message, plain_body_file, shared_key)

        self.emailSender.send_email(recipient, subject, encrypted_body_file, plain_key_file)

    def decrypt_email(self, email_id):
        message_attach_path = os.path.join("email_" + str(email_id), "EncryptedMessage.bin")
        key_attach_path = os.path.join("email_" + str(email_id), "EncryptedKey.bin")

        recipient_key = self.server.check_registration(self.inboxReader.sender)
        recipient_key = bytes(recipient_key, 'utf-8')
        # shared_key = cryption.decrypt_file(recipient_key, key_attach_path, nonce)

        with open(os.path.join(path_handler.ATTACH_FILES_DIR, key_attach_path), 'rb') as f:
            line = f.read()
            # print(f"{line=}")
            encrypted_shared_key = line[0:32]
            nonce = line[32:]
        
        # print(f"{encrypted_shared_key=} | {nonce=}")
        cipher_recipient = Crypto.Cipher.AES.new(recipient_key, Crypto.Cipher.AES.MODE_GCM, nonce=nonce)
        shared_key = cipher_recipient.decrypt(encrypted_shared_key)

        cryption.decrypt_file(shared_key, message_attach_path, "(dec)_" + "email_" + str(email_id))

    def read_emails(self, limit = None, unseen = False, sender = '', subject = ''):
        self.inboxReader.set_search_filter(unseen_only=unseen, from_filter=sender, subject_filter=subject)
        email_ids = self.inboxReader.get_messages_UIDs(limit=limit)
        return self.inboxReader.read_inbox(email_ids)

    def login_as_sender(self, sender_credentials):
        self.emailSender.read_credentials(sender_credentials)
        self.emailSender.login()

    def login_as_recipient(self, recipient_credentials):
        self.inboxReader.read_credentials(recipient_credentials)
        self.inboxReader.login()

    def logout_sender(self):
        self.emailSender.logout()

    def logout_recipient(self):
        self.inboxReader.logout()

 
if __name__ == "__main__":
    client = RPCClient()
    client.connect()
    client.login_as_recipient('email_2.dat')
    client.read_emails(limit=3, sender="18P9093@eng.asu.edu.eg")

    # print("Sending Email")
    # client.send_email("email_1.dat", "test.mail.test.v1@gmail.com", "auto", "My password is abc123")

    # print("Decrypting Email")
    # client.decrypt_email()

        




