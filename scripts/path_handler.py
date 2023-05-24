import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
DATA_FILES_DIR = os.path.join(ROOT, "data")
STORAGE_FILES_DIR = os.path.join(DATA_FILES_DIR, "storage_files")
ATTACH_FILES_DIR = os.path.join(DATA_FILES_DIR, "attachement_files")
PLAIN_FILES_DIR = os.path.join(DATA_FILES_DIR, "plain_files")
ENCRYPTED_FILES_DIR = os.path.join(DATA_FILES_DIR, "encrypted_files")
DECRYPTED_FILES_DIR = os.path.join(DATA_FILES_DIR, "decreypted_files")

if not os.path.exists(DATA_FILES_DIR):
    os.makedirs(DATA_FILES_DIR)

if not os.path.exists(ATTACH_FILES_DIR):
    os.makedirs(ATTACH_FILES_DIR)

if not os.path.exists(STORAGE_FILES_DIR):
    os.makedirs(STORAGE_FILES_DIR)

    with open(os.path.join(STORAGE_FILES_DIR, "email_1.dat", 'w')) as f:
        f.write("sender@eng.asu.edu.eg\n")
        f.write("password\n")

    with open(os.path.join(STORAGE_FILES_DIR, "email_2.dat", 'w')) as f:
        f.write("recipient@gmail.com\n")
        f.write("password\n")

    with open(os.path.join(STORAGE_FILES_DIR, "default_email.txt", 'w')) as f:
        f.write("test.mail.test.v1@gmail.com\n")
        f.write("auto\n")
        f.write("Top Secret Message Will Be Encrypted")

if not os.path.exists(PLAIN_FILES_DIR):
    os.makedirs(PLAIN_FILES_DIR)
    
if not os.path.exists(ENCRYPTED_FILES_DIR):
    os.makedirs(ENCRYPTED_FILES_DIR)
    
if not os.path.exists(DECRYPTED_FILES_DIR):
    os.makedirs(DECRYPTED_FILES_DIR)