import xmlrpc.server
import pickle
import secrets
import os
# from Crypto.Cipher import AES
import Crypto.Cipher.AES
from tabulate import tabulate

import path_handler

class KDS(xmlrpc.server.SimpleXMLRPCServer):

    def serve_forever(self):
        # self.register_function(self.add, "add")
        if(self.database_exist()):
            self.mappings = self.load_database()
        else:
            # print("="*50)
            # print("CREATING DATABASE")
            # print("="*50)
            self.mappings = {}
            self.create_database()

        self.display_database()
        self.register_function(self.check_registration, "check_registration")
        self.register_function(self.register, "register")
        self.register_function(self.generate_encrypted_shared_key, "generate_encrypted_shared_key")
        self.register_function(self.ping, "ping")
        super().serve_forever()

    def ping(self):
        return True

    def load_database(self):
        with open(self.get_database_path(), "rb") as f:
            return pickle.load(f)

    def create_database(self):
        with open(self.get_database_path(), "wb") as f:
                pickle.dump({}, f)

    def update_database(self):
        with open(self.get_database_path(), "wb") as f:
                pickle.dump(self.mappings, f)

    def get_database_path(self):
        return os.path.join(path_handler.STORAGE_FILES_DIR, "email_key_pair.pkl")
        # return "Support Code\server_database\email_key_pair.pkl"

    def database_exist(self):
        return os.path.exists(self.get_database_path())

    def generate_key(self):
        return secrets.token_hex(16)

    def register(self, email):
        email = email.lower()

        if(self.check_registration(email)):
            return self.get_key(email)

        key = self.generate_key()
        self.mappings[email] = key
        self.update_database()
        return key

    def get_key(self, email):
        email = email.lower()
        return self.mappings.get(email, False)

    def check_registration(self, email):
        # if(self.mappings.get(email, False)):
        #     return self.mappings[email]
        return self.get_key(email)

    def display_database(self):
        table = []
        for key, value in self.mappings.items():
            table.append([key, value])
        print(tabulate(table, tablefmt="plain", stralign="right"))

    def generate_encrypted_shared_key(self, sender_email, recipient_email):
        sender_key = self.check_registration(sender_email)
        recipient_key = self.check_registration(recipient_email)
        
        if(not sender_key and not recipient_key):
            return None
        
        shared_key = self.generate_key()

        shared_key = bytes(shared_key, "utf-8")
        sender_key = bytes(sender_key, "utf-8")
        recipient_key = bytes(recipient_key, "utf-8")
        
        cipher_sender = Crypto.Cipher.AES.new(sender_key, Crypto.Cipher.AES.MODE_GCM)
        sender_encrypted_shared_key = cipher_sender.encrypt(shared_key)

        cipher_recipient= Crypto.Cipher.AES.new(recipient_key, Crypto.Cipher.AES.MODE_GCM)
        recipient_encrypted_shared_key = cipher_recipient.encrypt(shared_key)
        
        return_values = (
            sender_encrypted_shared_key,
            recipient_encrypted_shared_key,
            cipher_sender.nonce,
            cipher_recipient.nonce
        )

        return return_values

if __name__ == "__main__":
    KDS = KDS(("localhost", 8000))
    KDS.serve_forever()

